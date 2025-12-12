# race-box
Single Board Computer based data logger and track mapper for race ops and simulations, built in python for simple extensibility, future C++ upgrade path 


// get the list of compenents down to ask gpt 
1) have the component on a seperate file andd then a main things to put it all togther
2) the gps neo 7m gps -> rasperby pie
MMA8452Q 

layer1: GPS             → UART (Serial)
Layer 2.1: IMU          → I²C
Layer 2.2: Magnetometer → I²C (same bus as IMU)
usually its a 6 axis ( we have a 3axis and not 6 )

GPS(neo 7m gps) = continuous stream (UDP - 1 send bit, 1 recieve bit)
IMU ((Inertial Measurement Unit) + Mag(Which way is North) = register-based sensors on shared bus

GPS Wriring (GPS is NOT I²C here.)
IMU: 
What it tells you:
Is the system accelerating or braking?
Tilt relative to gravity
Vibrations / shocks


Raspberry pie (main board)
Signal | Pi Pin | GPIO | Notes
SDA    |    3   | 2    | Signal
SCL    |    5   | 3    | Clock
GND    |    6   |      | Ground

So, both the wires connect to the same physical pin and a jumper is used to connect both the wires into one.
Each device has its own I²C address - IMU → 0x68 | Magnetometer → 0x1E


IMU wiring (2.1)
IMU pin | Raspberry Pi (Pin)
VCC	    |  1 (3.3V)
GND	    |  6 (GND)
SDA	    |  3 (GPIO 2)
SCL	    |  5 (GPIO 3)
INT1	|  16 (GPIO 23)
INT2	|  18 (GPIO 24)

INT pins - used for: data ready, fifo overflow, motion detection.

Magnetometer wiring (2.2)
Mag pin | Raspberry Pi (Pin)
VCC	    | 1 (3.3V)
GND	    | 6 (GND)
SDA	    | 3 (GPIO 2)
SCL	    | 5 (GPIO 3)


CODE

GPS (UART) - ser = serial.Serial("/dev/serial0", 9600) - continuous stream of data (UDP)

Each sentence:
Starts with $
Has a talker ID (GP, GN, etc.)
Has a message type (RMC, GGA, …)
Ends with a checksum

if line.startswith("$GPRMC"):
Only process sentences that are Recommended Minimum Navigation Data






I²C = a short-distance, on-board communication protocol that lets a controller talk to multiple chips using only two wires 
SCL (yellow)- serial clock - pin number 5 
SDA ()- serial data - pin number 3

int1 - pin 16 (gpio 23)
int2 - pin 18 (gpio 24)





