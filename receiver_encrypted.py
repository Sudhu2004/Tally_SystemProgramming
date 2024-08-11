import hashlib
import os
import socket
import threading
import zlib


# Receiver Function
def receive_file(sock, output_filename):
    CHUNK_SIZE = 1024
    try:
        with open(output_filename, 'wb') as file:
            while True:
                checksum, _ = sock.recvfrom(32)  # Receive checksum
                compressed_data, _ = sock.recvfrom(CHUNK_SIZE)

                if compressed_data == b"EOF":
                    print("File transfer complete.")
                    break

                # Decompress the file chunk
                file_data = zlib.decompress(compressed_data)

                # Verify checksum
                if hashlib.md5(file_data).hexdigest() != checksum.decode():
                    print("Checksum does not match. File transfer failed.")
                    return

                file.write(file_data)

        print(f"File {output_filename} received and saved.")

    except Exception as e:
        print(f"Error receiving file: {e}")

# Main function to join a group and receive files
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Allow the socket to reuse the address
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    sock.bind(('0.0.0.0', 5005))

    # Authenticate with the server
    server_ip = input("Enter server IP: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    sock.sendto(b"REQUEST_GROUPS", (server_ip, 5005))
    groups, _ = sock.recvfrom(1024)
    print("Available groups:", groups.decode())

    sock.sendto(f"{username},{password}".encode(), (server_ip, 5005))
    auth_response, _ = sock.recvfrom(1024)

    if auth_response == b"AUTH_SUCCESS":
        print("Authentication successful. Waiting for files...")

        while True:
            data, addr = sock.recvfrom(1024)

            if data.startswith(b"EOF"):
                print("File transfer complete.")
            else:
                output_filename = input("Enter output filename: ")
                receive_file(sock, output_filename)

    else:
        print("Authentication failed. Exiting.")

if __name__ == "_main_":
    main()
