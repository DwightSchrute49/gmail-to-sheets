import json
import os
from src.gmail_service import get_gmail_service
from src.email_parser import parse_email
from src.sheets_service import append_row

STATE_DIR = "state"
STATE_FILE = os.path.join(STATE_DIR, "processed_ids.json")


def load_state():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, "r") as f:
        return set(json.load(f))


def save_state(processed_ids):
    with open(STATE_FILE, "w") as f:
        json.dump(list(processed_ids), f)


def main():
    os.makedirs(STATE_DIR, exist_ok=True)

    processed_ids = load_state()
    gmail = get_gmail_service()

    response = gmail.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"]
    ).execute()

    messages = response.get("messages", [])

    for msg_meta in messages:
        msg_id = msg_meta["id"]

        if msg_id in processed_ids:
            continue  # 🚫 prevent duplicates

        message = gmail.users().messages().get(
            userId="me",
            id=msg_id,
            format="full"
        ).execute()

        sender, subject, received_at, body = parse_email(message)
        append_row([sender, subject, received_at, body])

        gmail.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

        processed_ids.add(msg_id)

    save_state(processed_ids)
    print("✅ Unread emails synced successfully.")

if __name__ == "__main__":
    main()
