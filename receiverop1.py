import socket
import threading

# Function to send authentication request
def send_auth_request(sock, server_address, login_id, password):
    while True:
        credentials = f"AUTH,{login_id},{password}".encode()
        sock.sendto(credentials, server_address)
        sock.settimeout(5)  # Set a timeout for the authentication response
        try:
            response, _ = sock.recvfrom(1024)
            if response == b"AUTH_SUCCESS":
                print("Authentication successful!")
                return True
            else:
                print("Authentication failed! Retrying...")
        except socket.timeout:
            print("Authentication request timed out. Retrying...")

# Function to receive a file from the server
def receive_file(output_filename, group_ip, port):
    CHUNK_SIZE = 1024

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.bind(('', port))
    
    # Join the multicast group
    mreq = socket.inet_aton(group_ip) + socket.inet_aton('0.0.0.0')
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    with open(output_filename, 'wb') as file:
        while True:
            chunk, _ = sock.recvfrom(CHUNK_SIZE)
            if chunk == b"EOF":
                break
            file.write(chunk)

    sock.close()# Function to request and list available groups from the server
def request_and_list_groups(sock, server_address):
    sock.sendto(b"REQUEST_GROUPS", server_address)
    try:
        response, _ = sock.recvfrom(1024)
        groups = response.decode().split(',')
        print(f"Available groups: {groups}")
    except Exception as e:
        print(f"Error listing groups: {e}")

# Function to request to join a group
def request_to_join_group(sock, server_address, group_ip, login_id):
    request = f"JOIN_GROUP,{group_ip},{login_id}".encode()
    sock.sendto(request, server_address)
    print(f"Join request sent for group {group_ip}.")

# Function to view the groups the receiver is currently part of
def view_my_groups(sock, server_address, login_id):
    request = f"MY_GROUPS,{login_id}".encode()
    sock.sendto(request, server_address)
    try:
        response, _ = sock.recvfrom(1024)
        my_groups = response.decode().split(',')
        print(f"Groups you are a part of: {my_groups}")
    except Exception as e:
        print(f"Error listing your groups: {e}")

# Function to handle file reception requests
def handle_file_requests(sock):
    while True:
        try:
            data, sender_address = sock.recvfrom(1024)
            if data.decode().startswith("RTS"):
                filename = data.decode().split(",")[1]
                print(f"Received request to send file {filename}.")
                # Send Clear to Send (CTS)
                sock.sendto(b"CTS", sender_address)
                # Start receiving file in a separate thread
                threading.Thread(target=receive_file, args=(filename, sender_address[0], 5006), daemon=True).start()
        except Exception as e:
            print(f"Error handling file request: {e}")

# Main function to interact with the receiver
def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('127.0.0.1', 5005)  # Address of the sender server

        # Authentication
        login_id = input("Enter your login ID: ")
        password = input("Enter your password: ")
        if not send_auth_request(sock, server_address, login_id, password):
            return

       
        # Start a thread to handle file reception requests
        # threading.Thread(target=handle_file_requests, args=(file_receive_sock,), daemon=True).start()

        while True:
            print("\nReceiver Menu:")
            print("1. Request and List Available Groups")
            print("2. Join Group")
            print("3. View My Groups")
            print("4. Receive File")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                request_and_list_groups(sock, server_address)
            elif choice == "2":
                group_ip = input("Enter the group IP to join: ")
                request_to_join_group(sock, server_address, group_ip, login_id)
            elif choice == "3":
                view_my_groups(sock, server_address, login_id)
            elif choice == "4":
                group_ip = input("Enter the group IP: ")
                filename = input("Enter the output filename: ")
                threading.Thread(target=receive_file, args=(filename, group_ip, 5004), daemon=True).start()
            elif choice == "5":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
