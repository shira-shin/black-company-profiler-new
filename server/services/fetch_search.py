import os
from openai import OpenAI, OpenAIError

# initialize OpenAI client once
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

async def fetch_search(company: str) -> str:
    """
    OpenAI Responses API を使って company の最新ニュースと概要を取得。
    失敗時は空文字を返す。
    """
    prompt = f"{company}の最新ニュースと企業概要を教えてください。"
    try:
        res = await client.responses.create(
            model='gpt-4o',
            input=prompt,
            tools=[{'type': 'web_search'}]
        )
        # .result が None だった場合にも文字列を返す
        return res.result or ""
    except OpenAIError:
        # APIエラー時はログ出力など入れても良いですが、ここでは空文字を返します
        return ""
