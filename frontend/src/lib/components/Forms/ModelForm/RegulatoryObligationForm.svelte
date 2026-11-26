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
	field="regulator"
	optionsEndpoint="regulators"
	optionsExtraFields={[['folder', 'str']]}
	cacheLock={cacheLocks['regulator']}
	bind:cachedValue={formDataCache['regulator']}
	label={m.regulator()}
/>
<TextField
	{form}
	field="legal_reference"
	label={m.legalReference()}
	helpText={m.legalReferenceHelpText()}
	cacheLock={cacheLocks['legal_reference']}
	bind:cachedValue={formDataCache['legal_reference']}
/>
<AutocompleteSelect
	{form}
	field="obligation_type"
	options={model.selectOptions?.obligation_type}
	cacheLock={cacheLocks['obligation_type']}
	bind:cachedValue={formDataCache['obligation_type']}
	label={m.obligationType()}
/>
<AutocompleteSelect
	{form}
	field="frequency"
	options={model.selectOptions?.frequency}
	cacheLock={cacheLocks['frequency']}
	bind:cachedValue={formDataCache['frequency']}
	label={m.frequency()}
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
<AutocompleteSelect
	{form}
	multiple
	field="institutions"
	optionsEndpoint="financial-institutions"
	optionsExtraFields={[['folder', 'str']]}
	cacheLock={cacheLocks['institutions']}
	bind:cachedValue={formDataCache['institutions']}
	label={m.financialInstitutions()}
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
		type="date"
		{form}
		field="effective_date"
		label={m.effectiveDate()}
		cacheLock={cacheLocks['effective_date']}
		bind:cachedValue={formDataCache['effective_date']}
	/>
	<AutocompleteSelect
		{form}
		multiple
		field="frameworks"
		optionsEndpoint="frameworks"
		optionsExtraFields={[['folder', 'str']]}
		cacheLock={cacheLocks['frameworks']}
		bind:cachedValue={formDataCache['frameworks']}
		label={m.frameworks()}
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
