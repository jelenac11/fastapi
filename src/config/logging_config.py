import logging
from datetime import UTC, datetime

from pythonjsonlogger import json

LOG_FORMAT_DEBUG = "%(time)s %(level)s %(name)s %(message)s"


class UtcJsonFormatter(json.JsonFormatter):
    """Timezone-aware JSON log formatter."""

    def format_time(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        dt = datetime.fromtimestamp(record.created, tz=UTC)
        return dt.strftime(datefmt) if datefmt else dt.isoformat()

    def format(self, record: logging.LogRecord) -> str:
        # Format the time first
        record.asctime = self.format_time(record)
        # Modify the record's dictionary to match the desired format
        record.time = record.asctime
        record.level = record.levelname
        return str(super().format(record))


def setup_logging() -> None:
    log_level = logging.INFO
    json_formatter = UtcJsonFormatter(fmt=LOG_FORMAT_DEBUG)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_handler = logging.StreamHandler()
    root_handler.setFormatter(json_formatter)
    root_logger.handlers = [root_handler]

    logging.getLogger("uvicorn.access").disabled = True

    # Configure Uvicorn loggers to use JSON formatting
    uvicorn_loggers = ["uvicorn", "uvicorn.error"]
    for logger_name in uvicorn_loggers:
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers = [root_handler]
        uvicorn_logger.propagate = False  # Prevent double logging
