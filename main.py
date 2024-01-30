from functions.join_guild import join_guild
from functions.leave_guild import leave_guild
from functions.send_message import send_message
from functions.send_message_massping import send_message_massping
from functions.checker import checker
from functions.click_button import click_button
from functions.join_vc import join_vc
from functions.react import react
from functions.accept_rules import accept_rules
from functions.onboarding_bypass import onboarding
from functions.nick import change_nick
from functions.thread_spam import create_thread
from colorama import Fore
import threading
import websocket
import datetime
import requests
import ctypes
import random
import string
import json
import time
import sys
import os
import re

W = Fore.RESET
C = "\033[38;2;75;0;130m"
L = Fore.LIGHTYELLOW_EX
V = Fore.GREEN
B = Fore.LIGHTBLACK_EX
I = Fore.LIGHTRED_EX
stop_event = threading.Event()

def get_stats():
    with open('data/valid.txt', 'r') as file:
        num_tokens = sum(1 for line in file)
    file.close()
    with open('data/proxies.txt', 'r') as file:
        num_proxies = sum(1 for line in file)
    file.close()
    return num_tokens, num_proxies

def headers(token):
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-EN,cs;q=0.9,en;q=0.8',
        'Authorization': token,
        'Cookie': '__dcfduid=bcdcc21048ec11eeb28aadb2936bc589; __sdcfduid=bcdcc21148ec11eeb28aadb2936bc58939681dcd50112431f1dc800e50f374628b27f03a40107a46ebf3a05065becb2c; _ga_Q149DFWHT7=GS1.1.1693589213.1.0.1693589414.0.0.0; __stripe_mid=a614d196-bfdf-4093-be94-44b2567c7c312dff1a; _ga_XXP2R74F46=GS1.2.1702481998.1.0.1702481998.0.0.0; _gid=GA1.2.1957939489.1702654470; _ga_YL03HBJY7E=GS1.1.1702654469.11.0.1702654469.0.0.0; _ga=GA1.1.1994256083.1693589213; OptanonConsent=isIABGlobal=false&datestamp=Fri+Dec+15+2023+16%3A34%3A29+GMT%2B0100+(czas+%C5%9Brodkowoeuropejski+standardowy)&version=6.33.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0&AwaitingReconsent=false; __cfruid=7c526e008192466f8ca27de600811cb9f9a9b039-1702664289; _cfuvid=ut98lvE6CAZQkcpuAaMXk7oTUSVGktwTdF16TRtT.EQ-1702664289884-0-604800000; cf_clearance=G65_tgviKwqVw0qNdhw0byG9ATZLTfAEAszCfqd.CMk-1702664599-0-1-3b6189e5.cb55b875.78db4fb0-0.2.1702664599; locale=en',
        'Referer': 'https://discord.com/channels/@me',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36',
        'X-Debug-Options': 'bugReporterEnabled',
        'X-Discord-Locale': 'en',
        'X-Discord-Timezone': 'Europe/London',
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InBsLVBMIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExOS4wLjYwNDUuMTk5IFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIxMTkuMC42MDQ1LjE5OSIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNTQ4ODgsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9'
}

def get_proxies():
    try:
        with open("data/proxies.txt", "r") as f:
            proxies = f.read().splitlines()

        if not proxies:
            return []

        proxy_list = []
        for proxy in proxies:
            parts = proxy.split(":")

            if len(parts) == 4:
                proxy_url = f"socks5://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
            elif len(parts) == 2:
                proxy_url = f"socks5://{parts[0]}:{parts[1]}"
            else:
                continue

            proxy_dict = {
                'http': proxy_url,
                'https': proxy_url
            }
            proxy_list.append(proxy_dict)

        return proxy_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_proxies2():
    try:
        with open("data/proxies.txt", "r") as f:
            proxies = f.read().splitlines()

        if not proxies:
            return None

        proxy_dict = []
        for proxy in proxies:
            parts = proxy.split(":")

            if len(parts) == 4:
                proxy_url = f"socks5://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
            elif len(parts) == 2:
                proxy_url = f"socks5://{parts[0]}:{parts[1]}"
            else:
                continue
            
            proxy_dict.append({
                "http": proxy_url,
                "https": proxy_url
            })

        if not proxy_dict:
            return None

        return proxy_dict

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_values(guild_id, token_to_use):
    url = f"https://discord.com/api/v9/guilds/{guild_id}/member-verification?with_guild=false"

    response = requests.get(url, headers=headers(token_to_use))
    
    resp = response.text

    resp_dict = json.loads(resp)
    form_fields = resp_dict["form_fields"]
    for field in form_fields:
        values = field["values"]
        return values

def get_messages(token, channel_id):
    resp = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=50", headers=headers(token))
    data = resp.text
    return data

class Scrape:
    def __init__(self, token) -> None:
        self.ws = websocket.WebSocket()
        self.ws.connect("wss://gateway.discord.gg/?v=8&encoding=json")
        response = self.ws.recv()
        if response:
            hello = json.loads(response)
            self.heartbeat_interval = hello['d']['heartbeat_interval']
            self.ws.send(json.dumps({"op": 2, "d": {"token": token, "properties": {"$os": "windows", "$browser": "Discord", "$device": "desktop"}}}))
        else:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"{W}{current_time}{C}||Token doesnt work: {token}")
        self.users = []

    def find_user_ids(self, data):
        ids = []
        if isinstance(data, dict):
            if 'username' in data and 'id' in data:
                ids.append(data['id'])
            else:
                for v in data.values():
                    if isinstance(v, (dict, list)):
                        ids.extend(self.find_user_ids(v))
        elif isinstance(data, list):
            for item in data:
                ids.extend(self.find_user_ids(item))
        return ids
    pass

    def send_op14(self, range):
        self.ws.send(json.dumps({
            "op": 14,
            "d": {
                "guild_id": self.guild_id,
                "typing": True,
                "threads": True,
                "activities": True,
                "members": [],
                "channels": {
                    f"{self.channel_id}": [[range * 100, range * 100 + 100 - 1]]
                },
                "thread_member_lists": []
            }
        }))
        pass

    def scrape(self, guild_id, channel_id):
            self.guild_id = guild_id
            self.channel_id = channel_id
            self.send_op14(0)
            self.first = False
            last_message = datetime.datetime.now()
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"{W}{current_time}{C}|| Scraping users from Guild ID {self.guild_id}")

            while True:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                response = self.ws.recv()
                if response:
                    try:
                        json_data = json.loads(response)
                        if json_data["t"] == "GUILD_MEMBER_LIST_UPDATE":
                            if not self.first:
                                _range = json_data["d"]["online_count"] / 100
                                for i in range(int(_range) + 2):
                                    time.sleep(1)
                                    self.send_op14(i)
                                self.first = True
                            for ops in json_data["d"]["ops"]:
                                if ops["op"] == "SYNC":
                                    for member in ops["items"]:
                                        try:
                                            member = member["member"]
                                        except KeyError:
                                            continue
                                        user_ids = self.find_user_ids(member)
                                        self.users.extend(user_ids)

                        if (datetime.datetime.now() - last_message).total_seconds() > 10:
                            print(f"{W}{current_time}{C}||Scraped {len(self.users)} users from {self.guild_id}")
                            time.sleep(2.5)
                            return True
                    except json.JSONDecodeError as e:
                        print(f"{W}{current_time}{C}||{I}Error: {e}")
                else:
                    print(f"{W}{current_time}{C}||Couldn't scrape {self.guild_id}")

class Tool:
    def __init__(self, version):
        self.version = version

    def join_guild(self):
        with open("data/valid.txt", "r") as f:
            tokens = f.read().splitlines()
        invite = input(f"{C}Invite >> ")
        delay = input(f"{C}Delay >> ")

        threads = []
        proxies = get_proxies2()

        for token in tokens:
            time.sleep(int(delay))
            if proxies:
                proxy = random.choice(proxies)["https"]
                t = threading.Thread(target=join_guild, args=(token, invite, proxy))
            else:
                t = threading.Thread(target=join_guild, args=(token, invite))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        input(f"{W}{current_time}{C}||Press Enter to continue...")
        sys.stdout.flush()

    def leave_guild(self):
        with open("data/valid.txt", "r") as f:
            tokens = f.read().splitlines()
        guild_id = input(f"{C}Guild id >> ")
        delay = input(f"{C}Delay >> ")

        threads = []
        for token in tokens:
            time.sleep(int(delay))
            t = threading.Thread(target=leave_guild, args=(token, guild_id))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        input(f"{W}{current_time}{C}||Press Enter to continue...")
        sys.stdout.flush()

    def raid_channel(self):
        with open("data/valid.txt", "r") as f:
            tokens = f.read().splitlines()
        channel_id = input(f"{C}channel id >> ")
        content = input(f"{C}Message >> ")
        proxies = get_proxies()
        print("\n")
        if not proxies:
            proxies = None
            print("No proxies found, using local IP")
        threads = []
        for token in tokens:
            proxy = random.choice(proxies) if proxies else None
            t = threading.Thread(target=send_message, args=(token, content, channel_id, proxy, stop_event))
            threads.append(t)
            t.start()

        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        input(f"{W}{current_time}{C}||Press Enter to stop...\n")
        stop_event.set()

        for t in threads:
            t.join()

    def raid_channel_massping(self):
        with open("data/valid.txt", "r") as f:
            tokens = f.read().splitlines()

        message_link = input("Channel link >> ")
        numbers = re.findall(r'\d+', message_link)
        channel_id = numbers[1]
        server_id = numbers[0]
        content = input(f"{C}Message >> ")
        proxies = get_proxies()
        print("\n")
        if not proxies:
            proxies = None
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"{W}{current_time}{C}||No proxies found, using local IP")

        random_token = tokens[0]
        scrape = Scrape(random_token)
        scrape.scrape(server_id, channel_id)
        user_ids = scrape.users

        if not user_ids:
            print("No user IDs available. Exiting.")
            return

        stop_event = threading.Event()
        threads = []
        for user_id in user_ids:
            for token in tokens:
                user_id = user_ids.pop(0)
                proxy = random.choice(proxies) if proxies else None
                random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
                t = threading.Thread(target=send_message_massping, args=(token, content, channel_id, proxy, stop_event, user_id, random_chars))
                threads.append(t)
                t.start()

        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        input(f"{W}{current_time}{C}||Press Enter to stop...\n")
        stop_event.set()

        for t in threads:
            t.join()

    def check_tokens(self):
        with open("data/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        for token in tokens:
            checker(token)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        input(f"{W}{current_time}{C}||Press Enter to continue...")
        sys.stdout.flush()

    def join_vc(self):
            with open("data/valid.txt", "r") as f:
                tokens = f.read().splitlines()
            channel = int(input("Channel ID >> "))
            server = int(input("Guild ID >> "))
            deaf = True
            mute = True
            stream = False
            video = False
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
                
            threads = []
            for token in tokens:
                t = threading.Thread(target=join_vc, args=(token, server, channel, mute, deaf, stream, video))
                print(f"{W}{current_time}{C}||{V}Joined voice channel")
                time.sleep(0.1)
                threads.append(t)
                t.start()

            for t in threads:
                t.join()    
                
                
            input(f"{W}{current_time}{C}||Press Enter to continue...")
            sys.stdout.flush()

    def thread_spam(self):
        with open("data/valid.txt", "r") as f:
            tokens = f.read().splitlines()
        channel_id = input("Channel ID >> ")
        name = input("Thread name >> ")

        def get_message_id(data):
            if data is None:
                return []
            message_ids = []
            messages = json.loads(data)
            for message in messages:
                message_ids.append(message['id'])
            return message_ids
        
        login = tokens[0]
        data = get_messages(login, channel_id)
        message_ids = get_message_id(data)

        if len(message_ids) < len(tokens):
            tokens = tokens[:len(message_ids)]

        threads = []
        for token, message_id in zip(tokens, message_ids):
            t = threading.Thread(target=create_thread, args=(token, channel_id, message_id, name))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        input(f"{W}{current_time}{C}||Press Enter to continue...") 
        sys.stdout.flush()

    def react(self):
        with open("data/valid.txt", "r") as f:
            tokens = f.read().splitlines()

        message_link = input("Message link >> ")
        numbers = re.findall(r'\d+', message_link)
        channel_id = numbers[1]
        message_id = numbers[2]
        index = 0
        threads = []
        
        for token in tokens:
            t = threading.Thread(target=react, args=((token, channel_id, message_id, index)))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        input(f"{W}{current_time}{C}||Press Enter to continue...")
        sys.stdout.flush()
    
    def accept_rules(self):
        with open("data/valid.txt", "r") as f:
                tokens = f.read().splitlines()

        guild_id = input("Guild ID >> ")
        token_to_use = tokens[0]

        values = get_values(guild_id, token_to_use)

        threads = []
        for token in tokens:
            t = threading.Thread(target=accept_rules, args=(token, values, guild_id))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        input(f"{W}{current_time}{C}||Press Enter to continue...")
        sys.stdout.flush()

    def click_button(self):
        message_link = input("Message link >> ")
        numbers = re.findall(r'\d+', message_link)
        guild_id = numbers[0]
        channel_id = numbers[1]
        message_id = numbers[2]

        threads = []

        with open("data/valid.txt", "r") as f:
            tokens = f.read().splitlines()
        
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        response = requests.get(url, headers=headers(tokens[0]))
        data = json.loads(response.text)

        def get_custom_ids(data):
            custom_ids = []
            for component in data[0]['components']:
                for sub_component in component['components']:
                    custom_id = sub_component['custom_id']
                    custom_ids.append(custom_id)
            return custom_ids
        
        def get_application_id(data):
            if 'webhook_id' in data[0]:
                application_id = data[0]['application_id']
            else:
                application_id = data[0]['author']['id']
            return application_id
        
        for token in tokens:
            for custom_id in get_custom_ids(data):
                t = threading.Thread(target=click_button, args=(guild_id, channel_id, message_id, get_application_id(data), custom_id, token))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        input(f"{W}{current_time}{C}||Press Enter to continue...")
        sys.stdout.flush()

    def onboarding_bypass(self):
        with open("data/valid.txt", "r") as f:
            tokens = f.read().splitlines()
        guild_id = input("Guild ID >> ")

        threads = []
        for token in tokens:
            t = threading.Thread(target=onboarding, args=(token, guild_id))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        input(f"{W}{current_time}{C}||Press Enter to continue...")
        sys.stdout.flush()
    
    def change_nick(self):
        with open("data/valid.txt", "r") as f:
            tokens = f.read().splitlines()
        guild_id = input("Guild ID >> ")
        nick = input("Nickname >> ")

        threads = []
        for token in tokens:
            t = threading.Thread(target=change_nick, args=(token, nick, guild_id))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        input(f"{W}{current_time}{C}||Press Enter to continue...")
        sys.stdout.flush()

    def format_tokens(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{W}{current_time}{C}||Format EMAIL:PASS:TOKENS to TOKENS")
        print(f"{W}{current_time}{C}||Put tokens in data/tokens.txt")
        input(f"{W}{current_time}{C}||Press Enter to continue...")
        time.sleep(0.5)
        with open("data/tokens.txt", "r") as f:
            lines = [line.strip().split(":")[-1] + "\n" for line in f]
        with open("data/tokens.txt", "w") as f:
            f.writelines(lines)

        print(f"{W}{current_time}{C}||Done formatting tokens")
        input(f"{W}{current_time}{C}||Press Enter to continue...")
        sys.stdout.flush()
    
    def exit(self):
        pass

    def run(self):
        num_tokens, num_proxies = get_stats()
        while True:
            os.system("cls")
            ctypes.windll.kernel32.SetConsoleTitleW(f"Tool | Version: {self.version} | Tokens: {num_tokens} | Proxies: {num_proxies}")

            print(f"""

                                {C}$$\    $$\                      $$\                         
                                {C}$$ |   $$ |                     $$ |                        
                                {C}$$ |   $$ | $$$$$$\   $$$$$$\ $$$$$$\    $$$$$$\  $$\   $$\ 
                                {C}\$$\  $$  |$$  __$$\ $$  __$$\\_$$  _|  $$  __$$\ \$$\ $$  |
                                 {C}\$$\$$  / $$ /  $$ |$$ |  \__| $$ |    $$$$$$$$ | \$$$$  / 
                                  {C}\$$$  /  $$ |  $$ |$$ |       $$ |$$\ $$   ____| $$  $$<  
                                   {C}\$  /   \$$$$$$  |$$ |       \$$$$  |\$$$$$$$\ $$  /\$$\ 
                                    {C}\_/     \______/ \__|        \____/  \_______|\__/  \__|
                                                                                                                
                                                          

                        {C}[{W}01{C}]{W}JOIN GUILD                  {C}[{W}06{C}]{W}JOIN VC                 {C}[{W}11{C}]{W}ONBOARDING BYPASS
                        {C}[{W}02{C}]{W}LEAVE GUILD                 {C}[{W}07{C}]{W}THREAD SPAM             {C}[{W}12{C}]{W}CHANGE NICKNAME
                        {C}[{W}03{C}]{W}RAID CHANNEL                {C}[{W}08{C}]{W}REACT                   {C}[{W}13{C}]{W}FORMAT TOKENS
                        {C}[{W}04{C}]{W}RAID CHANNEL + MASSPING     {C}[{W}09{C}]{W}ACCEPT RULES            {C}[{W}14{C}]{W}TO BE MADE
                        {C}[{W}05{C}]{W}CHECK TOKENS                {C}[{W}10{C}]{W}CLICK BUTTON            {C}[{W}15{C}]{W}EXIT    
            """)

            choice = input(f"{C}Choice >> ")

            if choice == '1':
                self.join_guild()

            elif choice == '2':
                self.leave_guild()

            elif choice == '3':
                self.raid_channel()

            elif choice == '4':
                self.raid_channel_massping()

            elif choice == '5':
                self.check_tokens()

            elif choice == '6':
                self.join_vc()

            elif choice == '7':
                self.thread_spam()

            elif choice == '8':
                self.react()

            elif choice == '9':
                self.accept_rules()

            elif choice == '10':
                self.click_button()

            elif choice == '11':
                self.onboarding_bypass()

            elif choice == '12':
                self.change_nick()

            elif choice == '13':
                self.format_tokens()

            elif choice == '15':
                self.exit()
                break

if __name__ == "__main__":
    tool = Tool(version='6.9.420')
    tool.run()