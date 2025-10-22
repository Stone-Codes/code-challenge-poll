<script lang="ts">
	import { createMutation, createQuery } from '@tanstack/svelte-query';
	import { createQuestion, getQuestions } from './queryFn';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { toast } from 'svelte-sonner';
	import Loading from './_components/Loading.svelte';

	let text = '';

	const questionQuery = createQuery(() => ({
		queryKey: ['questions'],
		queryFn: getQuestions,
		onError: (error: Error) => {
			toast.error(error.message);
		}
	}));

	const questionMutation = createMutation(() => ({
		mutationFn: createQuestion,
		onSuccess: () => {
			toast.success('Question submitted successfully!');
			questionQuery.refetch();
			text = '';
		},
		onError: () => {
			toast.error('Something went wrong, please try again.');
		}
	}));

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		// Super simple validation here, could be improved by using shadcn forms with superforms / zod
		if (!text.trim()) return;
		questionMutation.mutate(text);
	}
</script>

<svelte:head>
	<title>Questions - Poll App</title>
	<meta name="description" content="Ask and explore questions" />
</svelte:head>

<div class="container mx-auto space-y-8 py-8">
	<div class="space-y-2">
		<h1 class="text-4xl font-bold tracking-tight">Questions</h1>
		<p class="text-lg text-muted-foreground">Ask a question or browse existing ones</p>
	</div>

	<Card.Root class="border-2 shadow-sm">
		<Card.Header>
			<Card.Title>Ask a Question</Card.Title>
			<Card.Description>Share your question with the community</Card.Description>
		</Card.Header>
		<Card.Content>
			<form on:submit|preventDefault={handleSubmit} class="space-y-4">
				<div class="space-y-2">
					<Label for="question">Your Question</Label>
					<Input
						id="question"
						type="text"
						bind:value={text}
						placeholder="What would you like to know?"
						required
						disabled={questionMutation.isPending}
						class="text-base"
					/>
				</div>
				<Button
					type="submit"
					disabled={questionMutation.isPending || !text.trim()}
					class="w-full sm:w-auto"
				>
					{questionMutation.isPending ? 'Submitting...' : 'Submit Question'}
				</Button>
			</form>
		</Card.Content>
	</Card.Root>

	<div class="space-y-4">
		<div class="flex items-center justify-between">
			<h2 class="text-2xl font-semibold tracking-tight">All Questions</h2>
			{#if questionQuery.data}
				<span class="text-sm text-muted-foreground">
					{questionQuery.data.length}
					{questionQuery.data.length === 1 ? 'question' : 'questions'}
				</span>
			{/if}
		</div>

		{#if questionQuery.isLoading}
			<Loading />
		{:else if questionQuery.error}
			<Card.Root class="border-destructive bg-destructive/5">
				<Card.Header>
					<Card.Title class="text-destructive">Error Loading Questions</Card.Title>
					<Card.Description>
						Something went wrong while fetching the questions. Please try again later.
					</Card.Description>
				</Card.Header>
				<Card.Content>
					<Button variant="outline" onclick={() => questionQuery.refetch()}>Retry</Button>
				</Card.Content>
			</Card.Root>
		{:else if questionQuery.data && questionQuery.data.length === 0}
			<Card.Root class="border-dashed bg-muted/50">
				<Card.Header class="py-12 text-center">
					<Card.Title class="text-muted-foreground">No Questions Yet</Card.Title>
					<Card.Description>Be the first to ask a question!</Card.Description>
				</Card.Header>
			</Card.Root>
		{:else if questionQuery.data}
			<div class="grid gap-4 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-1">
				{#each questionQuery.data as question (question.id)}
					<Card.Root class="transition-shadow hover:shadow-md">
						<Card.Header>
							<Card.Title class="text-xl">{question.text}</Card.Title>
							<Card.Description>Question #{question.id}</Card.Description>
						</Card.Header>
						<Card.Footer>
							<Button href="/answers/{question.id}" class="w-full sm:w-auto">View Answers</Button>
						</Card.Footer>
					</Card.Root>
				{/each}
			</div>
		{/if}
	</div>
</div>
