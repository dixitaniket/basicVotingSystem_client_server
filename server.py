import socket 
from _thread import *
import threading 
from threading import Lock
user_data={}
casted_votes={}
candidates={}
reverse_candidates={}
endpoint="127.0.0.1"
port =8000
lock=Lock()


with open("userlist.txt","r") as f:
    for i in f.readlines():
        username,password=i.strip().split(" ")
        user_data[username]=password
# print(data)
with open("poll.txt","r") as f:
    for i in f.readlines():
        candidate,symbol=i.strip().split(" ")
        candidates[candidate]=symbol
        reverse_candidates[symbol]=candidates
print(user_data)
total_votes={}
for i in reverse_candidates.keys():
    total_votes[i]=0
print(candidates)
# with open("total_votes")
buffer=1024
def new_thread_vote(c):
    while True:
        print(total_votes)
        print(casted_votes)
        c.send("enter username".encode("utf-8"))
        username=c.recv(buffer).decode().strip()
        c.send("enter password".encode("utf-8"))
        password=c.recv(buffer).decode().strip()
        if not username or not password:
            c.send('username or password is invalid'.encode("utf-8"))
            print("exiting thread")
            break
        if username in casted_votes.keys():
            c.send("you have already casted votes".encode("utf-8"))
            c.send("exit".encode("utf-8"))
            break
        if username not in user_data.keys():
            c.send("you are not authorised to cast vote".encode("utf-8"))
            break
        if username in user_data.keys() and user_data[username]!=password:
            c.send("invalid credentails".encode("utf-8"))
            c.send("exit".encode("utf-8"))
            break
        if username in user_data.keys() and user_data[username]==password:
            print("here")
            c.sendall("userlist".encode("utf-8"))
            c.recv(1024)
            c.sendall("enter the symbol".encode("utf-8"))
            c.recv(1024)    
            for candidate,symbol in candidates.items():
                c.sendall(f"candidate name >{candidate} , symbol > {symbol}".encode("utf-8"))
                c.recv(1024)
            c.send("over".encode("utf-8"))
    
            selection=c.recv(buffer).decode().strip()
            print(selection)
            if selection not in reverse_candidates.keys():
                c.send("invalid selection".encode("utf-8"))
                c.send("exit".encode("utf-8"))
            else:
                # to synchorize the number of votes and all
                lock.acquire()
                total_votes[selection]+=1
                casted_votes[username]=True
                lock.release()
            break 
    print(total_votes)
    print(casted_votes)
    c.close()

def main():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((endpoint,port))
    print(f"server started at {endpoint} on port > {port}")
    s.listen(5)
    while True:
        c,add=s.accept()
        print(f"client {add} is connected to the server")
        start_new_thread(new_thread_vote,(c,))
    s.close()




if __name__=="__main__":
    main()
            
        