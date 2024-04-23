import os
import time
from colorama import Fore, Style
import platform
from dotenv import load_dotenv, find_dotenv

dotenv_file = find_dotenv()
if dotenv_file:
    load_dotenv(dotenv_file)
else:
    print("The .env file could not be found.")

class i18n:
    def __init__(self):
        self.platform = platform.system()
        if self.platform == "Windows":
            self.install_drive = os.getenv("INSTALL_DRIVE", "C:\\")
            self.log_path = os.path.join(self.install_drive, "marutalauncher", "log", "MarutaLauncher.log")
        elif self.platform == "Linux":
            user_home = os.path.expanduser('~')
            self.log_path = os.path.join(user_home, "marutalauncher", "log", "MarutaLauncher.log")

        self.language = os.getenv('SCRIPT_LANGUAGE', 'English')
        print("현재 설정된 언어:", self.language)
        self.messages = {
            'messages': {
                "한국어": "설치가 완료되었습니다.",
                "English": "",
                "日本語": "",
                '中文(简体': "",
                '中文(繁體)': "",
                'Español': "",
                'Français':"",
                'Deutsch':"",
                'Русский':"",
                'Português':"",
                "Italiano":"",
                "Tiếng Việt": "",
                "ไทย": "",
                "Bahasa Indonesia": "",
                "हिन्दी": "",
                "العربية": "",
                "Filipino": "",
                "Nederlands": "",
                "Svenska": "",
                "Norsk": "",
                "Suomi": "",
                "Dansk": "",
                "Polski": "",
                "Čeština": "",
                "Magyar": "",
                "Română": "",
                "Ελληνικά": "",
                "Türkçe": "",
                "עברית": "",
                "فارسی": "",
                "ქართული": ""

            },

        }

    def log(self, message_key, level='INFO'):

        message = self.messages.get(message_key, {}).get(self.language, 'Message key or language not found')

        level = level.upper()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        console_color = Fore.MAGENTA if level == "ERROR" else Fore.YELLOW if level == "WARNING" else Fore.CYAN
        console_formatted_message = f"{current_time} {console_color}[{level}]{Style.RESET_ALL} {message}"
        print(console_formatted_message)

        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        file_formatted_message = f"{current_time} [{level}] {message}\n"
        with open(self.log_path, "a", encoding='utf-8') as file:
            file.write(file_formatted_message)

i18n = i18n()
i18n.log("installation_complete",level="info")