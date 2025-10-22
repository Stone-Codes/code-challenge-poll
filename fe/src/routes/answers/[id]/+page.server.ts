import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, fetch }) => {
  const { id } = params;

  // Just spray and pray here and ignore any errors, as its not relevant for the user
  try {
    fetch(`http://localhost:8000/question/${id}/visit/`);
  } catch (error) {
    console.error(error);
  }
}
