# GPS LOGGER 
import serial
import time
import pynmea2
from datetime import datetime, timezone

# PORT = "/dev/ttyACM0" # usb port for built in module usb
PORT = "/dev/serial0" # serial port via rasberry pi
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)

# ----------------------------
# UBX helper: Fletcher checksum
# ----------------------------
def ubx_checksum(payload):
    ck_a = 0
    ck_b = 0
    for b in payload:
        ck_a = (ck_a + b) & 0xFF
        ck_b = (ck_b + ck_a) & 0xFF
    return bytes([ck_a, ck_b])

# ----------------------------
# Set 5 Hz update rate
# ----------------------------
def set_rate_5hz():
    # UBX header + CFG-RATE + length
    msg = bytearray([
        0xB5, 0x62,     # UBX sync chars
        0x06, 0x08,     # Class=CFG, ID=RATE
        0x06, 0x00,     # Payload length = 6 bytes
        0xC8, 0x00,     # measRate = 200 ms → 5 Hz
        0x01, 0x00,     # navRate = 1 cycle
        0x01, 0x00      # timeRef = GPS
    ])
    # Compute checksum for last 6 bytes
    ck = ubx_checksum(msg[2:])
    msg.extend(ck)
    ser.write(msg)
    time.sleep(0.2)
    print("✔ Set GPS output rate to 5 Hz")


# Optional: disable all but GGA/RMC
def disable_noise():
    # (Not writing the full UBX-CFG-MSG set here unless you ask)
    pass


set_rate_5hz()
# disable_noise()

print("Logging… CTRL+C to stop")

f = open("gps_log.csv", "w")
f.write("timestamp,lat,lon,speed_m_s,heading_deg\n")

while True:
    try:
        line = ser.readline().decode("ascii", errors="ignore").strip()
        if line.startswith("$GPRMC"):
            msg = pynmea2.parse(line)

            if msg.status != "A":  # Valid fix?
                continue

            lat = msg.latitude
            lon = msg.longitude

            # Safe speed parsing
            try:
                speed_knots = float(msg.spd_over_grnd) if msg.spd_over_grnd not in (None, "") else 0.0
            except ValueError:
                speed_knots = 0.0

            speed_m_s = speed_knots * 0.514444  # knots → m/s
            heading = float(msg.true_course) if msg.true_course not in (None, "") else 0.0

            # Modern UTC timestamp
            ts = datetime.now(timezone.utc).isoformat()

            f.write(f"{ts},{lat},{lon},{speed_m_s},{heading}\n")
            f.flush()

            print(lat, lon, speed_m_s, heading)

    except KeyboardInterrupt:
        print("Stopping…")
        break
    except Exception as e:
        print("Error:", e)
        pass

f.close()
ser.close()
