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

<AutocompleteSelect
	{form}
	nullable
	field="institution"
	optionsEndpoint="financial-institutions"
	optionsExtraFields={[['folder', 'str']]}
	cacheLock={cacheLocks['institution']}
	bind:cachedValue={formDataCache['institution']}
	label={m.financialInstitution()}
/>
<AutocompleteSelect
	{form}
	nullable
	field="regulator"
	optionsEndpoint="regulators"
	optionsExtraFields={[['folder', 'str']]}
	cacheLock={cacheLocks['regulator']}
	bind:cachedValue={formDataCache['regulator']}
	label={m.regulator()}
/>
<AutocompleteSelect
	{form}
	nullable
	field="obligation"
	optionsEndpoint="regulatory-obligations"
	optionsExtraFields={[['folder', 'str']]}
	cacheLock={cacheLocks['obligation']}
	bind:cachedValue={formDataCache['obligation']}
	label={m.regulatoryObligation()}
/>
<AutocompleteSelect
	{form}
	field="report_type"
	options={model.selectOptions?.report_type}
	cacheLock={cacheLocks['report_type']}
	bind:cachedValue={formDataCache['report_type']}
	label={m.reportType()}
/>
<TextField
	{form}
	field="reporting_period"
	label={m.reportingPeriod()}
	helpText={m.reportingPeriodHelpText()}
	cacheLock={cacheLocks['reporting_period']}
	bind:cachedValue={formDataCache['reporting_period']}
/>
<AutocompleteSelect
	{form}
	field="status"
	options={model.selectOptions?.status}
	cacheLock={cacheLocks['status']}
	bind:cachedValue={formDataCache['status']}
	label={m.status()}
/>
<TextField
	type="date"
	{form}
	field="due_date"
	label={m.dueDate()}
	cacheLock={cacheLocks['due_date']}
	bind:cachedValue={formDataCache['due_date']}
/>
<TextField
	type="date"
	{form}
	field="submitted_on"
	label={m.submittedOn()}
	cacheLock={cacheLocks['submitted_on']}
	bind:cachedValue={formDataCache['submitted_on']}
/>
<AutocompleteSelect
	{form}
	multiple
	optionsEndpoint="actors"
	lazy
	optionsLabelField="str"
	optionsInfoFields={{
		fields: [{ field: 'type', translate: true }],
		position: 'prefix'
	}}
	field="owner"
	cacheLock={cacheLocks['owner']}
	bind:cachedValue={formDataCache['owner']}
	label={m.owner()}
/>
<Dropdown open={false} style="hover:text-primary-700" icon="fa-solid fa-ellipsis" header={m.more()}>
	<TextField
		{form}
		field="submission_reference"
		label={m.submissionReference()}
		helpText={m.submissionReferenceHelpText()}
		cacheLock={cacheLocks['submission_reference']}
		bind:cachedValue={formDataCache['submission_reference']}
	/>
	<AutocompleteSelect
		{form}
		multiple
		field="evidences"
		optionsEndpoint="evidences"
		optionsExtraFields={[['folder', 'str']]}
		cacheLock={cacheLocks['evidences']}
		bind:cachedValue={formDataCache['evidences']}
		label={m.evidences()}
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
