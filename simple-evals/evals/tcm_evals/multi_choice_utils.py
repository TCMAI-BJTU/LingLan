import re


def parse_multi_choice_answer(answer: list[str] | str) -> list[str]:
    """解析多选题标准答案，兼容 ["A", "C", "E"] 和旧格式 ["ACE"]。

    返回去重、排序后的大写选项；无效标签直接报错，避免静默误评分。
    """
    if isinstance(answer, str):
        parts = [answer]
    elif isinstance(answer, list):
        parts = answer
    else:
        raise ValueError(f"多选题 answer 必须是字符串列表或字符串，收到 {answer!r}")

    if not parts:
        raise ValueError("多选题 answer 不能为空")

    letters = set()
    for part in parts:
        if not isinstance(part, str):
            raise ValueError(f"多选题 answer 的每一项必须是字符串，收到 {part!r}")
        token = re.sub(r"[,，、\s]+", "", part).upper()
        if not re.fullmatch(r"[A-E]+", token):
            raise ValueError(f"多选题 answer 只能包含 A–E 选项，收到 {part!r}")
        letters.update(token)

    return sorted(letters)
