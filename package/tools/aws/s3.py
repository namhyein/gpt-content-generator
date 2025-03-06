import boto3


class S3:
    def __init__(self, region: str):
        self.client = boto3.client(service_name="s3", region_name=region)

    def parse(self, uri):
        """
            uri: s3://bucket/key or https://bucket.s3.region.amazonaws.com/key
        """
        if uri.startswith("s3://"):
            return uri.split("/", 3)[2:]

        if uri.startswith("https://"):
            uri, key = uri.split("/", 3)[2:]
            bucket = uri.split(".")[0]

            return bucket, key

        raise ValueError("Invalid URI")

    def get_object(self, bucket, key):
        obj = self.client.get_object(Bucket=bucket, Key=key)
