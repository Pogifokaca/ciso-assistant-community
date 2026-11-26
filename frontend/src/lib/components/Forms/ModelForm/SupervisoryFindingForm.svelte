<script lang="ts">
	import AutocompleteSelect from '../AutocompleteSelect.svelte';
	import TextField from '#lib/components/Forms/TextField.svelte';
	import MarkdownField from '#lib/components/Forms/MarkdownField.svelte';
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
<TextField
	{form}
	field="inspection"
	label={m.inspection()}
	helpText={m.inspectionHelpText()}
	cacheLock={cacheLocks['inspection']}
	bind:cachedValue={formDataCache['inspection']}
/>
<TextField
	type="date"
	{form}
	field="inspection_date"
	label={m.inspectionDate()}
	cacheLock={cacheLocks['inspection_date']}
	bind:cachedValue={formDataCache['inspection_date']}
/>
<AutocompleteSelect
	{form}
	field="severity"
	options={model.selectOptions?.severity}
	cacheLock={cacheLocks['severity']}
	bind:cachedValue={formDataCache['severity']}
	label={m.severity()}
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
<MarkdownField
	{form}
	field="remediation_plan"
	label={m.remediationPlan()}
	cacheLock={cacheLocks['remediation_plan']}
	bind:cachedValue={formDataCache['remediation_plan']}
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
		multiple
		field="applied_controls"
		optionsEndpoint="applied-controls"
		optionsExtraFields={[['folder', 'str']]}
		cacheLock={cacheLocks['applied_controls']}
		bind:cachedValue={formDataCache['applied_controls']}
		label={m.appliedControls()}
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
