# installs python and pip
FROM python:3.9.2

# can be any name (folder app)
WORKDIR /app

# where we run the server
EXPOSE 5050

# copies pipfile and pipfile.lock to working directory
# can use there names because they're in the same directory as the docker file
COPY Pipfile ./
COPY Pipfile.lock ./

# install pipenv 
RUN pip install pipenv

# RUN pipenv lock --clear
# get dependencies from lock file
RUN pipenv lock --requirements > requirements.txt
# install dependencies, they're installed globally, no need for .venv
RUN pip install -r requirements.txt

# copies all file to directory app
COPY . ./

# starts server
CMD ["python", "app.py"]