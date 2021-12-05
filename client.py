import socket
endpoint="127.0.0.1"
port =8000
def main():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((endpoint,port))
    while True:
        print(s.recv(1024).decode(), end = " : ")
        user = input()
        s.send(user.encode())
        print(s.recv(1024).decode(), end = " ")
        password = input(">")
        s.send(password.encode())
        msg = s.recv(1024)
        # print(msg.decode())
        while msg.decode()!='over':
            print(msg.decode())
            s.sendall("ok".encode())
            msg = s.recv(1024)
        choice = input('enter your choice : ')
        s.send(choice.encode())
        msg = s.recv(1024)
        if(msg.decode() == 'invalid selection'):
            while msg:
                print(msg.decode(),end='')
                msg = s.recv(1024)
            break
        



if __name__=="__main__":
    main()