import json
import re
import logging

logger = logging.getLogger(__name__)

def clean_json_response(response_text: str) -> str:
    """Clean text containing JSON by removing markdown fences and extracting the first JSON object."""
    if response_text is None:
        return ""
    logger.debug(f"Raw response_text for cleaning: {response_text!r}")

    cleaned = re.sub(r"```(?:json)?\s*", "", response_text)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", cleaned)
    if match:
        cleaned = match.group(1)
    return cleaned.strip()


def try_parse_json(text: str):
    """Try to extract and parse JSON objects from a string."""
    if text is None:
        return None

    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text).strip()

    matches = re.findall(r'(\{[\s\S]*?\})(?=\{|\Z)', text)
    parsed_list = []

    for m in matches:
        try:
            parsed_list.append(json.loads(m))
        except json.JSONDecodeError:
            continue

    if not parsed_list:
        return None
    if len(parsed_list) == 1:
        return parsed_list[0]
    return parsed_list
