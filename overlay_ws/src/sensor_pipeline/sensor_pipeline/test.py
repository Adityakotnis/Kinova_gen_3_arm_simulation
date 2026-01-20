import socket

# This matches the port in your Arduino code
UDP_IP = "0.0.0.0" 
UDP_PORT = 4242

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for ESP8266 on port {UDP_PORT}...")

while True:
    # Buffer size is 1024 bytes
    data, addr = sock.recvfrom(1024) 
    print(f"received message: {data.decode()} from {addr}")