# Yinon Shaul 211693114
import socket
import select
import ex_l2_protocol
from scapy.all import *

SERVER_PORT = 8888  # Unified port selection
SERVER_IP = "0.0.0.0"

messages_to_send = []
block_or_blocked_clients = {}

def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())

def find_client_by_socket(current_socket, clients_sockets_connection):
    for name, socket in clients_sockets_connection.items():
        if socket == current_socket:
            return name
    return None

def handle_client_request(current_socket, clients_names, data):
    command = data.split(" ")
    # Search if the command is in the available commands
    if command[0] in command_map:
        return command_map[command[0]](command, current_socket, clients_names)
    else:
        # If the command is not in the available commands
        return ex_l2_protocol.create_msg("Command not found please use in the "
                                                           "format GET_NAMES"), current_socket

def create_name_client(data, current_socket,clients_sockets_connection):
    # The format of the data is NAME Name so if the length of the data is > 2 don't accept it ,
    # and send message to the client , we already check if the first part is just NAME
    if len(data) > 2:
        return ex_l2_protocol.create_msg("The command syntax is wrong , please use in the "
                                                              "format NAME Name"), current_socket

    # Check if the name is already in clients
    if data[1] in clients_sockets_connection:
        return ex_l2_protocol.create_msg("Name already taken"), current_socket

    # If the name is BROADCAST is not allowed
    if data[1] == "BROADCAST":
        return ex_l2_protocol.create_msg("Name BROADCAST is not allowed"), current_socket

    else:
        # Add the name to the clients
        clients_sockets_connection[data[1]] = current_socket

        # Add the name to the optional block / blocked clients if it is not already there
        if data[1] not in block_or_blocked_clients.keys():
            # Add the name with an empty list to optional blocked clients
            block_or_blocked_clients[data[1]] = []

        return ex_l2_protocol.create_msg("Hello " + data[1]), current_socket

def get_names(data, current_socket,clients_sockets_connection):
    # The format of the data is GET_NAMES so if the length of the data is > 1 don't accept it ,
    # and send message to the client , we already check if the first part is just GET_NAMES
    if len(data) > 1:
        return ex_l2_protocol.create_msg("The command syntax is wrong , please use in the "
                                                              "format GET_NAMES"), current_socket

    names = "The clients are: "
    for client in clients_sockets_connection.keys():
        names += client + " "

    return ex_l2_protocol.create_msg(names), current_socket

def send_msg(data, current_socket,clients_sockets_connection):
    # The format of the data is MSG Name Message so if the length of the data is > 3 don't accept it ,
    # and send message to the client , we already check if the first part is just MSG , and in line 101 we check

    # if the len != 3 send to the client the message not in the right format
    if len(data) != 3:
        return ex_l2_protocol.create_msg("The command syntax is wrong , please use in the "
                                                              "format MSG Name Message"), current_socket

    # Found the name of the sender by socket number
    sender_name = find_client_by_socket(current_socket,clients_sockets_connection)

    # ----------------- My assumption is client can't send message to himself -----------------#
    # If sender = destination
    if sender_name == data[1]:
        return ex_l2_protocol.create_msg("You can't send message to yourself"), current_socket

    # If the destination is not in the clients
    if data[1] != "BROADCAST" and data[1] not in clients_sockets_connection:
        return ex_l2_protocol.create_msg(f"Client {data[1]} not found"), current_socket

    # In broadcast every client will get the message except the sender and the blocked clients
    if data[1] == "BROADCAST":
        for client in clients_sockets_connection.keys():
            # Check if the client is not the sender and the sender is not blocked by client
            if client != sender_name and sender_name not in block_or_blocked_clients[client]:
                message_after_protocol = ex_l2_protocol.create_msg(f"{sender_name} send {data[2]}")
                messages_to_send.append((clients_sockets_connection[client], message_after_protocol))
        return ex_l2_protocol.create_msg(f"I send the message to everyone"), current_socket

    # If the destination is in the clients but the sender is blocked
    if sender_name in block_or_blocked_clients[data[1]]:
        return ex_l2_protocol.create_msg(f"Thank you"), current_socket

    # If the destination is not blocked
    return ex_l2_protocol.create_msg(f"{sender_name} send {data[2]}"), clients_sockets_connection[data[1]]

def block_client(data, current_socket,clients_sockets_connection):
    # The format of the data is BLOCK Name so if the length of the data is > 2 don't accept it ,
    # and send message to the client , we already check if the first part is just BLOCK
    if len(data) > 2:
        return ex_l2_protocol.create_msg("The command syntax is wrong , please use in the "
                                                                "format BLOCK Name"), current_socket

    # Check if the name is already in clients
    if data[1] in clients_sockets_connection:
        # Add the name to the blocked list
        sender_name = find_client_by_socket(current_socket,clients_sockets_connection)
        block_or_blocked_clients[sender_name].append(data[1])
        return ex_l2_protocol.create_msg(f"Client {data[1]} blocked"), current_socket

    # If the client is not in the clients
    return ex_l2_protocol.create_msg(f"Client {data[1]} not found"), current_socket

def exit_client(current_socket,clients_sockets_connection):
    # Remove the client from the clients_sockets_connection dictionary
    client_to_remove = None
    for name, socket in clients_sockets_connection.items():
        if socket == current_socket:
            client_to_remove = name
            break
    # If the client is in the clients
    if client_to_remove:
        clients_sockets_connection.pop(client_to_remove)

# --- Optional use nslookup --- #
def nsl_client(data, current_socket,clients_sockets_connection):
    # The format of the data is NSLOOKUP CLIENT N_dest A/PTR _ so if the length of the data is > 4 don't accept it ,
    # and send message to the client , we already check if the first part is just NSLOOKUP
    if len(data) > 4:
        return ex_l2_protocol.create_msg("The command syntax is wrong , please use in the "
                                                              "format NSLOOKUP Name A/PTR"), current_socket

    # If the client is not in the clients
    if data[1] not in clients_sockets_connection:
        return ex_l2_protocol.create_msg(f"Client {data[1]} not found"), current_socket

    # Get the url or the ip
    query_value = data[2]
    # Get the query type
    query_type = data[3]

    # In case of Reverse Mapping, we need to convert the IP to PTR format
    # Reverse the IP address order
    if query_type == "PTR":
        ip_parts = query_value.split('.')
        # Append the suffix
        reversed_ip = '.'.join(ip_parts[::-1]) + ".in-addr.arpa"
        query_value = reversed_ip

    # Create the DNS request packet
    dns_packet = IP(dst="8.8.8.8") / UDP(sport=24601, dport=53) / DNS(rd=1,
                                                                      qd=DNSQR(qname=query_value, qtype=query_type))

    # Send the request and wait for a response
    reply = sr1(dns_packet, timeout=4)

    # Process the response
    res = ""
    if reply and DNS in reply:
        for ans in range(reply[DNS].ancount):
            if reply[DNS].an[ans].type == 1 and query_type == "A":
                res += reply[DNS].an[ans].rdata + " "
            elif reply[DNS].an[ans].type == 12 and query_type == "PTR":
                res += reply[DNS].an[ans].rdata.decode() + " "

    else:
        res = "No response or no valid answers received."

    return ex_l2_protocol.create_msg(res), current_socket



command_map = {
    "NAME": create_name_client,
    "GET_NAMES": get_names,
    "MSG": send_msg,
    "BLOCK": block_client,
    "NSLOOKUP": nsl_client
}

def main():
    print("Setting up server")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    print("Listening for clients")
    server_socket.listen()
    client_sockets = []
    clients_sockets_connection = {}

    while True:
        # The read_list is a list of all the sockets that we want to listen to
        read_list = client_sockets + [server_socket]
        ready_to_read, ready_to_write, in_error = select.select(read_list, client_sockets, [])
        # If the server is ready to read
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                connection, client_address = server_socket.accept()
                print("New client joined!", client_address)
                # Add the client to the clients_sockets exsiting list
                client_sockets.append(connection)
                print_client_sockets(client_sockets)
            else:
                print("Data from client\n")
                data = ex_l2_protocol.receive_msg(current_socket)
                # If the message is empty, this indicates a connection closure
                if data == "":
                    print("Connection closed")
                    # Function to remove the client from the clients_sockets_connection dictionary
                    exit_client(current_socket,clients_sockets_connection)
                    client_sockets.remove(current_socket)
                    current_socket.close()
                else:
                    print(data)
                    # Get the response and the destination socket
                    (response, dest_socket) = handle_client_request(current_socket, clients_sockets_connection, data)
                    messages_to_send.append((dest_socket, response))

        for message in messages_to_send:
            current_socket, data = message
            # If the current socket is can to write the data
            if current_socket in ready_to_write:
                current_socket.send(data.encode())
                messages_to_send.remove(message)

if __name__ == '__main__':
    main()
