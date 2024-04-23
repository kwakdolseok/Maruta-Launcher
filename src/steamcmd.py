import subprocess
import os
import platform
import urllib.request
import tarfile
import zipfile

class SteamCMD:
    def __init__(self):
        self.platform = platform.system()
        if self.platform == "Windows":
            self.steam_url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
            self.default_path = os.path.join("C:\\", "marutalauncher")
            self.executable_file = "steamcmd.exe"
        elif self.platform == "Linux":
            user_home = os.path.expanduser('~')
            self.default_path = os.path.join(user_home, "marutalauncher")
            self.steam_url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz"
            self.executable_file = "steamcmd.sh"
        else:
            raise Exception('Unsupported OS. Only Linux or Windows is supported.')
        self.steam_path = self.default_path
        self.server_path = self.default_path

    def setup_linux_environment(self):
        subprocess.call(['sudo', 'dpkg', '--add-architecture', 'i386'])
        subprocess.call(['sudo', 'apt-get', 'update'])
        subprocess.call(['sudo', 'apt-get', 'install', '-y', 'lib32gcc-s1'])


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

    def install(self, install_path=None):
        if install_path:
            self.steam_path = install_path
            self.server_path = install_path
        else:
            self.steam_path = self.default_path
            self.server_path = self.default_path

        executable_path = os.path.join(self.steam_path, self.executable_file)
        if os.path.exists(executable_path):
            print("SteamCMD is already installed.")
            return

        os.makedirs(self.steam_path, exist_ok=True)

        file_path = os.path.join(self.steam_path, os.path.basename(self.steam_url))
        if not os.path.exists(file_path):
            print("Downloading SteamCMD...")
            urllib.request.urlretrieve(self.steam_url, file_path)
        else:
            print("SteamCMD installer already downloaded.")

        if self.platform == "Windows":
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                print("Extracting SteamCMD...")
                zip_ref.extractall(self.steam_path)
            command = f'cd "{self.steam_path}"; & ".\\{self.executable_file}" +quit'
            subprocess.call(["powershell.exe", "-Command", command], shell=True)
        elif self.platform == "Linux":
            with tarfile.open(file_path, "r:gz") as tar:
                print("Extracting SteamCMD...")
                tar.extractall(self.steam_path)
            command = f'cd "{self.steam_path}"; chmod +x ./{self.executable_file}; ./{self.executable_file} +quit'
            subprocess.call(command, shell=True)

        os.remove(file_path)
        print("Installation complete.")
        
    def update(self, *, app_id, install_dir):
        steamcmd = f"+force_install_dir {install_dir} +login anonymous +app_update {str(app_id)} validate +quit"
        if self.platform == "Windows":
            command = ['powershell.exe', '-Command', f'cd "{self.steam_path}"; & ".\\{self.executable_file}" {steamcmd}']
        elif self.platform == "Linux":
            command = ['bash', '-c', f'cd "{self.steam_path}"; ./{self.executable_file} {steamcmd}']
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            print("오류 발생:", result.stderr)
        else:
            print("업데이트 성공적으로 완료됨:", result.stdout)

