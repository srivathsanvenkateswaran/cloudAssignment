import socket
import pickle
import time
header=20
import threading

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_adr="127.0.0.1"
port=5400
bind=(ip_adr,port)
Format="utf-8"
client.connect(bind)
print(socket.gethostbyname(socket.gethostname()))

def recv_msg():
    msg_len=client.recv(header).decode(Format)
    msg=client.recv(int(msg_len)).decode(Format)
    print(msg)
    print("------>data received")
    recv_msg()

def send_msg():
    data=str(input())
    data_len=str(len(data))
    data_len=data_len.encode(Format)
    data_len+=b' '*(header-len(data_len))
    client.send(data_len)
    data=data.encode(Format)
    client.send(data)
    print(f"------>The data was send to server: {ip_adr}")
    send_msg()
print("connected")
#while True:
if __name__=="__main__":
    try:
        thread_send_data = threading.Thread(target=send_msg)
        thread_rec_data = threading.Thread(target=recv_msg)
        thread_send_data.start()
        #time.sleep(10)
        thread_rec_data.start()
    except:
        print("some error")
    #break
