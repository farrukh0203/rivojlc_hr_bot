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

NAME, PHONE, PHOTO, CONFIRM = range(4)

TOKEN    = "8450077086:AAFyByDJazCWidwz4_z6-QViXQ-sCN5HYSM"
GROUP_ID = "-1003785938565"


async def start(update, context):
    await update.message.reply_text(
        "Salom! HR bo'limi botiga xush kelibsiz!\n\n"
        "Ism va familiyangizni kiriting:"
    )
    return NAME


async def get_name(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        f"Rahmat!\n\nTelefon raqamingizni kiriting:\nNamuna: +998901234567"
    )
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
        caption=f"Ma'lumotlaringiz:\n\nIsm: {name}\nTelefon: {phone}\n\nShu ma'lumotlar to'g'rimi?",
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
            "Yuborildi! HR bo'limi siz bilan bog'lanadi.",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            "Qayta boshlash uchun /start bosing.",
            reply_markup=ReplyKeyboardRemove()
        )
    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update, context):
    await update.message.reply_text("Bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def get_id(update, context):
    await update.message.reply_text(f"Bu chatning ID si: {update.effective_chat.id}")


def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            PHOTO:   [MessageHandler(filters.PHOTO | filters.Document.IMAGE, get_photo)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    app.add_handler(CommandHandler("id", get_id))
    print("Bot ishlamoqda...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
