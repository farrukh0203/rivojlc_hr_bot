import logging, os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ConversationHandler, filters, ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

MENU, NAME, PHONE, PHOTO, CONFIRM = range(5)

TOKEN    = "8450077086:AAFyByDJazCWidwz4_z6-QViXQ-sCN5HYSM"
GROUP_ID = "-1003785938565"

MENU_KB = [["📋 Hujjat topshirish"], ["ℹ️ Biz haqimizda"]]


async def start(update, context):
    await update.message.reply_text(
        "🇺🇿 Assalomu alaykum!\n\n"
        "Kompaniyamizga yangi ishga kirmoqchi bo'lgan "
        "xodimlarni rezyumelarini shu bot orqali qabul qilamiz.",
        reply_markup=ReplyKeyboardMarkup(MENU_KB, resize_keyboard=True),
    )
    return MENU


async def menu_handler(update, context):
    text = update.message.text
    if "Hujjat" in text:
        await update.message.reply_text(
            "Ismingizni yozib qoldiring:",
            reply_markup=ReplyKeyboardRemove(),
        )
        return NAME
    elif "haqimizda" in text:
        await update.message.reply_text(
            "🏢 Biz haqimizda ma'lumotni bu yerga yozing.",
            reply_markup=ReplyKeyboardMarkup(MENU_KB, resize_keyboard=True),
        )
        return MENU
    return MENU


async def get_name(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting:\nNamuna: +998901234567")
    return PHONE


async def get_phone(update, context):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Endi rasmingizni yuboring:")
    return PHOTO


async def get_photo(update, context):
    if update.message.photo:
        context.user_data["photo_id"] = update.message.photo[-1].file_id
    elif update.message.document:
        context.user_data["photo_id"] = update.message.document.file_id
    else:
        await update.message.reply_text("Iltimos, rasm yuboring!")
        return PHOTO

    name  = context.user_data["name"]
    phone = context.user_data["phone"]
    photo = context.user_data["photo_id"]
    kb = [["Ha, to'g'ri ✅", "Qayta kiritaman ❌"]]

    await update.message.reply_photo(
        photo=photo,
        caption=(
            f"Ma'lumotlaringiz:\n\n"
            f"Ism: {name}\n"
            f"Telefon: {phone}\n\n"
            "Shu ma'lumotlar to'g'rimi?"
        ),
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return CONFIRM


async def confirm(update, context):
    if "Ha" in update.message.text:
        name  = context.user_data["name"]
        phone = context.user_data["phone"]
        photo = context.user_data["photo_id"]
        caption = (
            f"Yangi ariza\n\n"
            f"Ism: {name}\n"
            f"Tel: {phone}\n"
            f"Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )
        await context.bot.send_photo(chat_id=GROUP_ID, photo=photo, caption=caption)
        await update.message.reply_text(
            "Yuborildi! Tez orada bog'lanamiz.",
            reply_markup=ReplyKeyboardMarkup(MENU_KB, resize_keyboard=True),
        )
    else:
        await update.message.reply_text(
            "Qayta boshlash uchun /start bosing.",
            reply_markup=ReplyKeyboardMarkup(MENU_KB, resize_keyboard=True),
        )
    context.user_data.clear()
    return MENU


async def cancel(update, context):
    await update.message.reply_text(
        "Bekor qilindi.",
        reply_markup=ReplyKeyboardMarkup(MENU_KB, resize_keyboard=True),
    )
    return MENU


def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU:    [MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler)],
            NAME:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE:   [MessageHandler(filters.TEXT & ~filters.COMMAND
