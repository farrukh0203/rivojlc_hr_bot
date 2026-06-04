import logging, os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

(MENU, NAME, PHONE, POSITION, BIRTHDAY, NATIONALITY, ADDRESS,
 EDUCATION, GENDER, PREV_WORK, PREV_POSITION, PREV_DURATION,
 PREV_REASON, ABROAD, FAMILY, CRIMINAL, LANGUAGES, COMPUTER,
 SALARY, ABOUT, WHY, PHOTO, CONFIRM) = range(23)

TOKEN    = "8450077086:AAFyByDJazCWidwz4_z6-QViXQ-sCN5HYSM"
GROUP_ID = "-1003785938565"

MENU_KB = [["📋 Hujjat topshirish"], ["ℹ️ Biz haqimizda"]]
BACK_KB  = [["🔙 Orqaga"]]

POSITION_KB = [
    ["👩‍🏫 O'qituvchi", "📞 Call center xodimi"],
    ["🖥 Administrator", "👔 Boshqaruvchi (Manager)"],
    ["🔙 Orqaga"]
]
EDUCATION_KB = [
    ["📚 O'rta", "🎓 O'rta maxsus", "🏛 Oliy"],
    ["🔙 Orqaga"]
]
GENDER_KB = [["👨 Erkak", "👩 Ayol"], ["🔙 Orqaga"]]
YES_NO_KB = [["✅ Ha", "❌ Yo'q"], ["🔙 Orqaga"]]
SALARY_KB = [
    ["💵 3-5 mln", "💵 4-6 mln"],
    ["💵 5-8 mln", "💵 8 mlndan ko'p"],
    ["🔙 Orqaga"]
]
CONFIRM_KB = [["✅ Ha, to'g'ri", "❌ Yo'q, noto'g'ri"]]

BIZ_HAQIMIZDA = """🏫 Rivoj LC Jamoasi Haqida

Assalomu alaykum!
«Rivoj LC» — xorijiy tillarni o'qitishga ixtisoslashgan markaz.

🇸🇦 Arab tili
🇬🇧 Ingliz tili
🇰🇷 Koreys tili
🇷🇺 Rus tili

Malakali o'qituvchilar, zamonaviy o'quv muhiti va amaliy yondashuv.

🎯 Maqsadimiz:
Har bir o'quvchini o'rganayotgan tilida erkin so'zlay oladigan darajaga yetkazish.

📞 94 595 84 04

Hurmat bilan, Rivoj LC Jamoasi"""


def summary(d):
    return (
        "📋 Yangi ariza\n\n"
        "1. Ism familiyasi: " + d.get("name","—") + "\n"
        "2. Telefon: " + d.get("phone","—") + "\n"
        "3. Lavozim: " + d.get("position","—") + "\n"
        "4. Tugrilgan sana: " + d.get("birthday","—") + "\n"
        "5. Millat: " + d.get("nationality","—") + "\n"
        "6. Yashash manzili: " + d.get("address","—") + "\n"
        "7. Malumot: " + d.get("education","—") + "\n"
        "8. Jinsi: " + d.get("gender","—") + "\n"
        "9. Oldingi ish joyi: " + d.get("prev_work","—") + "\n"
        "10. Oldingi lavozim: " + d.get("prev_position","—") + "\n"
        "11. Ish muddati: " + d.get("prev_duration","—") + "\n"
        "12. Bosash sababi: " + d.get("prev_reason","—") + "\n"
        "13. Chet elda: " + d.get("abroad","—") + "\n"
        "14. Oilaviy holat: " + d.get("family","—") + "\n"
        "15. Sudlangan: " + d.get("criminal","—") + "\n"
        "16. Chet tillari: " + d.get("languages","—") + "\n"
        "17. Word/Excel: " + d.get("computer","—") + "\n"
        "18. Istalgan maosh: " + d.get("salary","—") + "\n"
        "19. Oz haqida: " + d.get("about","—") + "\n"
        "20. Nima uchun: " + d.get("why","—") + "\n\n"
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
        "Kompaniyamizga ishga kirmoqchi bolgan xodimlarni\n"
        "rezyumelarini shu bot orqali qabul qilamiz.",
        reply_markup=ReplyKeyboardMarkup(MENU_KB, resize_keyboard=True),
    )
    return MENU


async def menu_handler(update, context):
    text = update.message.text
    if "Hujjat" in text:
        await update.message.reply_text(
            "1/21 — Ism va familiyangizni kiriting:",
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
        "2/21 — Telefon raqamingizni kiriting:\nMasalan: +998901234567",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return PHONE


async def get_phone(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["phone"] = update.message.text
    await update.message.reply_text(
        "3/21 — Qaysi lavozimda ishlamoqchisiz?",
        reply_markup=ReplyKeyboardMarkup(POSITION_KB, resize_keyboard=True),
    )
    return POSITION


async def get_position(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["position"] = update.message.text
    await update.message.reply_text(
        "4/21 — Tavallud topgan sanangizni kiriting:\nMasalan: 01.01.2000 (kun.oy.yil)",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return BIRTHDAY


async def get_birthday(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["birthday"] = update.message.text
    await update.message.reply_text(
        "5/21 — Millatingiz?",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return NATIONALITY


async def get_nationality(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["nationality"] = update.message.text
    await update.message.reply_text(
        "6/21 — Doimiy yashash manzilingizni kiriting:",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return ADDRESS


async def get_address(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["address"] = update.message.text
    await update.message.reply_text(
        "7/21 — Malumotingiz qanday?",
        reply_markup=ReplyKeyboardMarkup(EDUCATION_KB, resize_keyboard=True),
    )
    return EDUCATION


async def get_education(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["education"] = update.message.text
    await update.message.reply_text(
        "8/21 — Jinsingiz?",
        reply_markup=ReplyKeyboardMarkup(GENDER_KB, resize_keyboard=True),
    )
    return GENDER


async def get_gender(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["gender"] = update.message.text
    await update.message.reply_text(
        "9/21 — Oldin ishlagan ishxonangiz nomi?",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return PREV_WORK


async def get_prev_work(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["prev_work"] = update.message.text
    await update.message.reply_text(
        "10/21 — Oldin ishlagan lavozimingiz?",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return PREV_POSITION


async def get_prev_position(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["prev_position"] = update.message.text
    await update.message.reply_text(
        "11/21 — Oldingi ishingizda qancha muddat ishlagansiz?",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return PREV_DURATION


async def get_prev_duration(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["prev_duration"] = update.message.text
    await update.message.reply_text(
        "12/21 — Oldingi ishingizdan nima sabab bosagansiz?",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return PREV_REASON


async def get_prev_reason(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["prev_reason"] = update.message.text
    await update.message.reply_text(
        "13/21 — Chet elda ishlaganmisiz?\n(Ha bolsa, qaysi davlatda va lavozimda?)",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return ABROAD


async def get_abroad(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["abroad"] = update.message.text
    await update.message.reply_text(
        "14/21 — Oilalimisiz?",
        reply_markup=ReplyKeyboardMarkup(YES_NO_KB, resize_keyboard=True),
    )
    return FAMILY


async def get_family(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["family"] = update.message.text
    await update.message.reply_text(
        "15/21 — Sudlanganmisiz?",
        reply_markup=ReplyKeyboardMarkup(YES_NO_KB, resize_keyboard=True),
    )
    return CRIMINAL


async def get_criminal(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["criminal"] = update.message.text
    await update.message.reply_text(
        "16/21 — Qaysi chet tillarini bilasiz?",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return LANGUAGES


async def get_languages(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["languages"] = update.message.text
    await update.message.reply_text(
        "17/21 — Word / Excelda ishlashni yaxshi bilasizmi?",
        reply_markup=ReplyKeyboardMarkup(YES_NO_KB, resize_keyboard=True),
    )
    return COMPUTER


async def get_computer(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["computer"] = update.message.text
    await update.message.reply_text(
        "18/21 — Bizda qancha maosh olishni istaysiz?",
        reply_markup=ReplyKeyboardMarkup(SALARY_KB, resize_keyboard=True),
    )
    return SALARY


async def get_salary(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["salary"] = update.message.text
    await update.message.reply_text(
        "19/21 — Ozingiz haqingizda qisqacha malumot bering:",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return ABOUT


async def get_about(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["about"] = update.message.text
    await update.message.reply_text(
        "20/21 — Sizni nima uchun ishga olishimiz kerak? (3 ta fakt):",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return WHY


async def get_why(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    context.user_data["why"] = update.message.text
    await update.message.reply_text(
        "21/21 — Rasmingizni yuboring:",
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

    d = context.user_data
    caption = (
        "Malumotlaringiz:\n\n"
        "Ism: " + d.get("name","—") + "\n"
        "Telefon: " + d.get("phone","—") + "\n"
        "Lavozim: " + d.get("position","—") + "\n"
        "Tug'ilgan sana: " + d.get("birthday","—") + "\n"
        "Millat: " + d.get("nationality","—") + "\n"
        "Manzil: " + d.get("address","—") + "\n"
        "Malumot: " + d.get("education","—") + "\n"
        "Jinsi: " + d.get("gender","—") + "\n\n"
        "Shu malumotlar toghrimi?"
    )
    await update.message.reply_photo(
        photo=d["photo_id"],
        caption=caption,
        reply_markup=ReplyKeyboardMarkup(CONFIRM_KB, one_time_keyboard=True, resize_keyboard=True),
    )
    return CONFIRM


async def photo_text(update, context):
    if "Orqaga" in update.message.text:
        return await go_back(update, context)
    await update.message.reply_text(
        "Iltimos, rasm yuboring!",
        reply_markup=ReplyKeyboardMarkup(BACK_KB, resize_keyboard=True),
    )
    return PHOTO


async def confirm(update, context):
    if "Orqaga" in update.message.text or "noto'g'ri" in update.message.text:
        return await go_back(update, context)
    if "Ha" in update.message.text:
        d = context.user_data
        await context.bot.send_photo(
            chat_id=GROUP_ID,
            photo=d["photo_id"],
            caption=summary(d),
        )
        await update.message.reply_text(
            "Arizangiz qabul qilindi! Tez orada boglanamiz.",
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
            NATIONALITY:   [MessageHandler(TEXT, get_nationality)],
            ADDRESS:       [MessageHandler(TEXT, get_address)],
            EDUCATION:     [MessageHandler(TEXT, get_education)],
            GENDER:        [MessageHandler(TEXT, get_gender)],
            PREV_WORK:     [MessageHandler(TEXT, get_prev_work)],
            PREV_POSITION: [MessageHandler(TEXT, get_prev_position)],
            PREV_DURATION: [MessageHandler(TEXT, get_prev_duration)],
            PREV_REASON:   [MessageHandler(TEXT, get_prev_reason)],
            ABROAD:        [MessageHandler(TEXT, get_abroad)],
            FAMILY:        [MessageHandler(TEXT, get_family)],
            CRIMINAL:      [MessageHandler(TEXT, get_criminal)],
            LANGUAGES:     [MessageHandler(TEXT, get_languages)],
            COMPUTER:      [MessageHandler(TEXT, get_computer)],
            SALARY:        [MessageHandler(TEXT, get_salary)],
            ABOUT:         [MessageHandler(TEXT, get_about)],
            WHY:           [MessageHandler(TEXT, get_why)],
            PHOTO:         [MessageHandler(filters.PHOTO | filters.Document.IMAGE, get_photo),
                           MessageHandler(TEXT, photo_text)],
            CONFIRM:       [MessageHandler(TEXT, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)
    print("Bot ishlamoqda...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
