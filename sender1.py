import socket

def send_file(filename, group, port):
    # Define the chunk size (in bytes)
    CHUNK_SIZE = 1024

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    with open(filename, 'rb') as file:
        while chunk := file.read(CHUNK_SIZE):
            sock.sendto(chunk, (group, port))
        # Send EOF to indicate the end of the file
        sock.sendto(b"EOF", (group, port))

    sock.close()

# Usage
send_file('resume.docx', '224.1.1.1', 5004)     
send_file('resume.pdf', '224.1.1.2', 5004)     
