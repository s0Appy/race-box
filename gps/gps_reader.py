# gps/gps_reader.py

import serial
import time
import pynmea2
from datetime import datetime, timezone
from threading import Thread
from queue import Queue

from .gps_config import set_rate_5hz


class GPSReader(Thread):
    """
    Reads NMEA from a u-blox Neo-7M at ~5 Hz and pushes
    parsed data into a queue as simple dicts ready for CSV logging.
    """

    def __init__(self, port="/dev/serial0", baud=9600, queue: Queue | None = None):
        super().__init__(daemon=True)
        self.port = port
        self.baud = baud
        self.queue = queue or Queue()
        self._running = True

        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        # Configure GPS update rate once at startup
        set_rate_5hz(self.ser)

    def stop(self):
        self._running = False
        try:
            self.ser.close()
        except Exception:
            pass

    def run(self):
        print("GPSReader started")
        while self._running:
            try:
                line = self.ser.readline().decode("ascii", errors="ignore").strip()
                if not line.startswith("$GPRMC"):
                    continue

                print("lock found")

                msg = pynmea2.parse(line)

                # Only log valid fixes
                if getattr(msg, "status", None) != "A":
                    continue

                lat = msg.latitude
                lon = msg.longitude

                # Safe speed parsing
                try:
                    speed_knots = float(msg.spd_over_grnd or 0.0)
                except ValueError:
                    speed_knots = 0.0

                speed_m_s = speed_knots * 0.514444  # knots → m/s

                try:
                    heading = float(msg.true_course or 0.0)
                except ValueError:
                    heading = 0.0

                ts = datetime.now(timezone.utc).isoformat()

                self.queue.put({
                    "sensor": "gps",
                    "timestamp": ts,
                    "lat": lat,
                    "lon": lon,
                    "speed_m_s": speed_m_s,
                    "heading_deg": heading,
                })

            except Exception as e:
                print("GPS error:", e)
                time.sleep(0.1)
