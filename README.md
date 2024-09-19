# Biclocus
There are two options to run the app locally:
1. Run the app in a Docker container
## How to get started
set the environment variables in the `.env` file
`ENV_STATE` can be set to either `dev` or `prod`

You can run the app locally by running the following command:

```bash
docker compose up --build
```
This will run all the services in the docker-compose.yml file.

2. Run the app locally
## How to get started

```bash
python3.12 -m venv env
source env/bin/activate
```

Create a .env file following the example `example.env`

`app/config.py` has 3 sets of configurations: Test, Dev, and Prod.

```bash
touch .env
```

Run the following command to install dependencies. `runtime.txt` specifies the runtime version used.

```bash
bash reset.sh
```

## Run the app locally

```bash
python run.py
```

## Run tests.

We use the `TestConfig` to run tests

```bash
bash test.sh
```

### Features

- Routes / Crud.
- Base models with database persistence and relationships.
- Multiple configuration files.
- User authentication, authorization, and route protection.
- Logging
