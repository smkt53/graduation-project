import json
import os
from pathlib import Path
from typing import List, Optional
from enum import Enum

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class SupportStatus(str, Enum):
    ACTIVE = "提供中"
    DEPRECATED = "非推奨"
    SUNSET_PLANNED = "終了予定"
    ENDED = "提供終了"
    UNKNOWN = "不明"


class VersionCheckItem(BaseModel):
    version: str = Field(
        description="確認したバージョンまたは製品名（例: 2.5, One Call 3.0）"
    )
    status: SupportStatus = Field(
        description="そのバージョンの公式なサポート状況。確認できなければ「不明」"
    )
    next_hint: Optional[str] = Field(
        default=None,
        description="公式が示している後継・移行先の手がかり。なければnull",
    )
    evidence_url: Optional[str] = Field(
        default=None,
        description="状態や後継の根拠とした公式ページのURL。確認できなければnull",
    )


class APIItem(BaseModel):
    api_name: Optional[str] = Field(
        description="APIまたは外部サービスの名称"
    )
    endpoint: Optional[str] = Field(
        default=None,
        description="該当するAPIのエンドポイント（存在しない場合はnullまたは空文字）",
    )
    parameters: Optional[str] = Field(
        description=(
            "「取得したドキュメントのバージョン」「サポート状況と移行経路」"
            "「エンドポイント」「HTTPメソッド」「認証」「リクエストパラメータ」"
            "「レスポンス」を順に記載した、当該APIやライブラリの仕様の説明"
        )
    )


class APICodeResponse(BaseModel):
    version_check_log: List[VersionCheckItem] = Field(
        description="後継探索で確認したバージョン・製品を、確認した順に記録したログ"
    )
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

    NEED_INPUT_TAG = "[NEED_USER_INPUT]"
    first_output = (interaction.output_text or "").strip()

    if first_output.startswith(NEED_INPUT_TAG):
        question_text = first_output.removeprefix(NEED_INPUT_TAG).strip()
        response_data = {
            "sample_code": question_text,
            "apis": [],
        }
    else:
        interaction_check = client.interactions.create(
            model=model_gemini,
            input=first_output,
            system_instruction=prompt_check,
            previous_interaction_id=None,
            tools=[{"type": "google_search"}, {"type": "url_context"}],
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": APICodeResponse.model_json_schema(),
            },
        )
        response_data = json.loads(interaction_check.output_text)
        print("APIのレスポンス : ", interaction_check.output_text)

    output_path = BASE_DIR / "output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(response_data, f, ensure_ascii=False, indent=4)

    print("APIのレスポンス : ", interaction.output_text)
    


if __name__ == "__main__":
    sample_query = (BASE_DIR / "input.txt").read_text(encoding="utf-8")
    run_pipeline(sample_query)