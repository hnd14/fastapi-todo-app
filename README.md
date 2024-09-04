# Sample Setup 
## Set a virtual environment
### Create a base venv
#### Using built in venv module
```bash
python -m venv venv
```
#### Using virtualenv module (for more detailed configuration)
```bash
# Install module (globally)
pip install virtualenv

# Generate virtual environment
python -m virtualenv --python=<your-python-runtime-version> venv 
```

### Activate virtual environment
```bash
venv\Scripts\activate
```
### Install depdendency packages
```bash
pip install -r requirements.txt
```

## Setup a postgres instance at port 5432 
- This can be done through a local installment of postgreSQL or a docker container.
```bash
docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=<your-preferred-one> -d postgres:<your-preferred-version>
```
## Configure `.env` file by creating a copy from `.env.sample`
- Make a `.env` file that is a copy of the `.env.sample` file. You can access the `.env.sample` file under the `app` directory. Change the information in the `.env` file according to your postgres instance.
## Apply migration to your database
- At `app` directory, run `alembic` migration command. Please make sure your postgres DB is ready and accessible.
```bash
# Migrate to a specific revision
alembic upgrade <revision_number>

# Migrate to latest revison
alembic upgrade head

# Dowgragde to specific revision
alembic downgrade <revision_number>

# Downgrade to base (revert all revisions)
alembic downgrade base

# Create new revision
alembic revision -m <comment>
```
## Run `uvicorn` web server from `app` directory
```bash
uvicorn main:app
```
## Access the api documentations
- The api documentations is available at `http://localhost:<uvicorn-port>/docs` after the `uvicorn` server has started.
- The default user username is `todo_admin`, the default user password should be provided in the `.env` file
