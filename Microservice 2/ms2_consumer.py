from database.db_setup import SessionLocal
from rabbitmq_client import consume_messages
from services import BookService


def handle_ms1_user_event(message: dict) -> None:
    event_type = message.get("event_type")
    payload = message.get("payload", {})

    if event_type != "user.deleted":
        print(f"[MS2] Ignoring event: {event_type}")
        return

    owner_user_id = payload.get("user_id")
    if owner_user_id is None:
        print("[MS2] Event without user_id ignored")
        return

    db = SessionLocal()
    try:
        service = BookService(db)
        deactivated_count = service.deactivate_books_by_owner(owner_user_id)
        print(
            f"[MS2] Deactivated {deactivated_count} books after user deletion. "
            f"user_id={owner_user_id}"
        )
    finally:
        db.close()


if __name__ == "__main__":
    consume_messages("ms1_user_events", handle_ms1_user_event)
