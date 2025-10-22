<script lang="ts">
	import { createMutation, createQuery } from '@tanstack/svelte-query';
	import { createQuestion, getQuestions } from './queryFn';
	import { Button } from '$lib/components/ui/button';
	import { toast } from 'svelte-sonner';
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
		questionMutation.mutate(text);
	}
</script>

<form on:submit|preventDefault={handleSubmit}>
	<label for="question">Question:</label>
	<input id="question" type="text" bind:value={text} required />
	<button type="submit">Submit</button>
</form>

{#if questionQuery.isLoading}
	<p>Loading questions...</p>
{:else if questionQuery.error}
	<p>Something went wrong, while fetching the questions, please try again.</p>
{:else}
	<h2>All Questions</h2>
	<ul>
		{#each questionQuery.data as question (question.id)}
			<li>{question.text}</li>
			<Button href="/answers/{question.id}">Show Answers</Button>
		{/each}
	</ul>
{/if}
