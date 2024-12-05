import serial
import time

# Specify the correct serial port and baud rate
arduino = serial.Serial(port='COM15', baudrate=9600, timeout=1)  # Replace 'COM3' with your Arduino's port
time.sleep(2)  # Wait for Arduino to initialize

print("Type a message to send to Arduino. Type 'exit' to quit.")
while True:
    # Read input from the user
    user_input = input("Enter message: ")
    if user_input.lower() == "exit":
        print("Exiting...")
        break
    
    # Send the message to the Arduino
    arduino.write((user_input + '\n').encode())  # Encode to bytes and send
    
    # Read response from Arduino (if any)
    data1 = arduino.readline().decode().strip()  # Read response
    if data1:
        print("Arduino replied:", data1)

    data2=arduino.readline().decode().strip()
    data3=arduino.readline().decode().strip()
    data4=arduino.readline().decode().strip()
    data5=arduino.readline().decode().strip()

    print("data2", data2)
    print("data3", data3)
    print("data4", data4)
    print("data5", data5)


    f = open("data.txt", "w")
    f.write(data2+"\n"+data3+"\n"+data4+"\n"+data5)
    f.close()

    



# Close the serial connection
arduino.close()
