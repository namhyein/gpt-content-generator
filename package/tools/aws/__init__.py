import json
import logging
from typing import List

from package.setting import AWS_REGION, SLACK_QUEUE, STAGE
from package.tools.aws.sqs import SQS

sqs = SQS(region=AWS_REGION)


def send_slack(
    message_dict: dict,
    message_type: str = "INFO",
    module_name: str = "wineandnews-article-content-generator",
    members: List[str] = ["nam"],
    queue_name: str = SLACK_QUEUE,
):
    if message_dict.get("_id"):
        shortcut = f"https://admin.wineandnews.com/article/{message_dict['_id']}"
    else:
        shortcut = ""
    message_body = json.dumps({
        "stage": STAGE,
        "module": module_name,
        "members": members,
        "type": message_type,
        "shortcut": shortcut,
        **message_dict
    })
    logging.info(message_body)
    res = sqs.send_message(message_body, queue_name=queue_name)
    logging.info("[send slack msg]: %s", json.dumps(res))

    # if queue_name == RESULT_QUEUE:
    #     logging.info(message_dict)

    #     res = requests.put(
    #         f"{INTERNAL_API_HOST}/articles/mutation",
    #         headers={
    #             "Content-Type": "application/json",
    #         },
    #         json={
    #             "_id": message_dict["_id"],
    #             "slug": message_dict["_id"],
    #             "name": message_dict["title"],
    #             "category": {
    #                 "_id": message_dict["category"],
    #                 "name": CATEGORIES[message_dict["category"]]
    #             },
    #             "editor": message_dict["editor"],
    #             "markdown": message_dict["markdown"],
    #             "metadata": message_dict["metadata"]
    #         },
    #         timeout=30,
    #     )
    #     if not res.ok:
    #         logging.error("Internal API Error: %s", res.text)
    #     res.raise_for_status()
