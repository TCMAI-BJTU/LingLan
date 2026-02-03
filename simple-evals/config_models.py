from .sampler.chat_completion_sampler import (
    OPENAI_SYSTEM_MESSAGE_API,
    OPENAI_SYSTEM_MESSAGE_CHATGPT,
    ChatCompletionSampler,
)
from .sampler.claude_sampler import ClaudeCompletionSampler, CLAUDE_SYSTEM_MESSAGE_LMSYS
from .sampler.o_chat_completion_sampler import OChatCompletionSampler
from .sampler.responses_sampler import ResponsesSampler

def get_models(args):
    models = {
        # Reasoning Models
        "o3": ResponsesSampler(
            model="o3-2025-04-16",
            reasoning_model=True,
        ),
        "o3-temp-1": ResponsesSampler(
            model="o3-2025-04-16",
            reasoning_model=True,
            temperature=1.0,
        ),
        "o3_high": ResponsesSampler(
            model="o3-2025-04-16",
            reasoning_model=True,
            reasoning_effort="high",
        ),
        "o3_low": ResponsesSampler(
            model="o3-2025-04-16",
            reasoning_model=True,
            reasoning_effort="low",
        ),
        # Default == Medium
        "o4-mini": ResponsesSampler(
            model="o4-mini-2025-04-16",
            reasoning_model=True,
        ),
        "o4-mini_high": ResponsesSampler(
            model="o4-mini-2025-04-16",
            reasoning_model=True,
            reasoning_effort="high",
        ),
        "o4-mini_low": ResponsesSampler(
            model="o4-mini-2025-04-16",
            reasoning_model=True,
            reasoning_effort="low",
        ),
        "o1-pro": ResponsesSampler(
            model="o1-pro",
            reasoning_model=True,
        ),
        "o1": OChatCompletionSampler(
            model="o1",
        ),
        "o1_high": OChatCompletionSampler(
            model="o1",
            reasoning_effort="high",
        ),
        "o1_low": OChatCompletionSampler(
            model="o1",
            reasoning_effort="low",
        ),
        "o1-preview": OChatCompletionSampler(
            model="o1-preview",
        ),
        "o1-mini": OChatCompletionSampler(
            model="o1-mini",
        ),
        # Default == Medium
        "o3-mini": OChatCompletionSampler(
            model="o3-mini",
        ),
        "o3-mini_high": OChatCompletionSampler(
            model="o3-mini",
            reasoning_effort="high",
        ),
        "o3-mini_low": OChatCompletionSampler(
            model="o3-mini",
            reasoning_effort="low",
        ),
        # GPT-4.1 models
        "gpt-4.1": ChatCompletionSampler(
            model="gpt-4.1-2025-04-14",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
        ),
        "gpt-4.1-temp-1": ChatCompletionSampler(
            model="gpt-4.1-2025-04-14",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
            temperature=1.0,
        ),
        "gpt-4.1-mini": ChatCompletionSampler(
            model="gpt-4.1-mini-2025-04-14",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
        ),
        "gpt-4.1-nano": ChatCompletionSampler(
            model="gpt-4.1-nano-2025-04-14",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
        ),
        # GPT-4o models
        "gpt-4o": ChatCompletionSampler(
            model="gpt-4o",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=args.max_tokens,
        ),
        "gpt-4o-2024-11-20": ChatCompletionSampler(
            model="gpt-4o-2024-11-20",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=args.max_tokens,
        ),
        "gpt-4o-2024-08-06": ChatCompletionSampler(
            model="gpt-4o-2024-08-06",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
        ),
        "gpt-4o-2024-08-06-temp-1": ChatCompletionSampler(
            model="gpt-4o-2024-08-06",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
            temperature=1.0,
        ),
        "gpt-4o-2024-05-13": ChatCompletionSampler(
            model="gpt-4o-2024-05-13",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
        ),
        "gpt-4o-mini": ChatCompletionSampler(
            model="gpt-4o-mini-2024-07-18",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
        ),
        # GPT-4.5 model
        "gpt-4.5-preview": ChatCompletionSampler(
            model="gpt-4.5-preview-2025-02-27",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            max_tokens=2048,
        ),
        # GPT-4-turbo model
        "gpt-4-turbo-2024-04-09": ChatCompletionSampler(
            model="gpt-4-turbo-2024-04-09",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        # GPT-4 model
        "gpt-4-0613": ChatCompletionSampler(
            model="gpt-4-0613",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        # GPT-3.5 Turbo model
        "gpt-3.5-turbo-0125": ChatCompletionSampler(
            model="gpt-3.5-turbo-0125",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        "gpt-3.5-turbo-0125-temp-1": ChatCompletionSampler(
            model="gpt-3.5-turbo-0125",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
            temperature=1.0,
        ),
        # Chatgpt models:
        "chatgpt-4o-latest": ChatCompletionSampler(
            model="chatgpt-4o-latest",
            system_message=OPENAI_SYSTEM_MESSAGE_CHATGPT,
            max_tokens=2048,
        ),
        "gpt-4-turbo-2024-04-09_chatgpt": ChatCompletionSampler(
            model="gpt-4-turbo-2024-04-09",
            system_message=OPENAI_SYSTEM_MESSAGE_CHATGPT,
        ),
        # Claude models:
        "claude-3-opus-20240229_empty": ClaudeCompletionSampler(
            model="claude-3-opus-20240229",
            system_message=CLAUDE_SYSTEM_MESSAGE_LMSYS,
        ),
        "claude-3-7-sonnet-20250219": ClaudeCompletionSampler(
            model="claude-3-7-sonnet-20250219",
            system_message=CLAUDE_SYSTEM_MESSAGE_LMSYS,
        ),
        "claude-3-haiku-20240307": ClaudeCompletionSampler(
            model="claude-3-haiku-20240307",
        ),
        "qwen3-8b-stage-1": ChatCompletionSampler(
            model="qwen3-8b-stage-1",
            temperature=0.6,
            # max_tokens=args.max_tokens,
            # system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        "qwen3-8b-stage-2-half": ChatCompletionSampler(
            model="qwen3-8b-stage-2-half",
            temperature=0.6,
            # max_tokens=args.max_tokens,
            # system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        "kimi-k2-0711-preview": ChatCompletionSampler(
            model="kimi-k2-0711-preview",
            temperature=0.6,
            max_tokens=args.max_tokens,
            # system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        "gpt-5": ChatCompletionSampler(
            model="gpt-5",
            temperature=0.6,
            max_tokens=args.max_tokens,
            reasoning_effort="low",  # minimal, low, medium, high
            system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        "gpt-5-mini": ChatCompletionSampler(
            model="gpt-5-mini",
            temperature=0.6,
            max_tokens=args.max_tokens,
            reasoning_effort="medium",  # minimal, low, medium, high
            system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        ############# Baichuan #############
        "Baichuan-M2-32B": ChatCompletionSampler(
            model="Baichuan-M2-32B",
            temperature=0.6,
            max_tokens=args.max_tokens,
        ),
        ############# Qwen3 #############
        "Qwen3-32B": ChatCompletionSampler(
            model="Qwen3-32B",
            temperature=0.6,
            max_tokens=args.max_tokens,
        ),
        "Qwen3-14B": ChatCompletionSampler(
            model="Qwen3-14B",
            temperature=0.6,
            max_tokens=args.max_tokens,
        ),
        "Qwen3-8B": ChatCompletionSampler(
            model="Qwen3-8B",
            temperature=0.6,
            max_tokens=args.max_tokens,
        ),
        "Qwen3-4B": ChatCompletionSampler(
            model="Qwen3-4B",
            temperature=0.6,
            max_tokens=args.max_tokens,
        ),
        "Qwen3-Next-80B-A3B-Thinking": ChatCompletionSampler(
            model="Qwen3-Next-80B-A3B-Thinking",
            temperature=0.6,
            max_tokens=args.max_tokens,
        ),
        "qwen3-235b": ChatCompletionSampler(
            model="qwen3-235b-a22b-instruct-2507",
            temperature=0.6,
            max_tokens=args.max_tokens,
            # system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        "Qwen3-30B-A3B": ChatCompletionSampler(
            model="Qwen3-30B-A3B",
            temperature=0.6,
            max_tokens=args.max_tokens,
        ),
        ############# DeepSeek #############
        "deepseek-r1": ChatCompletionSampler(
            model="deepseek-r1-250528",
            temperature=0.6,
            max_tokens=args.max_tokens,
            # system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        "deepseek-v3.1-think-250821": ChatCompletionSampler(
            model="deepseek-v3.1-think-250821",
            temperature=0.6,
            max_tokens=args.max_tokens,
            # system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        "deepseek-v3.1": ChatCompletionSampler(
            model="deepseek-v3.1-250821",
            temperature=0.6,
            max_tokens=args.max_tokens,
            # system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        ############# GPT-OSS #############
        "gpt-oss-20b": ChatCompletionSampler(
            model="gpt-oss-20b",
            temperature=0.6,
            max_tokens=args.max_tokens,
            reasoning_effort="medium",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        "gpt-oss-120b": ChatCompletionSampler(
            model="gpt-oss-120b",
            temperature=0.6,
            max_tokens=args.max_tokens,
            reasoning_effort="medium",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        "gpt-5": ChatCompletionSampler(
            model="gpt-5",
            temperature=0.6,
            max_tokens=args.max_tokens,
            reasoning_effort="medium",
            system_message=OPENAI_SYSTEM_MESSAGE_API,
        ),
        "TCMChat": ChatCompletionSampler(
            model="TCMChat",
            temperature=0.6,
            max_tokens=2048,
        ),
        "Baichuan2-13B-Chat": ChatCompletionSampler(
            model="Baichuan2-13B-Chat",
            temperature=0.6,
            max_tokens=4096,
        ),
        "Lingdan-13B-TCPM": ChatCompletionSampler(
            model="Lingdan-13B-TCPM",
            temperature=0.6,
            max_tokens=2048,
        ),
        "BianCang-7B": ChatCompletionSampler(
            model="BianCang-7B",
            temperature=0.6,
            max_tokens=args.max_tokens,
        ),
        "BianCang-14B": ChatCompletionSampler(
            model="BianCang-14B",
            temperature=0.6,
            max_tokens=args.max_tokens,
        ),
    }
    return models
