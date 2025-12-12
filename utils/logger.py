# utils/logger.py

import csv
from threading import Lock


class CSVLogger:
    """
    Thread-safe CSV logger that writes a superset of fields for GPS + IMU.
    Columns that don't apply for a given sensor are left empty.
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._f = open(filepath, "w", newline="")
        self._lock = Lock()

        self._writer = csv.writer(self._f)
        # Superset of columns (you can expand later)
        self._writer.writerow([
            "timestamp",     # ISO 8601
            "sensor",        # "gps" or "imu"
            "lat",
            "lon",
            "speed_m_s",
            "heading_deg",
            "ax",
            "ay",
            "az",
        ])
        self._f.flush()

    def log_record(self, record: dict):
        """
        record should contain:
          - "timestamp" (str)
          - "sensor" (str)
        And any subset of:
          - "lat", "lon", "speed_m_s", "heading_deg"
          - "ax", "ay", "az"
        Missing keys are written as empty fields.
        """
        with self._lock:
            self._writer.writerow([
                record.get("timestamp", ""),
                record.get("sensor", ""),
                record.get("lat", ""),
                record.get("lon", ""),
                record.get("speed_m_s", ""),
                record.get("heading_deg", ""),
                record.get("ax", ""),
                record.get("ay", ""),
                record.get("az", ""),
            ])
            self._f.flush()

    def close(self):
        with self._lock:
            self._f.close()
