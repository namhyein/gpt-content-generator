from dataclasses import dataclass, field
from typing import List, Optional

from package.constants import CATEGORIES


@dataclass
class MessageBody:
    title: str
    category: str
    focus_keyword: str
    assistant_id: str
    additional_prompt: Optional[str] = field(default=None)
    additional_keywords: List[str] = field(default_factory=list)
    slack_id: Optional[str] = field(default=None)
    thread_id: Optional[str] = field(default=None)
    message_id: Optional[str] = field(default=None)
    # additional_files: List[str] = field(default_factory=list)
    
    def __post_init__(self, **kwargs):
        self._validate_category()
        
    def _validate_category(self):
        if self.category not in CATEGORIES.keys():
            raise ValueError(f"Invalid category: {self.category}, must be one of {CATEGORIES.keys()}")