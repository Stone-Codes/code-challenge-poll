export async function getVisits(customFetch = fetch) {
  try {
    const res = await customFetch('http://localhost:8000/question/');
    if (res.ok) {
      return await res.json() as Question[];
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
