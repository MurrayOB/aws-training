# App name example: 'aws-web-app-dev'

# AWS Example Overview

1. Create repo hosted on GitHub called 'your-project-name'.
2. Create Flask app (backend) inside that repo.
3. Create React app (frontend) inside that repo.
4. Create Build folder with build configurations inside that repo.
5. Create an S3 bucket for the frontend.
6. Create a CodePipeline for the frontend (include CodeBuild)
7. Create an Elastic Beanstalk App on AWS.
8. Create an environment, example: dev, for that app.
9. Create an ECR (Elastic Container Registry) for the docker image.
10. Create a CodePipeline for the backend (including CodeBuild) that deploys to the EB app.

# CodeBuild setup, both frontend and backend

- managed image: Ubuntu
- Standard
- aws/codebuild/5.0
- Env Type: Linux
- Enabled Privileged
- New Service Role

# FRONTEND STEPS:

## S3 bucket policy for frontend

1. Create public S3 Bucket

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CodeBuildPermission",
      "Effect": "Allow",
      "Principal": {
        "AWS": "code build service role"
      },
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::aws-web-app-dev/*",
        "arn:aws:s3:::aws-web-app-dev"
      ]
    },
    {
      "Sid": "PublicObjects",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::aws-web-app-dev/*"
    }
  ]
}
```

2. Create CodePipeline + CodeBuild

Must add

```json
{
  "AWS": "s3:*"
}
```

on codebuild role

# BACKEND STEPS:

- Create EB
  For Elastic Beanstalk environment otherwise an error will occur when trying to use ECR (docker image):
  Must add policy **AmazonEC2ContainerRegistryReadOnly** on aws-elasticbeanstalk-ec2-role

- **Create** an ECR for the docker image specified in the buildspec.yml
- Must add ecr:\* permissions to codebuild service role

ECR Permissions on Codebuild service role

```json
  {
            "Effect": "Allow",
            "Action": [
                "ecr:BatchCheckLayerAvailability",
                "ecr:CompleteLayerUpload",
                "ecr:GetAuthorizationToken",
                "ecr:InitiateLayerUpload",
                "ecr:PutImage",
                "ecr:UploadLayerPart"
            ],
            "Resource": "*"
        },
```

# Backend project re-creation steps (Flask):

Setup backend Notes/Steps:

1. Create backend folder
2. Create .venv folder
3. Create main.py file
4. Run:

```console
pipenv install flask
```

To run:

```console
pipenv shell
```

in project directory

To install everything run

```console
pipenv install
```

(npm install)

For vscode: Click python interpretor - "Enter Interpreter path..." - enter: "backend\.venv\Scripts\python.exe"

Flask only recognises "app.py" or "wsgi.py" when running flask run

To install: (env, db-operations)

```console
pipenv install python-dotenv
pipenv install psycopg2-binary
```

# Frontend project re-creation steps (React):

```console
npx create-react-app frontend
```

# Other

## Docker commands

docker images

docker build . -t react-app-api

docker run -p 5050:5050 react-app-api

docker exec -it quirky_wilson bash

ls -la

cat requirements.txt

docker exec it name sh

docker stop containername

docker exec mongoimage mongo --username root --password root

docker network ls

docker network inspect network_id
