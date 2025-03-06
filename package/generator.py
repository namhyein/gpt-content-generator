import logging

from package.api.gpt import GPTAssistant
from package.constants import OPENAI_ASSISTANT
from package.setting import OPENAI_API_KEY, OPENAI_ORGANIZATION_ID

logging.basicConfig(level=logging.INFO)


class ContentGenerator(GPTAssistant):
    def __init__(self, assistant_id: str = None):
        if not assistant_id:
            assistant_id = OPENAI_ASSISTANT.wina_versely.value

        super().__init__(
            assistant_id=assistant_id,
            api_key=OPENAI_API_KEY,
            organization=OPENAI_ORGANIZATION_ID
        )

    def construct_prompt(self,
                         title: str,
                         focus_keyword: str,
                         additional_prompt: str,
                         additional_keywords: str):
        prompt = f"Article Metadata\n  - Title: {title}\n  - Focused Keyword: {focus_keyword}\n"
        if additional_keywords:
            prompt += f"  - Additional Keywords: [{', '.join(additional_keywords)}]\n\n"

        if additional_prompt:
            prompt += f"In addition to following all the rules you already follow, be sure to read and follow the following\nAdditional Rules\n  {additional_prompt}"

        return prompt

    def generate_article(self,
                         title: str,
                         focus_keyword: str,
                         additional_prompt: str,
                         additional_keywords: str):

        prompt = self.construct_prompt(
            title=title,
            focus_keyword=focus_keyword,
            additional_prompt=additional_prompt,
            additional_keywords=additional_keywords
        )

        message = self.assistant(prompt=prompt)
        return {
            "id": message.id,
            "thread_id": message.thread_id,
            "run_id": message.run_id,
            "content": message.content
        }

    def continue_message(self, thread_id: str, last_message: str):
        if self.check_if_last_message(thread_id, last_message):
            message = self.assistant(thread_id=thread_id, prompt="Continue")
            return {
                "id": message.id,
                "thread_id": message.thread_id,
                "run_id": message.run_id,
                "content": message.content
            }
            
        messages = self.retrive_message_until_id(thread_id=thread_id, message_id=last_message)
        
        content = []
        for message in reversed(messages):
            content += message.content
        if len(messages) != 0:
            return {
                "id": messages[0].id,
                "thread_id": thread_id,
                "run_id": messages[0].run_id,
                "content": content
            }
