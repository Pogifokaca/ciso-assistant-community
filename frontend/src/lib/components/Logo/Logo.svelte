<script lang="ts">
	import ciso from '#lib/assets/regtech.svg';

	interface Props {
		height?: number;
		width?: number;
	}

	let { height = 200, width = 200 }: Props = $props();
</script>

<img class="c" {height} {width} src={ciso} alt="RegTech logo" data-testid="logo-image" />
