import json
import subprocess
from typing import Any


BOB_PATH = r"C:\Users\Trinayan\AppData\Roaming\npm\bob.cmd"


class AIService:

    def _chat(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise ValueError("Bob prompt cannot be empty.")

        try:
            result = subprocess.run(
                [
                    BOB_PATH,
                    "run",
                    "--format",
                    "json",
                    "--trust",
                ],
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=120,
                cwd=".",
            )

        except subprocess.TimeoutExpired:
            raise RuntimeError("IBM Bob request timed out.")

        except FileNotFoundError:
            raise RuntimeError(
                f"IBM Bob Shell was not found at: {BOB_PATH}"
            )

        if result.returncode != 0:
            error_message = (
                result.stderr.strip()
                if result.stderr
                else "Unknown Bob Shell error."
            )

            raise RuntimeError(
                f"IBM Bob request failed: {error_message}"
            )

        if not result.stdout:
            raise RuntimeError(
                "IBM Bob returned no output."
            )

        try:
            data = json.loads(result.stdout)

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"IBM Bob returned invalid JSON: {result.stdout}"
            ) from exc

        if data.get("status") != "success":
            raise RuntimeError(
                f"IBM Bob request was unsuccessful: {data}"
            )

        message = data.get("last_message")

        if not message:
            raise RuntimeError(
                "IBM Bob returned no assistant message."
            )

        return message

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