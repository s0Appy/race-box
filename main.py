# main.py

from queue import Queue, Empty
import time

from gps import GPSReader
#from imu.imu_reader import IMUReader
from utils.logger import CSVLogger


def main():
    # Shared queue for all sensor records
    telemetry_queue = Queue()

    # Create sensor threads (different speeds)
    gps_reader = GPSReader(queue=telemetry_queue)          # ~5 Hz
    #imu_reader = IMUReader(queue=telemetry_queue, rate_hz=100.0)  # 100 Hz

    # Single CSV log file for all telemetry
    logger = CSVLogger("telemetry_log.csv")

    print("Starting GPS + IMU telemetry logging… CTRL+C to stop")

    # Start sensor threads
    gps_reader.start()
    #imu_reader.start()

    try:
        while True:
            try:
                record = telemetry_queue.get(timeout=1.0)
            except Empty:
                # No new data; loop around
                continue

            # record is already shaped for CSVLogger.log_record
            logger.log_record(record)

    except KeyboardInterrupt:
        print("Stopping…")
    finally:
        gps_reader.stop()
        #imu_reader.stop()
        logger.close()
        print("Clean shutdown complete.")


if __name__ == "__main__":
    main()
