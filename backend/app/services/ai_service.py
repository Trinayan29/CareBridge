import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.core.config import settings


class AIService:
    def _chat(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise ValueError("AI prompt cannot be empty.")

        if not settings.BOB_API_KEY:
            raise RuntimeError(
                "AI service is not configured: BOB_API_KEY is missing."
            )

        payload = {
            "model": settings.BOB_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        }
        request = Request(
            settings.BOB_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {settings.BOB_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"AI provider returned HTTP {exc.code}: {detail[:500]}"
            ) from exc
        except URLError as exc:
            raise RuntimeError(
                f"Could not reach the AI provider: {exc.reason}"
            ) from exc
        except TimeoutError as exc:
            raise RuntimeError("AI provider request timed out.") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError("AI provider returned invalid JSON.") from exc

        choices = result.get("choices") or []
        if not choices:
            raise RuntimeError(
                "AI provider response did not contain any choices."
            )

        message = choices[0].get("message") or {}
        content = message.get("content")
        if isinstance(content, list):
            content = "\n".join(
                item.get("text", "")
                for item in content
                if isinstance(item, dict)
            )

        if not isinstance(content, str) or not content.strip():
            raise RuntimeError(
                "AI provider returned an empty assistant response."
            )

        return content.strip()

    def analyze_medical_report(
        self,
        extracted_text: str,
    ) -> dict[str, Any]:

        report_text = extracted_text.strip()

        if not report_text:
            raise ValueError(
                "The medical report does not contain readable text."
            )

        prompt = f"""
TASK: MEDICAL REPORT TEXT ANALYSIS

You are a medical-report text analysis component.

The following content is the COMPLETE medical report.
It is provided directly as TEXT.
There is NO attachment to request.
There is NO missing document.

Your task is ONLY to analyze the report text below.

Do NOT analyze:
- software
- programming
- CareBridge
- FastAPI
- Python
- SQLAlchemy
- backend architecture
- IBM Bob

Do NOT ask the user to upload or attach a report.

Do NOT diagnose disease.
Do NOT prescribe medication.
Do NOT invent information.

Use ONLY information explicitly present in the report.

If reference ranges are present, compare values against them.

MEDICAL_REPORT_BEGIN

{report_text}

MEDICAL_REPORT_END


Return exactly these four sections:

REPORT_SUMMARY:
Give a short, simple summary based only on the report.

KEY_FINDINGS:
- List important values or findings explicitly present in the report.
- Mention whether provided values are within their provided reference ranges.

WHAT_TO_DISCUSS_WITH_A_PROFESSIONAL:
- Give appropriate points to discuss with a qualified healthcare professional.
- Do not make a diagnosis.

FOLLOW_UP_QUESTIONS:
1. Question based on information missing from the report.
2. Question based on information missing from the report.
3. Question based on information missing from the report.
4. Question based on information missing from the report.

IMPORTANT:
The report text above is the data to analyze.
Do not request an attachment.
Do not discuss the application.
"""

        analysis = self._chat(prompt)

        return {
            "status": "completed",
            "analysis": analysis,
            "extracted_text_available": True,
        }

    def analyze_health_concern(
        self,
        title: str,
        description: str,
    ) -> dict[str, Any]:

        prompt = f"""
You are an AI component inside the CareBridge application.

You are NOT a doctor and must NOT diagnose medical conditions.

Analyze the following user's health concern.

TITLE:
{title}

DESCRIPTION:
{description}

Provide safe, general healthcare-navigation information.

Do not prescribe medication or dosage.
Do not tell the user to stop prescribed medication.

Return:

GUIDANCE:
<general non-diagnostic guidance>

MONITOR:
<what the user should monitor>

WHEN_TO_SEEK_CARE:
<when professional medical evaluation may be appropriate>

FOLLOW_UP_QUESTIONS:
1. <question>
2. <question>
3. <question>
4. <question>
"""

        guidance = self._chat(prompt)

        return {
            "guidance": guidance,
            "follow_up_questions": [
                "When did this problem start?",
                "How severe is it?",
                "Has it been getting better or worse?",
                "Are you experiencing any other symptoms?",
            ],
        }


ai_service = AIService()