"""Example Sensor monitoring implementation."""

import logging
import random
import time
from typing import Any

import zelos_sdk
from zelos_sdk.actions import action

logger = logging.getLogger(__name__)


class SensorMonitor:
    """Monitors sensor data and streams to Zelos."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the sensor monitor.

        :param config: Configuration from config.json
        """
        self.config = config
        self.running = False
        self._start_time = 0.0

        # Create trace source for this extension
        self.source = zelos_sdk.TraceSource("{{cookiecutter.project_slug}}")
        self._define_schema()

    def start(self) -> None:
        """Start monitoring."""
        sensor_name = self.config.get("sensor_name", "sensor")
        logger.info(f"Starting {sensor_name}")
        self.running = True
        self._start_time = time.time()

    def stop(self) -> None:
        """Stop monitoring gracefully."""
        logger.info("Stopping monitor")
        self.running = False

    def run(self) -> None:
        """Main run loop - collect and stream sensor data."""
        while self.running:
            try:
                # Collect and log environmental sensor readings
                temp = 20.0 + random.uniform(-5, 5)  # Simulate 15-25°C
                humidity = 50.0 + random.uniform(-15, 15)  # Simulate 35-65%

                self.source.environmental.log(
                    temperature=temp,
                    humidity=humidity,
                )

                # Collect and log power readings
                voltage = 12.0 + random.uniform(-0.5, 0.5)  # Simulate 11.5-12.5V
                current = 2.5 + random.uniform(-0.3, 0.3)  # Simulate 2.2-2.8A

                self.source.power.log(
                    voltage=voltage,
                    current=current,
                )

                # Sleep for configured interval
                time.sleep(self.config.get("interval", 0.1))

            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                time.sleep(1)

    @action("Set Interval", "Change sample rate")
    @action.number(
        "seconds",
        minimum=0.001,
        maximum=1.0,
        multiple_of=0.001,
        default=0.1,
        title="Interval (seconds)",
        description="Sample interval from 1kHz to 1Hz",
        widget="range",
    )
    def set_interval(self, seconds: float) -> dict[str, Any]:
        """Update the sample interval.

        :param seconds: New interval in seconds (0.001 to 1.0)
        :return: Confirmation dictionary with keys:
            - message (str): Success message
            - interval (float): The new interval value
        """
        self.config["interval"] = seconds
        logger.info(f"Interval updated to {seconds}s")
        return {"message": f"Interval set to {seconds}s", "interval": seconds}

    def _define_schema(self) -> None:
        """Define trace event schemas with types and units."""
        # Environmental sensor readings - temperature and humidity
        self.source.add_event(
            "environmental",
            [
                zelos_sdk.TraceEventFieldMetadata("temperature", zelos_sdk.DataType.Float32, "°C"),
                zelos_sdk.TraceEventFieldMetadata("humidity", zelos_sdk.DataType.Float32, "%"),
            ],
        )

        # Power readings - voltage and current
        self.source.add_event(
            "power",
            [
                zelos_sdk.TraceEventFieldMetadata("voltage", zelos_sdk.DataType.Float32, "V"),
                zelos_sdk.TraceEventFieldMetadata("current", zelos_sdk.DataType.Float32, "A"),
            ],
        )
