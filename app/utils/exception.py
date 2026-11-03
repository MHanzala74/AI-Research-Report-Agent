"""
Custom exception with traceback-enriched messages.
"""
import sys
import logging

log = logging.getLogger("app")


def _detail(error: Exception) -> str:
    _, _, tb = sys.exc_info()
    if tb is None:
        return str(error)
    file_name = tb.tb_frame.f_code.co_filename
    line_no   = tb.tb_lineno
    return f"[{file_name}] line {line_no} — {error}"


class AgentException(Exception):
    """Top-level exception for all agent pipeline errors."""

    def __init__(self, error: Exception):
        self.detail = _detail(error)
        log.error("AgentException: %s", self.detail)
        super().__init__(self.detail)

    def __str__(self) -> str:
        return self.detail
