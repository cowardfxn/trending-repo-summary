"""
util class for calling zhipu ai api
"""

import os
from time import sleep

from zhipuai import ZhipuAI
from zhipuai.core._errors import APIRequestFailedError

from utils import timer

API_KEY = os.getenv("API_KEY")


class ZAI:
    """
    util class for calling zhipu ai api
    """

    def __init__(self):
        self.client = ZhipuAI(api_key=API_KEY)

    @timer
    def call_api(self, model: str, messages: list, stream=False) -> dict:
        """
        Call ZhipuAI chat API
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=stream,
            )

            return response

        except APIRequestFailedError as e:
            # handle sensitive content error
            print(f"API request failed\n{str(e)}")

    @timer
    def acall_api(self, model: str, messages: list) -> dict:
        """
        call async chat api
        """
        try:
            response = self.client.chat.asyncCompletions.create(
                model=model,
                messages=messages,
            )

            return response
        except APIRequestFailedError as e:
            # handle sensitive content error
            print(f"API request failed\n{str(e)}")

    @timer
    def get_async_rslt(self, ids: list) -> dict:
        """
        get async api result
        """
        try:
            results = []
            for id_str in ids:
                resp = self.client.chat.asyncCompletions.retrieve_completion_result(
                    id_str
                )
                if resp.task_status == "SUCCESS":
                    results.append(resp.choices[0].message.content)
                elif resp.task_status == "PROCESSING":
                    print(f"Task {id_str} is still processing, retrying in 10 seconds")
                    sleep(10)
                    return self.get_async_rslt(ids)
                elif resp.task_status == "FAILED":
                    print(f"Task {id_str} failed")
            return results
        except APIRequestFailedError as e:
            # handle sensitive content error
            print(f"API request failed\n{str(e)}")
