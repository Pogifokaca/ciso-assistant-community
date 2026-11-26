<script lang="ts">
	import AutocompleteSelect from '../AutocompleteSelect.svelte';
	import TextField from '#lib/components/Forms/TextField.svelte';
	import Checkbox from '#lib/components/Forms/Checkbox.svelte';
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
	field="institution_type"
	options={model.selectOptions?.institution_type}
	cacheLock={cacheLocks['institution_type']}
	bind:cachedValue={formDataCache['institution_type']}
	label={m.institutionType()}
/>
<AutocompleteSelect
	{form}
	field="status"
	options={model.selectOptions?.status}
	cacheLock={cacheLocks['status']}
	bind:cachedValue={formDataCache['status']}
	label={m.status()}
/>
<AutocompleteSelect
	{form}
	multiple
	field="regulators"
	optionsEndpoint="regulators"
	optionsExtraFields={[['folder', 'str']]}
	cacheLock={cacheLocks['regulators']}
	bind:cachedValue={formDataCache['regulators']}
	label={m.regulators()}
/>
<TextField
	{form}
	field="license_number"
	label={m.licenseNumber()}
	cacheLock={cacheLocks['license_number']}
	bind:cachedValue={formDataCache['license_number']}
/>
<TextField
	type="date"
	{form}
	field="license_date"
	label={m.licenseDate()}
	cacheLock={cacheLocks['license_date']}
	bind:cachedValue={formDataCache['license_date']}
/>
<Checkbox
	{form}
	field="is_systemic"
	label={m.isSystemic()}
	cacheLock={cacheLocks['is_systemic']}
	bind:cachedValue={formDataCache['is_systemic']}
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
		field="registration_number"
		label={m.registrationNumber()}
		helpText={m.registrationNumberHelpText()}
		cacheLock={cacheLocks['registration_number']}
		bind:cachedValue={formDataCache['registration_number']}
	/>
	<TextField
		{form}
		field="tax_number"
		label={m.taxNumber()}
		cacheLock={cacheLocks['tax_number']}
		bind:cachedValue={formDataCache['tax_number']}
	/>
	<TextField
		{form}
		field="lei"
		label={m.lei()}
		cacheLock={cacheLocks['lei']}
		bind:cachedValue={formDataCache['lei']}
	/>
	<TextField
		{form}
		field="address"
		label={m.address()}
		cacheLock={cacheLocks['address']}
		bind:cachedValue={formDataCache['address']}
	/>
	<TextField
		{form}
		field="website"
		label={m.website()}
		cacheLock={cacheLocks['website']}
		bind:cachedValue={formDataCache['website']}
	/>
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
