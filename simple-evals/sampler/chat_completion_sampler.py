import time
from typing import Any
from openai import OpenAI
import openai

from ..types import MessageList, SamplerBase, SamplerResponse

OPENAI_SYSTEM_MESSAGE_API = "You are a helpful assistant."

OPENAI_SYSTEM_MESSAGE_CHATGPT = (
    "You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture."
    + "\nKnowledge cutoff: 2023-12\nCurrent date: 2024-04-01"
)


class ChatCompletionSampler(SamplerBase):
    """
    Sample from OpenAI's chat completion API
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        system_message: str | None = None,
        temperature: float = 0.6,
        max_tokens: int = 2048,
        api_key: str | None = None,
        base_url: str | None = None,
        reasoning_effort: str | None = None,
        enable_thinking: bool = True,
    ):
        if api_key and base_url:
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url,
            )

        else:
            self.client = OpenAI()
        self.model = model
        self.system_message = system_message
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.image_format = "url"
        self.reasoning_effort = reasoning_effort
        self.enable_thinking = enable_thinking

    def _handle_image(
        self,
        image: str,
        encoding: str = "base64",
        format: str = "png",
        fovea: int = 768,
    ):
        new_image = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/{format};{encoding},{image}",
            },
        }
        return new_image

    def _handle_text(self, text: str):
        return {"type": "text", "text": text}

    def _pack_message(self, role: str, content: Any):
        return {"role": str(role), "content": content}

    def __call__(self, message_list: MessageList) -> SamplerResponse:
        if self.system_message:
            message_list = [self._pack_message("system", self.system_message)] + message_list

        trial = 0
        while True:
            try:
                if "gpt" in self.model:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=message_list,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        reasoning_effort=self.reasoning_effort if self.reasoning_effort is not None else None,
                    )
                # GLM-4.5/4.6
                elif "GLM" in self.model:
                    response = self.client.chat.completions.create(
                        model="zai-org/" + self.model,
                        messages=message_list,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        stream=False,
                        extra_body={"enable_thinking": self.enable_thinking},
                    )
                else:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=message_list,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        stream=False,
                    )
                content = ""
                if hasattr(response.choices[0].message, "reasoning_content") and response.choices[0].message.reasoning_content:
                    content += "<think>"
                    content += response.choices[0].message.reasoning_content
                    content += "</think>"
                content += response.choices[0].message.content
                if content is None:
                    raise ValueError("OpenAI API returned empty response; retrying")

                return SamplerResponse(
                    response_text=content,
                    response_metadata={"usage": response.usage},
                    actual_queried_message_list=message_list,
                )
            except Exception as e:
                exception_backoff = 2**trial  # expontial back off
                print(
                    f"Rate limit exception so wait and retry {trial} after {exception_backoff} sec",
                    e,
                )
                print(response.choices[0].message)
                time.sleep(exception_backoff)
                trial += 1
