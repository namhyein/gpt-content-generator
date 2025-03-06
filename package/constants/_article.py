from enum import Enum


class STATUS(Enum):
    IN_PROGRESS = -1102
    SUCCESS = -1201
    FAIL = -1500
    

EDITORS = [
    {"_id": "isabelle-carter", "name": "Isabelle Carter"},
    {"_id": "ai-analyst", "name": "AI Analyst"},
]


CATEGORIES = {
    "ranking": "Ranking",
    "news": "News",
    "knowledge": "Knowledge",
    "culture": "Culture",
    "feature": "Feature",
}


READ_PER_MINUTE = 300
