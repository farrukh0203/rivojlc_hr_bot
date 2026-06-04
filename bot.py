import logging, os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

(MENU, NAME, PHONE, POSITION, BIRTHDAY, PHOTO,
 ADDRESS, EDUCATION, GENDER, PREV_WORK, PREV_POSITION,
 PREV_DURATION, PREV_REASON, FAMILY, LANGUAGES,
 SALARY, ABOUT, WHY, CONFIRM) = range(19)

TOKEN    = "8984989724:AAHbirZWRVfm0oFfhLA20i72zeQiF01OcUc"
GROUP_ID = "-1003572531739"

MENU_KB = [["📋 Hujjat topshirish"], ["ℹ️ Biz haqimizda"]]
BACK_KB  = [["🔙 Orqaga"]]

POSITION_KB = [
    ["📸 Mobilgraf", "🎬 Video Montajchi"],
    ["📱 SMM manager", "🎯 Targetolog"],
    ["🔙 Orqaga"]
]
EDUCATION_KB = [
    ["📚 O'rta", "🎓 O'rta maxsus", "🏛 Oliy"],
    ["🔙 Orqaga"]
]
GENDER_KB  = [["👨 Erkak", "👩 Ayol"], ["🔙 Orqaga"]]
YES_NO_KB  = [["✅ Ha", "❌ Yo'q"], ["🔙 Orqaga"]]
SALARY_KB  = [
    ["💵 3-5 mln", "💵 4-6 mln"],
    ["💵 5-8 mln", "💵 8 mlndan ko'p"],
    ["🔙 Orqaga"]
]
CONFIRM_KB = [["✅ Ha, to'g'ri", "❌ Yo'q, noto'g'ri"]]

BIZ_HAQIMIZDA = """🏢 RIA Marketing Jamoasi Haqida

«RIA Marketing» — SMM va Performance marketingga ixtisoslashgan agentlik.

📱 SMM (Ijtimoiy tarmoqlar boshqaruvi)
🎯 Targetli reklama
📢 TG Ads

Tajribali mutaxassislar, aniq strategiya va o'lchanadigan natijalar — bularning barchasi sotuvlarni oshirish uchun.

🎯 Maqsadimiz:
Har bir mijozning biznesi sotuvlarini oshirish va taniqli brendga aylantirish.

Bizning jamoaga qo'shiling — birgalikda muvaffaqiyatga erishamiz, inshaAlloh!

📞 94 595 84 04

Hurmat bilan, RIA Marketing Jamoasi"""


def make_summary(d):
    return (
        "📋 Yangi ariza — RIA Marketing\n\n"
        "1. Ism familiyasi: "    + d.get("name","—")          + "\n"
        "2. Telefon: "           + d.get("phone","—")         + "\n"
        "3. Lavozim: "           + d.get("position","—")      + "\n"
        "4. Tug'ilgan sana: "    + d.get("birthday","—")      + "\n"
        "5. Manzil: "            + d.get("address","—")       + "\n"
        "6. Ma'lumot: "          + d.get("education","—")     + "\n"
        "7. Jinsi: "             + d.get("gender","—")        + "\n"
        "8. Oldingi ish joyi: "  + d.get("prev_work","—")    + "\n"
        "9. Oldingi lavozim: "   + d.get("prev_position","—") + "\n"
        "10. Ish muddati: "      + d.get("prev_duration","—") + "\n"
        "11. Bo'shash sababi: "  + d.get("prev_reason","—")   + "\n"
        "12. Oilaviy holat: "    + d.get("family","—")        + "\n"
        "13. Chet tillari: "     + d.get("languages","—")     + "\n"
        "14. Istalgan maosh: "   + d.get("salary","—")        + "\n"
        "15. O'zi haqida: "      + d.get("about","—")         + "\n"
        "16. Nima uchun: "       + d.get("why","—")           + "\n\n"
        "📅 " + datetime.now().strftime("%d.%m.%Y %H:%M")
    )


async def go_back(update, context):
    context.user_data.clear()
    await update.message.reply_text(
        "Asosiy menyu:",
        reply_markup=ReplyKeyboardMarkup(MENU_KB, resize_keyboard=True),
    )
    return MENU


async def start(update, context):
    await update.message.reply_text(
        "Assalomu alaykum!\n\n"
        "RIA Marketing jamoasiga ishga kirmoqchi bo'lganlar\n"
        "uchun ariza qabul qilamiz.",
        reply_markup=ReplyKeyboardMarkup(MENU_KB, resize_keyboard=True),
    )
    return MENU


async def menu_handler(update, context):
    text = update.message.text
    if "Hujjat" in text:
        await update.message.reply_text(
            "1/16 — Ism va familiyangizni kiriting:",
            reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
        )
        return NAME
    elif "haqimizda" in text:
        await update.message.reply_text(
            BIZ_HAQIMIZDA,
            reply_markup=ReplyKeyboardMarkup(MENU_KB, resize_keyboard=True),
        )
    return MENU


async def get_name(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        "2/16 — Telefon raqamingizni kiriting:\nMasalan: +998901234567",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return PHONE


async def get_phone(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["phone"] = update.message.text
    await update.message.reply_text(
        "3/16 — Kim bo'lib ishlamoqchisiz?",
        reply_markup=ReplyKeyboardMarkup(POSITION_KB, resize_keyboard=True),
    )
    return POSITION


async def get_position(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["position"] = update.message.text
    await update.message.reply_text(
        "4/16 — Tavallud topgan sanangizni kiriting:\nMasalan: 01.01.2000 (kun.oy.yil)",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return BIRTHDAY


async def get_birthday(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["birthday"] = update.message.text
    await update.message.reply_text(
        "5/16 — Rasmingizni yuboring:",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return PHOTO


async def get_photo(update, context):
    if update.message.photo:
        context.user_data["photo_id"] = update.message.photo[-1].file_id
    elif update.message.document:
        context.user_data["photo_id"] = update.message.document.file_id
    else:
        await update.message.reply_text(
            "Iltimos, rasm yuboring!",
            reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
        )
        return PHOTO
    await update.message.reply_text(
        "6/16 — Doimiy yashash manzilingizni kiriting:",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return ADDRESS


async def photo_text(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    await update.message.reply_text(
        "Iltimos, rasm yuboring!",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return PHOTO


async def get_address(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["address"] = update.message.text
    await update.message.reply_text(
        "7/16 — Ma'lumotingiz qanday?",
        reply_markup=ReplyKeyboardMarkup(EDUCATION_KB, resize_keyboard=True),
    )
    return EDUCATION


async def get_education(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["education"] = update.message.text
    await update.message.reply_text(
        "8/16 — Jinsingiz?",
        reply_markup=ReplyKeyboardMarkup(GENDER_KB, resize_keyboard=True),
    )
    return GENDER


async def get_gender(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["gender"] = update.message.text
    await update.message.reply_text(
        "9/16 — Oldin ishlagan ishxonangiz nomi?",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return PREV_WORK


async def get_prev_work(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["prev_work"] = update.message.text
    await update.message.reply_text(
        "10/16 — Oldin ishlagan lavozimingiz?",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return PREV_POSITION


async def get_prev_position(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["prev_position"] = update.message.text
    await update.message.reply_text(
        "11/16 — Oldingi ishingizda qancha muddat ishlagansiz?",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return PREV_DURATION


async def get_prev_duration(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["prev_duration"] = update.message.text
    await update.message.reply_text(
        "12/16 — Oldingi ishingizdan nima sabab bo'shagansiz?",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return PREV_REASON


async def get_prev_reason(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["prev_reason"] = update.message.text
    await update.message.reply_text(
        "13/16 — Oilalimisiz?",
        reply_markup=ReplyKeyboardMarkup(YES_NO_KB, resize_keyboard=True),
    )
    return FAMILY


async def get_family(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["family"] = update.message.text
    await update.message.reply_text(
        "14/16 — Qaysi chet tillarini bilasiz?",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return LANGUAGES


async def get_languages(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["languages"] = update.message.text
    await update.message.reply_text(
        "15/16 — Bizda qancha maosh olishni istaysiz?",
        reply_markup=ReplyKeyboardMarkup(SALARY_KB, resize_keyboard=True),
    )
    return SALARY


async def get_salary(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["salary"] = update.message.text
    await update.message.reply_text(
        "16/16 — O'zingiz haqingizda qisqacha ma'lumot bering va sizni nima uchun ishga olishimiz kerak? (3 ta fakt):",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return ABOUT


async def get_about(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["about"] = update.message.text
    d = context.user_data
    caption = (
        "Ma'lumotlaringizni tekshiring:\n\n"
        "Ism: "         + d.get("name","—")          + "\n"
        "Telefon: "     + d.get("phone","—")         + "\n"
        "Lavozim: "     + d.get("position","—")      + "\n"
        "Tug'ilgan: "   + d.get("birthday","—")      + "\n"
        "Manzil: "      + d.get("address","—")       + "\n"
        "Ma'lumot: "    + d.get("education","—")     + "\n"
        "Jinsi: "       + d.get("gender","—")        + "\n"
        "Ish joyi: "    + d.get("prev_work","—")   + "\n"
        "Oldingi lavozim: " + d.get("prev_position","—") + "\n"
        "Muddat: "      + d.get("prev_duration","—") + "\n"
        "Sabab: "       + d.get("prev_reason","—")   + "\n"
        "Oilaviy: "     + d.get("family","—")        + "\n"
        "Tillar: "      + d.get("languages","—")     + "\n"
        "Maosh: "       + d.get("salary","—")        + "\n"
        "Haqida: "      + d.get("about","—")         + "\n\n"
        "Shu ma'lumotlar to'g'rimi?"
    )
    await update.message.reply_photo(
        photo=d["photo_id"],
        caption=caption,
        reply_markup=ReplyKeyboardMarkup(CONFIRM_KB, one_time_keyboard=True, resize_keyboard=True),
    )
    return CONFIRM


async def confirm(update, context):
    if "noto'g'ri" in update.message.text or "Orqaga" in update.message.text:
        return await go_back(update, context)
    if "Ha" in update.message.text:
        d = context.user_data
        await context.bot.send_photo(
            chat_id=GROUP_ID,
            photo=d["photo_id"],
            caption=make_summary(d),
        )
        await update.message.reply_text(
            "Arizangiz qabul qilindi! Tez orada bog'lanamiz.",
            reply_markup=ReplyKeyboardMarkup(MENU_KB, resize_keyboard=True),
        )
    context.user_data.clear()
    return MENU


async def cancel(update, context):
    return await go_back(update, context)


def main():
    app = Application.builder().token(TOKEN).build()
    TEXT = filters.TEXT & ~filters.COMMAND
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU:          [MessageHandler(TEXT, menu_handler)],
            NAME:          [MessageHandler(TEXT, get_name)],
            PHONE:         [MessageHandler(TEXT, get_phone)],
            POSITION:      [MessageHandler(TEXT, get_position)],
            BIRTHDAY:      [MessageHandler(TEXT, get_birthday)],
            PHOTO:         [MessageHandler(filters.PHOTO | filters.Document.IMAGE, get_photo),
                           MessageHandler(TEXT, photo_text)],
            ADDRESS:       [MessageHandler(TEXT, get_address)],
            EDUCATION:     [MessageHandler(TEXT, get_education)],
            GENDER:        [MessageHandler(TEXT, get_gender)],
            PREV_WORK:     [MessageHandler(TEXT, get_prev_work)],
            PREV_POSITION: [MessageHandler(TEXT, get_prev_position)],
            PREV_DURATION: [MessageHandler(TEXT, get_prev_duration)],
            PREV_REASON:   [MessageHandler(TEXT, get_prev_reason)],
            FAMILY:        [MessageHandler(TEXT, get_family)],
            LANGUAGES:     [MessageHandler(TEXT, get_languages)],
            SALARY:        [MessageHandler(TEXT, get_salary)],
            ABOUT:         [MessageHandler(TEXT, get_about)],
            CONFIRM:       [MessageHandler(TEXT, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    print("Bot ishlamoqda...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
