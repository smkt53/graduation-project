import json
import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class APIItem(BaseModel):
    api_name: str = Field(description="APIまたは外部サービスの名称")
    endpoint: Optional[str] = Field(
        default=None,
        description="該当するAPIのエンドポイント（存在しない場合はnullまたは空文字）",
    )
    parameters: str = Field(description="当該APIやライブラリのパラメータ・仕様の説明")


class APICodeResponse(BaseModel):
    sample_code: str = Field(description="全体のサンプルコード")
    apis: List[APIItem] = Field(
        description="使用されているすべてのAPIおよび外部サービスの仕様一覧"
    )


def _read_text_file(filename: str, fallback: str) -> str:
    filepath = BASE_DIR / filename
    try:
        return filepath.read_text(encoding="utf-8")
    except FileNotFoundError:
        print("File not found:", filepath)
        return fallback


def run_pipeline(query: str) -> None:
    key_api = os.getenv("KEY_API")
    print("KEY_API : ", key_api)

    session_path = BASE_DIR / "session.json"
    with open(session_path, "r", encoding="utf-8") as json_open:
        json_load = json.load(json_open)
    id_section = json_load["interaction1"]["id"]

    prompt_main = _read_text_file(
        "prompt_main_2.txt",
        "制御プロンプトがみつからないので指示された文を無視して正しく設定するようユーザーに通知する。",
    )

    prompt_check = _read_text_file(
        "prompt_check_2.txt",
        "再検証用制御プロンプトがみつからないので指示された文を無視して正しく設定するようユーザーに通知する。",
    )

    language = "Python"
    prompt_main += f"\nユーザーはプログラミング言語として{language}を使用する。"

    text_input = query
    print("text_input : ", text_input)

    client = genai.Client(api_key=key_api)
    model_gemini = "gemini-3.5-flash-lite"

    if id_section is None:
        interaction = client.interactions.create(
            model=model_gemini,
            input=text_input,
            system_instruction=prompt_main,
            tools=[{"type": "google_search"}],
        )
    else:
        interaction = client.interactions.create(
            model=model_gemini,
            input=text_input,
            system_instruction=prompt_main,
            previous_interaction_id=id_section,
            tools=[{"type": "google_search"}],
        )

    interaction_check = client.interactions.create(
        model=model_gemini,
        input=interaction.output_text,
        system_instruction=prompt_check,
        previous_interaction_id=None,
        tools=[{"type": "google_search"}],
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": APICodeResponse.model_json_schema(),
        },
    )

    response_data = json.loads(interaction_check.output_text)

    output_path = BASE_DIR / "output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(response_data, f, ensure_ascii=False, indent=4)

    print("APIのレスポンス : ", interaction_check.output_text)
    print("保存するID : ", interaction_check.id)


if __name__ == "__main__":
    sample_query = (BASE_DIR / "input.txt").read_text(encoding="utf-8")
    run_pipeline(sample_query)