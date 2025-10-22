<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { get } from 'svelte/store';
	const id = get(page).params.id;
	let answer: Answer[] = [];
	let loading = true;
	let error = '';
	let text = '';
	let message = '';

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		try {
			const response = await fetch('http://localhost:8000/answer', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ text, question_id: id })
			});
			if (response.ok) {
				message = 'Answer submitted successfully!';
				text = '';
			} else {
				message = 'Failed to submit answer.';
			}
		} catch (error) {
			message = 'Error submitting answer.';
		}
	}

	async function fetchAnswers() {
		loading = true;
		error = '';
		try {
			const res = await fetch('http://localhost:8000/answer');
			if (res.ok) {
				const answers: Answer[] = await res.json();
				answer = answers.filter((ans) => ans.question_id === parseInt(id));
			} else {
				error = 'Failed to load answer.';
			}
		} catch (e) {
			error = 'Error loading answer.';
		} finally {
			loading = false;
			message = '';
		}
	}
	onMount(() => {
		fetchAnswers();
	});

	$: if (message === 'Answer submitted successfully!') {
		fetchAnswers();
	}
</script>

<form on:submit|preventDefault={handleSubmit}>
	<label for="answer">Answer:</label>
	<input id="answer" type="text" bind:value={text} required />
	<button type="submit">Submit</button>
</form>

{#if loading}
	<p>Loading...</p>
{:else if error}
	<p>{error}</p>
{:else}
	<ul>
		{#each answer as ans}
			<li>{ans.text}</li>
		{/each}
	</ul>
{/if}
