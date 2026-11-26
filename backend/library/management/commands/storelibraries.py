import signal
from pathlib import Path

import structlog
from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef

from django.conf import settings
from core.models import StoredLibrary, LoadedLibrary

logger = structlog.getLogger(__name__)

signal.signal(signal.SIGINT, signal.SIG_DFL)


class Command(BaseCommand):
    help = "Store libraries in the database"

    def add_arguments(self, parser) -> None:
        parser.add_argument("--path", type=str, help="Path to library files")

    def handle(self, *args, **options):
        StoredLibrary.__init_class__()
        path = Path(options.get("path") or settings.LIBRARIES_PATH)
        if path.is_dir():
            library_files = sorted(
                f for f in path.iterdir() if f.is_file and f.suffix == ".yaml"
            )
        else:
            library_files = [path]
        for fname in library_files:
            try:
                library, error = StoredLibrary.store_library_file(fname, True)
                if library:
                    if library.is_preset:
                        from library.utils import upsert_preset_from_stored_library

                        try:
                            upsert_preset_from_stored_library(library)
                        except Exception:
                            logger.exception(
                                "Failed to upsert preset from stored library",
                                filename=fname,
                                urn=library.urn,
                            )
                    logger.info(
                        "Successfully stored library",
                        filename=fname,
                        library=library,
                    )
                elif error:
                    if error == "libraryAlreadyLoadedError":
                        continue
                    logger.warning(
                        "Library skipped",
                        filename=fname,
                        reason=error,
                    )
            except Exception:
                logger.error("Invalid library file", filename=fname)

        self.prune_removed_builtin_libraries(library_files)

        invisible_libraries = (
            LoadedLibrary.objects.filter(
                builtin=False,
            )
            .annotate(
                is_stored=Exists(StoredLibrary.objects.filter(urn=OuterRef("urn")))
            )
            .filter(is_stored=False)
        )

        # If a user loaded a custom library with an urn U and then deleted the stored library with an urn U
        # Then the user would not be able to see the library in the frontend libraries list view as it fetches from the stored-libraries endpoint, making the library effectively "invisible".
        # This fixes this problem by recreating a StoredLibrary for every "orphaned" custom library.
        # The library will fail to be reloaded if the user ever unloads it (because content is empty(== dict()))
        # In that case the user will have to delete it and reupload it again to get back a sane version of the StoredLibrary.
        for library in invisible_libraries:
            StoredLibrary.objects.create(
                urn=library.urn,
                locale=library.locale,
                name=library.name,
                description=library.description,
                annotation=library.annotation,
                copyright=library.copyright,
                provider=library.provider,
                packager=library.packager,
                publication_date=library.publication_date,
                translations=library.translations,
                builtin=library.builtin,
                objects_meta=library.objects_meta,
                dependencies=[
                    dependency.urn for dependency in library.dependencies.all()
                ],
                version=library.version,
                ref_id=library.ref_id,
                is_loaded=True,
                hash_checksum="0" * 64,
                content=dict(),
                autoload=True,
            )

    def prune_removed_builtin_libraries(self, library_files):
        """RegTech: drop built-in store entries whose YAML file was removed.

        Only built-in libraries that are not loaded are removed; libraries
        uploaded by users (builtin=False) and anything already loaded stay.
        """
        import yaml

        from core.models import Preset, PresetJourney

        file_urns = set()
        for fname in library_files:
            try:
                with open(fname, encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("urn:"):
                            file_urns.add(yaml.safe_load(line)["urn"])
                            break
            except Exception:
                logger.warning("Could not read library URN", filename=fname)
        if not file_urns:
            return
        # Built-in libraries the app loaded by itself (autoload) and that nothing
        # uses: unload them too. Libraries a user loaded stay.
        autoloaded = set(
            StoredLibrary.objects.filter(builtin=True, autoload=True)
            .exclude(urn__in=file_urns)
            .values_list("urn", flat=True)
        )
        progress = True
        while progress:
            progress = False
            for lib in LoadedLibrary.objects.filter(urn__in=autoloaded):
                if lib.reference_count == 0:
                    logger.info("Unloading removed autoloaded library", urn=lib.urn)
                    lib.delete()
                    progress = True
        loaded_urns = set(LoadedLibrary.objects.values_list("urn", flat=True))
        stale = StoredLibrary.objects.filter(builtin=True).exclude(
            urn__in=file_urns | loaded_urns
        )
        stale_urns = list(stale.values_list("urn", flat=True))
        if not stale_urns:
            return
        preset_urns = {u.replace(":library:", ":preset:", 1) for u in stale_urns}
        used_presets = set(
            PresetJourney.objects.values_list("preset__urn", flat=True)
        )
        Preset.objects.filter(urn__in=(preset_urns | set(stale_urns)) - used_presets).delete()
        deleted, _ = stale.delete()
        logger.info("Pruned removed built-in libraries", count=len(stale_urns))

