"""
parse git repo intro
"""

from utils import ZAI, timer
from zhipuai.core import StreamResponse

zai = ZAI()


def distil(cont: str) -> str:
    """
    generate repo brief intro
    """
    messages = [
        {
            "role": "system",
            "content": "You are an expert in computer science.",
        },
        {
            "role": "user",
            "content": f"阅读以下多个用```分割的github项目介绍，生成简介、优缺点介绍和快速开始步骤。\n{cont}",
        },
    ]
    resp = zai.call_api("GLM-4-Flash", messages, False)
    cont = None
    if resp:
        if isinstance(resp, StreamResponse):
            # streaming response
            cont = "\n".join([c.choices[0].delta.content for c in resp])
        else:
            # non-streaming response
            cont = resp.choices[0].message.content
    return cont


def streaming_distil(cont: str, messages=None) -> str:
    """
    generate repo brief intro
    """
    if not messages:
        messages = [
            {
                "role": "system",
                "content": "You are an expert in computer science.",
            },
            {
                "role": "user",
                "content": f"阅读以下多个用```分割的github项目介绍，生成简介、优缺点介绍和快速开始步骤。\n{cont}",
            },
        ]
    else:
        messages.append(
            {
                "role": "user",
                "content": cont,
            }
        )
    resp = zai.call_api("GLM-4-Flash", messages, True)
    cont = None
    if resp:
        # streaming response
        cont = "\n".join([c.choices[0].delta.content for c in resp])
    return cont, messages


def adistil(cont: str) -> str:
    """
    generate repo brief intro
    """
    messages = [
        {
            "role": "system",
            "content": "You are an expert in computer science.",
        },
        {
            "role": "user",
            "content": f"阅读以下github项目介绍，生成简介、优缺点介绍和快速开始步骤。\n{cont}",
        },
    ]
    resp = zai.acall_api("GLM-4-Flash", messages)
    cont = None
    if resp:
        return resp.id


def get_adistil_rslt(ids: list) -> str:
    """
    get async distil result
    """
    rslt = zai.get_async_rslt(ids)
    return rslt


@timer
def test():
    import json

    with open("./a-output.txt") as ifs:
        cont = json.load(ifs)

    # infos = [c[2] for c in cont]
    # joints = "\n```\n\n```\n".join(infos)
    # print(distil(joints))

    d = []
    ids = [adistil(c[2]) for c in cont]
    d = get_adistil_rslt(ids)
    # print(d)
    with open("./a-output-distil.txt", "w", encoding="utf-8") as f:
        json.dump(d, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    test()
