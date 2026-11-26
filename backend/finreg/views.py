from django.db.models import Count
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response

from core.views import BaseModelViewSet as AbstractBaseModelViewSet, ExportMixin
from iam.models import RoleAssignment

from .models import (
    FinancialInstitution,
    RegulatoryObligation,
    RegulatoryReport,
    Regulator,
    Sector,
    SupervisoryFinding,
)


class BaseModelViewSet(AbstractBaseModelViewSet):
    serializers_module = "finreg.serializers"


def _choices(choices):
    return Response(dict(choices))


class RegulatorViewSet(ExportMixin, BaseModelViewSet):
    model = Regulator
    search_fields = ["name", "abbreviation", "ref_id", "description"]
    filterset_fields = ["folder", "sector", "filtering_labels"]
    export_config = {
        "filename": "regulators_export",
        "fields": {
            "ref_id": {"source": "ref_id", "label": "ref_id", "escape": True},
            "abbreviation": {"source": "abbreviation", "label": "abbreviation"},
            "name": {"source": "name", "label": "name", "escape": True},
            "sector": {"source": "sector", "label": "sector"},
            "legal_basis": {"source": "legal_basis", "label": "legal_basis"},
            "website": {"source": "website", "label": "website"},
            "domain": {"source": "folder.name", "label": "domain", "escape": True},
        },
        "select_related": ["folder"],
        "wrap_columns": ["name"],
    }

    @action(detail=False, name="Get sector choices")
    def sector(self, request):
        return _choices(Sector.choices)


class FinancialInstitutionViewSet(ExportMixin, BaseModelViewSet):
    model = FinancialInstitution
    search_fields = [
        "name",
        "ref_id",
        "description",
        "license_number",
        "registration_number",
        "tax_number",
        "lei",
    ]
    filterset_fields = [
        "folder",
        "institution_type",
        "status",
        "regulators",
        "is_systemic",
        "owner",
        "filtering_labels",
    ]
    export_config = {
        "filename": "financial_institutions_export",
        "fields": {
            "ref_id": {"source": "ref_id", "label": "ref_id", "escape": True},
            "name": {"source": "name", "label": "name", "escape": True},
            "institution_type": {
                "source": "institution_type",
                "label": "institution_type",
            },
            "status": {"source": "status", "label": "status"},
            "license_number": {"source": "license_number", "label": "license_number"},
            "license_date": {"source": "license_date", "label": "license_date"},
            "registration_number": {
                "source": "registration_number",
                "label": "registration_number",
            },
            "tax_number": {"source": "tax_number", "label": "tax_number"},
            "lei": {"source": "lei", "label": "lei"},
            "regulators": {
                "source": "regulators",
                "label": "regulators",
                "format": lambda qs: "\n".join(str(r) for r in qs.all()),
            },
            "is_systemic": {"source": "is_systemic", "label": "is_systemic"},
            "domain": {"source": "folder.name", "label": "domain", "escape": True},
        },
        "select_related": ["folder"],
        "prefetch_related": ["regulators"],
        "wrap_columns": ["name"],
    }

    @action(detail=False, name="Get institution type choices")
    def institution_type(self, request):
        return _choices(FinancialInstitution.InstitutionType.choices)

    @action(detail=False, name="Get status choices")
    def status(self, request):
        return _choices(FinancialInstitution.Status.choices)

    @action(detail=False, name="Financial institutions overview")
    def overview(self, request):
        """Counts for the overview page, limited to what the user may see."""
        user = request.user
        today = timezone.localdate()

        def visible(model):
            return model.objects.filter(
                id__in=RoleAssignment.get_viewable_object_ids(user, model)
            )

        def by(qs, field):
            return {
                row[field]: row["n"]
                for row in qs.values(field).annotate(n=Count("id")).order_by()
            }

        institutions = visible(FinancialInstitution)
        obligations = visible(RegulatoryObligation)
        reports = visible(RegulatoryReport)
        findings = visible(SupervisoryFinding)

        open_reports = reports.exclude(
            status__in=[
                RegulatoryReport.Status.SUBMITTED,
                RegulatoryReport.Status.ACCEPTED,
            ]
        )
        open_findings = findings.exclude(
            status__in=[
                SupervisoryFinding.Status.REMEDIATED,
                SupervisoryFinding.Status.VERIFIED,
                SupervisoryFinding.Status.CLOSED,
            ]
        )

        upcoming_reports = open_reports.filter(due_date__gte=today).order_by(
            "due_date"
        )[:8]
        overdue_reports = open_reports.filter(due_date__lt=today).order_by("due_date")

        return Response(
            {
                "counts": {
                    "institutions": institutions.count(),
                    "regulators": visible(Regulator).count(),
                    "obligations": obligations.count(),
                    "reports": reports.count(),
                    "findings": findings.count(),
                    "open_reports": open_reports.count(),
                    "overdue_reports": overdue_reports.count(),
                    "open_findings": open_findings.count(),
                    "overdue_findings": open_findings.filter(
                        due_date__lt=today
                    ).count(),
                },
                "institutions_by_type": by(institutions, "institution_type"),
                "obligations_by_status": by(obligations, "status"),
                "reports_by_status": by(reports, "status"),
                "findings_by_severity": by(open_findings, "severity"),
                "upcoming_reports": [
                    {
                        "id": str(r.id),
                        "name": r.name,
                        "ref_id": r.ref_id,
                        "due_date": r.due_date,
                        "status": r.status,
                        "institution": str(r.institution) if r.institution else None,
                    }
                    for r in list(overdue_reports[:8]) + list(upcoming_reports)
                ][:12],
            }
        )


class RegulatoryObligationViewSet(ExportMixin, BaseModelViewSet):
    model = RegulatoryObligation
    search_fields = ["name", "ref_id", "description", "legal_reference"]
    filterset_fields = [
        "folder",
        "regulator",
        "obligation_type",
        "frequency",
        "status",
        "institutions",
        "frameworks",
        "applied_controls",
        "owner",
        "due_date",
        "filtering_labels",
    ]
    export_config = {
        "filename": "regulatory_obligations_export",
        "fields": {
            "ref_id": {"source": "ref_id", "label": "ref_id", "escape": True},
            "name": {"source": "name", "label": "name", "escape": True},
            "regulator": {"source": "regulator.name", "label": "regulator"},
            "legal_reference": {
                "source": "legal_reference",
                "label": "legal_reference",
                "escape": True,
            },
            "obligation_type": {"source": "obligation_type", "label": "type"},
            "frequency": {"source": "frequency", "label": "frequency"},
            "status": {"source": "status", "label": "status"},
            "due_date": {"source": "due_date", "label": "due_date"},
            "domain": {"source": "folder.name", "label": "domain", "escape": True},
        },
        "select_related": ["folder", "regulator"],
        "wrap_columns": ["name", "legal_reference"],
    }

    @action(detail=False, name="Get obligation type choices")
    def obligation_type(self, request):
        return _choices(RegulatoryObligation.ObligationType.choices)

    @action(detail=False, name="Get frequency choices")
    def frequency(self, request):
        return _choices(RegulatoryObligation.Frequency.choices)

    @action(detail=False, name="Get status choices")
    def status(self, request):
        return _choices(RegulatoryObligation.Status.choices)


class RegulatoryReportViewSet(ExportMixin, BaseModelViewSet):
    model = RegulatoryReport
    search_fields = [
        "name",
        "ref_id",
        "description",
        "reporting_period",
        "submission_reference",
    ]
    filterset_fields = [
        "folder",
        "institution",
        "regulator",
        "obligation",
        "report_type",
        "status",
        "owner",
        "due_date",
        "submitted_on",
        "filtering_labels",
    ]
    export_config = {
        "filename": "regulatory_reports_export",
        "fields": {
            "ref_id": {"source": "ref_id", "label": "ref_id", "escape": True},
            "name": {"source": "name", "label": "name", "escape": True},
            "institution": {"source": "institution.name", "label": "institution"},
            "regulator": {"source": "regulator.name", "label": "regulator"},
            "report_type": {"source": "report_type", "label": "type"},
            "reporting_period": {
                "source": "reporting_period",
                "label": "reporting_period",
            },
            "status": {"source": "status", "label": "status"},
            "due_date": {"source": "due_date", "label": "due_date"},
            "submitted_on": {"source": "submitted_on", "label": "submitted_on"},
            "submission_reference": {
                "source": "submission_reference",
                "label": "submission_reference",
            },
        },
        "select_related": ["institution", "regulator"],
        "wrap_columns": ["name"],
    }

    @action(detail=False, name="Get report type choices")
    def report_type(self, request):
        return _choices(RegulatoryReport.ReportType.choices)

    @action(detail=False, name="Get status choices")
    def status(self, request):
        return _choices(RegulatoryReport.Status.choices)


class SupervisoryFindingViewSet(ExportMixin, BaseModelViewSet):
    model = SupervisoryFinding
    search_fields = ["name", "ref_id", "description", "inspection"]
    filterset_fields = [
        "folder",
        "institution",
        "regulator",
        "obligation",
        "severity",
        "status",
        "owner",
        "due_date",
        "inspection_date",
        "applied_controls",
        "filtering_labels",
    ]
    export_config = {
        "filename": "supervisory_findings_export",
        "fields": {
            "ref_id": {"source": "ref_id", "label": "ref_id", "escape": True},
            "name": {"source": "name", "label": "name", "escape": True},
            "institution": {"source": "institution.name", "label": "institution"},
            "regulator": {"source": "regulator.name", "label": "regulator"},
            "inspection": {"source": "inspection", "label": "inspection"},
            "inspection_date": {
                "source": "inspection_date",
                "label": "inspection_date",
            },
            "severity": {"source": "severity", "label": "severity"},
            "status": {"source": "status", "label": "status"},
            "due_date": {"source": "due_date", "label": "due_date"},
        },
        "select_related": ["institution", "regulator"],
        "wrap_columns": ["name"],
    }

    @action(detail=False, name="Get severity choices")
    def severity(self, request):
        return _choices(SupervisoryFinding.Severity.choices)

    @action(detail=False, name="Get status choices")
    def status(self, request):
        return _choices(SupervisoryFinding.Status.choices)
