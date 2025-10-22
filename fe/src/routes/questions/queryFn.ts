export async function createQuestion(text: string) {
  try {
    const response = await fetch('http://localhost:8000/question/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text })
    });
    if (response.ok) {
      return 'Question submitted successfully!';
    } else {
      // Here we probably want to do something with the error we get returned to show clearer messages
      throw new Error('Failed to submit question.');
    }
  } catch (error) {
    // There should be proper error handling here, for example sentry
    console.error(error);
    throw new Error('Error submitting question.');
  }
}

export async function getQuestions(customFetch = fetch) {
  try {
    const res = await customFetch('http://localhost:8000/question/');
    if (res.ok) {
      return await res.json();
    } else {
      // Here we probably want to do something with the error we get returned to show clearer messages
      throw new Error('Failed to load questions.');
    }
  } catch (e) {
    // There should be proper error handling here, for example sentry
    console.error(e);
    throw new Error('Error loading questions.');
  }
}
