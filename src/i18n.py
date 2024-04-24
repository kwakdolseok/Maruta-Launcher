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

class I18N:
    def __init__(self):
        self.platform = platform.system()
        self.install_drive = os.getenv("INSTALL_DRIVE", "C:\\")
        if self.platform == "Windows":
            self.log_path = os.path.join(self.install_drive, "marutalauncher", "log", "MarutaLauncher.log")
        else:
            user_home = os.path.expanduser('~')
            self.log_path = os.path.join(user_home, "marutalauncher", "log", "MarutaLauncher.log")

        self.language = os.getenv('SCRIPT_LANGUAGE', 'English') 
        print("현재 설정된 언어:", self.language)
        self.messages = {
            'steamcmd_installed': {
                "한국어": "[마루타 구동기] 시스템에 이미 SteamCMD가 설치되어 있습니다.",
                "English": "[Maruta Launcher] SteamCMD is already installed on the system.",
                "日本語": "[マルタ ランチャー] システムにはすでに SteamCMD がインストールされています。",
                '中文(简体': "[Maruta启动器] 系统中已安装了 SteamCMD。",
                '中文(繁體)': "[Maruta啟動器] 系統中已安裝了 SteamCMD。",
                'Español': "[Lanzador de Maruta] SteamCMD ya está instalado en el sistema.",
                'Français': "[Lanceur Maruta] SteamCMD est déjà installé sur le système.",
                'Deutsch': "[Maruta Launcher] SteamCMD ist bereits im System installiert.",
                'Русский': "[Лаунчер Маруты] SteamCMD уже установлен в системе.",
                'Português': "[Iniciador Maruta] O SteamCMD já está instalado no sistema.",
                "Italiano": "[Launcher Maruta] SteamCMD è già installato nel sistema.",
                "Tiếng Việt": "[Trình khởi chạy Maruta] SteamCMD đã được cài đặt trên hệ thống.",
                "ไทย": "[เริ่มต้น Maruta] SteamCMD ได้ถูกติดตั้งบนระบบแล้ว",
                "Bahasa Indonesia": "[Penggerak Maruta] SteamCMD sudah terpasang di sistem.",
                "हिन्दी": "[Maruta लॉन्चर] सिस्टम पर पहले से ही SteamCMD स्थापित है।",
                "العربية": "[مطلق Maruta] تم تثبيت SteamCMD بالفعل على النظام.",
                "Filipino": "[Launcher ng Maruta] Naka-install na ang SteamCMD sa system.",
                "Nederlands": "[Maruta Launcher] SteamCMD is al geïnstalleerd op het systeem.",
                "Svenska": "[Maruta Launcher] SteamCMD är redan installerat på systemet.",
                "Norsk": "[Maruta Launcher] SteamCMD er allerede installert på systemet.",
                "Suomi": "[Maruta Launcher] SteamCMD on jo asennettu järjestelmään.",
                "Dansk": "[Maruta Launcher] SteamCMD er allerede installeret på systemet.",
                "Polski": "[Maruta Launcher] SteamCMD jest już zainstalowany w systemie.",
                "Čeština": "[Maruta Launcher] SteamCMD je již nainstalován v systému.",
                "Magyar": "[Maruta indító] A SteamCMD már telepítve van a rendszerben.",
                "Română": "[Lansator Maruta] SteamCMD este deja instalat în sistem.",
                "Ελληνικά": "[Εκκινητής Maruta] Το SteamCMD είναι ήδη εγκατεστημένο στο σύστημα.",
                "Türkçe": "[Maruta Başlatıcı] SteamCMD zaten sistemde yüklü.",
                "עברית": "[מפעיל Maruta] SteamCMD כבר מותקן במערכת.",
                "فارسی": "[راه‌انداز Maruta] SteamCMD در سیستم قبلاً نصب شده است.",
                "ქართული": "[Maruta ლანჩერი] SteamCMD უკვე დაყენებულია სისტემაში."
            },

            'game_installed': {
                "한국어": "[마루타 구동기] 시스템에 이미 {game} 설치되어 있습니다.",
                "English": "[Maruta Launcher] The game {game} is already installed on the system.",
                "日本語": "[マルタ ランチャー] システムにはすでに{game}がインストールされています。",
                '中文(简体': "[Maruta启动器] 系统中已安装了{game}。",
                '中文(繁體)': "[Maruta啟動器] 系統中已安裝了{game}。",
                'Español': "[Lanzador de Maruta] El juego {game} ya está instalado en el sistema.",
                'Français': "[Lanceur Maruta] Le jeu {game} est déjà installé sur le système.",
                'Deutsch': "[Maruta Launcher] Das Spiel {game} ist bereits im System installiert.",
                'Русский': "[Лаунчер Маруты] Игра {game} уже установлена в системе.",
                'Português': "[Iniciador Maruta] O jogo {game} já está instalado no sistema.",
                "Italiano": "[Launcher Maruta] Il gioco {game} è già installato nel sistema.",
                "Tiếng Việt": "[Trình khởi chạy Maruta] Trò chơi {game} đã được cài đặt trên hệ thống.",
                "ไทย": "[เริ่มต้น Maruta] เกม {game} ได้ถูกติดตั้งบนระบบแล้ว",
                "Bahasa Indonesia": "[Penggerak Maruta] Permainan {game} sudah terpasang di sistem.",
                "हिन्दी": "[Maruta लॉन्चर] खेल {game} सिस्टम पर पहले से ही स्थापित है।",
                "العربية": "[مطلق Maruta] اللعبة {game} مثبتة بالفعل على النظام.",
                "Filipino": "[Launcher ng Maruta] Ang laro na {game} ay naka-install na sa system.",
                "Nederlands": "[Maruta Launcher] Het spel {game} is al geïnstalleerd op het systeem.",
                "Svenska": "[Maruta Launcher] Spelet {game} är redan installerat på systemet.",
                "Norsk": "[Maruta Launcher] Spillet {game} er allerede installert på systemet.",
                "Suomi": "[Maruta Launcher] Peli {game} on jo asennettu järjestelmään.",
                "Dansk": "[Maruta Launcher] Spillet {game} er allerede installeret på systemet.",
                "Polski": "[Maruta Launcher] Gra {game} jest już zainstalowana w systemie.",
                "Čeština": "[Maruta Launcher] Hra {game} je již nainstalována v systému.",
                "Magyar": "[Maruta indító] A(z) {game} játék már telepítve van a rendszerben.",
                "Română": "[Lansator Maruta] Jocul {game} este deja instalat în sistem.",
                "Ελληνικά": "[Εκκινητής Maruta] Το παιχνίδι {game} είναι ήδη εγκατεστημένο στο σύστημα.",
                "Türkçe": "[Maruta Başlatıcı] Oyun {game} zaten sistemde yüklü.",
                "עברית": "[מפעיל Maruta] המשחק {game} כבר מותקן במערכת.",
                "فارسی": "[راه‌انداز Maruta] بازی {game} در سیستم قبلاً نصب شده است.",
                "ქართული": "[Maruta ლანჩერი] თამაში {game} უკვე დაყენებულია სისტემაში."
            },
            'error': {
                "한국어": "[마루타 구동기] 오류 발생: {error}",
                "English": "[Maruta Launcher] Error occurred: {error}",
                "日本語": "[マルタ ランチャー] エラーが発生しました: {error}",
                '中文(简体': "[Maruta启动器] 出现错误：{error}",
                '中文(繁體)': "[Maruta啟動器] 發生錯誤：{error}",
                'Español': "[Lanzador de Maruta] Error ocurrió: {error}",
                'Français':"[Lanceur Maruta] Une erreur s'est produite : {error}",
                'Deutsch':"[Maruta Launcher] Fehler aufgetreten: {error}",
                'Русский':"[Лаунчер Маруты] Произошла ошибка: {error}",
                'Português':"[Iniciador Maruta] Ocorreu um erro: {error}",
                "Italiano":"[Launcher Maruta] Si è verificato un errore: {error}",
                "Tiếng Việt":"[Trình khởi chạy Maruta] Đã xảy ra lỗi: {error}",
                "ไทย":"[เริ่มต้น Maruta] มีข้อผิดพลาด: {error}",
                "Bahasa Indonesia":"[Penggerak Maruta] Kesalahan terjadi: {error}",
                "हिन्दी":"[Maruta लॉन्चर] त्रुटि हुई: {error}",
                "العربية":"[مطلق Maruta] حدث خطأ: {error}",
                "Filipino":"[Launcher ng Maruta] May naganap na error: {error}",
                "Nederlands":"[Maruta Launcher] Fout opgetreden: {error}",
                "Svenska":"[Maruta Launcher] Fel uppstod: {error}",
                "Norsk":"[Maruta Launcher] Feil oppstod: {error}",
                "Suomi":"[Maruta Launcher] Virhe tapahtui: {error}",
                "Dansk":"[Maruta Launcher] Fejl opstod: {error}",
                "Polski":"[Maruta Launcher] Wystąpił błąd: {error}",
                "Čeština":"[Maruta Launcher] Došlo k chybě: {error}",
                "Magyar":"[Maruta indító] Hiba történt: {error}",
                "Română":"[Lansator Maruta] A apărut o eroare: {error}",
                "Ελληνικά":"[Εκκινητής Maruta] Σφάλμα προέκυψε: {error}",
                "Türkçe":"[Maruta Başlatıcı] Hata oluştu: {error}",
                "עברית":"[מפעיל Maruta] אירעה שגיאה: {error}",
                "فارسی":"[راه‌انداز Maruta] خطا رخ داد: {error}",
                "ქართული":"[Maruta ლანჩერი] მოხდა შეცდომა: {error}"
            },


            'messages': {
                    "한국어": "",
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

    def log(self, message_key, level='INFO', **kwargs):
        message_template = self.messages.get(message_key, {}).get(self.language, 'Message key or language not found')
        message = message_template.format(**kwargs)  # 메시지 템플릿에 매개변수 치환

        level = level.upper()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        console_color = Fore.MAGENTA if level == "ERROR" else Fore.YELLOW if level == "WARNING" else Fore.CYAN
        console_formatted_message = f"{current_time} {console_color}[{level}]{Style.RESET_ALL} {message}"
        print(console_formatted_message)

        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        file_formatted_message = f"{current_time} [{level}] {message}\n"
        with open(self.log_path, "a", encoding='utf-8') as file:
            file.write(file_formatted_message)