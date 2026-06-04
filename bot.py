import logging, os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

MENU, NAME, PHONE, PHOTO, CONFIRM = range(5)

TOKEN    = "8450077086:AAFyByDJazCWidwz4_z6-QViXQ-sCN5HYSM"
GROUP_ID = "-1003785938565"

MENU_KB = [["📋 Hujjat topshirish"], ["ℹ️ Biz haqimizda"]]


async def start(update, context):
    await update.message.reply_text(
        "🇺🇿 Assalomu alaykum!\n\n"
        "Kompaniyamizga ishga kirmoqchi bolgan xodimlarni\n"
        "rezyumelarini shu bot orqali qabul qilamiz.",
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
            "Biz haqimizda malumotni bu yerga yozing.",
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
    kb = [["Ha, togri", "Qayta kiritaman"]]

    await update.message.reply_photo(
        photo=photo,
        caption="Malumotlaringiz:\n\nIsm: " + name + "\nTelefon: " + phone + "\n\nShu malumotlar toghrimi?",
        reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True, resize_keyboard=True),
    )
    return CONFIRM


async def confirm(update, context):
    if "Ha" in update.message.text:
        name  = context.user_data["name"]
        phone = context.user_data["phone"]
        photo = context.user_data["photo_id"]
        sana  = datetime.now().strftime("%d.%m.%Y %H:%M")
        caption = "Yangi ariza\n\nIsm: " + name + "\nTel: " + phone + "\nSana: " + sana
        await context.bot.send_photo(chat_id=GROUP_ID, photo=photo, caption=caption)
        await update.message.reply_text(
            "Yuborildi! Tez orada boglanamiz.",
            reply_markup=ReplyKeyboardMarkup(MENU_KB, resize_keyboard=True),
        )
    else:
        await update.message.reply_text(
            "Qayta boshlash: /start",
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
    TEXT = filters.TEXT & ~filters.COMMAND
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU:    [MessageHandler(TEXT, menu_handler)],
            NAME:    [MessageHandler(TEXT, get_name)],
            PHONE:   [MessageHandler(TEXT, get_phone)],
            PHOTO:   [MessageHandler(filters.PHOTO | filters.Document.IMAGE, get_photo)],
            CONFIRM: [MessageHandler(TEXT, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    print("Bot ishlamoqda...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
