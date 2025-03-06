import requests

from package.setting import INTERNAL_API_HOST


class InternalAPI:
    
    def __init__(self, api_host: str = INTERNAL_API_HOST):
        self.host = api_host
        self.headers = {
            "Content-Type": "application/json",
        }
        
    def update_article(self, _id: str, body: dict) -> requests.Response:
        request_body = {**body, "_id": _id}
        request_url = f"{self.host}/articles/mutation"
        
        return requests.put(url=request_url,
                            json=request_body,
                            headers=self.headers,
                            timeout=30)        
    
    def update_article_status(self, _id: str, status: int) -> requests.Response:
        request_body = {"_id": _id, "status": status}
        request_url = f"{self.host}/articles/mutation"
        
        return requests.patch(url=request_url,
                              json=request_body,
                              headers=self.headers,
                              timeout=30)