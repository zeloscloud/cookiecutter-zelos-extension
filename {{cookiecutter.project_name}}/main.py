#!/usr/bin/env python3
"""{{cookiecutter.project_description}}"""

import logging
import signal
from types import FrameType

import zelos_sdk
from zelos_sdk.extensions import load_config
from zelos_sdk.hooks.logging import TraceLoggingHandler

from {{cookiecutter.project_slug}}.extension import SensorMonitor

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # Configure logging before SDK initialization
    logging.basicConfig(level=logging.INFO)

    # Initialize SDK
    zelos_sdk.init(name="{{cookiecutter.project_slug}}", actions=True)

    # Add trace logging handler to send logs to Zelos
    handler = TraceLoggingHandler("{{cookiecutter.project_slug}}_logger")
    logging.getLogger().addHandler(handler)

    # Load configuration and create sensor monitor
    config = load_config()
    monitor = SensorMonitor(config)

    # Register interactive actions for the Zelos App
    zelos_sdk.actions_registry.register(monitor)

    def shutdown_handler(signum: int, frame: FrameType | None) -> None:
        """Handle graceful shutdown on SIGTERM or SIGINT."""
        logger.info("Shutting down...")
        monitor.stop()

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    logger.info("Starting {{cookiecutter.project_name}}")
    monitor.start()
    monitor.run()
