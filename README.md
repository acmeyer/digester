# Digester

This is a simple app for generating summaries of articles and documents and then asking follow-up questions. This is just a prototype. There are numerous ways it could be improved.

## Demo

https://github.com/acmeyer/digester/assets/852932/c059f2a1-7234-49c7-a572-7c1e309173b6


## How to Use

This application has three main components:
1. Supabase Database
2. Backend Python Server
3. Frontend Nextjs app

Assuming you have a Supabase account (you can get a free one [here](https://supabase.io/)), you can run a local supabase instance by running
```bash
supabase start
```

or you can just add a `.env` file to the root of the project with the `DATABASE_URL` variable and set it to your Supabase database url.

**Note:** in order for the app to work, you need to get a user's id and set it to the `ADMIN_USER_ID` in the `.env` file. This user will automatically be created if you run the supabase script above (you'll just have to grab it from the local Supabase studio dashboard) or you can manually create this user on Supabase and grab the id there.

The backend server can be run by running
```bash
poetry install && poetry run start
```

The frontend app can be run by running
```bash
cd client && yarn install && yarn dev
```

## Ways to Improve
- Fix file upload, it's currently broken
- Add authentication to the app
- Move the summarization functionality to a background job
- In the conversation view, when you scroll, show the article title in navbar
- Add chat streaming instead of waiting for the full response to come in (ala ChatGPT)
- Better handle cases where content doesn't exist
- Add the ability to authenticate your own accounts for accessing articles from sources with paywalls
- Better parse websites to only get the text of the article, not the whole site
