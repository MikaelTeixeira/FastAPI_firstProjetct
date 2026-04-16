from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import HTTPException, Request, status

_request_store: dict[tuple[str, str], list[datetime]] = defaultdict(list)


def limit_requests(bucket: str, max_requests: int = 5, window_seconds: int = 60):
    async def dependency(request: Request):
        now = datetime.utcnow()
        key = (bucket, request.client.host if request.client else "unknown")
        window_start = now - timedelta(seconds=window_seconds)

        _request_store[key] = [
            request_time
            for request_time in _request_store[key]
            if request_time > window_start
        ]

        if len(_request_store[key]) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Try again later.",
            )

        _request_store[key].append(now)

    return dependency
