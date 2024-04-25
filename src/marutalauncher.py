import os
import platform
import psutil
import subprocess
from dotenv import load_dotenv, find_dotenv
from steamcmd import SteamCMD


dotenv_file = find_dotenv()
if dotenv_file:
    load_dotenv(dotenv_file)
else:
    print("환경 설정 파일을 찾을 수 없습니다.")

steamcmd = SteamCMD()

class MarutaLauncher:
    def __init__(self):
        self.steamapps_id = os.getenv("APPID")
        self.service_name = os.getenv("SERVICE_NAME")
        self.serverfile = os.getenv("SERVER_FILE")
        self.running_process = None  

        self.platform = platform.system()
        if self.platform == "Windows":
            self.install_drive = os.getenv("INSTALL_DRIVE", "C:\\")
            self.server_path = os.path.join(self.install_drive, "marutalauncher")
            self.executable_file = "steamcmd.exe"
            
        elif self.platform == "Linux":
            user_home = os.path.expanduser('~')
            self.server_path = os.path.join(user_home, "marutalauncher")
            self.executable_file = "steamcmd.sh"
            
        else:
            raise Exception('Linux 또는 Windows만 지원됩니다.')

    def check_process(self):
        for process in psutil.process_iter(['pid', 'name']):
            if self.serverfile in process.info['name']:
                return process
        return None
    
    def start(self):
        if self.check_process():
            print(f"[마루타 구동기] {self.service_name} 게임엔진이 이미 실행 중입니다.")
            return

        log_file_path = os.path.join(self.server_path, 'game_engine.log')
        with open(log_file_path, 'a') as log_file:
            executable_file = f"{self.serverfile}" + (".exe" if self.platform == "Windows" else ".sh")

            if self.platform == "Windows":
                command = f'cmd /c "cd /d "{self.server_path}" && "{executable_file}" {os.getenv("OPTIONS") or ""}"'
                self.running_process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=log_file,
                    stderr=subprocess.STDOUT
                )

            elif self.platform == "Linux":
                command = f'cd "{self.server_path}"; ./"{executable_file}" {os.getenv("OPTIONS")}'
                self.running_process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=log_file,
                    stderr=subprocess.STDOUT
                )

            print(f"[마루타 구동기] {self.service_name} 게임엔진을 실행 완료했습니다")

    def stop(self):
        found = False
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if self.serverfile in process.info['name']:
                children = process.children(recursive=True)
                for child in children:
                    child.terminate()
                process.terminate()
                found = True
        if found:
            print(f"[마루타 구동기] {self.service_name} 게임엔진 프로세스를 종료했습니다.")
        else:
            print(f"실행 중인 {self.service_name} 게임엔진 프로세스가 없습니다.")



# 사용 예
launcher = MarutaLauncher()

launcher.start()
#launcher.stop()
