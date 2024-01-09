

about = """
---------------------------------------------------------------
Name: Fredmark Ivan D. Dizon
GitHub: https://github.com/saphiraaa
Email: fredmarkivand@gmail.com
Location: Bulacan, Philippines

Project: MIRA - CyberGuard Innovation's CLI Password Manager
GitHub Repository: https://github.com/saphiraaa/MIRA
License: MIT License

Version: 2.12.9
Release Date: 2024-01-04
                                                            
New Features:                                                 
- Debit/Credit Card PINs are now acceptable                   
- API Keys are now acceptable                                 
- Bug fixes and optimizations                                 
- Password Expiration for Card PINs (2mnths)                   
---------------------------------------------------------------
"""

remember = r"""

 ____________________
/                    \
|       Always       |
|      Remember      |      
\____________________/
         !  !
         !  !
         L_ !
        / _)!
       / /__L
 _____/ (____)
        (____)
 _____  (____)
      \_(____)
         !  !
         !  !
         \__/
"""

blehhh = r"""
                                \\_V_//
                                \/=|=\/
                                 [=v=]
                               __\___/_____
                              /..[  _____  ]
                             /_  [ [  M /] ]
                            /../.[ [ M /@] ]
                           <-->[_[ [M /@/] ]
                          /../ [.[ [ /@/ ] ]
     _________________]\ /__/  [_[ [/@/ C] ]
    <_________________>>0---]  [=\ \@/ C / /
       ___      ___   ]/000o   /__\ \ C / /
          \    /              /....\ \_/ /
       ....\||/....           [___/=\___/
      .    .  .    .          [...] [...]
     .      ..      .         [___/ \___]
     .    0 .. 0    .         <---> <--->
  /\/\.    .  .    ./\/\      [..]   [..]
 / / / .../|  |\... \ \ \    _[__]   [__]_
/ / /       \/       \ \ \  [____>   <____]
"""

wolf = r'''
                                 ,ood8888booo,
                              ,od8           8bo,
                           ,od                   bo,
                         ,d8                       8b,
                        ,o                           o,    ,a8b
                       ,8                             8,,od8  8
                       8'                             d8'     8b
                       8                           d8'ba     aP'                                
                       Y,                       o8'         aP'
                        Y8,                      YaaaP'    ba                       __  ___________  ___
                         Y8o                   Y8'         88                      /  |/  /  _/ __ \/   |
                          `Y8               ,8"           `P                      / /|_/ // // /_/ / /| |
                            Y8o        ,d8P'              ba                     / /  / // // _, _/ ___ |
                       ooood8888888P"""'                  P'                    /_/  /_/___/_/ |_/_/  |_|
                    ,od                                  8                       CyberGuard Innovations
                 ,dP     o88o                           o'                               2.12.9
                ,dP          8                          8
               ,d'   oo       8                       ,8
               $    d$"8      8           Y    Y  o   8
              d    d  d8    od  ""boooooooob   d"" 8   8
              $    8  d   ood' ,   8        b  8   '8  b
              $   $  8  8     d  d8        `b  d    '8  b
               $  $ 8   b    Y  d8          8 ,P     '8  b
               `$$  Yb  b     8b 8b         8 8,      '8  o,
                    `Y  b      8o  $$o      d  b        b   $o
                     8   '$     8$,,$"      $   $o      '$o$$
                      $o$$P"                 $$o$
'''

from cryptography.fernet import Fernet
import os
import getpass
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from secrets import token_bytes
import argon2
import time
from password_strength import PasswordPolicy
from datetime import datetime, timedelta
from threading import Thread
from termcolor import colored
from pyotp import TOTP, random_base32
from functools import wraps
import string 
import random
import json
import platform
import sys

def clear_terminal():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")

def get_os_distribution():
    """
    This function, get_os_distribution(), retrieves information about the operating system.
    For Linux, it reads /etc/os-release to gather distribution details.
    For macOS, it utilizes platform.mac_ver().
    For Windows, it uses platform.version().
    Returns formatted strings with relevant OS details.
    """
    system_info = platform.system()

    if system_info == 'Linux':
        try:
            with open('/etc/os-release', 'r') as f:
                lines = f.readlines()
                distribution_info = {}
                for line in lines:
                    key, value = line.strip().split('=')
                    distribution_info[key] = value.replace('"', '')

                distribution = distribution_info.get('PRETTY_NAME', 'Unknown Distribution')
                version = distribution_info.get('VERSION_ID', 'Unknown Version')
                codename = distribution_info.get('VERSION_CODENAME', 'Unknown Codename')
                base = distribution_info.get('ID_LIKE', 'Unknown Base')
                return f"Linux Distribution: {distribution}\nVersion: {version}\nCodename: {codename}\nBase: {base}\nArchitecture: {platform.architecture()[0]}"

        except FileNotFoundError:
            return "Unable to determine distribution. /etc/os-release file not found."

    elif system_info == 'Darwin':
        version, _, _ = platform.mac_ver()
        return f"macOS Version: {version}\nArchitecture: {platform.architecture()[0]}"

    elif system_info == 'Windows':
        version = platform.version()
        return f"Windows Version: {version}\nArchitecture: {platform.architecture()[0]}"

    else:
        return f"Operating System: {system_info}"

def get_python_version():
    """
    Returns python's current version
    """
    return f"Python Version: {platform.python_version()}"

def check_linux_privileges():
    """
    Check for elevated privileges. For LINUX
    """
    if 'SUDO_UID' in os.environ.keys() or os.getenv('USER') == 'root':
        return True
    return False

def is_admin():
    """
    Check for elavated privileges. For WINDOWS
    """
    if platform.system() == 'Windows':
        try:
            from ctypes import windll
            return windll.shell32.IsUserAnAdmin()
        except Exception:
            return False
    else:
        return False

def check_windows_privileges():
    return is_admin()

def get_current_datetime():
    """
    Retrieve the current date and time, formatted for display.
    """
    current_datetime = datetime.now()
    date_str = current_datetime.strftime("%Y-%m-%d")
    time_str = current_datetime.strftime("%H:%M:%S")

    return f"Current Time: {time_str}\nDate: {date_str}"

class PasswordManager:
    MAX_LOGIN_ATTEMPTS = 4 
    LOCKOUT_DURATION_SECONDS = 300
    """--------File Paths for specific Operating Systems--------"""
    if os.name == "posix":
        LOCKOUT_FILE = os.environ.get('LOCKOUT_FILE', '/etc/.lockout')
        USER_DATA_FILE = os.environ.get('USER_DATA_FILE', '/etc/.user')
        SECFILE = os.environ.get('SECFILE', '/etc/.sec')
        PASSFILE = os.environ.get('PASSFILE', '/etc/.pass')
        API = os.environ.get('API', '/etc/.api')
        CARD_PIN_FILE = os.environ.get('CARD_PIN_FILE', '/etc/.card')
    elif os.name == "nt":
        program_files_dir = os.environ.get('ProgramFiles', 'C:\\Program Files')
        app_folder_name = 'Mira'
        app_folder_path = os.path.join(program_files_dir, app_folder_name)
        os.makedirs(app_folder_path, exist_ok=True)
        LOCKOUT_FILE = os.path.join(app_folder_path, 'lockout')
        USER_DATA_FILE = os.path.join(app_folder_path, 'user_data')
        SECFILE = os.path.join(app_folder_path, 'sec')
        PASSFILE = os.path.join(app_folder_path, 'pass')
        API = os.path.join(app_folder_path, 'api')
        CARD_PIN_FILE = os.path.join(app_folder_path, 'card')

    def __init__(self):
        """--------Initializers--------"""
        self.master_password = None
        self.cipher = None
        self.ph = PasswordHasher()
        expiry_thread = Thread(target=self.notify_expiry_background)
        pin_expiry_thread = Thread(target=self.notify_pin_expiry_background)
        pin_expiry_thread.daemon = True
        expiry_thread.daemon = True
        expiry_thread.start()
        pin_expiry_thread.start()
        self.totp_secret_key = None
        self.failed_login_attempts = 0
        self.lockout_time = None
        self.load_lockout_time()
        self.replacements = {
                'a' or 'A': ['4', '@', 'á', 'ä', 'å', 'ą', 'ey', 'a', 'A'],
                'b' or 'B': ['8', '6', 'ß', 'B', 'b'],
                'c' or 'C': ['(', '<', 'ç', 'ć', 'si', 'C', 'c'],
                'd' or 'D': ['[)', '|)', 'đ', 'D', 'd'],
                'e' or 'E': ['3', '€', 'é', 'è', 'ê', 'ë', 'ę', 'E', 'e'],
                'f' or 'F': ['ph', '|=', 'ƒ', 'F', 'f'],
                'g' or 'G': ['9', '6', 'ğ', 'ji', 'G', 'g'],
                'h' or 'H': ['#', '|-|', 'ħ', 'eych', 'H', 'h'],
                'i' or 'I': ['1', '!', 'í', 'ì', 'î', 'ï', 'į', 'ay', 'I', 'i'],
                'j' or 'J': ['_|', '_]', 'й', 'j', 'J'],
                'k' or 'K': ['|<', '|{', 'ķ', 'K', 'k'],
                'l' or 'L': ['1', '|_', 'ł', 'L', 'l'],
                'm' or 'M': ['/\\/\\', '|\\/|', 'м', 'M', 'm'],
                'n' or 'N': ['|\\|', '/\\/', 'ñ', 'ń', 'ň', 'N', 'n'],
                'o' or 'O': ['0', '*', 'ó', 'ö', 'ø', 'ô', 'ő', 'O', 'o'],
                'p' or 'P': ['|>', '|D', 'þ', 'р', 'P'],
                'q' or 'Q': ['(,)', 'kw', 'q', 'Q'],
                'r' or 'R': ['2', '|?', 'г', 'ř', 'R', 'r'],
                's' or 'S': ['$', '5', 'ś', 'š', 'ş', 'ș', 'S', 's'],
                't' or 'T': ['+', '7', 'ţ', 'ť', 'T', 't'],
                'u' or 'U': ['|_|', '\\_\\', 'ü', 'ú', 'ů', 'ű', 'U', 'u'],
                'v' or 'V': ['\\/', 'V', 'v'],
                'w' or 'W': ['\\/\\/', '|/\\|', 'ш', 'щ', 'uu', 'W', 'w'],
                'x' or 'X': ['><', '%', 'ж', 'X', 'x'],
                'y' or 'Y': ['`/', 'ý', 'ÿ', 'ŷ', 'y', 'Y'],
                'z' or 'Z': ['2', '7_', 'ž', 'ź', 'ż', 'z', 'Z'],
                '0': ['o', 'ð', 'ø'],
                '1': ['i', 'l', 'ł'],
                '2': ['z', 'ż', 'ź'],
                '3': ['e', 'ę', 'ė'],
                '4': ['a', 'å', 'ä', 'à', 'á', 'â'],
                '5': ['s', 'š', 'ş', 'ș', 'ś'],
                '6': ['g', 'ğ'],
                '7': ['t', 'ţ', 'ť'],
                '8': ['b', 'ß', 'ь'],
                '9': ['g', 'ğ', 'ĝ'],
            }

    def clear_terminal(self):
        if os.name == "posix":
            os.system("clear")
        elif os.name == "nt":
            os.system("cls")

    def save_lockout_time(self):
        """
        Saves the lockout time to a file in JSON format if lockout_time is set. It creates a dictionary with 'lockout_time' as the key and the lockout time value, then writes it to the LOCKOUT_FILE using json.dump().
        """
        if self.lockout_time:
            lockout_data = {'lockout_time': self.lockout_time}
            with open(self.LOCKOUT_FILE, 'w') as lockout_file:
                json.dump(lockout_data, lockout_file)

    def load_lockout_time(self):
        """
        Attempts to load lockout time from the LOCKOUT_FILE. It reads the file, extracts 'lockout_time' from the JSON data, and sets it to self.lockout_time. If the file is not found or there is a JSON decoding error, it gracefully handles the exception.
        """
        try:
            with open(self.LOCKOUT_FILE, 'r') as lockout_file:
                lockout_data = json.load(lockout_file)
                self.lockout_time = lockout_data.get('lockout_time')
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def increment_failed_attempts(self):
        """
        Handles incrementing the count of failed login attempts. If the lockout_time is set and the current time is less than the lockout_time, it prints a message and exits. Otherwise, it increments the failed login attempts counter and checks if it exceeds the maximum allowed attempts. If exceeded, it sets a lockout time and prints a message before exiting. Otherwise, it returns True.
        """
        if self.lockout_time and time.time() < self.lockout_time:
            print(colored(blehhh, "red"))
            print(colored(f"[-] Account locked. WE ALREADY TOLD YOU THAT WE DON'T ACCEPT BUGS HERE! If you are the real user, try again after {int(self.lockout_time - time.time())} seconds.", "red"))
            exit()
            return False

        self.failed_login_attempts += 1

        if self.failed_login_attempts >= self.MAX_LOGIN_ATTEMPTS:
            self.lockout_time = time.time() + self.LOCKOUT_DURATION_SECONDS
            self.save_lockout_time()
            print(colored(blehhh, "red"))
            print(colored(f"[-] Too many failed attempts. ARE YOU TRYING TO BRUTEFORCE THIS? WE DON'T ACCEPT SHITTY BUGS HERE! Account locked for {self.LOCKOUT_DURATION_SECONDS} seconds.", "red"))
            exit()
            return False

        return True

    def generate_password(self):
        """
        Generate a strong password based on user's choice.
        """
        while True:
            try:
                choice = input(colored("[**] Choose password generation method:\n1. Random by length\n2. Custom phrase\n3. Combination of Random and Phrase\n4. Multiple Phrase\n5. Pattern\n> ", "cyan"))

                if choice == '1':
                    try:
                        length = int(input(colored("[*] Enter the desired password length: ", "yellow")))
                    except ValueError:
                        length = 30
                        print(colored(f"[**] No length provided!! (default: {length})", "magenta"))
                    password = self.generate_random_password(length)
                elif choice == '2':
                    phrase = input(colored("[*] Enter a custom phrase: ", "yellow"))
                    if not phrase:
                        print(colored("[**] No phrase provided!! using default phrase", "magenta"))
                        phrase = 'saphirathebestpasswordmanager'
                    else:
                        phrase = str(phrase)
                    password = self.generate_password_from_phrase(phrase)
                elif choice == '3':
                    try:
                        length = int(input(colored("[*] Enter the desired password length: ", "yellow")))
                    except ValueError:
                        length = 30
                        print(colored(f"[**] No length provided!! (default: {length})", "magenta"))
                    phrase = input(colored("[*] Enter a custom phrase: ", "yellow"))
                    if not phrase:
                        print(colored("[**] No phrase provided, using default phrase!!", "magenta"))
                        phrase = 'saphirathebestpasswordmanager'
                    else:
                        phrase = str(phrase)
                    password = self.generate_combined_password(length, phrase)
                elif choice == '4':
                    try:
                        num_phrases = int(input(colored("[*] Enter the number of phrases: ", "yellow")))
                    except ValueError:
                        num_phrases = 4
                        print(colored(f"[**] No number of phrases provided!! (default: {num_phrases})", "magenta"))
                    phrases = [input(colored(f"[*] Enter phrase {i + 1}: ", "yellow")) for i in range(num_phrases)]
                    password = self.generate_multi_phrase_password(phrases)
                elif choice == '5':
                    pattern = input(colored("[*] Enter the password pattern: ", "yellow"))
                    if not pattern:
                        pattern = 'uuuullaaddsssslllaaalssdddaaaaasasasldld'
                        print(colored("[**] No pattern provided!! (default: {pattern})", "magenta"))
                    else:
                        pattern = str(pattern)
                    password = self.generate_pattern_password(pattern)
                else:
                    print(colored("[-] Invalid choice. Generating random password by length.", "red"))
                    try:
                        length = int(input(colored("[-] Enter the desired password length: ", "yellow")))
                    except ValueError:
                        length = 30
                        print(colored("[**] No length provided!! (default: {length}).", "magenta"))
                    password = self.generate_random_password(length)

                print(colored(f"[+] Generated Password: {password}", "green"))
                break
            except ValueError as e:
                print(colored(f"[-] an error occured: {e}", "red"))

    def generate_combined_password(self, length, phrase):
        """
        Generate a password combining random characters and a user-provided phrase.
        """
        position = random.choice(['beginning', 'middle', 'end'])

        if position == 'beginning':
            random_part_length = length - len(phrase)
            random_part = self.generate_random_password(random_part_length)
            transformed_phrase = ''.join([random.choice(self.replacements.get(char.lower(), [char])) for char in phrase])
            password = transformed_phrase + random_part
            return password
        elif position == 'middle':
            random_part1_length = (length - len(phrase)) // 2
            random_part2_length = length - len(phrase) - random_part1_length
            random_part1 = self.generate_random_password(random_part1_length)
            random_part2 = self.generate_random_password(random_part2_length)
            transformed_phrase = ''.join([random.choice(self.replacements.get(char.lower(), [char])) for char in phrase])
            password = random_part1 + transformed_phrase + random_part2
            return password
        elif position == 'end':
            random_part_length = length - len(phrase)
            random_part = self.generate_random_password(random_part_length)
            transformed_phrase = ''.join([random.choice(self.replacements.get(char.lower(), [char])) for char in phrase])
            password = random_part + transformed_phrase
            return password

    def generate_multi_phrase_password(self, phrases):
        """
        Generate a password combining multiple user-provided phrases with random placement.
        """
        transformed_phrases = [''.join([random.choice(self.replacements.get(char.lower(), [char])) for char in phrase]) for phrase in phrases]

        random.shuffle(transformed_phrases)
        password = ''.join(transformed_phrases)
        return password

    def generate_random_password(self, length):
        """
        Generate a random password of the specified length.
        """
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def generate_password_from_phrase(self, phrase):
        """
        Generate a strong password based on a user-provided phrase.
        """
        transformed_phrase = ''.join([random.choice(self.replacements.get(char.lower(), [char])) for char in phrase])
        password = ''.join([random.choice([char.upper(), char.lower()]) for char in transformed_phrase])
        return password

    def generate_pattern_password(self, pattern):
        """
        Generate a password based on a user-defined pattern.
        """
        characters = {
            'u': string.ascii_uppercase,
            'l': string.ascii_lowercase,
            'd': string.digits,
            's': string.punctuation,
            'a': string.ascii_letters + string.digits,
        }

        password = ''.join([random.choice(characters.get(char, char)) for char in pattern])
        return password

    def enable_2fa(self):
        """
        Enables Two-Factor Authentication (2FA) for a user. It reads user data from the USER_DATA_FILE, checks if 2FA is already enabled, generates a random base32-encoded secret key for TOTP, hashes it, updates user_data, and saves it. Finally, it prints a success message with the account name, key, and issuer name.
        """
        with open(self.USER_DATA_FILE, 'r') as file:
            user_data = json.load(file)

        if user_data.get('2fa_enabled', False):
            print(colored("[-] 2FA is already enabled for this user.", "red"))
            return

        self.totp_secret_key = random_base32()
        ph = argon2.PasswordHasher()
        hashed_totp_key = ph.hash(self.totp_secret_key)
        user_data['2fa_enabled'] = True
        user_data['2fa_secret_key'] = hashed_totp_key

        with open(self.USER_DATA_FILE, 'w') as file:
            json.dump(user_data, file)

        totp = TOTP(self.totp_secret_key)
        print(colored(f"[+] 2FA Enabled. Now use the account name and the kwy to get the 6 digit code.\nAccount Name - {user_data.get('username', 'Unknown')}\nKey - {self.totp_secret_key}\nIssuer Name - MIRA (CyberGuard Innovations)", "green"))        

    def verify_2fa(self, secret_key, code):
        """
        Verifies a Two-Factor Authentication (2FA) code for a given secret key. It uses the TOTP class to generate a TOTP instance based on the provided secret_key and then verifies the input code against the generated code. Returns True if the verification is successful.
        """
        totp = TOTP(secret_key)
        return totp.verify(code)

    def notify_expiry_background(self):
        """
        Runs in the background to periodically notify about password expiry. It continuously calls self.notify_expiry() in a loop, catching FileNotFoundError and sleeping for 86400 seconds (24 hours).
"""
        while True:
            try:
                self.notify_expiry()
            except FileNotFoundError:
                pass
            time.sleep(86400)

    def notify_expiry(self):
        """
        Checks the expiry status of passwords in the PASSFILE. If passwords are close to expiry (within 1-7 days), it prints a warning. If expiring within 1 day, it issues an alert. If expired, it indicates a mandatory update for accessibility. Handles FileNotFoundError gracefully.
"""
        try:
            with open(self.PASSFILE, 'r') as file:
                data = json.load(file)

            for entry in data:
                if 'expiry_at' in entry and entry['expiry_at']:
                    expiry_date = datetime.strptime(entry['expiry_at'], "%Y-%m-%d %H:%M:%S")
                    time_left = expiry_date - datetime.now()

                    if timedelta(days=1) <= time_left <= timedelta(days=7):
                        days_left = time_left.days
                        hours, remainder = divmod(time_left.seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        print(colored(f"[!] Warning: Some of your passwords will expire in {days_left} days, {hours} hours, {minutes} minutes, and {seconds} seconds. Please update them!", 'yellow'))

                    elif time_left < timedelta(days=1) and time_left >= timedelta(seconds=0):
                        print(colored(f"[!] Alert: Some of your passwords will expired in any minute! Please update them!", 'red'))
                    elif time_left <= timedelta(seconds=0):
                        print(colored(f"[!] Alert: Some of your passwords has expired. Update is now mandatory for accessibility!", 'red'))
        
        except FileNotFoundError:
            pass

    def notify_pin_expiry_background(self):
        """
        Same as the notify_expiry_background() function but for PIN.
        """
        while True:
            try:
                self.notify_pin_expiry()
            except FileNotFoundError:
                pass
            time.sleep(86400)

    def notify_pin_expiry(self):
        """
        Same as the notify_expiry() function but for PIN again.
        """
        try:
            with open(self.CARD_PIN_FILE, 'r') as file:
                data = json.load(file)

            for entry in data:
                if 'expiry_at' in entry and entry['expiry_at']:
                    expiry_date = datetime.strptime(entry['expiry_at'], "%Y-%m-%d %H:%M:%S")
                    time_left = expiry_date - datetime.now()

                    if timedelta(days=1) <= time_left <= timedelta(days=7):
                        days_left = time_left.days
                        hours, remainder = divmod(time_left.seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        print(colored(f"[!] Warning: Some of your PINs will expire in {days_left} days, {hours} hours, {minutes} minutes, and {seconds} seconds. Please update them!", 'yellow'))

                    elif time_left < timedelta(days=1) and time_left >= timedelta(seconds=0):
                        print(colored(f"[!] Alert: Some of your PINs will expire in any minute! Please update them!", 'red'))
                    elif time_left <= timedelta(seconds=0):
                        print(colored(f"[!] Alert: Some of your PINs has expired. Update is now mandatory for accessibility!", 'red'))

        except FileNotFoundError:
            pass

    def load_encryption_key(self, encryption_key):
        self.cipher = self.initialize_cipher(encryption_key)

    def initialize_cipher(self, key):
        return Fernet(key)

    def check_master_password_strength(self, password):
        """
        Checks the strength of the provided master password against MIRA's password policy. If the password doesn't meet the criteria, it prompts the user for generating a strong password or aborts the process.
        """
        policy = PasswordPolicy.from_names(
            length=20,
            uppercase=3,
            numbers=3,
            special=4,
            nonletters=4,
        )
        result = policy.test(password)
        if result:
            print(colored("[-] Master password is not strong enough (Not Added). Please follow our password policy for master password:", "red"))
            for violation in result:
                print(colored(f"    {violation}", "red"))   
            generate_strong_pass = input(colored("[*] Do you want Mira to generate a strong password for you? (y/N): ", "yellow"))
            if generate_strong_pass == 'y':
                self.generate_password()
                print(colored("[*] Now repeat the process and use that password instead.", "magenta"))
            else:
                print(colored("[-] Abort.", "red"))
            return False
        return True

    def check_password_strength(self, password):
        """
        Same as the check_master_password_strength() function but for PINs.
        """
        policy = PasswordPolicy.from_names(
            length=10,
            uppercase=1,
            numbers=1,
            special=3,
        )
        result = policy.test(password)
        
        if result:
            print(colored("[-] Password is not strong enough:", "red"))
            for violation in result:
                print(colored(f"    {violation}", "red"))

            user_choice = input(colored("[*] Do you want to use this password anyway? (y/N): ", "yellow"))

            if user_choice.lower() == 'y':
                return True
            else:
                generate_strong_pass = input(colored("[*] Do you want Mira to generate a strong password for you? (y/N): ", "yellow"))
                if generate_strong_pass.lower() == 'y':
                    self.generate_password()
                    print(colored("[*] Now repeat the process and use that password instead.", "magenta"))
                else:
                    print(colored("[-] Abort.", "red"))
                return False
        return True
    
    def register(self, username, master_password):
        """
        Handles user registration by checking master password strength, creating a new user with encrypted data, and saving security information. Prompts for additional security details and prints registration completion with encryption key.
        Hashing Algorithm used:
        - Argon2
        """
        if not self.check_master_password_strength(master_password):
            return

        if os.path.exists(self.USER_DATA_FILE) and os.path.getsize(self.USER_DATA_FILE) != 0:
            print(colored("[-] Master user already exists!!", "red"))
        else:
            self.master_password = master_password
            salt = token_bytes(100)
            salt_hex = salt.hex()
            hashed_master_password = self.ph.hash(master_password + salt_hex)
            encryption_key = Fernet.generate_key()

            ph = argon2.PasswordHasher()
            hashed_encryption_key = ph.hash(encryption_key.decode())

            user_data = {
                'username': username,
                'salt': salt_hex,
                'master_password': hashed_master_password,
                'encryption_key': hashed_encryption_key
            }
            with open(self.USER_DATA_FILE, 'w') as file:
                json.dump(user_data, file)
            print(colored("[**] For authentication just in case you forgot your master password", "magenta"))
            school = getpass.getpass(colored("[*] School where you finish high-school: ", "yellow"))
            kiss_date = getpass.getpass(colored("[*] Date of first kiss: ", "yellow"))
            fear = getpass.getpass(colored("[*] One thing that you're afraid of:  ", "yellow"))
            hashed_school = ph.hash(school)
            hashed_kiss_date = ph.hash(kiss_date)
            hashed_fear = ph.hash(fear)
            security_data = {
                'scl': hashed_school,
                'kss': hashed_kiss_date,
                'fr': hashed_fear
            }
            with open(self.SECFILE, 'w') as security_file:
                json.dump(security_data, security_file)
                clear_terminal()
                print(colored(wolf, "blue"))
                print(colored("\n[+] Registration complete!!", "green"))
                print(colored(f"[+] Encryption key: {encryption_key.decode()}", "green"))
                print(colored("\n[*] Caution: Save your encryption key and store it somewhere safe Mira will never recover your encryption key once you forgot it!!! So please don't be stupid:)", "yellow"))

    def forgot_master_password(self, username):
        """
        Facilitates the process of resetting a forgotten master password. Verifies the user by asking security questions and allows the setting of a new master password.
        """
        if not os.path.exists(self.USER_DATA_FILE):
            print(colored("[-] Please register first.", "red"))
            return

        with open(self.USER_DATA_FILE, 'r') as file:
            user_data = json.load(file)

        if username != user_data.get('username'):
            print(colored("[-] Incorrect username! QUITTING!", "red"))
            return

        if not os.path.exists(self.SECFILE):
            print(colored("[-] Security questions not set for this user. Cannot reset master password.", "red"))
            return

        with open(self.SECFILE, 'r') as security_file:
            security_data = json.load(security_file)

        entered_school = getpass.getpass(colored("[*] School where you finish High-School: ", "yellow"))
        entered_kiss_date = getpass.getpass(colored("[*] Date of First Kiss: ", "yellow"))
        entered_fear = getpass.getpass(colored("[*] One thing that you're afraid of: ", "yellow"))

        ph = argon2.PasswordHasher()
        try:
            ph.verify(security_data['scl'], entered_school)
            ph.verify(security_data['kss'], entered_kiss_date)
            ph.verify(security_data['fr'], entered_fear)
        except argon2.exceptions.VerifyMismatchError:
            print(colored("[-] Incorrect answers to security questions. Resetting master password failed.", "red"))
            return

        new_master_password = getpass.getpass(colored("[*] Enter your new master password: ", "yellow"))
        re_enter = getpass.getpass(colored("[*] Re-Enter your new master password: ", "yellow"))

        if not self.check_master_password_strength(new_master_password):
            return

        if new_master_password != re_enter:
            print(colored("[-] New Master Passwords Did Not Match! Resetting master password failed.", "red"))
            return

        with open(self.USER_DATA_FILE, 'r') as file:
            user_data = json.load(file)

        salt = token_bytes(30)
        hashed_new_master_password = self.ph.hash(new_master_password + salt.hex())
        user_data['master_password'] = hashed_new_master_password
        user_data['salt'] = salt.hex()

        with open(self.USER_DATA_FILE, 'w') as file:
            json.dump(user_data, file)

        print(colored("[+] Master password reset successful!", "green"))

    def login(self, username, entered_password, encryption_key):
        """
        Handles user login by verifying entered credentials against stored data. Uses Argon2 hashing for master password and encryption key verification. Checks for account lockout and 2FA if enabled. Prints success and proceeds to the main menu upon successful login.
        """
        if not os.path.exists(self.USER_DATA_FILE):
            print(colored("\n[-] You have not registered. Do that first!", "red"))
        else:
            with open(self.USER_DATA_FILE, 'r') as file:
                user_data = json.load(file)

            if self.lockout_time and time.time() < self.lockout_time:
                clear_terminal()
                print(colored(blehhh, "red"))
                print(colored(f"[-] Account locked. WE ALREADY TOLD YOU THAT WE DON'T ACCEPT SHITTY BUGS HERE! If you are the real user, try again after {int(self.lockout_time - time.time())} seconds.", "red"))
                exit()
                return

            try:
                self.ph.verify(user_data['master_password'], entered_password + user_data['salt'])
            except VerifyMismatchError:
                print(colored("[-] Invalid Login credentials!!", "red"))
                if self.increment_failed_attempts():
                    return  
                else:
                    return

            if username == user_data['username']:
                stored_encryption_key = user_data['encryption_key']

                ph = argon2.PasswordHasher()
                try:
                    ph.verify(stored_encryption_key, encryption_key)
                except argon2.exceptions.VerifyMismatchError:
                    print(colored("[-] Invalid encryption key. Login failed!", "red"))
                    if self.increment_failed_attempts():
                        return  
                    else:
                        return

                self.load_encryption_key(encryption_key.encode())

                if '2fa_enabled' in user_data and user_data['2fa_enabled']:
                    key = getpass.getpass(colored("[*] Secret Key: ", "yellow"))
                    try:
                        self.ph.verify(user_data['2fa_secret_key'], key)
                    except VerifyMismatchError:
                        print(colored("[-] Invalid Secret Key!!", "red"))
                        return
                    code = getpass.getpass(colored("[*] 6-Digit Code (2FA): ", "yellow"))
                    if not self.verify_2fa(key, code):
                        print(colored("[-] Invalid 2FA code. Login failed!", "red"))
                        if self.increment_failed_attempts():
                            return
                        else:
                            return

                print(colored("[+] Login Successful..", "green"))
                time.sleep(3)
                clear_terminal()
                print(colored(wolf, "blue"))
                self.master_password = entered_password
                self.main_menu()

            else:
                print(colored("[-] Invalid Login credentials!!", "red"))
                if self.increment_failed_attempts():
                    clear_terminal()
                    return  
                else:
                    return

    def show_api_key(self):
        """
        Displays API key information based on the specified platform or all platforms. Reads API key data from the API file, formats and prints the relevant information. Handles FileNotFoundError and prints an error message if no API keys are saved.
        """
        try:
            with open(self.API, 'r') as file:
                data = json.load(file)

            platform = input(colored("[*] Platform: ", "yellow")).lower()
            key_status = []

            for entry in data:
                if entry['platform'] == platform or platform.lower() == 'all':
                    added_at = datetime.strptime(entry['added_at'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

                    key_status.append({
                        'platform': entry['platform'],
                        'key_name': entry['key_name'],
                        'added_at': added_at
                    })

            if key_status:
                if platform == 'all' or not platform:
                    print(colored("[+] All Available API Keys:", "green"))
                    print(colored("\nPlatform".ljust(31) + "API Key Name".ljust(30) + "Added At", "cyan"))
                    print(colored("--------------------".ljust(30) + "--------------------".ljust(30) + "-------------------", "cyan"))
                    for user_status in key_status:
                        print(f"{colored(user_status['platform'].ljust(30), 'cyan')}{colored(user_status['key_name'].ljust(30), 'cyan')}{colored(user_status['added_at'].ljust(25), 'cyan')}")
                else:
                    print(colored(f"[+] Available API Keys for {platform}:", "green"))
                    print(colored("\nAPI Key Name".ljust(31) + "Added At", "cyan"))
                    print(colored("--------------------".ljust(30) + "-------------------", "cyan"))
                    for user_status in key_status:
                        print(f"{colored(user_status['key_name'].ljust(30), 'cyan')}{colored(user_status['added_at'].ljust(25), 'cyan')}")
            else:
                print(colored("[-] No matching entries found for the specified Platform.", "red"))

        except FileNotFoundError:
            print(colored("[-] No API Key saved. Show expiry status failed!", "red"))
    
    def show_pin_expiry_status(self):
        """
        Displays the expiry status of PINs based on the specified card type or all card types. Reads PIN data from the CARD_PIN_FILE, formats and prints the relevant information including expiry status and remaining time. Handles FileNotFoundError and prints an error message if no PINs are saved.
        """
        try:
            with open(self.CARD_PIN_FILE, 'r') as file:
                data = json.load(file)

            card_type = input(colored("[*] Card Type: ", "yellow")).lower()
            if card_type != 'debit' and card_type != 'credit' and card_type != 'all':
                print(colored("[-] Please specify if debit or credit.", "red"))
                return
            card_status = []

            for entry in data:
                if entry['card_type'] == card_type or card_type.lower() == 'all':
                    expiry_status, remaining_time = self.check_expiry_status(entry.get('expiry_at'))
                    added_at = datetime.strptime(entry['added_at'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                    expiry_at = datetime.strptime(entry['expiry_at'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

                    card_status.append({
                        'card_type': entry['card_type'],
                        'card_number': entry['card_number'],
                        'status': expiry_status,
                        'added_at': added_at,
                        'expiry_at': expiry_at,
                        'remaining_time': remaining_time
                    })

            if card_status:
                if card_type == 'all' or not card_type:
                    print(colored("[+] All Available Card Numbers:", "green"))
                    print(colored("\nCard Type".ljust(31) + "Card Number".ljust(30) + "Status".ljust(16) + "Added At".ljust(25) + "Expiry At".ljust(25) + "Remaining Time", "cyan"))
                    print(colored("--------------------".ljust(30) + "--------------------".ljust(30) + "----------".ljust(16) + "-------------------".ljust(25) + "-------------------".ljust(25) + "------------------------", "cyan"))
                    for user_status in card_status:
                        print(f"{colored(user_status['card_type'].ljust(30), 'cyan')}{colored(user_status['card_number'].ljust(30), 'cyan')}{user_status['status'].ljust(25)}{colored(user_status['added_at'].ljust(25), 'cyan')}{colored(user_status['expiry_at'].ljust(24), 'cyan')} {colored(user_status['remaining_time'].ljust(30), 'cyan')}")
                else:
                    print(colored(f"[+] Available Card Numbers for {card_type}:", "green"))
                    print(colored("\nCard Number".ljust(31) + "Status".ljust(24) + "Added At".ljust(25) + "Expiry At".ljust(25) + "Remaining Time", "cyan"))
                    print(colored("--------------------".ljust(30) + "----------".ljust(24) + "-------------------".ljust(25) + "-------------------".ljust(25) + "------------------------", "cyan"))
                    for user_status in card_status:
                        print(f"{colored(user_status['card_number'].ljust(30), 'cyan')}{user_status['status'].ljust(33)}{colored(user_status['added_at'].ljust(25), 'cyan')}{colored(user_status['expiry_at'].ljust(24), 'cyan')} {colored(user_status['remaining_time'].ljust(30), 'cyan')}")
            else:
                print(colored("[-] No matching entries found for the specified card type.", "red"))

        except FileNotFoundError:
            print(colored("[-] No PIN saved. Show expiry status failed!", "red"))

    def show_expiry_status(self):
        """
        Displays the expiry status of passwords based on the specified platform URL or all platforms. Reads password data from the PASSFILE, formats and prints the relevant information including expiry status and remaining time. Handles FileNotFoundError and prints an error message if no passwords are saved.
        """
        try:
            with open(self.PASSFILE, 'r') as file:
                data = json.load(file)

            platform_url = input(colored("[*] URL of the Platform: ", "yellow"))
            usernames_status = []

            for entry in data:
                if entry['website'] == platform_url or platform_url.lower() == 'all':
                    expiry_status, remaining_time = self.check_expiry_status(entry.get('expiry_at'))
                    added_at = datetime.strptime(entry['added_at'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                    expiry_at = datetime.strptime(entry['expiry_at'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

                    usernames_status.append({
                        'website': entry['website'],
                        'username': entry['username'],
                        'status': expiry_status,
                        'added_at': added_at,
                        'expiry_at': f"{expiry_at}",
                        'remaining_time': remaining_time
                    })

            if usernames_status:
                if platform_url == 'all' or not platform_url:
                    print(colored("[+] All Available Users:", "green"))
                    print(colored("\nPlatform".ljust(31) + "Username".ljust(30) + "Status".ljust(16) + "Added At".ljust(25) + "Expiry At".ljust(25) + "Remaining Time", "cyan"))
                    print(colored("--------------------".ljust(30) + "--------------------".ljust(30) + "----------".ljust(16) + "-------------------".ljust(25) + "-------------------".ljust(25) + "------------------------", "cyan"))
                    for user_status in usernames_status:
                        print(f"{colored(user_status['website'].ljust(30), 'cyan')}{colored(user_status['username'].ljust(30), 'cyan')}{user_status['status'].ljust(25)}{colored(user_status['added_at'].ljust(25), 'cyan')}{colored(user_status['expiry_at'].ljust(24), 'cyan')} {colored(user_status['remaining_time'].ljust(30), 'cyan')}")
                else:
                    print(colored(f"[+] Available Users for {platform_url}:", "green"))
                    print(colored("\nUsername".ljust(31) + "Status".ljust(24) + "Added At".ljust(25) + "Expiry At".ljust(25) + "Remaining Time", "cyan"))
                    print(colored("--------------------".ljust(30) + "----------".ljust(24) + "-------------------".ljust(25) + "-------------------".ljust(25) + "------------------------", "cyan"))
                    for user_status in usernames_status:
                        print(f"{colored(user_status['username'].ljust(30), 'cyan')}{user_status['status'].ljust(33)}{colored(user_status['added_at'].ljust(25), 'cyan')}{colored(user_status['expiry_at'].ljust(24), 'cyan')} {colored(user_status['remaining_time'].ljust(30), 'cyan')}")
            else:
                print(colored("[-] No matching entries found for the specified platform.", "red"))

        except FileNotFoundError:
            print(colored("[-] No passwords saved. Show expiry status failed!", "red"))

    def check_expiry_status(self, expiry_date):
        """
        Checks the expiry status of a given expiry date. Returns a tuple with the expiry status (colored) and the remaining time as a string. Handles different cases like nearly expired, about to expire, expired, and normal expiration scenarios.
        """
        if expiry_date:
            expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d %H:%M:%S")
            time_left = expiry_date - datetime.now()

            if timedelta(days=1) <= time_left <= timedelta(days=7):
                return colored("Nearly Expired", "yellow"), str(time_left)
            elif time_left < timedelta(days=1) and time_left >= timedelta(seconds=0):
                return colored("About to Expire", "magenta"), str(time_left)
            elif time_left <= timedelta(seconds=0):
                return colored("Expired", "red"), colored("0 days, 0 hours, 0 minutes, 0 seconds", "red")
            else:
                days_left = time_left.days
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                remaining_time = f"{days_left} days, {hours} hours, {minutes} minutes, {seconds} seconds"
                return colored("Updated", "green"), str(time_left)
        return "OK", "N/A"

    def main_menu(self):
        """
        Main menu of MIRA with a wide range of commands.
        """
        with open(self.USER_DATA_FILE, 'r') as file:
            user_data = json.load(file)
        while True:
            choice = input(colored(f"{user_data.get('username')}@MIRA ~> ", "blue"))

            if choice == "":
                continue

            elif choice == 'add_platform_passwd':
                website = input(colored("[*] Platform: ", "yellow"))
                if not website.startswith('http://') and not website.startswith('https://'):
                    print(colored("[-] Provide a platform in URL form please.", "red"))
                    continue

                username = input(colored("[*] Username: ", "yellow"))
                password = getpass.getpass(colored("[*] Password: ", "yellow"))
                re_enter = getpass.getpass(colored("[*] Re-Enter Password: ", "yellow"))
                if re_enter != password:
                    print(colored("[-] Password did not match! QUITTING!", "red"))
                else:
                    self.add_password(website, username, password)
                    self.notify_expiry()
                    self.notify_pin_expiry()

            elif choice == 'get_platform_passwd':
                website = input(colored("[*] Platform: ", "yellow"))
                if not website.startswith('http://') and not website.startswith('https://'):
                    print(colored("[-] Provide a platform in URL form please.", "red"))
                    continue
                username = input(colored("[*] Username: ", "yellow"))
                decrypted_password = self.get_password(website, username)
                
                try:
                    with open(self.PASSFILE, 'r') as file:
                        data = json.load(file)

                    if website not in [entry['website'] for entry in data]:
                        print(colored("[-] This platform is not available on your vault.", "red"))
                        continue
                    elif username not in [entry['username'] for entry in data]:
                        print(colored("[-] This username doesn't exist for that platform.", "red"))
                        continue

                    for entry in data:
                        if entry['website'] == website and entry['username'] == username and 'expiry_at' in entry and entry['expiry_at']:
                            expiry_date = datetime.strptime(entry['expiry_at'], "%Y-%m-%d %H:%M:%S")
                            if datetime.now() > expiry_date:
                                response = input(colored("[*] Password has expired. Do you want to update the password or delete the website? (U/D): ", "yellow")).lower()
                                if response == 'u':
                                    new_password = getpass.getpass(colored("[*] New Password: ", "yellow"))
                                    re_enter = getpass.getpass(colored("[*] Re-Enter New Password: ", "yellow"))

                                    if any(self.decrypt_password(entry['password']) == new_password for entry in data):
                                        print(colored("[-] Password has been used, avoid reusing passwords. QUITTING!!", "red"))
                                        continue

                                    if re_enter != new_password:
                                        print(colored("[-] Password did not match! QUITTING!", "red"))
                                        continue


                                    if self.check_password_reuse(password, data):
                                        print(colored("[-] Password has been used to other platforms. (Password not added) Avoid using the same password on other platforms!!", "red"))
                                        continue
    
                                    if not self.check_password_strength(new_password):
                                        continue

                                    entry['password'] = self.encrypt_password(new_password)
                                    entry['expiry_at'] = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')

                                    with open(self.PASSFILE, 'w') as file:
                                        json.dump(data, file, indent=4)

                                    decrypted_password = self.decrypt_password(entry['password'])
                                    if decrypted_password:
                                        print(colored("[+] Key Content Update Successfully!", "green"))
                                    else:
                                        print(colored("[-] Password has expired. Please update your password.", "red"))
                                    return

                                elif response == 'd':
                                    caution = input(colored("[*] Caution: Once you remove it, it will be permanently deleted to your system. Are you sure you want to proceed? (y/N): ", "yellow"))
                                    if caution == 'n':
                                        print(colored("[-] Abort.", "red"))
                                        continue
                                    elif caution == 'y':
                                        data = [e for e in data if not (e['website'] == website and e['username'] == username)]
                                        with open(self.PASSFILE, 'w') as file:
                                            json.dump(data, file, indent=4)

                                        print(colored("[-] Website permanently deleted.", "red"))
                                    continue
                            else:
                                if decrypted_password is not None:
                                    print(colored(f"[+] Key Content: {decrypted_password}", "green"))
                                else:
                                    print(colored("[-] Password not found! Did you save the password?", "red"))

                except FileNotFoundError:
                    print(colored("[-] No passwords has been saved yet!", "red"))

            elif choice == 'chmast':
                self.change_master_password()
                self.notify_expiry()
                self.notify_pin_expiry()

            elif choice == 'genpasswd':
                self.generate_password()
                self.notify_expiry()
                self.notify_pin_expiry()

            elif choice == 'del_platform_passwd':
                self.delete_password()
                self.notify_expiry()
                self.notify_pin_expiry()

            elif choice == 'del_card_pin':
                self.delete_card_pin()
                self.notify_expiry()
                self.notify_pin_expiry()

            elif choice == 'del_api_key':
                self.delete_key()
                self.notify_expiry()
                self.notify_pin_expiry()

            elif choice == 'show_api_key':
                self.show_api_key()
                self.notify_expiry()
                self.notify_pin_expiry()

            elif choice == 'ch_platform_passwd':
                website = input(colored("[*] Platform: ", "yellow"))
                if not website.startswith('http://') and not website.startswith('https://'):
                    print(colored("[-] Provide a platform in URL form please.", "red"))
                    continue
                username = input(colored("[+] Username: ", "yellow"))
                self.change_password(website, username)
                self.notify_expiry()
                self.notify_pin_expiry()

            elif choice == 'ch_card_pin':
                card_type = input(colored("[*] Card Type: ", "yellow"))
                card_number = input(colored("[*] Card Number: ", "yellow"))
                self.change_pin(card_type, card_number)
                self.notify_expiry()
                self.notify_pin_expiry()

            elif choice == 'enable2fa':
                with open(self.USER_DATA_FILE, 'r') as file:
                    user_data = json.load(file)

                if user_data.get('2fa_enabled', False):
                    print(colored("[-] 2FA is already enabled for this user.", "red"))
                    continue

                verify = input(colored("[*] After this, you will need to provide the 6-digit code before you can successfully logged in to your vault. Are you sure you want to proceed? (y/N): ", "yellow"))
                if verify == 'y':
                    self.enable_2fa()
                    self.notify_expiry()
                    self.notify_pin_expiry()
                else:
                    print(colored("[-] Abort!", "red"))

            elif choice == 'show_passwd_exp':
                self.show_expiry_status()
                self.notify_expiry()
                self.notify_pin_expiry()

            elif choice == 'show_pin_exp':
                self.show_pin_expiry_status()
                self.notify_expiry()
                self.notify_pin_expiry()

            elif choice == 'reset':
                caution = input(colored("[*] Caution: After attempting to do reset, all of the data including your passwords and your master user in mira will be deleted permanently! Are you sure that you want to proceed? (y/N): ", "yellow"))
                if caution == 'y':
                    master_password = getpass.getpass(colored("Master Password: ", "yellow"))
                    with open(self.USER_DATA_FILE, 'r') as file:
                        user_data = json.load(file)

                    stored_master_password = user_data['master_password']
                    salt = user_data['salt']

                    try:
                        self.ph.verify(stored_master_password, master_password + salt)
                    except VerifyMismatchError:
                        print(colored("\n[-] Incorrect current master password. Reset procedure failed!", "red"))
                        continue

                    if os.path.exists(self.LOCKOUT_FILE):
                        os.remove(self.LOCKOUT_FILE)
                    else:
                        pass
                    if os.path.exists(self.PASSFILE):
                        os.remove(self.PASSFILE)
                    else:
                        pass
                    if os.path.exists(self.SECFILE):
                        os.remove(self.SECFILE)
                    else:
                        pass
                    if os.path.exists(self.CARD_PIN_FILE):
                        os.remove(self.CARD_PIN_FILE)
                    else:
                        pass
                    if os.path.exists(self.API):
                        os.remove(seld.API)
                    else:
                        pass
                    os.remove(self.USER_DATA_FILE)
                    print(colored("[+] All data has been successfully removed.", "green"))
                    start_again = input(colored("[*] Do you want to start a new account? (y/N): ", "yellow"))
                    if start_again == 'y':
                        username = input(colored("[*] New Username: ", "yellow"))
                        master_password = getpass.getpass(colored("[*] New Master Password: ", "yellow"))
                        re_enter = getpass.getpass(colored("[*] Re-enter Master Password: ", "yellow"))
                        if re_enter != master_password:
                            print(colored("[-] Master Password Did Not Match! QUITTING!", "red"))
                        else:
                            if not self.check_master_password_strength(master_password):
                                return
                            password_manager.register(username, master_password)
                            break
                    else:
                        print(colored("[-] Abort.", "red"))
                else:
                    print(colored("[-] Abort.", "red"))

            elif choice == 'add_api_key':
                platform = input(colored("[*] Platform: ", "yellow"))
                if not platform.startswith('http://') and not platform.startswith('https://'):
                    print(colored("[-] Provide a platform in URL form please.", "red"))
                    continue
                key_name = input(colored("[*] API Key Name: ", "yellow"))
                if not key_name:
                    print(colored("[-] No key name provided! QUITTING!", "red"))
                    continue
                key = getpass.getpass(colored("[*] API Key: ", "yellow"))
                if not key:
                    print(colored("[-] No key provided! QUITTING!", "red"))
                    continue
                self.add_key(platform, key_name, key)
                self.notify_expiry()
                self.notify_pin_expiry()

            elif choice == 'add_card_pin':
                card_type = input(colored("[*] Card Type: ", "yellow")).lower()
                if card_type != 'debit' and card_type != 'credit':
                    print(colored("[-] Please specify if Debit or Credit.", "red"))
                    continue
                try:
                    card_number = input(colored("[*] Card Number: ", "yellow"))
                    if not card_number:
                        print(colored("[-] No card number provided! QUITTING!", "red"))
                        continue
                    if card_number.isdigit() and len(card_number) == 16:
                        pin = getpass.getpass(colored("[*] Card PIN: ", "yellow"))
                        if not pin:
                            print(colored("[-] No PIN provided! QUITTING!", "red"))
                            continue
                        digits = [char for char in pin if char.isdigit()]
                        num_digits = len(digits)

                        if pin.isdigit() and len(pin) in (4, 6):
                            re_enter = getpass.getpass(colored("[*] Re-Enter Card PIN: ", "yellow"))
                            if not re_enter:
                                print(colored("[-] Re-Enter your PIN! QUITTING!", "red"))
                                continue
                            if re_enter != pin:
                                print(colored("[-] PIN did not match. QUITTING!", "red"))
                                continue
                            self.add_card_pin(card_type, card_number, pin)
                            self.notify_expiry()
                            self.notify_pin_expiry()
                        else:
                            print(colored(f"[-] Typical PIN length ranges from 4 to 6, the length of the PIN that you've has {num_digits} digits.", "red"))
                    else:
                        print(colored("[-] Invalid Account Number! Account Numbers should be 16-digits", "red"))
                except ValueError:
                    print(colored("[-] No Account Number provided.", "red"))
                    continue

            elif choice == 'get_api_key':
                platform= input(colored("[*] Platform: ", "yellow"))
                key_name = input(colored("[*] API Key Name: ", "yellow"))

                decrypted_key = self.get_key(platform, key_name)

                if decrypted_key is not None:
                    print(colored(f"[+] API Key: {decrypted_key}", "green"))
                else:
                    print(colored("[-] API Key not found!", "red"))

            elif choice == 'get_card_pin':
                card_type = input(colored("[*] Card Type: ", "yellow")).lower()
                card_number = input(colored("[*] Card Number: ", "yellow"))
                if card_type != 'debit' and card_type != 'credit':
                    print(colored("[-] Please specify if Debit or Credit.", "red"))
                    continue

                decrypted_pin = self.get_card_pin(card_type, card_number)

                try:
                    with open(self.CARD_PIN_FILE, 'r') as file:
                        data = json.load(file)

                    if card_type not in [entry['card_type'] for entry in data]:
                        print(colored("[-] This card type is not available in your vault.", "red"))
                    elif card_number not in [entry['card_number'] for entry in data]:
                        print(colored("[-] This card number doesn't exist for that card type.", "red"))
                    else:
                        for entry in data:
                            if entry['card_type'] == card_type and entry['card_number'] == card_number:
                                expiry_date = datetime.strptime(entry['expiry_at'], "%Y-%m-%d %H:%M:%S") if 'expiry_at' in entry else None

                                if expiry_date and datetime.now() > expiry_date:
                                    response = input(colored("[*] Card PIN has expired. Do you want to update the PIN or delete the card details? (u/d): ", "yellow")).lower()
                                    if response == 'u':
                                        new_pin = getpass.getpass(colored("[*] New Card PIN: ", "yellow"))
                                        re_enter = getpass.getpass(colored("[*] Re-Enter New Card PIN: ", "yellow"))

                                        if re_enter != new_pin:
                                            print(colored("[-] PIN did not match. QUITTING!", "red"))
                                            continue

                                        if any(self.decrypt_information(entry['pin']) == new_pin for entry in data):
                                            print(colored("[-] Card PIN has been used, avoid reusing PINs. QUITTING!!", "red"))
                                            continue

                                        entry['pin'] = self.encrypt_information(new_pin)
                                        entry['expiry_at'] = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d %H:%M:%S')

                                        with open(self.CARD_PIN_FILE, 'w') as file:
                                            json.dump(data, file, indent=4)

                                        decrypted_pin = self.decrypt_information(entry['pin'])
                                        if decrypted_pin:
                                            print(colored("[+] Card PIN Update Successfully!", "green"))
                                        else:
                                            print(colored("[-] Card PIN update failed.", "red"))
                                        continue

                                    elif response == 'd':
                                        caution = input(colored("[*] Caution: Once you remove it, it will be permanently deleted from your system. Are you sure you want to proceed? (y/N): ", "yellow"))
                                        if caution == 'n':
                                            print(colored("[-] Abort.", "red"))
                                            continue
                                        elif caution == 'y':
                                            data = [e for e in data if not (e['card_type'] == card_type and e['card_number'] == card_number)]
                                            with open(self.CARD_PIN_FILE, 'w') as file:
                                                json.dump(data, file, indent=4)

                                            print(colored("[-] Card details permanently deleted.", "red"))
                                        continue

                                else:
                                    if decrypted_pin is not None:
                                        print(colored(f"[+] Card PIN: {decrypted_pin}", "green"))
                                    else:
                                        print(colored("[-] Card PIN not found! Did you save the Card PIN?", "red"))

                except FileNotFoundError:
                    print(colored("[-] No card details have been saved yet!", "red"))

            elif choice == 'ch_api_key':
                platform = input(colored("[*] Platform: ", "yellow"))
                key_name = input(colored("[*] API Key Name: ", "yellow"))
                self.change_key(platform, key_name)

            elif choice == 'lout':
                self.logout()
                break

            elif choice == 'h' or choice == 'help':
                print(colored("""[**] Available Commands:
'add_platform_passwd' - Add a new password for the desired platform
'add_api_key' - Add new API Key
'add_card_pin' - Add a new PIN for the desired card number
'get_platform_passwd' - Display the plaintext version of the password for the desired platform
'get_api_key' - Display the plaintext version of the key
'get_card_pin' - Display the plaintext version of the PIN for the desired card number
'del_platform_passwd' - Delete a saved password according to your desired Platform
'del_api_key' - Delete key according to your desired Username and Key Name
'del_card_pin' - Delete a saved PIN according to your desired Card Number
'ch_platform_pass' - Change the password for the desired platform
'ch_card_pin' - Change the password for the desired platform
'ch_api_key' - Change the API Key for the desired platform and API Key name
'enable2fa' - Enable Two-Factor Authentication for added security
'genpasswd' - Generate a strong password
'changemaster' - Change the masterkey
'show_passwd_exp' - List all usernames and their status on a specific platform or all
'show_pin_exp' - List all card numbers and their status on a specific card type or all
'show_api_key' - List all API Key name and their date when they were added (No Expiry when it comes to API Keys)
'lout' - Logout
'exit' - Terminate MIRA
'reset' - Delete all data, including the user account permanently (Be cautious with this command! It can result in permanent data loss!)

[**] Security Recommendations: 
Regularly check for password expiration using 'showexp' command.
Keep your master password and encryption key secure.
Enable Two-Factor Authentication for an additional layer of security.

[**] Note: Master Password strength policy requires at least 20 characters with uppercase, numbers, and special characters. (Mandatory).
[**] Note: Password strength policy for platforms requires at least 10 characters with uppercase, numbers, and special characters also. (Optional, but we recommend you to follow our password policy.) """, "cyan"))

            elif choice == 'exit':
                print(colored("[*] MIRA Terminated!", "red"))
                exit()

            elif choice == 'clear':
                self.clear_terminal()

            else:
                print(colored("[-] Invalid Option", "red"))

    def check_username_reuse(self, new_website, new_username, existing_data):
        """
        Checks if a new website and username combination already exists in the existing data. Returns True if the combination is found, indicating reuse, otherwise returns False.
        """
        for entry in existing_data:
            existing_website = entry['website']
            existing_username = entry['username']
            if existing_website == new_website and existing_username == new_username:
                return True
        return False

    def check_password_reuse(self, new_password, existing_data):
        """
        Checks if a new password already exists in the existing data. Returns True if the password is found, indicating reuse, otherwise returns False.
        """
        for entry in existing_data:
            decrypted_password = self.decrypt_password(entry['password'])
            if decrypted_password == new_password:
                return True
        return False

    def add_password(self, website, username, password):
        """
        Adds a new password entry for a given website and username. Checks for valid URL form and whether the username or password has been used before. Encrypts the password, checks its strength, and saves the new entry to the PASSFILE.
        """
        if not website.startswith('http://') and not website.startswith('https://'):
            print(colored("[-] Provide a platform in URL form please.", "red"))
            return

        if not os.path.exists(self.PASSFILE):
            data = []
        else:
            try:
                with open(self.PASSFILE, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = []
            except FileNotFoundError:
                pass

        if self.check_username_reuse(website, username, data):
            print(colored(f"[-] The username {username} already exists for this platform!", "red"))
            return

        if self.check_password_reuse(password, data):
            print(colored("[-] Password has been used to other platforms. (Password not added) Avoid using the same password on other platforms!!", "red"))
            return

        salt = token_bytes(16)
        if self.check_password_strength(password):
            encrypted_password = self.encrypt_password(password)
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            password_entry = {
                'website': website,
                'username': username,
                'password': encrypted_password,
                'added_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'expiry_at': (datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')

            }
            data.append(password_entry)
            with open(self.PASSFILE, 'w') as file:
                json.dump(data, file, indent=4)
            print(colored("[+] Password added!", "green"))
        else:
            print(colored("[-] Password not added. Please choose a stronger password.", "red"))

    def get_password(self, website, username):
        """
        Retrieves the decrypted password for a given website and username. Checks for the existence of the PASSFILE, loads data, and decrypts the password if the entry matches.Handles JSONDecodeError and expiry date verification. Returns the decrypted password or None if not found or expired.
        """
        if not os.path.exists(self.PASSFILE):
            return None

        try:
            with open(self.PASSFILE, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []

        for entry in data:
            if entry['website'] == website and entry['username'] == username:
                if 'expiry_at' in entry and entry['expiry_at']:
                    expiry_date = datetime.strptime(entry['expiry_at'], "%Y-%m-%d %H:%M:%S")
                    if datetime.now() > expiry_date:
                        return None

                decrypted_password = self.decrypt_password(entry['password'])
                return decrypted_password

        return None

    def delete_password(self):
        """
        Allows the user to delete a password entry for a given platform (website) and username. Prompts for platform URL, username, and current master password for verification. Verifies the master password, loads data from PASSFILE, deletes the matching entry, and updates the file. Handles incorrect master password, non-existent passwords, and deletion failure scenarios.
        """
        website = input(colored("[*] Platform: ", "yellow"))
        if not website.startswith('http://') and not website.startswith('https://'):
            print(colored("[-] Provide a platform in URL form please.", "red"))
            return
        username = input(colored("[*] Username: ", "yellow"))
        master_pass = getpass.getpass(colored("[*] Master Password: ", "yellow"))

        if not os.path.exists(self.PASSFILE):
            print(colored("[-] No passwords saved. Deletion failed!", "red"))
            return

        with open(self.USER_DATA_FILE, 'r') as file:
            user_data = json.load(file)

        stored_master_password = user_data['master_password']
        salt = user_data['salt']

        try:
            self.ph.verify(stored_master_password, master_pass + salt)
        except VerifyMismatchError:
            print(colored("[-] Incorrect current master password. Delete password failed!", "red"))
            return

        try:
            with open(self.PASSFILE, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []

        for entry in data:
            if entry['website'] == website and entry['username'] == username:
                data.remove(entry)
                with open(self.PASSFILE, 'w') as file:
                    json.dump(data, file, indent=4)
                print(colored("[+] Password deleted successfully!", "green"))
                return

        print(colored("[-] Password not found! Deletion failed!", "red"))

    def change_password(self, website, username):
        """
        Allows the user to change the password for a given platform (website) and username. It prompts for the current password, verifies it, and then prompts for a new password. It encrypts and updates the password entry in the PASSFILE. Handles scenarios like incorrect current password, non-existent passwords, and password strength requirements.
        """
        data = []

        if not os.path.exists(self.PASSFILE):
            print(colored("[-] No passwords saved!", "red"))
            return

        try:
            with open(self.PASSFILE, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            pass  

            
        current_password = getpass.getpass(colored("[*] Current password for the given platform and username: ", "yellow"))

        decrypted_password = self.get_password(website, username)
    
        if decrypted_password is not None and current_password == decrypted_password:
            new_password = getpass.getpass(colored("[*] New Password: ", "yellow"))
            re_enter = getpass.getpass(colored("[*] Re-Enter New Password: ", "yellow"))

            if not self.check_password_strength(new_password):
                return

            if new_password != re_enter:
                print(colored("[-] New Passwords Did Not Match! Change password failed!", "red"))
                return

            encrypted_new_password = self.encrypt_password(new_password)

            if any(self.decrypt_password(entry['password']) == new_password for entry in data):
                print(colored("[-] Password has been used. (Change password failed) Avoid reusing passwords!", "red"))
                return

            try:
                with open(self.PASSFILE, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = []

            for entry in data:
                if entry['website'] == website and entry['username'] == username:
                    entry['password'] = encrypted_new_password
                    entry['expiry_at'] = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')

                    with open(self.PASSFILE, 'w') as file:
                        json.dump(data, file, indent=4)

                    decrypted_password = self.decrypt_password(entry['password'])
                    if decrypted_password:
                        print(colored("[+] Password updated successfully!", "green"))
                        print(colored(f"[+] Updated Password: {decrypted_password}", "green"))
                    else:
                        print(colored("[-] Password update failed.", "red"))
                    return

        elif website not in [entry['website'] for entry in data]:
            print(colored("[-] This platform is not available on your vault.", "red"))
        elif username not in [entry['username'] for entry in data]:
            print(colored("[-] This username doesn't exist for that platform.", "red"))
        else:
            print(colored("[-] Incorrect current password. Change password failed!", "red"))

    def encrypt_password(self, password):
        """
        It takes a password, encodes it, encrypts it using the cipher, and returns the encrypted password as a string.
        """
        return self.cipher.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        """
        It takes a cipher version of the password, encodes it, decrypts it, and returns the decrypted password as a string.
        """
        return self.cipher.decrypt(encrypted_password.encode()).decode()

    def change_master_password(self):
        """
        Prompts the user for the current master password, verifies it, and then allows the user to set a new master password.
        """
        current_password = getpass.getpass(colored("[*] Current Master Password: ", "yellow"))
        with open(self.USER_DATA_FILE, 'r') as file:
            user_data = json.load(file)

        stored_master_password = user_data['master_password']
        salt = user_data['salt']

        try:
            self.ph.verify(stored_master_password, current_password + salt)
        except VerifyMismatchError:
            print(colored("[-] Incorrect current master password. Change password failed!", "red"))
            return

        new_password = getpass.getpass(colored("[*] New Master Password: ", "yellow"))
        re_enter = getpass.getpass(colored("[*] Re-Enter Master Password: ", "yellow"))

        if not self.check_master_password_strength(new_password):
            return

        if new_password != re_enter:
            print(colored("[-] New Master Passwords Did Not Match! Change password failed!", "red"))
            return

        hashed_new_password = self.ph.hash(new_password + salt)
        user_data['master_password'] = hashed_new_password

        with open(self.USER_DATA_FILE, 'w') as file:
            json.dump(user_data, file)

        self.master_password = new_password
        print(colored("[+] Master password changed successfully!", "green"))
        print(colored(f"[+] New Master Password: {re_enter}", "green"))

    def check_keyname_reuse(self, new_platform, new_key_name, existing_data):
        """
        Checks if a new API key's platform and key name combo is already in use in existing_data.
        """
        for entry in existing_data:
            existing_platform = entry['platform']
            existing_key_name = entry['key_name']
            if existing_platform == new_platform and existing_key_name == new_key_name:
                return True
        return False

    def check_key_reuse(self, new_key, existing_data):
        """
        Checks if a new API key is already in use in existing_data.
        """
        for entry in existing_data:
            decrypted_key = self.decrypt_information(entry['key'])
            if decrypted_key == new_key:
                return True
        return False

    def add_key(self, platform, key_name, key):
        """
        Adds a new API key entry with the specified platform, key name, and key to the API file.
        """
        if not os.path.exists(self.API):
            data = []
        else:
            try:
                with open(self.API, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = []
            except FileNotFoundError:
                pass

        if self.check_keyname_reuse(platform, key_name, data):
            print(colored(f"[-] The key name {key_name} already exists for this Platform!", "red"))
            return

        if self.check_key_reuse(key, data):
            print(colored("[-] API Key has been used to other Key Name. (API Key not added) Avoid using the same API on other Key Name!!", "red"))
            return

        api_key_entry = {
            'platform': platform,
            'key_name': key_name,
            'key': self.encrypt_information(key),
            'added_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        data.append(api_key_entry)
        with open(self.API, 'w') as file:
            json.dump(data, file, indent=4)

        print(colored("[+] API Key added!", "green"))

    def check_cardnumber_reuse(self, new_card_type, new_card_number, existing_data):
        """
        Checks if the new card type and number combo already exists in the existing data.
        """
        for entry in existing_data:
            existing_card_type = entry['card_type']
            existing_card_number = entry['card_number']
            if existing_card_type == new_card_type and existing_card_number == new_card_number:
                return True
        return False

    def check_pin_reuse(self, new_pin, existing_data):
        """
        Checks if the new PIN is used in other entries.
        """ 
        for entry in existing_data:
            decrypted_pin = self.decrypt_information(entry['pin'])
            if decrypted_pin == new_pin:
                return True
        return False

    def add_card_pin(self, card_type, card_number, pin):
        if not os.path.exists(self.CARD_PIN_FILE):
            data = []
        else:
            try:
                with open(self.CARD_PIN_FILE, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = []
            except FileNotFoundError:
                pass

        if self.check_cardnumber_reuse(card_type, card_number, data):
            print(colored(f"[-] The card number {card_number} already exists for this card type!", "red"))
            return

        if self.check_pin_reuse(pin, data):
            print(colored("[-] PIN has been used to other card number. (PIN not added) Avoid using the same PIN on other card numbers!!", "red"))
            return

        card_pin_entry = {
            'card_type': card_type,
            'card_number': card_number,
            'pin': self.encrypt_information(pin),
            'added_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'expiry_at': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d %H:%M:%S')
        }

        data.append(card_pin_entry)
        with open(self.CARD_PIN_FILE, 'w') as file:
            json.dump(data, file, indent=4)

        print(colored("[+] Card PIN added!", "green"))

    def get_key(self, platform, key_name):
        if not os.path.exists(self.API):
            return None

        try:
            with open(self.API, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            return None

        for entry in data:
            if entry['platform'] == platform and entry['key_name'] == key_name:
                decrypted_key = self.decrypt_information(entry['key'])
                return decrypted_key

        return None

    def get_card_pin(self, card_type, card_number):
        if not os.path.exists(self.CARD_PIN_FILE):
            return None

        try:
            with open(self.CARD_PIN_FILE, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            return None

        for entry in data:
            if entry['card_type'] == card_type and entry['card_number'] == card_number:
                decrypted_pin = self.decrypt_information(entry['pin'])
                return decrypted_pin

        return None

    def delete_card_pin(self):
        card_type = input(colored("[*] Card Type: ", "yellow")).lower()
        if card_type != 'debit' and card_type != 'credit':
            print(colored("[-] Please specify if Debit or Credit.", "red"))
            return
        card_number = input(colored("[*] Card Number: ", "yellow"))
        master_pass = getpass.getpass(colored("[*] Master Password: ", "yellow"))

        if not os.path.exists(self.CARD_PIN_FILE):
            print(colored("[-] No PIN saved. Deletion failed!", "red"))
            return

        with open(self.USER_DATA_FILE, 'r') as file:
            user_data = json.load(file)

        stored_master_password = user_data['master_password']
        salt = user_data['salt']

        try:
            self.ph.verify(stored_master_password, master_pass + salt)
        except VerifyMismatchError:
            print(colored("[-] Incorrect current master password. Deletion failed!", "red"))
            return

        try:
            with open(self.CARD_PIN_FILE, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []

        for entry in data:
            if entry['card_type'] == card_type and entry['card_number'] == card_number:
                data.remove(entry)
                with open(self.CARD_PIN_FILE, 'w') as file:
                    json.dump(data, file, indent=4)
                print(colored("[+] Card PIN deleted successfully!", "green"))
                return

        print(colored("[-] PIN not found! Deletion failed!", "red"))

    def delete_key(self):
        platform = input(colored("[*] Platform: ", "yellow"))
        key_name = input(colored("[*] Key Name: ", "yellow"))
        master_pass = getpass.getpass(colored("[*] Master Password: ", "yellow"))

        if not os.path.exists(self.API):
            print(colored("[-] No API Keys saved. Deletion failed", "red"))
            return

        with open(self.USER_DATA_FILE, 'r') as file:
            user_data = json.load(file)

        stored_master_password = user_data['master_password']
        salt = user_data['salt']

        try:
            self.ph.verify(stored_master_password, master_pass + salt)
        except VerifyMismatchError:
            print(colored("[-] Incorrect current master password. Deletion failed!", "red"))
            return

        try:
            with open(self.API, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []

        for entry in data:
            if entry['platform'] == platform and entry['key_name'] == key_name:
                data.remove(entry)
                with open(self.API, 'w') as file:
                    json.dump(data, file, indent=4)
                print(colored("[+] API Key successfully deleted!", "green"))
                return

        print(colored("[-] API Key not found! Deletion failed!", "red"))

    def change_pin(self, card_type, card_number):
        data = []

        if not os.path.exists(self.CARD_PIN_FILE):
            print(colored("[-] No PIN saved!", "red"))
            return

        try:
            with open(self.CARD_PIN_FILE, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            pass


        current_pin = getpass.getpass(colored("[*] Current PIN for the given card number: ", "yellow"))

        decrypted_pin = self.get_card_pin(card_type, card_number)

        if decrypted_pin is not None and current_pin == decrypted_pin:
            try:
                new_pin = getpass.getpass(colored("[*] New PIN: ", "yellow"))
                digits = [char for char in new_pin if char.isdigit()]
                num_digits = len(digits)
                if new_pin.isdigit() and len(new_pin) not in (4, 6):
                    print(colored(f"[-] Typical length of PINs are ranges from 4 to 6 digits! The PIN you've entered has {num_digits} digits.", "red"))
                    return
                if not new_pin:
                    print(colored("[-] No PIN provided! Changing process failed.", "red"))
                    return
                new_pin_input = int(new_pin)
                re_enter = getpass.getpass(colored("[*] Re-Enter New PIN: ", "yellow"))
                if not re_enter:
                    print(colored("[-] Please Re-Enter your new PIN! QUITTING!", "red"))
                    return
                re_enter_input = int(re_enter)
            except ValueError:
                print(colored("[-] Please provide a PIN", "red"))
                return
                
            if new_pin_input != re_enter_input:
                print(colored("[-] New PINs Did Not Match! Change PIN failed!", "red"))
                return

            encrypted_new_pin = self.encrypt_information(new_pin)
        
            if any(self.decrypt_information(entry['pin']) == new_pin for entry in data):
                print(colored("[-] PIN has been used. (Change PIN failed) Avoid reusing PINs!", "red"))
                return

            try:
                with open(self.CARD_PIN_FILE, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = []

            for entry in data:
                if entry['card_type'] == card_type and entry['card_number'] == card_number:
                    entry['pin'] = encrypted_new_pin
                    entry['expiry_at'] = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d %H:%M:%S')

                    with open(self.CARD_PIN_FILE, 'w') as file:
                        json.dump(data, file, indent=4)

                    decrypted_pin = self.decrypt_information(entry['pin'])
                    if decrypted_pin:
                        print(colored("[+] PIN updated successfully!", "green"))
                    else:
                        print(colored("[-] PIN update failed.", "red"))
                    return

        elif card_type not in [entry['card_type'] for entry in data]:
            print(colored("[-] This card type is not available on your PIN vault.", "red"))
        elif card_number not in [entry['card_number'] for entry in data]:
            print(colored("[-] This card number doesn't exist for that card type.", "red"))
        else:
            print(colored("[-] Incorrect current PIN. Change PIN failed!", "red"))

    def change_key(self, platform, key_name):
        data = []

        if not os.path.exists(self.API):
            print(colored("[-] No KEYS saved!", "red"))
            return

        try:
            with open(self.API, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            pass


        current_key = getpass.getpass(colored("[*] Current API key for the given key name: ", "yellow"))

        decrypted_key = self.get_key(platform, key_name)

        if decrypted_key is not None and current_key == decrypted_key:
            new_key = getpass.getpass(colored("[*] New API Key: ", "yellow"))
            re_enter = getpass.getpass(colored("[*] Re-Enter New API Key: ", "yellow"))

            if new_key != re_enter:
                print(colored("[-] New API Key Did Not Match! Change Key failed!", "red"))
                return

            encrypted_new_key = self.encrypt_information(new_key)

            if any(self.decrypt_information(entry['key']) == new_key for entry in data):
                print(colored("[-] API Key has been used. (Change Key failed) Avoid reusing Keys!", "red"))
                return

            try:
                with open(self.API, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = []

            for entry in data:
                if entry['platform'] == platform and entry['key_name'] == key_name:
                    entry['key'] = encrypted_new_key

                    with open(self.API, 'w') as file:
                        json.dump(data, file, indent=4)

                    decrypted_key = self.decrypt_information(entry['key'])
                    if decrypted_key:
                        print(colored("[+] API Key updated successfully!", "green"))
                    else:
                        print(colored("[-] API Key update failed.", "red"))
                    return

        elif platform not in [entry['platform'] for entry in data]:
            print(colored("[-] This platform is not available on your API key vault.", "red"))
        elif key_name not in [entry['key_name'] for entry in data]:
            print(colored("[-] This key name doesn't exist for that plaltform.", "red"))
        else:
            print(colored("[-] Incorrect current API Key. Change Key failed!", "red"))

    def encrypt_information(self, information):
        return self.cipher.encrypt(information.encode()).decode()

    def decrypt_information(self, encrypted_information):
        return self.cipher.decrypt(encrypted_information.encode()).decode()

    def logout(self):
        self.master_password = None
        self.cipher = None
        print(colored("[+] Logged out!", "cyan"))

if __name__ == '__main__':
    if platform.system() == 'Linux':
        if not check_linux_privileges():
            print(colored("[-] Mira requires elevated privileges on Linux. QUITTING!", "red"))
            exit()
        else:
            try:
                clear_terminal()
                current_datetime_info = get_current_datetime()
                os_distribution_info = get_os_distribution()                                                                          
                print(colored(os_distribution_info, "blue"))
                time.sleep(2)
                print(colored(get_python_version(), "blue"))
                time.sleep(2)                                                                                                         
                print(colored(current_datetime_info, "blue"))                                                                         
                time.sleep(2)
                print(colored("[+] Starting Mira Password Manager.....", "blue"))
                password_manager = PasswordManager()
                time.sleep(20)
                if password_manager.lockout_time and time.time() < password_manager.lockout_time:                                         
                    clear_terminal()
                    print(colored(blehhh, "red"))
                    print(colored(f"[-] Account locked. WE'VE ALREADY TOLD YOU THAT WE DON'T ACCEPT SHITTY BUGS HERE! If you are the real user, try again after {int(password_manager.lockout_time - time.time())} seconds.", "red"))                           
                    exit()                                                                                                            
                clear_terminal()
                print(colored(wolf, "blue"))
                while True:
                    choice = input(colored("MIRA> ", "blue"))

                    if choice == "":
                        continue

                    elif choice == 'regis':
                        if os.path.exists(password_manager.USER_DATA_FILE) and os.path.getsize(password_manager.USER_DATA_FILE) != 0:
                            print(colored("[-] Master user already exists!!", "red"))                                                         
                        else:
                            username = input(colored("[*] New Username: ", "yellow"))
                            master_password = getpass.getpass(colored("[*] New Master Password: ", "yellow"))                                     
                            re_enter = getpass.getpass(colored("[*] Re-Enter Master Password: ", "yellow"))                                       
                            if re_enter != master_password:
                                print(colored("[-] Master Password Did Not Match! QUITTING!", "red"))
                            else:
                                password_manager.register(username, master_password)

                    elif choice == 'log':
                        if password_manager.lockout_time and time.time() < password_manager.lockout_time:
                            clear_terminal()
                            print(colored(blehhh, "red"))
                            print(colored(f"[-] Account locked. WE'VE ALREADY TOLD YOU THAT WE DON'T ACCEPT SHITTY BUGS HERE! If you are the real user, try again after {int(password_manager.lockout_time - time.time())} seconds.", "red"))
                            exit()
                        if os.path.exists(password_manager.USER_DATA_FILE):
                            username = input(colored("[*] Username: ", "yellow"))
                            master_password = getpass.getpass(colored("[*] Master password: ", "yellow"))
                            encryption_key = getpass.getpass(colored("[*] Encryption key: ", "yellow"))
                            password_manager.login(username, master_password, encryption_key)
                        else:
                            print(colored("[-] You have not registered. Please do that.", "red"))

                    elif choice == 'help' or choice == 'h':
                        if password_manager.lockout_time and time.time() < password_manager.lockout_time:
                            clear_terminal()
                            print(colored(blehhh, "red"))
                            print(colored(f"[-] Account locked. WE'VE ALREADY TOLD YOU THAT WE DON'T ACCEPT SHITTY BUGS HERE! If you are the real user, try again after {int(password_manager.lockout_time - time.time())} seconds.", "red"))
                            exit()
                        print(colored(""""[**] Available Commands:
'log' - Login (Mske sure you're registered before attempt to login)
'regis' - Register for new user (Only one user!)
'forgot' - Master Password Recovery
'quit' - Terminate MIRA
'about' - More information about MIRA
'h' - Help""", "cyan"))

                    elif choice == 'forgot':
                        if password_manager.lockout_time and time.time() < password_manager.lockout_time:
                            clear_terminal()
                            print(colored(blehhh, "red"))
                            print(colored(f"[-] Account locked. WE'VE ALREADY TOLD YOU THAT WE DON'T ACCEPT SHITTY BUGS HERE! If you are the real user, try again after {int(password_manager.lockout_time - time.time())} seconds.", "red"))
                            exit()
                        username = input(colored("[*] Username: ", "yellow"))
                        password_manager.forgot_master_password(username)

                    elif choice == 'quit':
                        print(colored("\n[-] Exiting Mira.....", "red"))
                        time.sleep(3)
                        clear_terminal()
                        print(colored(remember, "cyan"))
                        print(colored("Creating a password is like crafting a witty joke: it should be unique, memorable, and leave hackers scratching their heads. So, don't be shy to sprinkle a dash of humor into your password game – after all, laughter is the best encryption!", "cyan"))
                        exit()

                    elif choice == 'about':
                        clear_terminal()
                        print(colored(wolf, "cyan"))
                        print(colored(about, "cyan"))

                    elif choice == 'clear':
                        clear_terminal()
                    else:
                        print(colored("[-] Invalid Option", "red"))

            except KeyboardInterrupt:
                print(colored("\n[-] Exiting Mira.....", "red"))
                time.sleep(3)
                clear_terminal()
                print(colored(remember, "cyan"))
                print(colored("Creating a password is like crafting a witty joke: it should be unique, memorable, and leave hackers scratching their heads. So, don't be shy to sprinkle a dash of humor into your password game – after all, laughter is the best encryption!", "cyan"))
                exit()

    elif platform.system() == 'Windows':
        if not check_windows_privileges():
            print(colored("[-] Mira requires elevated privileges on Windows. QUITTING!", "red"))
            exit()
        else:
            try:
                clear_terminal()
                current_datetime_info = get_current_datetime()
                os_distribution_info = get_os_distribution()
                print(colored(os_distribution_info, "blue"))
                time.sleep(2)
                print(colored(get_python_version(), "blue"))
                time.sleep(2)
                print(colored(current_datetime_info, "blue"))
                time.sleep(2)
                print(colored("[+] Starting Mira Password Manager.....", "blue"))
                password_manager = PasswordManager()
                time.sleep(20)
                if password_manager.lockout_time and time.time() < password_manager.lockout_time:
                    clear_terminal()
                    print(colored(blehhh, "red"))
                    print(colored(f"[-] Account locked. WE'VE ALREADY TOLD YOU THAT WE DON'T ACCEPT SHITTY BUGS HERE! If you are the real user, try again after {int(password_manager.lockout_time - time.time())} seconds.", "red"))
                    exit()
                clear_terminal()
                print(colored(wolf, "blue"))
                while True:
                    choice = input(colored("MIRA> ", "blue"))
    
                    if choice == "":
                        continue

                    elif choice == 'regis':
                        if os.path.exists(password_manager.USER_DATA_FILE) and os.path.getsize(password_manager.USER_DATA_FILE) != 0:
                            print(colored("[-] Master user already exists!!", "red"))
                        else:
                            username = input(colored("[*] New Username: ", "yellow"))
                            master_password = getpass.getpass(colored("[*] New Master Password: ", "yellow"))
                            re_enter = getpass.getpass(colored("[*] Re-Enter Master Password: ", "yellow"))
                            if re_enter != master_password:
                                print(colored("[-] Master Password Did Not Match! QUITTING!", "red"))
                            else:
                                password_manager.register(username, master_password)

                    elif choice == 'log':
                        if password_manager.lockout_time and time.time() < password_manager.lockout_time:
                            clear_terminal()
                            print(colored(blehhh, "red"))
                            print(colored(f"[-] Account locked. WE'VE ALREADY TOLD YOU THAT WE DON'T ACCEPT SHITTY BUGS HERE! If you are the real user, try again after {int(password_manager.lockout_time - time.time())} seconds.", "red"))
                            exit()
                        if os.path.exists(password_manager.USER_DATA_FILE):
                            username = input(colored("[*] Username: ", "yellow"))
                            master_password = getpass.getpass(colored("[*] Master password: ", "yellow"))
                            encryption_key = getpass.getpass(colored("[*] Encryption key: ", "yellow"))
                            password_manager.login(username, master_password, encryption_key)
                        else:
                            print(colored("[-] You have not registered. Please do that.", "red"))

                    elif choice == 'help' or choice == 'h':
                        if password_manager.lockout_time and time.time() < password_manager.lockout_time:
                            clear_terminal()
                            print(colored(blehhh, "red"))
                            print(colored(f"[-] Account locked. WE'VE ALREADY TOLD YOU THAT WE DON'T ACCEPT SHITTY BUGS HERE! If you are the real user, try again after {int(password_manager.lockout_time - time.time())} seconds.", "red"))
                            exit()
                        print(colored(""""[**] Available Commands:
'log' - Login (Mske sure you're registered before attempt to login)
'regis' - Register for new user (Only one user!)
'forgot' - Master Password Recovery
'about' - More information about MIRA
'quit' - Terminate MIRA
'h' - Help""", "cyan"))

                    elif choice == 'forgot':
                        if password_manager.lockout_time and time.time() < password_manager.lockout_time:
                            clear_terminal()
                            print(colored(blehhh, "red"))
                            print(colored(f"[-] Account locked. WE'VE ALREADY TOLD YOU THAT WE DON'T ACCEPT SHITTY BUGS HERE! If you are the real user, try again after {int(password_manager.lockout_time - time.time())} seconds.", "red"))
                            exit()
                        username = input(colored("[*] Username: ", "yellow"))
                        password_manager.forgot_master_password(username)

                    elif choice == 'quit':
                        print(colored("\n[-] Exiting Mira.....", "red"))
                        time.sleep(3)
                        clear_terminal()
                        print(colored(remember, "cyan"))
                        print(colored("Creating a password is like crafting a witty joke: it should be unique, memorable, and leave hackers scratching their heads. So, don't be shy to sprinkle a dash of humor into your password game – after all, laughter is the best encryption!", "cyan"))
                        exit()

                    elif choice == 'about':
                        clear_terminal()
                        print(colored(wolf, "cyan"))
                        print(colored(about, "cyan"))

                    elif choice == 'clear':
                        clear_terminal()
                    else:
                        print(colored("[-] Invalid Option", "red"))

            except KeyboardInterrupt:
                print(colored("\n[-] Exiting Mira.....", "red"))
                time.sleep(3)
                clear_terminal()
                print(colored(remember, "cyan"))
                print(colored("Creating a password is like crafting a witty joke: it should be unique, memorable, and leave hackers scratching their heads. So, don't be shy to sprinkle a dash of humor into your password game – after all, laughter is the best encryption!", "cyan"))
                exit()