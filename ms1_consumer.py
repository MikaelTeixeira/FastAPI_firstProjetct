from rabbitmq_client import consume_messages


def handle_book_event(message: dict) -> None:
    event_type = message.get("event_type")
    payload = message.get("payload", {})
    print(f"[MS1] Received event from MS2: {event_type} -> {payload}")


if __name__ == "__main__":
    consume_messages("ms2_book_events", handle_book_event)
