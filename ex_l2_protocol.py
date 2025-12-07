# Yinon Shaul 211693114
LENGTH_FILE_SIZE = 2

def create_msg(data):
    # Create a massage with the length of the data
    length = str(len(data))
    length_filled_value = length.zfill(LENGTH_FILE_SIZE)
    # Return the length of the data and the data
    return length_filled_value + data


def receive_msg(sock):
    try:
        # Extract the length of the data from the message
        length = sock.recv(LENGTH_FILE_SIZE).decode()

        # If the message is empty, this indicates a connection closure
        if not length:
            return ""

        # Decode and convert the length to an integer
        length = int(length)
        # Receive the data and decode it
        msg = sock.recv(length).decode()
        return msg
    # If the client close the connection in unexpected way
    except ConnectionResetError:
        # Tell to the server that the client is disconnected
        return ""

