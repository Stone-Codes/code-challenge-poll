<script lang="ts">
	import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query';
	import { Toaster } from '$lib/components/ui/sonner/index.js';
	import Header from './Header.svelte';
	import '../app.css';

	let { children } = $props();

	const queryClient = new QueryClient();
</script>

<Toaster />
<div class="app">
	<Header />

	<QueryClientProvider client={queryClient}>
		<main>
			{@render children()}
		</main>
	</QueryClientProvider>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 64rem;
		margin: 0 auto;
		box-sizing: border-box;
	}
</style>
