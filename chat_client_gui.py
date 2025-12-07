# GUI Chat Client using Tkinter and socket programming
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import ex_l2_protocol  # Using the existing protocol

class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        self.root.geometry("450x500")  # Window size
        self.root.configure(bg="#ECF0F1")

        # Header
        self.header_label = tk.Label(root, text="Chat Client", font=("Calibri", 16, "bold"), fg="#2C3E50", bg="#ECF0F1")
        self.header_label.pack(pady=10)

        # Message display area (scroll box)
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=18,
                                                   bg="white", fg="black", font=("Verdana", 12), relief=tk.GROOVE, bd=2)
        self.text_area.pack(padx=10, pady=5)
        self.text_area.config(state=tk.DISABLED)

        # Setting style for server messages
        self.text_area.tag_configure("server_msg", foreground="#2980B9", font=("Comic Sans MS", 13, "bold"))

        # Frame for input field and send button
        self.input_frame = tk.Frame(root, bg="#ECF0F1")
        self.input_frame.pack(pady=10, fill=tk.X, padx=10)

        # Input field for messages
        self.entry_field = tk.Entry(self.input_frame, width=35, font=("Arial", 12), bg="white", fg="black",
                                    relief=tk.GROOVE, bd=2)
        self.entry_field.grid(row=0, column=0, padx=5, pady=5, ipady=5)
        self.entry_field.bind("<Return>", lambda event: self.send_message())  # Support Enter key for sending

        # Button to send message
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message,
                                     font=("Arial", 12, "bold"),
                                     bg="#3498DB", fg="white", activebackground="#2980B9",
                                     relief=tk.GROOVE, bd=2, padx=10, pady=5)
        self.send_button.grid(row=0, column=1, padx=5)

        # Connect to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 8888)) # loopback address
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        message = self.entry_field.get().strip()
        if message:
            ready_msg = ex_l2_protocol.create_msg(message)  # Prepare message in protocol
            self.client_socket.send(ready_msg.encode())  # Send to server
            self.entry_field.delete(0, tk.END)  # Clear input field
            if message.upper() == "EXIT":  # End connection
                self.client_socket.close()  # Close connection
                self.root.destroy()  # Close window

    def receive_messages(self):
        while True:
            try:
                message = ex_l2_protocol.receive_msg(self.client_socket)
                if message:
                    self.text_area.config(state=tk.NORMAL)
                    self.text_area.insert(tk.END, "Server send : " + message + "\n", "server_msg")
                    self.text_area.config(state=tk.DISABLED)
                    self.text_area.yview(tk.END)  # Auto-scroll to last message
            except:
                break

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClientGUI(root)
    root.mainloop()