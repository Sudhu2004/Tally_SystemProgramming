# Group Management System with Authentication - README

## Overview

The Group Management System with Authentication is a client-server application that allows for secure group-based file sharing over a network. The system is designed with a server (Sender) that manages groups, handles authentication, and sends files, and clients (Receivers) that can join groups, receive files, and interact with the server to manage their memberships.

## Features

- **Authentication**: Ensures that only authorized users can access and interact with the system.
- **Group Management**: Create, delete, and manage groups to organize users and files.
- **File Transmission**: Securely send files to active group members over a network using UDP multicast.
- **Pending File Handling**: Files can be added to a pending list and sent when group members are active.
- **Join Requests**: Clients can request to join a group, and the server can approve or deny these requests.
- **Client Management**: Track which clients are in which groups and manage their memberships.
- **Receiver Activity Check**: Verify if a receiver is active before sending files.

## Prerequisites

- Python 3.x
- Basic understanding of networking, UDP, and sockets.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/group-management-system.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd group-management-system
   ```
3. **Install required Python packages** (if any):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Start the Sender (Server)
The sender is responsible for managing groups, handling client authentication, and sending files to group members.

- Run the `main()` function in the sender script:
  ```bash
  python sender.py
  ```

#### Sender Menu Options:
- **Create Group**: Create a new group with a specific IP.
- **Delete Group**: Delete an existing group.
- **Add Client to Group**: Manually add a client to a group.
- **Remove Client from Group**: Remove a client from a group.
- **List Groups**: Display all available groups.
- **Add File to Pending List**: Add a file to a group’s pending list, which will be sent when the group members are active.
- **Send Pending Files**: Send all pending files to the active members of a group.
- **View Pending Files Status**: Display the status of pending files for each group.
- **View Join Requests**: View pending join requests from clients.
- **Approve Join Request**: Approve a client's request to join a group.
- **View Client Groups**: Display the groups a specific client is a part of.
- **Check Active Receivers**: Check if a receiver is active on the network.
- **View Group Members**: Display the current members of a group.
- **Exit**: Exit the application.

### 2. Start the Receiver (Client)
The receiver interacts with the sender, allowing the user to authenticate, join groups, and receive files.

- Run the `main()` function in the receiver script:
  ```bash
  python receiver.py
  ```

#### Receiver Menu Options:
- **Request and List Available Groups**: Request and display the list of available groups from the server.
- **Join Group**: Send a request to join a specific group.
- **View My Groups**: Display the groups the receiver is currently a part of.
- **Receive File**: Actively receive files sent to the group by the sender.
- **Exit**: Exit the application.

### 3. Authentication
When a receiver tries to interact with the server, they are prompted to authenticate using their `login ID` and `password`. The credentials are validated against those stored on the server.

### 4. File Transmission
Files are sent over the network using UDP multicast. The server sends files to all active members of a group, and clients can receive these files, which are written to the local filesystem.

## Example Workflow

1. **Sender** creates a group with IP `224.0.0.1`.
2. **Receiver** authenticates and requests to join the group.
3. **Sender** approves the join request.
4. **Sender** adds a file to the group's pending list.
5. **Sender** sends the pending file to the active members of the group.
6. **Receiver** receives the file and saves it locally.

## Notes

- **Multithreading**: The system uses threading to handle multiple clients simultaneously and to manage file transmission without blocking the main process.
- **Error Handling**: Basic error handling is implemented to manage network issues and authentication failures.

## Future Enhancements

- **Encryption**: Implement encryption for file transmission to enhance security.
- **Web Interface**: Develop a web-based interface for easier management of groups and clients.
- **Database Integration**: Store user credentials and group information in a database for persistence.

## Troubleshooting

- Ensure that the correct IP and port are used for communication between the sender and receivers.
- Verify network connectivity between the sender and receivers.
- Check for any firewall or network restrictions that may block UDP traffic.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any issues or contributions, please contact [your-email@example.com].
