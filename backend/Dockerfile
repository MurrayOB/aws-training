# installs python and pip
FROM python:3.9.2 AS base

##############################
FROM base AS build
# can be any name (folder app)
WORKDIR /usr/src/app

# copies pipfile and pipfile.lock to working directory
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt
# copies all file to directory app
COPY . .

##############################
FROM base AS production
ARG FLASK_ENV=production
ENV FLASK_ENV=${FLASK_ENV}

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt
# copies all file to directory app
COPY . .
COPY --from=build /usr/src/app/ .

# starts server
EXPOSE 80
ENTRYPOINT ["python", "app.py"]
# CMD ["app.py"]