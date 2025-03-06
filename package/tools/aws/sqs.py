import boto3


class SQS:
    def __init__(self, region: str):
        self.client = boto3.client(region_name=region, service_name="sqs")

    def queue_url(self, queue_name: str):
        return self.client.get_queue_url(QueueName=queue_name)["QueueUrl"]

    def send_message(self, message_body: str, queue_name: str):
        res = self.client.send_message(
            QueueUrl=self.queue_url(queue_name=queue_name),
            MessageBody=message_body
        )
        return res
