import os

STAGE = os.getenv("STAGE", "dev")

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SLACK_QUEUE = os.getenv("SLACK_QUEUE")
RESULT_QUEUE = os.getenv( "RESULT_QUEUE")

INTERNAL_API_HOST = os.getenv("INTERNAL_API_HOST")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORGANIZATION_ID = os.getenv("OPENAI_ORGANIZATION_ID")

