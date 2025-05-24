import serial

# Replace with your actual Arduino port
arduino_port = 'COM7'
baud_rate = 9600

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to {arduino_port} at {baud_rate} baud rate.")

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print("Raw:", line)

            try:
                # Example expected format:
                # Temp: 25.00 C, Hum: 60.00 %, MQ-3: 400, LDR: 300
                parts = line.split(',')
                temperature = float(parts[0].split(':')[1].strip().replace('C', ''))
                humidity = float(parts[1].split(':')[1].strip().replace('%', ''))
                mq3_value = int(parts[2].split(':')[1].strip())
                ldr_value = int(parts[3].split(':')[1].strip())

                print(f"Temperature: {temperature} °C")
                print(f"Humidity: {humidity} %")
                print(f"MQ-3 Value: {mq3_value}")
                print(f"LDR Value: {ldr_value}")
                print("-" * 40)

            except (IndexError, ValueError) as e:
                print("Error parsing line:", e)

except serial.SerialException as e:
    print("Error opening serial port:", e)
except KeyboardInterrupt:
    print("Serial reading stopped by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")