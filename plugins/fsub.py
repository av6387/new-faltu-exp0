from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ChatJoinRequest
from pyrogram import Client, enums, filters
from pyrogram.errors import UserNotParticipant
from config import FORCE_SUB_CHANNEL, ADMINS
from database.fsub_db import Fsub_DB

LINK = None

@Client.on_chat_join_request(filters.chat(FORCE_SUB_CHANNEL))
async def filter_join_reqs(bot, message: ChatJoinRequest):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    date = message.date
    await Fsub_DB().add_user(user_id, first_name, username, date)

@Client.on_message(filters.command("total_reqs") & filters.private & filters.user(ADMINS))
async def count_reqs(bot, message):
    total = await Fsub_DB().total_users()
    await message.reply_text(f"<b>Hey {message.from_user.mention}, Total Join Requests: {str(total)} !</b>")

@Client.on_message(filters.command("delete_reqs") & filters.private & filters.user(ADMINS))
async def purge_reqs(bot, message):
    await Fsub_DB().purge_all()
    total = await Fsub_DB().total_users()
    await message.reply_text(f"<b>Hey {message.from_user.mention}, Successfully deleted all {total} join requests !</b>")

async def Force_Sub(bot: Client, message: Message, file_id = False):
    global LINK
    if not FORCE_SUB_CHANNEL:
        return True
    else:
        pass
    try:
        if LINK == None:
            link = await bot.create_chat_invite_link(
                chat_id=FORCE_SUB_CHANNEL,
                creates_join_request=True
            )
            LINK = link
            print("Created Invite Link !")
        else:
            link = LINK
    except Exception as e:
        print(f"Unable to create invite link !\n\nError: {e}")
        return False
    try:
        user = await Fsub_DB().get_user(message.from_user.id)
        if user and str(user["id"]) == str(message.from_user.id):
            return True
    except Exception as e:
        print(f"ERROR: {e}")
        await message.reply(
            text=f"ERROR: {e}",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return False
    try:
        await bot.get_chat_member(
            chat_id=FORCE_SUB_CHANNEL,
            user_id=message.from_user.id
        )
        return True
    except UserNotParticipant:
        btn = [[
            InlineKeyboardButton("Request To Our Back-Up Channel", url=link.invite_link)
        ]]
        if file_id != False:
            btn.append([InlineKeyboardButton("Try Again !", url=f"https://t.me/{bot.username}?start={file_id}")])
        else:
            pass
        await message.reply(
            text=f"**Hey Dear 💖💚 \n\nYou need to Request my channel to use me ! Kindly Request and try again!*\n\n Not able to get lecture watch video:-https://youtu.be/GzmuXff6OJY*",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return False
