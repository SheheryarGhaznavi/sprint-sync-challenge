from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
import logging
import json


def registerLogging(app: FastAPI) -> None:
    logger = logging.getLogger("uvicorn.access")


    class LoggingMiddleware(BaseHTTPMiddleware):


        async def dispatch(self, request: Request, call_next):
            start_time = time.time()

            try:
                # Read request body (must replace the stream so downstream can still use it)
                request_body = await request.body()
                request_body_text = request_body.decode("utf-8") if request_body else ""

                # Process request and capture response
                response = await call_next(request)

                # Read response body
                response_body = b""
                async for chunk in response.body_iterator:
                    response_body += chunk

                # Replace response since we've consumed body_iterator
                new_response = Response(
                    content=response_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type
                )

                latency_ms = int((time.time() - start_time) * 1000)

                payload = {
                    "request": {
                        "method": request.method,
                        "path": str(request.url),
                        "requestHeaders": dict(request.headers),
                        "requestBody": request_body_text,
                    },
                    "response": {
                        "status": response.status_code,
                        "responseHeaders": dict(response.headers),
                        "responseBody": response_body.decode("utf-8"),
                    },
                    "latencyMs": latency_ms
                }

                logger.info(json.dumps(payload))

                return new_response

            except Exception as e:
                latency_ms = int((time.time() - start_time) * 1000)

                payload = {
                    "method": request.method,
                    "path": str(request.url),
                    "status": 500,
                    "requestHeaders": dict(request.headers),
                    "requestBody": request_body_text if 'request_body_text' in locals() else None,
                    "latencyMs": latency_ms,
                    "error": str(e),
                }

                logger.exception(json.dumps(payload))
                raise

    app.add_middleware(LoggingMiddleware)
