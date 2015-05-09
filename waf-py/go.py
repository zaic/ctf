import socket
import select
import time
import sys
import threading

LOCAL_ADDR   = '0.0.0.0'
LOCAL_PORT   = 1807
SERVICE_ADDR = '127.0.0.1'
SERVICE_PORT = 2609
BUFFER_SIZE  = 100500

def process_connection(conn_client, addr):
    print('One more fucking connection from ', addr)
    
    conn_service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_service.connect((SERVICE_ADDR, SERVICE_PORT))

    history = []
    socks = [conn_client, conn_service]
    history_prefix = ['client->service: ', 'service->client: ']
    is_alive = 1

    while is_alive == 1:
        await, _, _ = select.select([conn_client, conn_service], [], [], 10)
        for sockid in range(0, 2):
            if socks[sockid] in await:
                data = socks[sockid].recv(BUFFER_SIZE)
                if not data:
                    is_alive = 0
                    break
                history.append(history_prefix[sockid] + bytes.decode(data))
                socks[1 - sockid].sendall(data)

    conn_service.close()
    conn_client.close()
    print('One more fucking connection closed')
    print(history)

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCAL_ADDR, LOCAL_PORT))
    server.listen(100500)

    while 1:
        conn, addr = server.accept()
        th = threading.Thread(target = process_connection, args = (conn, addr))
        th.start()

    conn.close()
    server.close()
