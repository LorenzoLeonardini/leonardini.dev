<script lang="ts">
	export let src: string
	export let width: string
	export let height: string
	export let alt: string
</script>

<style>
	img {
		width: 100%;
		height: auto;
	}
</style>

<img loading="lazy" src="{src}" alt="{alt}" width="{width}" height="{height}" />
