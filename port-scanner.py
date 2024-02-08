import socket

def scan_port(ip, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        sock.settimeout(1)
        # Attempt to connect to the specified IP and port
        sock.connect((ip, port))
        # If successful, mark the port as open
        print(f"Port {port} is open on {ip}")
        # Log the IP in a text file
        with open("open_ports.txt", "a") as file:
            file.write(f"{ip}:{port}\n")
        # Close the socket
        sock.close()
    except socket.error:
        # If connection attempt fails, mark the port as closed
        print(f"Port {port} is closed on {ip}")
        

def scan_ip_range(start_ip, end_ip, port):
    # Convert start and end IPs to integers
    start_ip_int = int(''.join(f"{int(octet):03}" for octet in start_ip.split('.')))
    end_ip_int = int(''.join(f"{int(octet):03}" for octet in end_ip.split('.')))

    # Loop through the IP range and scan each IP for the specified port
    for ip_int in range(start_ip_int, end_ip_int + 1):
        ip = '.'.join(str((ip_int >> (8 * i)) & 0xFF) for i in range(3, -1, -1))
        scan_port(ip, port)

if __name__ == "__main__":
    # Get user input for IP range and port
    start_ip = input("Enter starting IP: ")
    end_ip = input("Enter ending IP: ")
    port = int(input("Enter port to scan: "))

    # Call the function to scan the IP range for the specified port
    scan_ip_range(start_ip, end_ip, port)
