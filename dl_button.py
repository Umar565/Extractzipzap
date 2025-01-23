import logging
import asyncio
import aiohttp
import os
import time
from datetime import datetime
from config import Config
from translation import Translation
from plugins.custom_thumbnail import *
from helper_funcs.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

async def ddl_call_back(bot, update):
    logger.info(update)
    cb_data = update.data
    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    pdf_url = update.message.reply_to_message.text
    custom_file_name = os.path.basename(pdf_url)
    if "|" in pdf_url:
        url_parts = pdf_url.split("|")
        if len(url_parts) == 2:
            pdf_url = url_parts[0]
            custom_file_name = url_parts[1]
        else:
            for entity in update.message.reply_to_message.entities:
                if entity.type == "text_link":
                    pdf_url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    pdf_url = pdf_url[o:o + l]
        if pdf_url is not None:
            pdf_url = pdf_url.strip()
        if custom_file_name is not None:
            custom_file_name = custom_file_name.strip()
        logger.info(pdf_url)
        logger.info(custom_file_name)
    else:
        for entity in update.message.reply_to_message.entities:
            if entity.type == "text_link":
                pdf_url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                pdf_url = pdf_url[o:o + l]
    user = await bot.get_me()
    mention = user["mention"]
    description = Translation.CUSTOM_CAPTION_UL_FILE.format(mention)
    start = datetime.now()
    await bot.edit_message_text(
        text=Translation.DOWNLOAD_START,
        chat_id=update.message.chat.id,
        message_id=update.message.message_id
    )
    tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = tmp_directory_for_each_user + "/" + custom_file_name
    async with aiohttp.ClientSession() as session:
        c_time = time.time()
        try:
            await download_pdf(
                bot,
                session,
                pdf_url,
                download_directory,
                update.message.chat.id,
                update.message.message_id,
                c_time
            )
        except asyncio.TimeoutError:
            await bot.edit_message_text(
                text=Translation.SLOW_URL_DECED,
                chat_id=update.message.chat.id,
                message_id=update.message.message_id
            )
            return False
    if os.path.exists(download_directory):
        end_one = datetime.now()
        await bot.edit_message_text(
            text=Translation.UPLOAD_START,
            chat_id=update.message.chat.id,
            message_id=update.message.message_id
        )
        file_size = Config.TG_MAX_FILE_SIZE + 1
        try:
            file_size = os.stat(download_directory).st_size
        except FileNotFoundError as exc:
            download_directory = os.path.splitext(download_directory)[0] + "." + "pdf"
            file_size = os.stat(download_directory).st_size
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
                document=download_directory,
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
                os.remove(download_directory)
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

async def download_pdf(bot, session, url, file_name, chat_id, message_id, start):
    async with session.get(url, timeout=Config.PROCESS_MAX_TIMEOUT) as response:
        total_length = int(response.headers["Content-Length"])
        await bot.edit_message_text(
            chat_id,
            message_id,
            text=f"Initiating Download...\nURL: {url}\nFile Size: {humanbytes(total_length)}"
        )
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(Config.CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
