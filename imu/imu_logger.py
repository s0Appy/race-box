import math
import random
import time
from datetime import datetime, timezone
import csv

# =====================================================
# Mock IMU (Accelerometer + Gyroscope)
# =====================================================
class MockIMU:
    def read_accel(self):
        return {
            "ax": random.uniform(-0.05, 0.05),
            "ay": random.uniform(-0.05, 0.05),
            "az": 9.81 + random.uniform(-0.1, 0.1),
        }

    def read_gyro(self):
        return {
            "gx": random.uniform(-0.2, 0.2),
            "gy": random.uniform(-0.2, 0.2),
            "gz": random.uniform(-0.5, 0.5),
        }


# =====================================================
# Mock Magnetometer
# =====================================================
class MockMagnetometer:
    def read_mag(self):
        t = time.time()
        return {
            "mx": math.cos(t),
            "my": math.sin(t),
            "mz": 0.0,
        }


# =====================================================
# Math / Logic
# =====================================================
def compute_heading_deg(mx: float, my: float) -> float:
    heading = math.degrees(math.atan2(my, mx))
    return heading if heading >= 0 else heading + 360


def compute_roll_pitch_deg(ax: float, ay: float, az: float):
    roll = math.degrees(math.atan2(ay, az))
    pitch = math.degrees(math.atan2(-ax, math.sqrt(ay * ay + az * az)))
    return roll, pitch


# =====================================================
# Main
# =====================================================
def main():
    imu = MockIMU()
    mag = MockMagnetometer()

    # Open CSV file
    with open("layer2_imu_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "roll_deg",
            "pitch_deg",
            "heading_mag_deg"
        ])

        print("Layer 2 CSV logger running (mock data)")
        print("Writing to layer2_imu_log.csv")
        print("Ctrl+C to stop\n")

        try:
            while True:
                accel = imu.read_accel()
                magv = mag.read_mag()

                roll, pitch = compute_roll_pitch_deg(
                    accel["ax"], accel["ay"], accel["az"]
                )
                heading = compute_heading_deg(
                    magv["mx"], magv["my"]
                )

                ts = datetime.now(timezone.utc).isoformat()

                writer.writerow([
                    ts,
                    round(roll, 3),
                    round(pitch, 3),
                    round(heading, 3)
                ])
                f.flush()

                print(
                    f"ROLL={roll:6.2f}°  "
                    f"PITCH={pitch:6.2f}°  "
                    f"HEADING={heading:6.2f}°"
                )

                time.sleep(0.2)

        except KeyboardInterrupt:
            print("\nStopped logging.")


if __name__ == "__main__":
    main()
