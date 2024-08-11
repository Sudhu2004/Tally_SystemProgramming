import hashlib
import os
import socket
import threading
import time
import zlib
from queue import Queue


# Group Management System
class GroupManager:
    def __init__(self):
        self.groups = {}
        self.credentials = {"admin": "adminpass"}  # Example credentials
        self.offline_clients = {}

    def create_group(self, group_ip):
        if group_ip not in self.groups:
            self.groups[group_ip] = []
            print(f"Group {group_ip} created.")
        else:
            print(f"Group {group_ip} already exists.")

    def delete_group(self, group_ip):
        if group_ip in self.groups:
            del self.groups[group_ip]
            print(f"Group {group_ip} deleted.")
        else:
            print(f"Group {group_ip} does not exist.")

    def add_client_to_group(self, group_ip, client_ip):
        if group_ip in self.groups:
            if client_ip not in self.groups[group_ip]:
                self.groups[group_ip].append(client_ip)
                print(f"Client {client_ip} added to group {group_ip}.")
            else:
                print(f"Client {client_ip} is already in group {group_ip}.")
        else:
            print(f"Group {group_ip} does not exist.")

    def remove_client_from_group(self, group_ip, client_ip):
        if group_ip in self.groups:
            if client_ip in self.groups[group_ip]:
                self.groups[group_ip].remove(client_ip)
                print(f"Client {client_ip} removed from group {group_ip}.")
            else:
                print(f"Client {client_ip} is not in group {group_ip}.")
        else:
            print(f"Group {group_ip} does not exist.")

    def list_groups(self):
        return ','.join(self.groups.keys())

    def authenticate(self, username, password):
        return self.credentials.get(username) == password

    def queue_file_for_offline_client(self, client_ip, filename):
        if client_ip not in self.offline_clients:
            self.offline_clients[client_ip] = []
        self.offline_clients[client_ip].append(filename)
        print(f"Queued {filename} for offline client {client_ip}.")

    def get_offline_files(self, client_ip):
        return self.offline_clients.get(client_ip, [])

# Sender Function
def send_file(sock, filename, group, port):
    CHUNK_SIZE = 1024
    try:
        with open(filename, 'rb') as file:
            while True:
                chunk = file.read(CHUNK_SIZE)
                if not chunk:
                    break
                compressed_data = zlib.compress(chunk)
                checksum = hashlib.md5(compressed_data).hexdigest()

                # Send the checksum first
                sock.sendto(checksum.encode(), (group, port))

                # Send the file chunk
                sock.sendto(compressed_data, (group, port))

        # Signal end of file transfer
        sock.sendto(b"EOF", (group, port))

        print(f"Sent file {filename} to group {group}:{port}")

    except Exception as e:
        print(f"Error sending file: {e}")

# Function to handle each receiver's request
def handle_receiver_request(sock, manager):
    try:
        while True:
            data, addr = sock.recvfrom(1024)

            if data == b"REQUEST_GROUPS":
                groups = manager.list_groups()
                sock.sendto(groups.encode(), addr)

                login_info, _ = sock.recvfrom(1024)
                username, password = login_info.decode().split(',')
                if manager.authenticate(username, password):
                    sock.sendto(b"AUTH_SUCCESS", addr)
                else:
                    sock.sendto(b"AUTH_FAIL", addr)

            elif data == b"PING":
                sock.sendto(b"PONG", addr)

            elif data.startswith(b"OFFLINE"):
                client_ip = addr[0]
                filename = data.decode().split()[1]
                manager.queue_file_for_offline_client(client_ip, filename)

    except Exception as e:
        print(f"Error handling request: {e}")

# Function to send queued files when client comes online
def send_queued_files(manager, sock, port):
    while True:
        time.sleep(5)
        for client_ip, files in manager.offline_clients.items():
            sock.sendto(b"PING", (client_ip, port))
            response, _ = sock.recvfrom(1024)
            if response == b"PONG":
                for filename in files:
                    send_file(sock, filename, client_ip, port)
                manager.offline_clients[client_ip] = []

# Main function to interact with the Group Manager
def main():
    manager = GroupManager()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 5005))

    threading.Thread(target=handle_receiver_request, args=(sock, manager)).start()
    threading.Thread(target=send_queued_files, args=(manager, sock, 5005)).start()

    while True:
        print("\nGroup Management System")
        print("1. Create Group")
        print("2. Delete Group")
        print("3. Add Client to Group")
        print("4. Remove Client from Group")
        print("5. List Groups")
        print("6. Send File to Group")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            group_ip = input("Enter group IP: ")
            manager.create_group(group_ip)
        elif choice == "2":
            group_ip = input("Enter group IP: ")
            manager.delete_group(group_ip)
        elif choice == "3":
            group_ip = input("Enter group IP: ")
            client_ip = input("Enter client IP: ")
            manager.add_client_to_group(group_ip, client_ip)
        elif choice == "4":
            group_ip = input("Enter group IP: ")
            client_ip = input("Enter client IP: ")
            manager.remove_client_from_group(group_ip, client_ip)
        elif choice == "5":
            print(manager.list_groups())
        elif choice == "6":
            group_ip = input("Enter group IP: ")
            port = int(input("Enter port: "))
            filenames = input("Enter filenames (comma-separated): ").split(',')

            for filename in filenames:
                # Ping receivers to check if they are active
                active = False
                for client in manager.groups.get(group_ip, []):
                    sock.sendto(b"PING", (client, port))
                    response, _ = sock.recvfrom(1024)
                    if response == b"PONG":
                        active = True
                        send_file(sock, filename.strip(), client, port)

                if not active:
                    print("No active receivers found. Queuing the file.")
                    for client in manager.groups.get(group_ip, []):
                        manager.queue_file_for_offline_client(client, filename.strip())

        elif choice == "7":
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "_main_":
    main()
