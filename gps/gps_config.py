import time

def ubx_checksum(payload: bytes | bytearray) -> bytes:
    ck_a = 0
    ck_b = 0
    for b in payload:
        ck_a = (ck_a + b) & 0xFF
        ck_b = (ck_b + ck_a) & 0xFF
    return bytes([ck_a, ck_b])


def set_rate_10hz(ser):
    """
    Configure u-blox Neo-7M (or similar) to 10 Hz using UBX-CFG-RATE.
    measRate = 100 ms, navRate = 1, timeRef = GPS.
    """
    msg = bytearray([
        0xB5, 0x62,     # sync chars
        0x06, 0x08,     # class, id = CFG-RATE
        0x06, 0x00,     # payload length = 6
        0x64, 0x00,     # measRate = 100 ms
        0x01, 0x00,     # navRate = 1
        0x01, 0x00,     # timeRef = GPS
    ])

    ck = ubx_checksum(msg[2:])
    msg.extend(ck)
    ser.write(msg)
    time.sleep(0.2)
    print("✔ Set GPS output rate to 10 Hz")

