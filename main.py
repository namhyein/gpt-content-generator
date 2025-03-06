import argparse
import json
import logging
import random

from dacite import from_dict

from package.api.internal import InternalAPI
from package.constants import CATEGORIES, EDITORS, STATUS
from package.generator import ContentGenerator
from package.setting import RESULT_QUEUE
from package.tools.aws import send_slack
from package.tools.exceptions import handle_error
from package.tools.utils import make_slug
from package.validate import MessageBody

parser = argparse.ArgumentParser()
parser.add_argument("--event", required=True, type=str)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

api = InternalAPI()


def handle_sqs_message(body: str):
    """
        Message Body Example:
        {
            "category": STRING, required,
            "title": STRING, required,
            "assistant_id": STRING, required,
            "focus_keyword": STRING, required,
            "slack_id": STRING,
            "thread_id": STRING,
            "additonal_prompt": STRING,
            "additional_keywords": STRING[],
            "additional_files": STRING[] (s3 file paths),
        }
    """
    try:
        body: MessageBody = from_dict(data_class=MessageBody, data=body)
        generator = ContentGenerator(body.assistant_id)
    except Exception as e:
        handle_error(e)
        return
    
    _id = make_slug(body.title)
    try:
        if body.thread_id:
            status = "article_generated"
            message = generator.continue_message(
                body.thread_id,
                body.message_id
            )
        else:
            status = "article_modified"
            message = generator.generate_article(
                body.title,
                body.focus_keyword,
                body.additional_prompt,
                body.additional_keywords
            )

        editor = random.choice(EDITORS)
        markdown = "\n\n".join([
            msg.text.value
            for msg in message["content"]
            if msg.type == "text"
        ])
        metadata = {
            "message_id": message.get("id"),
            "thread_id": message.get("thread_id"),
            "run_id": message.get("run_id"),
            "assistant_id": body.assistant_id,
            "status": status,
            "slack_id": body.slack_id,
        }
        send_slack(
            queue_name=RESULT_QUEUE,
            message_dict={
                "_id": _id,
                "title": body.title,
                "category": body.category,
                "editor": editor,
                "markdown": markdown,
                "slack_id": body.slack_id,
                "metadata": metadata
            }
        )
        data = {
            "_id": _id,
            "slug": _id,
            "name": body.title,
            "category": {
                "_id": body.category,
                "name": CATEGORIES[body.category]
            },
            "editor": editor,
            "markdown": markdown,
            "metadata": metadata,
        }
        res = api.update_article(_id, data)
        if res.ok:
            api.update_article_status(_id, STATUS.SUCCESS.value)
        else:
            raise Exception(f"Internal API Error: {res.text}")
    
    except Exception as e:
        handle_error(e)
        api.update_article_status(_id, STATUS.FAIL.value)


if __name__ == "__main__":
    args = parser.parse_args()
    logging.info(args.event)
    handle_sqs_message(json.loads(args.event))
