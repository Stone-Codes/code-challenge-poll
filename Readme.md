# Poll Code Challenge

A full-stack poll application built with **Svelte** (frontend) and **FastAPI** (backend).

## Features

- Create and manage Questions
- See Answers to Questions

## Tech Stack

- **Frontend:** [Svelte](https://svelte.dev/)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)


## Run & Develop

See:
 - **Frontend:** [Readme](./fe/README.md)
 - **Backend:** [Readme](./be/README.md)

## Review

### Summary
- Several frontend and backend issues identified and addressed
- Multiple suggestions for future improvements documented

---

## Issues Found & Fixed

### Frontend

✅ **Simple version missmatch in package.json / packge-lock (fixed)**
- Fixed by rerunning npm install

✅ **Submitting multiple answers in a row not working (fixed)**
- The issue is that we are relying on the "message" variable for refetching the answers. It will work the first time submitting one, because the message is set to the success string. After fetching its not reset to an empty string, so it will not refetch properly as the value doesnt change anymore.

✅ **Routing & Navigation (fixed)**
- Missing trailing slashes in the links / fetch routes
- The "Answers" link in the navbar is not serving any purpose right now => Removed
- Same with "Home" link, either add some landing page or just remove it

✅ **Data Fetching (fixed)**
- The "Answers" page fetches all questions and filters client side instead of using the get single question via id Endpoint
- The "Answers" page also fetches all answers and filters client side => added new endpoint for that purpose

✅ **State Management (fixed)**
- Answers uses page store, but should use the state svelte 5 basically made stores obsolete

### Additions

**UI/UX**
- Introduced shadcn-svelte for quick, and easy UI overhaul
- Added card based layout for questions / answer pages
- Added toasts for success and error messages

**View/Visist counts**
- Added a new /visits page that lists all questions with their visit counts ordered by visist counts

### Backend

✅ **CORS issues (fixed)**
- Cors ist not properly configured in the backend. The frontend is not able to access the backend.
- Fixed by adding cors middleware

✅ **Code structure (fixed)**
- Everything is in one file => Split up code into multiple files to make it more readable / easier to maintain
- Replaced on startup event with a lifespan context manager
- Moved the routes into separate routers
- Added further validation of the create answer / question data (check chars etc)


### Additions

**Visists endpoint**
- Added new endpoint to increment the visist of a question

**Answers by question id endpoint**
- Added a new endpoint to fetch answers via question id
---

## Suggestions for Future Improvements

### UX Enhancements
- Upvotes for answers (maybe also downvotes)
- Pagination for the questions and answers page, infinite scrolling might be suitable here
- Some way to prevent spamming visists to question, refreshing the page will just add a new visist

### Technical Improvements
- OpenAPI Schema for type generation for the frontend in combination wiht for example openapi-fetch client
- Shadnc forms with superforms / form-snap / zod, helps with validation, but more usefull for larger forms tbh
- The fetching / mutating of answer should be done similar to the questions page, questions page can serve as an example
  - Limited to time constraints, but the example in the questions page should be enough to get started
- When this would be live, we would need a solution for running migrations like alembic, right now just regenerating the db is ok
- Depending on the needs could also return the question together with the answers instead of two separate requests
- Content moderation (if needed, depending also on the environment the app is used)
  - Could use some lightweight AI model for flagging the answers, and then pull a human into the loop for example
- Error handling for the frontend for example with sentry is missing right now

### Testing Strategy
**Tests not implemented due to time constraints**

My general testing approach for apps like this:
- **Unit tests**: Small/ good amount of unit tests, testing functions / utils, making sure those work
- **Integration tests**: Large chunk of integration tests, written with playwright, mocking the network requests with something like prism + openapi schema
- **E2E tests**: Super small, around max 10 end to end tests for testing all the critical paths of the application, also written with playwright

### Minor Notes
- Didnt adjust the navbar much, but it works fine right now
- Nothing added to the "Home" page
- Could further reduce duplication with the card layout by creation even more reusable components between question / answer page
- No Docker setup, could be added later, i personally prefer to run most things locally except services like the DB / redis etc.
