import logging
import asyncio
import aiohttp
import os
import time
from datetime import datetime
from pytube import YouTube
from config import Config
from translation import Translation
from plugins.custom_thumbnail import *
from helper_funcs.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levellevelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

async def ddl_call_back(bot, update):
    logger.info(update)
    cb_data = update.data
    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    youtube_urls = update.message.reply_to_message.text.split()
    download_directory = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)

    if not os.path.isdir(download_directory):
        os.makedirs(download_directory)

    user = await bot.get_me()
    mention = user["mention"]
    description = Translation.CUSTOM_CAPTION_UL_FILE.format(mention)
    start = datetime.now()
    
    await bot.edit_message_text(
        text=Translation.DOWNLOAD_START,
        chat_id=update.message.chat.id,
        message_id=update.message.message_id
    )

    for youtube_url in youtube_urls:
        custom_file_name = os.path.basename(youtube_url)
        custom_file_name = custom_file_name.strip()
        logger.info(youtube_url)
        logger.info(custom_file_name)

        try:
            await download_youtube_video(youtube_url, download_directory, custom_file_name)
        except Exception as e:
            await bot.edit_message_text(
                text=f"Failed to download video: {str(e)}",
                chat_id=update.message.chat.id,
                message_id=update.message.message_id
            )
            return False

    end_one = datetime.now()
    await bot.edit_message_text(
        text=Translation.UPLOAD_START,
        chat_id=update.message.chat.id,
        message_id=update.message.message_id
    )

    for youtube_url in youtube_urls:
        custom_file_name = os.path.basename(youtube_url)
        download_path = download_directory + "/" + custom_file_name

        if os.path.exists(download_path):
            file_size = Config.TG_MAX_FILE_SIZE + 1
            try:
                file_size = os.stat(download_path).st_size
            except FileNotFoundError as exc:
                download_path = os.path.splitext(download_path)[0] + "." + "mp4"
                file_size = os.stat(download_path).st_size
            if file_size > Config.TG_MAX_FILE_SIZE:
                await bot.edit_message_text(
                    chat_id=update.message.chat.id,
                    text=Translation.RCHD_TG_API_LIMIT,
                    message_id=update.message.message_id
                )
            else:
                start_time = time.time()
                await bot.send_document(
                    chat_id=update.message.chat.id,
                    document=download_path,
                    thumb=thumb_image_path,
                    caption=description,
                    reply_to_message_id=update.message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, update.message, start_time)
                )
                end_two = datetime.now()
                time_taken_for_download = (end_one - start).seconds
                time_taken_for_upload = (end_two - end_one).seconds
                await bot.edit_message_text(
                    text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload),
                    chat_id=update.message.chat.id,
                    message_id=update.message.message_id,
                    disable_web_page_preview=True
                )
                try:
                    os.remove(download_path)
                    os.remove(thumb_image_path)
                except:
                    pass
        else:
            await bot.edit_message_text(
                text=Translation.NO_VOID_FORMAT_FOUND.format("Incorrect Link"),
                chat_id=update.message.chat.id,
                message_id=update.message.message_id,
                disable_web_page_preview=True
            )

async def download_youtube_video(url, download_directory, file_name):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path=download_directory, filename=file_name)
