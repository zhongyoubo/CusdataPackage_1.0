from sys import stderr, stdin, stdout
import paramiko
from paramiko import AutoAddPolicy
from paramiko import AuthenticationException
from paramiko.ssh_exception import NoValidConnectionsError

class SSHManager():
    def __init__(self):
        print("SSHManager init")
        self.ssh_client = paramiko.SSHClient()
    

    def ssh_connect(self,hostname,username,password,port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        print(f"Connectint to {self.username}@{self.hostname} Port:{self.port}")
        try:
            self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            self.ssh_client.connect(hostname=self.hostname,port=self.port,username=self.username,password=self.password)
        except AuthenticationException:
            print(f"username({self.username}) or password({self.password}) error")
            return 1001
        except NoValidConnectionsError:
            print(f"Connect to {self.username}@{self.hostname} time out")
            return 1002
        except:
            print(f"Connect to {self.username}@{self.hostname} Unexcept error")
            return 1003 
        return 1000

    #通过ssh执行远程命令
    def ssh_exec_command(self,cmd):
        try:
            #stdin为输入的命令，stdout为命令返回结果，stderr为命令错误是返回结果
            #这里我们都会发现，使用exec_command('cd dirname')时并不会切换目录，
            # execute_command() 是a single session，每次执行完后都要回到缺省目录。
            # 所以可以 .execute_command('cd /var; pwd')。
            stdin,stdout,stderr = self.ssh_client.exec_command(command=cmd,get_pty=True)
            #print('stdin:',stdin,'\n','stdout:',stdout,'\n','stderr:',stderr)
            result = stdout.read().decode('utf-8')
            print(cmd)
            #print(result)
            return result 
        except Exception as e:
            raise RuntimeError('exec command[%s] failed'%str(cmd))

    def close(self):
        self.ssh_client.close()

    