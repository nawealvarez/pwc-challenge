import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

CORRELATION_ID_HEADER = "X-Correlation-ID"

class CorrelationIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        incoming_id = request.headers.get(CORRELATION_ID_HEADER)
        correlation_id = incoming_id or str(uuid.uuid4())

        request.state.correlation_id = correlation_id 

        response = await call_next(request)
        response.headers[CORRELATION_ID_HEADER] = correlation_id
        return response