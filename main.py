import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess
import urllib.parse
import yt_dlp
import cloudscraper

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

cookies_file_path = os.getenv("COOKIES_FILE_PATH", "youtube_cookies.txt")

# Define aiohttp routes
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("https://text-leech-bot-for-render.onrender.com/")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

async def main():
    if WEBHOOK:
        # Start the web server
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()
        site = web.TCPSite(app_runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

    # Start the bot
    await start_bot()

    # Keep the program running
    try:
        while True:
            await bot.polling()  # Run forever, or until interrupted
    except (KeyboardInterrupt, SystemExit):
        await stop_bot()
    
@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(
       "𝐇𝐞𝐥𝐥𝐨 ❤️\n\n◆〓◆ ❖ Sanjay Kagra ❖ ™ ◆〓◆\n\n❈ I Am A Bot For Download Links From Your **.TXT** File And Then Upload That File Om Telegram So Basically If You Want To Use Me First Send Me ⟰ /Moni Command And Then Follow Few Steps..")

@bot.on_message(filters.command(["stop"]))
async def restart_handler(_, m):
    await m.reply_text("♦ 𝐒𝐭𝐨𝐩𝐩𝐞𝐭 ♦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)



@bot.on_message(filters.command(["Moni"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text('𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐀 𝐓𝐱𝐭 𝐅𝐢𝐥𝐞 𝐒𝐞𝐧𝐝 𝐇𝐞𝐫𝐞 ⏍')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"
    file_name = os.path.splitext(os.path.basename(x))[0]

    try:
       with open(x, "r") as f:
           content = f.read().strip()
    
       lines = content.splitlines()
       links = []
    
       for line in lines:
           line = line.strip()
           if line:
               link = line.split("://", 1)
               if len(link) > 1:
                   links.append(link)
    
       os.remove(x)
       print(len(links))
    
    except:
           await m.reply_text("∝ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐢𝐥𝐞 𝐢𝐧𝐩𝐮𝐭.")
           os.remove(x)
           return
   
    await editable.edit(f"∝ 𝐓𝐨𝐭𝐚𝐥 𝐋𝐢𝐧𝐤 𝐅𝐨𝐮𝐧𝐝 𝐀𝐫𝐞 🔗** **{len(links)}**\n\n𝐒𝐞𝐧𝐝 𝐅𝐫𝐨𝐦 𝐖𝐡𝐞𝐫𝐞 𝐘𝐨𝐮 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐈𝐧𝐢𝐭𝐚𝐥 𝐢𝐬 **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)
    
    await editable.edit("**Enter Batch Name or send d for grabing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == 'd':
        b_name = file_name
    else:
        b_name = raw_text0
     
    await editable.edit("∝ 𝐄𝐧𝐭𝐞𝐫 𝐄𝐞𝐬𝐨𝐥𝐮𝐭𝐢𝐨𝐧 🎬\n☞ 144,240,360,480,720,1080\nPlease Choose Quality")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    

    await editable.edit("**Enter Your Name or send `de` for use default**")

    # Listen for the user's response
    input3: Message = await bot.listen(editable.chat.id)

    # Get the raw text from the user's message
    raw_text3 = input3.text

    # Delete the user's message after reading it
    await input3.delete(True)

    # Default credit message
    credit = "️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'de':
        CR = '@SanjayKagra86🩷'
    elif raw_text3:
        CR = raw_text3
    else:
        CR = credit
   
    await editable.edit("🌄 Now send the Thumb url if don't want thumbnail send no ")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        # Assuming links is a list of lists and you want to process the second element of each sublist
        for i in range(len(links)):
            original_url = links[i][1]

            # Replace parts of the URL as needed
            V = links[i][1].replace("file/d/","uc?export=download&id=")\
               .replace("www.youtube-nocookie.com/embed", "youtu.be")\
               .replace("?modestbranding=1", "")\
               .replace("/view?usp=sharing","")\
               .replace("youtube.com/embed/", "youtube.com/watch?v=")
            
            url = "https://" + V
            
            class ParseLink(object):
              def olive(Q, url, path):
                if not re.search("https://videos.sproutvideo.com/embed/.*/.*", url):
                   print("\nThis does not seem like a valid type of url supported by the script. Follow the instructions on the README correctly and enter the embed link!")
                else:
                  site_link = Store.SPROUT_URL  # "https://discuss.oliveboard.in/"

                  try:
                    domain_name = re.search(
                     'http.?://([A-Za-z_0-9.-]+).*', site_link).group(1)
                  except Exception as e:
                    print(f"\nError: {e}")
                    domain_name = None
                  else:
                    proceed_further_1 = True

            if domain_name and proceed_further_1:
                if "https" in site_link:
                    referer_link = "https://" + domain_name + "/"
                else:
                    referer_link = "http://" + domain_name + "/"

                headers = {
                    'Referer': referer_link,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36}'
                }
                response = requests.get(url, headers=headers)

                if response.status_code != 200:
                    print(f"\nError - Site Response:\n{response.text}")
                    print("\n\nMake sure your links are correct!")
                else:
                    print("\nA successful response has been issued!")
                    try:
                        response_parts = response.text.split("var dat = '")
                        token = response_parts[1].split("'")[0]
                    except Exception as e:
                        print(f"\nError: {e}")
                        LOGS.error(str(e))
                    else:
                        proceed_further_2 = True
                      
        if proceed_further_2:
            token_to_json = json.loads(
                base64.urlsafe_b64decode(token).decode('UTF-8'))
            video_name = token_to_json['title'].replace(
                "/", "").replace(":", "").strip()
            session_id = token_to_json['sessionID']
            cdn = token_to_json['base']
            sprout_host = token_to_json['analytics_host']
            user_hash = token_to_json['s3_user_hash']
            video_hash = token_to_json['s3_video_hash']

            m3u8_policy = token_to_json['signatures']['m']['CloudFront-Policy']
            m3u8_signature = token_to_json['signatures']['m']['CloudFront-Signature']
            m3u8_keypair_id = token_to_json['signatures']['m']['CloudFront-Key-Pair-Id']

            index_link = f"https://{cdn}.{sprout_host}/{user_hash}/{video_hash}/video/index.m3u8?Policy={m3u8_policy}&Signature={m3u8_signature}&Key-Pair-Id={m3u8_keypair_id}&sessionID={session_id}"

            qualities = requests.get(index_link).text.split("\n")
            print("\nAvailable Qualities :-\n")
            Qlty = []
            for i in qualities:
                if ".m3u8" in i:
                    quality = i.split(".m3u8")[0]
                    print(quality)
                    Qlty.append(quality)
                else:
                    continue
            if Q not in Qlty:
                Q = quality
            else:
                Q = Q
            Q_link = f"https://{cdn}.{sprout_host}/{user_hash}/{video_hash}/video/{Q}.m3u8?Policy={m3u8_policy}&Signature={m3u8_signature}&Key-Pair-Id={m3u8_keypair_id}&sessionID={session_id}"
            playlist_contents = requests.get(Q_link).text

            ts_policy = token_to_json['signatures']['t']['CloudFront-Policy']
            ts_signature = token_to_json['signatures']['t']['CloudFront-Signature']
            ts_keypair_id = token_to_json['signatures']['t']['CloudFront-Key-Pair-Id']

            ts_parts = re.findall(".*_.*ts", playlist_contents)
            for ts_part in ts_parts:
                ts_link = f"https://{cdn}.{sprout_host}/{user_hash}/{video_hash}/video/{ts_part}?Policy={ts_policy}&Signature={ts_signature}&Key-Pair-Id={ts_keypair_id}&sessionID={session_id}"
                playlist_contents = playlist_contents.replace(ts_part, ts_link)

            key_policy = token_to_json['signatures']['k']['CloudFront-Policy']
            key_signature = token_to_json['signatures']['k']['CloudFront-Signature']
            key_keypair_id = token_to_json['signatures']['k']['CloudFront-Key-Pair-Id']

            key_link = f"https://{cdn}.{sprout_host}/{user_hash}/{video_hash}/video/{Q}.key?Policy={key_policy}&Signature={key_signature}&Key-Pair-Id={key_keypair_id}&sessionID={session_id}"

            final_playlist = playlist_contents.replace(f"{Q}.key", key_link)

            full_title = video_name + "-" + str(Q) + "p"
            # file_to_download = full_title + ".m3u8"
            file_to_download = f"{path}/{full_title}.m3u8"
            try:
                with open(file_to_download, "a") as m3u8_writer:
                    m3u8_writer.write(final_playlist)
                    m3u8_writer.close()
            except Exception as e:
                LOGS.error(str(e))
                print(f"\nError: {e}")
        return file_to_download

    def vision_m3u8_link(link, Q):
        Q = str(Q)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'http://www.visionias.in/',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }
        response = requests.get(f'{link}', headers=headers)
        r = response.content
        soup = BeautifulSoup(r, 'html.parser')
        paras = soup.find('script')
        url = paras.text.split('"')[3]
        print(url)
        # URL = visio_url(url , Q)
        return url
else:
    
        
    def vision_mpd_link(r_link):
        link = f'http://visionias.in/student/videoplayer_v2/video.php?{r_link.split("?")[-1]}'
        print(link)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'http://www.visionias.in/',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Mobile Safari/537.36',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
        }
        response = requests.get(f'{link}', headers=headers)
        r = response.content
        # r = open("vod.html")
        soup = BeautifulSoup(r, features="xml")
        res_link1 = soup.find_all("Location")[0].get_text()
        return res_link1


    def classplus_link(link):
        headers = {
            'Host': 'api.classplusapp.com',
            'x-access-token': Store.CPTOKEN,
            'user-agent': 'Mobile-Android',
            'app-version': '1.4.37.1',
            'api-version': '18',
            # 'accept-encoding': 'gzip',
        }
        response = requests.get(
            f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={link}', headers=headers)
        url = response.json()['url']
        print(url)
        return url

    def is_pw(url):
        """
        Sample Link :- https://d1d34p8vz63oiq.cloudfront.net/8eca5705-a305-4c1d-863f-a5b101c1983a/master.m3u8
        """
        r_code = requests.get(url=url)
        print(r_code)
        if r_code.status_code != 200:
            link = f'https://d3nzo6itypaz07.cloudfront.net/{url.split("/")[3]}/master.m3u8'
            print(link)
            r_code1 = requests.get(url=link)
            if r_code1.status_code == 200:
                return link
        else:
            link = url
            return link
        
    
    def topranker_link(url: str):
        host = f"https://{url.split('/')[2]}"
        _id = url.split('/')[-1].split('-')[0]
        print(host)
        r = requests.post(f"{host}/route?route=item%2Fliveclasses&id={_id}&response-type=2&fromapp=1&loadall=1&clientView=1&liveFromCDN=1&clientVersion=1.9").json()
        if None == r['data']['tr1info']['primPlaybackUrl']:
            ytid =r['data']['tr1info']['data']['youtubeId']
            link = f'https://www.youtube.com/watch?v={ytid}'
        else:
            link = r['data']['tr1info']['primPlaybackUrl']
        LOGS.info(link)
        return link

    def rout(url, m3u8):
        rout_link = f'https://{url.split("/")[2]}/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream={"/".join(m3u8.split("/")[0:-1]).replace("/", "%2F").replace(":", "%3A")}master.m3u8'
        LOGS.info(rout_link)
        return rout_link

    def is_drive_pdf(url):
        if url.startswith('https://drive.google.com/') and ("file" or "open" or "sharing" or "view" or "/d" in url):
            print("Drive link", True)
            _id = url.split('/')[5]
            res = f"https://drive.google.com/uc?export=download&id={_id}"
            LOGS.info(res)
            return res
        else:
            return  url

    def cw_url2(class_id):
        ACCOUNT_ID = "6206459123001"
        BCOV_POLICY = "BCpkADawqM1474MvKwYlMRZNBPoqkJY-UWm7zE1U769d5r5kqTjG0v8L-THXuVZtdIQJpfMPB37L_VJQxTKeNeLO2Eac_yMywEgyV9GjFDQ2LTiT4FEiHhKAUvdbx9ku6fGnQKSMB8J5uIDd"
        BC_URL = (
            f"https://edge.api.brightcove.com/playback/v1/accounts/{ACCOUNT_ID}/videos"
        )
        BC_HDR = {"BCOV-POLICY": BCOV_POLICY}
        video_response = requests.get(f"{BC_URL}/{class_id}", headers=BC_HDR)
        video = video_response.json()
        # print(video["sources"])
        try:
            video_source = video["sources"][5]
            video_url = video_source["src"]
        except IndexError:
            video_source = video["sources"][1]
            video_url = video_source["src"]
        return video_url
            
            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
                

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'videos.classplusapp' in url or "tencdn.classplusapp" in url or "webvideos.classplusapp.com" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "videos.classplusapp.com" in url or "media-cdn-a.classplusapp" in url or "media-cdn.classplusapp" in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}).json()['url']

            elif '/master.mpd' in url:
             id =  url.split("/")[-2]
             url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'
                      
            if "/master.mpd" in url :
                if "https://sec1.pw.live/" in url:
                    url = url.replace("https://sec1.pw.live/","https://d1d34p8vz63oiq.cloudfront.net/")
                    print(url)
                else: 
                    url = url    

                print("mpd check")
                key = await helper.get_drm_keys(url)
                print(key)
                await m.reply_text(f"got keys form api : \n`{key}`")
          
            if "/master.mpd" in url:
                cmd= f" yt-dlp -k --allow-unplayable-formats -f bestvideo.{quality} --fixup never {url} "
                print("counted")

            

            if "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                url = url.split("bcov_auth")[0]+bcov
                
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
            
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'

            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:  
                
                cc = f'**🎥 VIDEO ID: {str(count).zfill(3)}.\n\n📄 Title: {name1} {res} Sanju.mkv\n\n<pre><code>🔖 Batch Name: {b_name}</code></pre>\n\n📥 Extracted By : {CR}**'
                cc1 = f'**📁 FILE ID: {str(count).zfill(3)}.\n\n📄 Title: {name1} Moni.pdf \n\n<pre><code>🔖 Batch Name: {b_name}</code></pre>\n\n📥 Extracted By : {CR}**'
                    
                
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                
                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(4)
        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")
 
        # Create a cloudscraper session
                        scraper = cloudscraper.create_scraper()

        # Send a GET request to download the PDF
                        response = scraper.get(url)

        # Check if the response status is OK
                        if response.status_code == 200:
            # Write the PDF content to a file
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)

            # Send the PDF document
                            await asyncio.sleep(4)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1

            # Remove the PDF file after sending
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        await asyncio.sleep(2)  # Use asyncio.sleep for non-blocking sleep
                        return  # Exit the function to avoid continuation

                    except Exception as e:
                        await m.reply_text(f"An error occurred: {str(e)}")
                        await asyncio.sleep(4)  # You can replace this with more specific
                        continue
                        
                          
                else:
                    Show = f"❊⟱ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 ⟱❊ »\n\n📄 Title:- `{name}\n\n⌨ 𝐐𝐮𝐥𝐢𝐭𝐲 » {raw_text2}`\n\n**🔗 𝐔𝐑𝐋 »** `{url}`"
                    prog = await m.reply_text(f"**Downloading:-**\n\n**📄 Title:-** `{name}\n\nQuality - {raw_text2}`\n\n**link:**`{url}`\n\n **Bot Made By SanjaKagra86🩷 **")
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"⌘ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n\n⌘ 𝐍𝐚𝐦𝐞 » {name}\n⌘ 𝐋𝐢𝐧𝐤 » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("🔰Done Boss🔰")



bot.run()
if __name__ == "__main__":
    asyncio.run(main())
