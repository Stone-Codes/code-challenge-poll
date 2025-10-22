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

### Frontend

*Simple version missmatch in package.json / packge-lock*
Fix: rerun npm install

*Submitting multiple answers in a row not working*
- The issue is that we are relying on the "message" variable for refetching the answers.
It will work the first time submitting one, because the message is set to the success string.
After fetching its not reset to an empty string, so it will not refetch properly as the value doesnt change anymore.

- Missing trailing slashes in the links / fetch routes


### Backend

*CORS issues*
Cors ist not properly configured in the backend. The frontend is not able to access the backend.
Fix: Add cors middleware


*Code structure*
Everything is in one file, splitting the code up will make it more readable, and easier to figure out were things live
for example, models.py, routes.py etc. 



#### Further Improvements
- Show the amount of answers for each question on the questions page next to "Show Answers"
- Upvotes for answers (maybe also downvotes)
- OpenAPI Schema for type generation for the frontend in combination wiht for example openapi-fetch client
