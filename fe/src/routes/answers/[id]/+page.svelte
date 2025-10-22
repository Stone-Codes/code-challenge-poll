<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { toast } from 'svelte-sonner';
	import Loading from '../_components/Loading.svelte';

	const questionID = $derived(page.params.id);
	let answer = $state<Answer[]>([]);
	let question = $state<Question | null>(null);
	let loading = $state(true);
	let questionLoading = $state(true);
	let error = $state('');
	let questionError = $state('');
	let text = $state('');
	let submitting = $state(false);

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		if (!text.trim()) return;

		submitting = true;
		try {
			const response = await fetch('http://localhost:8000/answer', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ text, question_id: questionID })
			});
			if (response.ok) {
				toast.success('Answer submitted successfully!');
				text = '';
				fetchAnswers();
			} else {
				toast.error('Failed to submit answer.');
			}
		} catch (error) {
			console.error(error);
			toast.error('Error submitting answer.');
		} finally {
			submitting = false;
		}
	}

	async function fetchQuestion() {
		questionLoading = true;
		questionError = '';
		try {
			const res = await fetch(`http://localhost:8000/question/${questionID}`);
			if (res.ok) {
				const question = await res.json();
				if (!question) {
					questionError = 'Question not found.';
				}
			} else {
				questionError = 'Failed to load question.';
			}
		} catch (e) {
			questionError = 'Error loading question.';
		} finally {
			questionLoading = false;
		}
	}

	async function fetchAnswers() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`http://localhost:8000/question/${questionID}/answers/`);
			if (res.ok) {
				const answers: Answer[] = await res.json();
				answer = answers.filter((ans) => ans.question_id === parseInt(questionID));
			} else {
				error = 'Failed to load answer.';
			}
		} catch (e) {
			error = 'Error loading answer.';
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		fetchQuestion();
		fetchAnswers();
	});
</script>

<svelte:head>
	<title>Answers - Poll App</title>
	<meta name="description" content="View and submit answers" />
</svelte:head>

<div class="container mx-auto space-y-8 py-8">
	<div class="space-y-2">
		<h1 class="text-4xl font-bold">Answers</h1>
		<p class="text-lg text-muted-foreground">Submit your answer or browse existing ones</p>
	</div>

	{#if questionLoading}
		<Card.Root>
			<Card.Header>
				<Card.Title>
					<div class="flex items-center gap-2">
						<span class="animate-pulse">Loading question...</span>
					</div>
				</Card.Title>
			</Card.Header>
		</Card.Root>
	{:else if questionError}
		<Card.Root class="border-destructive bg-destructive/5">
			<Card.Header>
				<Card.Title class="text-destructive">Error Loading Question</Card.Title>
				<Card.Description>{questionError}</Card.Description>
			</Card.Header>
			<Card.Content>
				<Button variant="outline" onclick={() => fetchQuestion()}>Retry</Button>
			</Card.Content>
		</Card.Root>
	{:else if question}
		<Card.Root class="border-primary/20 bg-primary/5">
			<Card.Header>
				<Card.Title class="text-2xl">{question.text}</Card.Title>
				<Card.Description>Question #{question.id}</Card.Description>
			</Card.Header>
		</Card.Root>
	{/if}

	<Card.Root class="border-2 shadow-sm">
		<Card.Header>
			<Card.Title>Submit an Answer</Card.Title>
			<Card.Description>Share your answer with the community</Card.Description>
		</Card.Header>
		<Card.Content>
			<form onsubmit={handleSubmit} class="space-y-4">
				<div class="space-y-2">
					<Label for="answer">Your Answer</Label>
					<Input
						id="answer"
						type="text"
						bind:value={text}
						placeholder="Type your answer here..."
						required
						disabled={submitting}
						class="text-base"
					/>
				</div>
				<Button type="submit" disabled={submitting || !text.trim()} class="w-full sm:w-auto">
					{submitting ? 'Submitting...' : 'Submit Answer'}
				</Button>
			</form>
		</Card.Content>
	</Card.Root>

	<div class="space-y-4">
		<div class="flex items-center justify-between">
			<h2 class="text-2xl font-semibold">All Answers</h2>
			{#if answer.length > 0}
				<span class="text-sm text-muted-foreground">
					{answer.length}
					{answer.length === 1 ? 'answer' : 'answers'}
				</span>
			{/if}
		</div>

		{#if loading}
			<Loading />
		{:else if error}
			<Card.Root class="border-destructive bg-destructive/5">
				<Card.Header>
					<Card.Title class="text-destructive">Error Loading Answers</Card.Title>
					<Card.Description>
						Something went wrong while fetching the answers. Please try again later.
						<br />
						{error}
					</Card.Description>
				</Card.Header>
				<Card.Content>
					<Button variant="outline" onclick={() => fetchAnswers()}>Retry</Button>
				</Card.Content>
			</Card.Root>
		{:else if answer.length === 0}
			<Card.Root class="border-dashed bg-muted/50">
				<Card.Header class="py-12 text-center">
					<Card.Title class="text-muted-foreground">No Answers Yet</Card.Title>
					<Card.Description>Be the first to answer this question!</Card.Description>
				</Card.Header>
			</Card.Root>
		{:else}
			<div class="grid gap-4 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-1">
				{#each answer as ans (ans.id)}
					<Card.Root class="transition-shadow hover:shadow-md">
						<Card.Header>
							<Card.Title class="text-xl">{ans.text}</Card.Title>
							<Card.Description>Answer #{ans.id}</Card.Description>
						</Card.Header>
					</Card.Root>
				{/each}
			</div>
		{/if}
	</div>
</div>
