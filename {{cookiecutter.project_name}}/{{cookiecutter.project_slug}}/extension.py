"""Example Sensor monitoring implementation."""

import logging
import random
import time
from typing import Any

import zelos_sdk

logger = logging.getLogger(__name__)


class SensorMonitor:
    """Monitors sensor data and streams to Zelos."""

    STATUS = {
        0: "OK",
        1: "WARNING",
        2: "ERROR",
    }

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the sensor monitor.

        :param config: Configuration from config.json
        """
        self.config = config
        self.running = False

        self.source = zelos_sdk.TraceSourceCacheLast("{{cookiecutter.project_slug}}")
        self._define_schema()

    def start(self) -> None:
        """Start monitoring."""
        logger.info(f"Starting {self.config.get('sensor_name', 'sensor')}")
        self.running = True

    def stop(self) -> None:
        """Stop monitoring."""
        logger.info("Stopping monitor")
        self.running = False

    def run(self) -> None:
        """Main monitoring loop."""
        loop_count = 0
        while self.running:
            # Simulate sensor readings
            temp = 20.0 + random.uniform(-5, 5)
            pressure = 1013.25 + random.uniform(-10, 10)
            voltage = 12.0 + random.uniform(-0.5, 0.5)
            current = 2.5 + random.uniform(-0.3, 0.3)

            # Determine status based on cached temperature
            status = 0  # OK
            last_temp = self.source.environmental.temperature.get()
            if last_temp:
                if last_temp > 30:
                    status = 2  # ERROR
                elif last_temp > 25:
                    status = 1  # WARNING

            self.source.environmental.log(
                temperature=temp,
                pressure=pressure,
                status=status,
            )

            self.source.power.log(
                voltage=voltage,
                current=current,
            )

            # Log every 10 loops
            loop_count += 1
            if loop_count % 10 == 0:
                logger.info(
                    f"temp={temp:.1f}°C, pressure={pressure:.1f}hPa, "
                    f"voltage={voltage:.1f}V, current={current:.1f}A, "
                    f"status={self.STATUS[status]}"
                )

            time.sleep(self.config.get("interval", 0.1))

    @zelos_sdk.action("Set Interval", "Change sample rate")
    @zelos_sdk.action.number(
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
        return {"message": f"Interval set to {seconds}s", "interval": seconds}

    @zelos_sdk.action("Get Status", "Get current sensor status")
    def get_status(self) -> dict[str, Any]:
        """Get current sensor status.

        :return: Status dictionary with current values
        """
        return {
            "running": self.running,
            "interval": self.config.get("interval", 0.1),
            "temperature": self.source.environmental.temperature.get(),
            "pressure": self.source.environmental.pressure.get(),
            "voltage": self.source.power.voltage.get(),
            "current": self.source.power.current.get(),
            "status": self.STATUS[self.source.environmental.status.get()],
        }

    def _define_schema(self) -> None:
        """Define trace schema."""
        self.source.add_event(
            "environmental",
            [
                zelos_sdk.TraceEventFieldMetadata("temperature", zelos_sdk.DataType.Float32, "°C"),
                zelos_sdk.TraceEventFieldMetadata("pressure", zelos_sdk.DataType.Float32, "hPa"),
                zelos_sdk.TraceEventFieldMetadata("status", zelos_sdk.DataType.UInt8),
            ],
        )

        self.source.add_event(
            "power",
            [
                zelos_sdk.TraceEventFieldMetadata("voltage", zelos_sdk.DataType.Float32, "V"),
                zelos_sdk.TraceEventFieldMetadata("current", zelos_sdk.DataType.Float32, "A"),
            ],
        )

        # Value table for status field
        self.source.add_value_table("environmental", "status", self.STATUS)
