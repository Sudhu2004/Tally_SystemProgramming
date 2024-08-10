import socket

def receive_file(output_filename, group, port):
    # Define the chunk size
    CHUNK_SIZE = 1024

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.bind(('', port))
    
    # Join the multicast group
    mreq = socket.inet_aton(group) + socket.inet_aton('0.0.0.0')
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    with open(output_filename, 'wb') as file:
        while True:
            chunk, _ = sock.recvfrom(CHUNK_SIZE)
            if chunk == b"EOF":
                break
            file.write(chunk)

    sock.close()

# Usage
receive_file('received_example_2.pdf', '224.1.1.2', 5004)
