import serial
import struct
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import itertools

# COM 포트 지정
PORT = 'COM12'
MAX_POINTS = 200

ser = serial.Serial(PORT, 115200, timeout=1)
x_buffer = deque(maxlen=MAX_POINTS)
y_buffer = deque(maxlen=MAX_POINTS)
counter = itertools.count()
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-')
ax.set_ylim(0, 360)
ax.set_ylabel('Angle (deg)')
ax.set_xlabel('Sample')
ax.set_title('Real-time CAN Angle Data')
ax.grid(True)

def update(frame):
    while ser.in_waiting:
        raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
        if raw_line.startswith('rcv'):
            parts = raw_line.split()
            if len(parts) >= 3:
                hex_data = parts[2]
                try:
                    raw = bytes.fromhex(hex_data[0:8])
                    angle = struct.unpack('f', raw)[0] 
                    
                    y_buffer.append(angle)
                    x_buffer.append(next(counter))
                except (ValueError, struct.error):
                    continue

    if not x_buffer:
        return line,

    line.set_data(x_buffer, y_buffer)

    ax.set_xlim(x_buffer[0], x_buffer[-1] + 1)

    return line,

ani = animation.FuncAnimation(fig, update, interval=50, blit=False)
plt.tight_layout()
plt.show()