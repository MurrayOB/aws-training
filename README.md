# App name example: 'aws-web-app-dev'

# code build

- managed image: Ubuntu, Standard, aws/codebuild/5.0, Env Type: Linux, Enabled Privileged, New Service Role

# AWS Code build Backend:

**Create** an ECR for the docker image specified in the buildspec.yml
Must add ecr:\* permissions to codebuild service role

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

For Elastic Beanstalk environment otherwise an error will occur when trying to use ECR (docker image):
Must add policy **AmazonEC2ContainerRegistryReadOnly** on aws-elasticbeanstalk-ec2-role

# AWS Code build Frontend:

Must add

```json
{
  "AWS": "s3:*"
}
```

on codebuild role

## S3 bucket for frontend

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

# aws setup

1. Create application on EBS
2. Create environment
3. Create code pipeline
   - New Service Role
4. Create a CodeBuild

# backend re-creation steps:

Setup backend Notes/Steps:

Create backend folder
Create .venv folder
Create main.py file
Run: pipenv install flask

To run: "pipenv shell" in project directory
To install everything: run "pipenv install" (npm install)

For vscode: Click python interpretor - "Enter Interpreter path..." - enter: "backend\.venv\Scripts\python.exe"

Flask only recognises "app.py" or "wsgi.py" when running flask run

To install: (env, db-operations)
pipenv install python-dotenv
pipenv install psycopg2-binary

# frontend re-creation steps:

npx create-react-app frontend

# docker commands

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
