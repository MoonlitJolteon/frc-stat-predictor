import logging
import os
from datetime import datetime


class Logger:
    """Handles logging for the application"""

    def __init__(self, log_dir="logs", log_level=logging.INFO):
        self.log_dir = log_dir

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(
            log_dir, f"frcsp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

        self.logger = logging.getLogger("frcsp")
        self.logger.setLevel(log_level)

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        """Log an info message"""
        self.logger.info(message)

    def warning(self, message):
        """Log a warning message"""
        self.logger.warning(message)

    def error(self, message):
        """Log an error message"""
        self.logger.error(message)

    def debug(self, message):
        """Log a debug message"""
        self.logger.debug(message)
