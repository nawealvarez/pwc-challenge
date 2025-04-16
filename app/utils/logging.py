import logging
from typing import Optional
from fastapi import Request

def log_with_correlation(level: str, message: str, request: Optional[Request] = None):
  logger = logging.getLogger(__name__)
  correlation_id = getattr(request.state, "correlation_id", "N/A") if request else "N/A"
  log_method = getattr(logger, level, logger.info)
  log_method(message, extra={"correlation_id": correlation_id})