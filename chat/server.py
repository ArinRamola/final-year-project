import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = [] 
HANDSHAKE = b'CHATAPPv1\n'

def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                final_msg = username + '~' + message
                send_messages_to_all(final_msg)
            else:
                print(f"Empty message from {username}. Closing connection.")
                remove_client(client)
                break
        except Exception as e:
            print(f"Error receiving message from {username}: {e}")
            remove_client(client)
            break

def send_message_to_client(client, message):
    try:
        client.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending message: {e}")
        remove_client(client)

def send_messages_to_all(message):
    for username, client in active_clients[:]:
        send_message_to_client(client, message)

def remove_client(client):
    for entry in active_clients:
        if entry[1] == client:
            active_clients.remove(entry)
            client.close()
            send_messages_to_all(f"SERVER~{entry[0]} has left the chat.")
            break

def client_handler(client):
    try:
        header = client.recv(len(HANDSHAKE))
        if header != HANDSHAKE:
            print(f"Unknown connection, wrong header: {header}")
            client.close()
            return
        username_bytes = client.recv(2048)
        username = username_bytes.decode('utf-8').strip()
    except Exception as e:
        print(f"Failed to receive username: {e}")
        client.close()
        return

    if username:
        active_clients.append((username, client))
        print(f"{username} joined the chat.")
        send_messages_to_all(f"SERVER~{username} joined the chat.")
        threading.Thread(target=listen_for_messages, args=(client, username), daemon=True).start()
    else:
        print("Received empty username. Closing connection.")
        client.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except Exception as e:
        print(f"Unable to bind to {HOST}:{PORT} - {e}")
        return

    server.listen(LISTENER_LIMIT)
    print("Server is listening for connections...")

    while True:
        try:
            client, address = server.accept()
            print(f"Connected to client {address[0]}:{address[1]}")
            threading.Thread(target=client_handler, args=(client,), daemon=True).start()
        except KeyboardInterrupt:
            print("\nServer shutting down.")
            break
        except Exception as e:
            print(f"Error accepting connections: {e}")

    server.close()

if __name__ == '__main__':
    main()
