import subprocess
import os
import platform
import urllib.request
import tarfile
import zipfile
from i18n import I18N

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
        executable_path = os.path.join(self.steam_path, self.executable_file)
        if os.path.exists(executable_path):
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
        steamcmd = f"+force_install_dir \"{self.server_path}\" +login anonymous +app_update {self.steamapps_id} validate +quit"
        if self.platform == "Windows":
            command = f'cd "{self.steam_path}"; & ".\\{self.executable_file}" {steamcmd}'
            subprocess.call(["powershell.exe", "-Command", command], shell=True)
        elif self.platform == "Linux":
            command = f'cd "{self.steam_path}" && ./{self.executable_file} {steamcmd}'
            try:
                subprocess.check_call(command, shell=True)  
            except subprocess.CalledProcessError as e:
                print("Failed to install game via SteamCMD:", e)  


st = SteamCMD()
st.download()
st.install()