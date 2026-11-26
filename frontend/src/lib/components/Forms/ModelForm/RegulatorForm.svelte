<script lang="ts">
	import AutocompleteSelect from '../AutocompleteSelect.svelte';
	import TextField from '#lib/components/Forms/TextField.svelte';
	import Dropdown from '#lib/components/Dropdown/Dropdown.svelte';
	import type { SuperValidated } from 'sveltekit-superforms';
	import type { ModelInfo, CacheLock } from '#lib/utils/types.js';
	import { m } from '#paraglide/messages.js';

	interface Props {
		form: SuperValidated<any>;
		model: ModelInfo;
		cacheLocks?: Record<string, CacheLock>;
		formDataCache?: Record<string, any>;
		initialData?: Record<string, any>;
		object?: any;
	}

	let {
		form,
		model,
		cacheLocks = {},
		formDataCache = $bindable({}),
		initialData = {},
		object = {}
	}: Props = $props();
</script>

<TextField
	{form}
	field="abbreviation"
	label={m.abbreviation()}
	cacheLock={cacheLocks['abbreviation']}
	bind:cachedValue={formDataCache['abbreviation']}
/>
<AutocompleteSelect
	{form}
	field="sector"
	options={model.selectOptions?.sector}
	cacheLock={cacheLocks['sector']}
	bind:cachedValue={formDataCache['sector']}
	label={m.sector()}
/>
<TextField
	{form}
	field="legal_basis"
	label={m.legalBasis()}
	helpText={m.regulatorLegalBasisHelpText()}
	cacheLock={cacheLocks['legal_basis']}
	bind:cachedValue={formDataCache['legal_basis']}
/>
<TextField
	{form}
	field="website"
	label={m.website()}
	cacheLock={cacheLocks['website']}
	bind:cachedValue={formDataCache['website']}
/>
<Dropdown open={false} style="hover:text-primary-700" icon="fa-solid fa-ellipsis" header={m.more()}>
	<TextField
		{form}
		field="contact_email"
		label={m.email()}
		cacheLock={cacheLocks['contact_email']}
		bind:cachedValue={formDataCache['contact_email']}
	/>
	<TextField
		{form}
		field="contact_phone"
		label={m.phone()}
		cacheLock={cacheLocks['contact_phone']}
		bind:cachedValue={formDataCache['contact_phone']}
	/>
	<AutocompleteSelect
		multiple
		{form}
		createFromSelection={true}
		optionsEndpoint="filtering-labels"
		optionsLabelField="label"
		field="filtering_labels"
		helpText={m.labelsHelpText()}
		label={m.labels()}
		translateOptions={false}
		allowUserOptions="append"
	/>
</Dropdown>
