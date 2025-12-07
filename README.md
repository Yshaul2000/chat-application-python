# Chat Application Python

A feature-rich, multi-client chat application built with Python, featuring a custom messaging protocol, intuitive GUI client, and robust server architecture with advanced features like DNS lookups and client blocking.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Server](#running-the-server)
  - [Running the GUI Client](#running-the-gui-client)
- [Custom Protocol](#custom-protocol)
- [Available Commands](#available-commands)
- [Technical Details](#technical-details)
- [Requirements](#requirements)
- [License](#license)

## 🎯 Overview

This is a Python-based chat application that enables multiple clients to communicate simultaneously through a central server. The application implements a custom messaging protocol for reliable message transmission and features a user-friendly GUI built with Tkinter.

The project demonstrates socket programming, multi-client handling with select(), custom protocol design, and GUI development in Python.

## ✨ Features

### Server Features
- **Multi-client Support**: Handle multiple simultaneous client connections using the `select` module
- **Custom Protocol**: Implements a custom length-prefixed message protocol for reliable data transmission
- **User Management**: Unique username assignment and validation
- **Private Messaging**: Send direct messages to specific users
- **Broadcast Messages**: Send messages to all connected clients at once
- **Client Blocking**: Users can block other users from sending them messages
- **DNS Lookups**: Integrated NSLOOKUP functionality for A and PTR record queries using Scapy
- **Connection Management**: Graceful handling of client connections and disconnections

### Client Features
- **Graphical User Interface**: Clean and modern GUI built with Tkinter
- **Real-time Messaging**: Instant message display with automatic scrolling
- **Message Styling**: Formatted display for server messages
- **Enter Key Support**: Send messages using the Enter key
- **Easy Navigation**: Simple and intuitive interface

## 🏗️ Architecture

The application consists of three main components:

1. **Server (`chat_server_skeleton.py`)**: 
   - Manages client connections using socket programming
   - Implements command routing and message handling
   - Maintains client state and blocked users list
   - Uses select() for non-blocking I/O multiplexing

2. **Client GUI (`chat_client_gui.py`)**: 
   - Provides a graphical interface for users
   - Handles message sending and receiving in separate threads
   - Connects to the server on localhost (127.0.0.1) port 8888

3. **Protocol Module (`ex_l2_protocol.py`)**: 
   - Implements the custom messaging protocol
   - Handles message encoding/decoding
   - Ensures reliable message transmission with length prefixing

## 📦 Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Install Dependencies

```bash
# Install Scapy for DNS functionality
pip install scapy

# For GUI support, ensure tkinter is installed (usually comes with Python)
# On Ubuntu/Debian:
sudo apt-get install python3-tk

# On Fedora/RHEL:
sudo dnf install python3-tkinter
```

### Clone the Repository

```bash
git clone https://github.com/Yshaul2000/chat-application-python.git
cd chat-application-python
```

## 🚀 Usage

### Running the Server

Start the chat server before connecting any clients:

```bash
python chat_server_skeleton.py
```

The server will start listening on:
- **IP**: 0.0.0.0 (all interfaces)
- **Port**: 8888

You should see output indicating the server is ready:
```
Setting up server
Listening for clients
```

### Running the GUI Client

In a separate terminal, launch the GUI client:

```bash
python chat_client_gui.py
```

A GUI window will open. The client automatically connects to the server at `127.0.0.1:8888`.

### First-Time Setup

1. **Set Your Username**: First command should be `NAME YourUsername`
2. **Get Connected Users**: Use `GET_NAMES` to see who's online
3. **Start Chatting**: Send messages using the available commands

## 📡 Custom Protocol

The application uses a custom length-prefixed protocol for message transmission:

### Protocol Format
```
[2-byte length][message data]
```

- **Length Field**: 2 digits (zero-padded) indicating message length
- **Message Data**: The actual message content

### Example
```
Message: "Hello"
Encoded: "05Hello"
         └─ Length (5 characters)
```

This protocol ensures:
- Reliable message boundaries
- No message truncation
- Efficient parsing

## 🎮 Available Commands

### NAME
Set your username when first connecting.
```
NAME YourUsername
```
- Username must be unique
- "BROADCAST" is reserved and cannot be used

### GET_NAMES
Retrieve a list of all connected clients.
```
GET_NAMES
```

### MSG
Send a private message to a specific user.
```
MSG Username YourMessage
```
- Cannot send messages to yourself
- User must be online
- Blocked users won't receive your messages

### MSG BROADCAST
Send a message to all connected clients.
```
MSG BROADCAST YourMessage
```
- All users receive the message except:
  - The sender
  - Users who have blocked the sender

### BLOCK
Block a user from sending you messages.
```
BLOCK Username
```
- User must exist in the system
- Blocked users can still send messages, but you won't receive them

### NSLOOKUP
Perform DNS lookups (A or PTR records).
```
NSLOOKUP ClientName domain.com A
NSLOOKUP ClientName 8.8.8.8 PTR
```
- **A Record**: Get IP address for a domain
- **PTR Record**: Get domain name for an IP (reverse DNS)
- Uses Google's DNS server (8.8.8.8)

### EXIT
Disconnect from the server.
```
EXIT
```

## 🔧 Technical Details

### Server Implementation
- **Socket Type**: TCP (SOCK_STREAM)
- **I/O Multiplexing**: select() module for handling multiple clients
- **Port**: 8888
- **Concurrency Model**: Event-driven single-threaded server

### Client Implementation
- **GUI Framework**: Tkinter
- **Threading**: Separate thread for receiving messages
- **Connection**: TCP socket to localhost:8888

### Security Considerations
- Basic blocking mechanism for user privacy
- No authentication system (intended for local network use)
- Messages are transmitted in plain text

### Data Structures
```python
# Client socket mapping
clients_sockets_connection = {
    "Username1": socket_object,
    "Username2": socket_object,
    ...
}

# Block list
block_or_blocked_clients = {
    "Username1": ["BlockedUser1", "BlockedUser2"],
    "Username2": [],
    ...
}
```

## 📋 Requirements

- **Python**: 3.6+
- **Scapy**: For DNS lookup functionality
- **Tkinter**: For GUI (usually included with Python)
- **Standard Library Modules**:
  - socket
  - select
  - threading

## 👨‍💻 Author

Yinon Shaul

## 🤝 Feedback

Feedback, suggestions, and improvement ideas are always welcome!

## 📝 Notes

- The server must be running before clients can connect
- All clients connect to localhost by default (modify `chat_client_gui.py` for remote connections)
- DNS lookup feature requires appropriate network permissions
- This is an educational project demonstrating network programming concepts

---

**Enjoy chatting! 💬**
