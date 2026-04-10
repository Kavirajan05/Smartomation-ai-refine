from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv

load_dotenv(PROJECT_ROOT / '.env')

from services.summarizer import generate_summary
from services.email import build_summary_html
from services.youtube import extract_video_id, fetch_transcript


def _load_payload() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    return json.loads(raw)


def _emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=True))


async def main() -> None:
    payload = _load_payload()

    youtube_url = str(payload.get('youtube_url', '')).strip()
    email = str(payload.get('email', '')).strip()

    if not youtube_url:
        raise ValueError('youtube_url is required')
    if not email:
        raise ValueError('email is required')

    video_id = extract_video_id(youtube_url)
    if not video_id:
        raise ValueError('Invalid YouTube URL')

    transcript = fetch_transcript(video_id)
    summary = generate_summary(transcript)
    email_body = build_summary_html(summary)

    result = {
        'status': 'success',
        'youtube_url': youtube_url,
        'video_id': video_id,
        'email': email,
        'summary': summary,
        'email_subject': 'Your YouTube Video Summary',
        'email_format': 'html',
        'email_body': email_body,
    }

    _emit(result)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as exc:  # noqa: BLE001
        _emit({'status': 'error', 'error': str(exc)})
        raise SystemExit(1) from exc