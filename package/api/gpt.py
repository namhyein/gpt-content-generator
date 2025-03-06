import logging
import time
from io import BytesIO
from typing import List

from openai import OpenAI
from openai.types import FileObject
from openai.types.beta import Assistant, Thread
from openai.types.beta.threads import Message, Run


class GPTAssistant:
    def __init__(self, assistant_id: str, api_key: str, organization: str):
        self.assistant_id = assistant_id
        self.client = OpenAI(
            api_key=api_key,
            organization=organization
        )

    def create_assistant(self,
                         name: str,
                         model: str,
                         instructions: str,
                         file_based: bool = False) -> Assistant:
        logging.info("Creating Assistant: %s", name)
        return self.client.beta.assistants.create(
            name=name,
            model=model,
            instructions=instructions,
            tools=[{"type": "retrieval"}] if file_based else []
        )

    def create_file(self, file: BytesIO) -> FileObject:
        file = self.client.files.create(
            file=file,
            purpose="assistants"
        )
        logging.info("Creating File: %s", file.id)
        return file

    def create_thread(self) -> Thread:
        thread = self.client.beta.threads.create()
        logging.info("Creating Thread: %s", thread.id)
        return thread

    def create_run(self, thread_id: str) -> Run:
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id
        )

        logging.info("Creating Run: %s", run.id)
        return run

    def create_message(self, thread_id: str, prompt: str) -> Run:
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt
        )

        logging.info("Creating Message: %s", message.id)
        return self.create_run(thread_id=thread_id)

    def retrieve_run(self, thread_id: str, run_id: str) -> Run:
        return self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

    def retrive_recent_message(self, thread_id: str) -> Message:
        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id
        )
        logging.info("Retrieving Recent Message %s", str(len(messages.data)))

        return messages.data[0]

    def retrive_message_until_id(self, thread_id: str, message_id: str) -> List[Message]:
        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id
        )
        logging.info(messages.data)
        output = []
        for message in messages.data:
            if message.id == message_id:
                break
            if message.role != "assistant":
                continue
            output.append(message)
        logging.info("Retrieving Messages Until ID %s (%s)", str(len(output)), message_id)
        return output

    def check_thread_status(self, thread_id: str, run_id: str) -> str:
        run = self.retrieve_run(thread_id=thread_id, run_id=run_id)

        logging.info("Run Status: %s", run.status)
        if run.status not in ["queued", "in_progress", "completed"]:
            raise RuntimeError("Run failed with status: " + run.status)
        return run.status

    def check_if_last_message(self, thread_id: str, message_id: str) -> bool:
        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id
        )
        logging.info("Last Message ID %s (%s)", messages.data[-1].id, message_id)
        return messages.data[0].id == message_id

    def assistant(self, prompt: str, thread_id: str = None) -> Message:
        if not thread_id:
            thread = self.create_thread()
            thread_id = thread.id

        run = self.create_message(thread_id=thread_id, prompt=prompt)
        while True:
            time.sleep(60)
            status = self.check_thread_status(
                thread_id=thread_id,
                run_id=run.id
            )

            if status == "completed":
                return self.retrive_recent_message(thread_id=thread_id)
