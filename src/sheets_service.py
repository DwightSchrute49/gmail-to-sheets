from googleapiclient.discovery import build
from src.gmail_service import get_gmail_service
from config import SPREADSHEET_ID, SHEET_NAME


def append_row(values):
    service = build(
        "sheets",
        "v4",
        credentials=get_gmail_service()._http.credentials
    )

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:D",
        valueInputOption="RAW",
        body={"values": [values]}
    ).execute()
