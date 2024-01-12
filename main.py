import srt
import os
import openai

api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")


sub_file = "subtitle.srt"
openai_clinet = openai.Client(api_key=api_key, base_url=api_base)


def sub_obj(sub_file):
    with open(sub_file, "r") as f:
        subs = srt.parse(f.read())
    return list(subs)


def get_transalte(target: str, context: str) -> str:
    prompt_template = f"""\
### CONTEXT
{context}
### TARGET
{target}
### ANSWER
请根据上下文，将 TARGET 翻译成恰当的中文，然后返回翻译结果 \
"""

    response = openai_clinet.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt_template},
        ],
    )
    return response.choices[0].message.content  # type: ignore


def main():
    subs = sub_obj(sub_file)
    for index, sub in enumerate(subs):
        context = "\n".join([ss.content for ss in subs[index - 2 : index + 3]])
        target: str = sub.content
        print(get_transalte(target=target, context=context).strip("。"))


if __name__ == "__main__":
    main()
