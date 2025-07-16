def has_channel_id_and_thread_ts(payload: dict) -> bool:
    """Verifies if the given payload has both channel_id and thread_ts under assistant_thread property.
    This data pattern is available for assistant_* events.
    """
    return (
        payload.get("assistant_thread") is not None
        and payload["assistant_thread"].get("channel_id") is not None
        and payload["assistant_thread"].get("thread_ts") is not None
    )
