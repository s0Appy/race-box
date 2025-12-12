import math
import random
import time

# =====================================================
# Mock IMU (Accelerometer + Gyroscope)
# =====================================================
class MockIMU:
    def __init__(self):
        # Later: calibration values can go here
        pass

    def read_accel(self):
        """
        Simulate accelerometer readings in m/s^2.
        Assumes the sensor is mostly stationary with gravity on Z.
        """
        return {
            "ax": random.uniform(-0.05, 0.05),        # small noise
            "ay": random.uniform(-0.05, 0.05),
            "az": 9.81 + random.uniform(-0.1, 0.1),   # gravity + noise
        }

    def read_gyro(self):
        """
        Simulate gyroscope readings in deg/s.
        Small drift/noise only.
        """
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
        """
        Simulate Earth's magnetic field rotating slowly.
        This makes heading change smoothly over time.
        """
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
    """
    Compute compass heading from magnetometer X/Y.
    Returns heading in degrees [0, 360).
    """
    heading = math.degrees(math.atan2(my, mx))
    return heading if heading >= 0 else heading + 360


def compute_roll_pitch_deg(ax: float, ay: float, az: float):
    """
    Compute roll and pitch from accelerometer.
    Assumes gravity dominates (valid for low acceleration).
    """
    roll = math.degrees(math.atan2(ay, az))
    pitch = math.degrees(math.atan2(-ax, math.sqrt(ay * ay + az * az)))
    return roll, pitch


# =====================================================
# Main Test Loop
# =====================================================
def main():
    imu = MockIMU()
    mag = MockMagnetometer()

    print("=== Layer 2 Sensor Test (NO HARDWARE REQUIRED) ===")
    print("Press Ctrl+C to stop\n")

    while True:
        accel = imu.read_accel()
        gyro = imu.read_gyro()
        magv = mag.read_mag()

        roll, pitch = compute_roll_pitch_deg(
            accel["ax"], accel["ay"], accel["az"]
        )
        heading = compute_heading_deg(magv["mx"], magv["my"])

        print(
            f"ROLL={roll:6.2f}°  "
            f"PITCH={pitch:6.2f}°  "
            f"HEADING={heading:6.2f}°"
        )

        time.sleep(0.2)


if __name__ == "__main__":
    main()
