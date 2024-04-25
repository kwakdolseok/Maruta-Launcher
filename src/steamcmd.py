import subprocess
import os
import platform
import urllib.request
import tarfile
import zipfile
import requests
from i18n import I18N
from xml.etree import ElementTree as ET


i18n = I18N()

class SteamCMD:

    def __init__(self):
        self.steamapps_id = os.getenv("APPID")
        self.service_name = os.getenv("SERVICE_NAME")
        self.serverfile = os.getenv("SERVER_FILE")
        self.platform = platform.system()

        if self.platform == "Windows":
            self.install_drive = os.getenv("INSTALL_DRIVE", "C:\\")
            self.steam_path = os.path.join(self.install_drive, "marutalauncher", "steamcmd")
            self.server_path = os.path.join(self.install_drive, "marutalauncher")
            self.steam_url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
            self.executable_file = "steamcmd.exe"
            
        elif self.platform == "Linux":
            user_home = os.path.expanduser('~')
            self.steam_path = os.path.join(user_home, "marutalauncher", "steamcmd")
            self.server_path = os.path.join(user_home, "marutalauncher")
            self.steam_url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
            self.executable_file = "steamcmd.sh"

    def create_symbolic_links(self):
        user_home = os.path.expanduser('~')
        steam_root = os.path.join(user_home, '.steam')
        os.makedirs(steam_root, exist_ok=True)

        sdk32_path = os.path.join(steam_root, 'sdk32')
        sdk64_path = os.path.join(steam_root, 'sdk64')
        os.makedirs(sdk32_path, exist_ok=True)
        os.makedirs(sdk64_path, exist_ok=True)

        steamclient_src32 = os.path.join(self.steam_path, 'linux32', 'steamclient.so')
        steamclient_src64 = os.path.join(self.steam_path, 'linux64', 'steamclient.so')

        steamclient_link32 = os.path.join(sdk32_path, 'steamclient.so')
        steamclient_link64 = os.path.join(sdk64_path, 'steamclient.so')

        for src, link in [(steamclient_src32, steamclient_link32), (steamclient_src64, steamclient_link64)]:
            if os.path.exists(src):
                if not os.path.exists(link):
                    os.symlink(src, link)
            else:
                print(f"Error: Source file '{src}' does not exist. Symbolic link was not created.")

    def download(self):
        steam_path = os.path.join(self.steam_path, self.executable_file)
        if os.path.exists(steam_path):
            i18n.log('steamcmd_installed', level="Warning")
            return
        
        os.makedirs(self.steam_path, exist_ok=True)

        file_path = os.path.join(self.steam_path, os.path.basename(self.steam_url))
        if not os.path.exists(file_path):
            urllib.request.urlretrieve(self.steam_url, file_path)

        if self.platform == "Windows":
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(self.steam_path)
            command = f'cd "{self.steam_path}"; & ".\\{self.executable_file}" validate +quit'
            subprocess.call(["powershell.exe", "-Command", command], shell=True)
        elif self.platform == "Linux":
            with tarfile.open(file_path, "r:gz") as tar:
                tar.extractall(self.steam_path)
            command = f'cd "{self.steam_path}"; chmod +x ./{self.executable_file}; ./{self.executable_file} validate +quit'
            subprocess.call(command, shell=True)
            self.create_symbolic_links()
        os.remove(file_path)


    def install(self):
        executable_path = os.path.join(self.server_path, "steamapps", f"appmanifest_{self.steamapps_id}.acf")
        if os.path.exists(executable_path):
            i18n.log('game_installed', level="Warning", game=os.getenv("SERVICE_NAME"))
            return
        steamcmd = f"+force_install_dir \"{self.server_path}\" +login anonymous +app_update {self.steamapps_id} validate +quit"
        if self.platform == "Windows":
            command = f'cd "{self.steam_path}"; & ".\\{self.executable_file}" {steamcmd}'
            subprocess.call(["powershell.exe", "-Command", command], shell=True)
        elif self.platform == "Linux":
            command = f'cd "{self.steam_path}" && ./{self.executable_file} {steamcmd}'
            try:
                subprocess.check_call(command, shell=True)  
            except subprocess.CalledProcessError as e: 
                i18n.log("error", level="error", error=str(e))


    def update(self):
        appmanifest_path = os.path.join(self.server_path, "steamapps", f"appmanifest_{self.steamapps_id}.acf")
        if not os.path.exists(appmanifest_path):
            i18n.log("file_not_found", level="Warning" , file=appmanifest_path)
            return

        local_build_id = None
        try:
            with open(appmanifest_path, 'r') as file:
                for line in file:
                    if 'buildid' in line.strip():
                        local_build_id = line.split('"')[3]
                        break
        except Exception as e:
            i18n.log('reading_file', level="error",error={str(e)})
            return

        if local_build_id is None:
            i18n.log("not_build",level="Warning",id=self.steamapps_id)
            return

        try:
            response = requests.get(f'https://steamdb.info/api/PatchnotesRSS/?appid={self.steamapps_id}')
            if response.status_code != 200:
                i18n.log('steamdb_data', level='Warning', stastatus_code=response.status_code)
                return

            root = ET.fromstring(response.content)
            latest_build_id = root.find('.//item/guid').text.split('#')[-1]
        except ET.ParseError as e:
            print(f"XML 파싱 오류: {e}")
            return

        if local_build_id != latest_build_id:
            steamcmd = f"+force_install_dir \"{self.server_path}\" +login anonymous +app_update {self.steamapps_id} validate +quit"
            if self.platform == "Windows":
                command = f'cd "{self.steam_path}"; & ".\\{self.executable_file}" {steamcmd}'
                subprocess.call(["powershell.exe", "-Command", command], shell=True)
            elif self.platform == "Linux":
                command = f'cd "{self.steam_path}" && ./{self.executable_file} {steamcmd}'
                try:
                    subprocess.check_call(command, shell=True)  
                except subprocess.CalledProcessError as e:
                    i18n.log("error", level="error", error=str(e))
            print(f"BUILD_ID를 {latest_build_id}(으)로 업데이트했습니다.")
