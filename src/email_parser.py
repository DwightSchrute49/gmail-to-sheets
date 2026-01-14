import base64
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime


def _decode_base64(data):
    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")


def extract_body(payload):
    if "parts" not in payload:
        if payload.get("mimeType") == "text/plain":
            return _decode_base64(payload["body"].get("data", ""))
        return ""

    plain_text = None
    html_text = None

    for part in payload["parts"]:
        mime = part.get("mimeType")

        if mime == "text/plain" and "data" in part["body"]:
            plain_text = _decode_base64(part["body"]["data"])
            break 

        if mime == "text/html" and "data" in part["body"]:
            html_text = _decode_base64(part["body"]["data"])

    if plain_text:
        return plain_text.strip()

    if html_text:
        soup = BeautifulSoup(html_text, "html.parser")
        return soup.get_text(separator="\n").strip()

    return ""


def parse_email(message):
    headers = message["payload"]["headers"]

    sender = subject = date = ""

    for h in headers:
        if h["name"] == "From":
            sender = h["value"]
        elif h["name"] == "Subject":
            subject = h["value"]
        elif h["name"] == "Date":
            date = parsedate_to_datetime(h["value"]).strftime("%Y-%m-%d %H:%M:%S")

    body = extract_body(message["payload"])

    return sender, subject, date, body
