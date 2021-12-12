import socket
import pickle
import time
import threading
header =20


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_adr="127.0.0.1"
print(ip_adr)
port=5400
bind=('',port)
Format='utf-8'

server.bind(bind)
server.listen(3)
#server.setblocking(1)
def send_msg(conn_obj,client_address):
    data=str(input())
    data_len=str(len(data))
    data_len=data_len.encode(Format)
    data_len+=b' '*(header-len(data_len))
    conn_obj.send(data_len)
    data=data.encode(Format)
    conn_obj.send(data)
    print(f"----->The data was send to {client_address}")
    send_msg(conn_obj,client_address)

def recv_msg(conn_obj,addr):
    msg_len = conn_obj.recv(header).decode(Format)
    msg = conn_obj.recv(int(msg_len)).decode(Format)
    print(msg)
    print(f"------>data is received to {addr}")
    recv_msg(conn_obj,addr)
if __name__=="__main__":
    while True:
        print("waiting for connection...!")
        conn_obj,client_address=server.accept()
        thread_send_data = threading.Thread(target=send_msg,args=(conn_obj,client_address))
        thread_rec_data = threading.Thread(target=recv_msg,args=(conn_obj,client_address))
        thread_send_data.start()
        thread_rec_data.start()
        print(f"object:{conn_obj}address:{client_address}connected")
