<script lang="ts">
	import { createQuery } from '@tanstack/svelte-query';
	import { getVisits } from './queryFn';
	import { toast } from 'svelte-sonner';
	import { Badge } from '$lib/components/ui/badge';
	import Eye from '$lib/icons/eye.svg';

	const questionQuery = createQuery(() => ({
		queryKey: ['questions'],
		queryFn: () => getVisits(),
		onError: (error: Error) => {
			toast.error(error.message);
		}
	}));

	// Sort questions by visits in descending order
	const sortedQuestions = $derived(
		questionQuery.data ? questionQuery.data.sort((a, b) => b.visits - a.visits) : []
	);
</script>

<svelte:head>
	<title>Visit Statistics - Poll App</title>
	<meta name="description" content="View question visit statistics" />
</svelte:head>

<div class="container mx-auto space-y-6 py-8">
	<div class="space-y-2">
		<h1 class="text-3xl font-bold">Visit Statistics</h1>
	</div>

	{#if questionQuery.isLoading}
		<div class="flex items-center justify-center py-12">
			<div class="animate-pulse text-muted-foreground">Loading statistics...</div>
		</div>
	{:else if questionQuery.error}
		<div class="rounded-lg border border-destructive bg-destructive/5 p-4">
			<p class="text-sm text-destructive">Failed to load statistics. Please try again.</p>
		</div>
	{:else if sortedQuestions.length === 0}
		<div class="rounded-lg border border-dashed bg-muted/50 py-12 text-center">
			<p class="text-muted-foreground">No questions to display.</p>
		</div>
	{:else}
		<div class="rounded-lg border bg-card">
			<div class="divide-y">
				{#each sortedQuestions as question, index (question.id)}
					<div class="flex items-center gap-4 px-6 py-4 transition-colors hover:bg-muted/50">
						<div class="flex items-center justify-center">
							<span class="text-2xl font-bold text-muted-foreground">#{index + 1}</span>
						</div>
						<div class=" flex-1">
							<p class="text-sm text-muted-foreground">Question #{question.id}</p>
							<p class="font-medium">{question.text}</p>
						</div>
						<Badge>
							<img src={Eye} alt="views" class="h-5 w-5" />
							<span class="text-lg font-semibold">{question.visits}</span>
						</Badge>
					</div>
				{/each}
			</div>
		</div>
	{/if}
</div>
