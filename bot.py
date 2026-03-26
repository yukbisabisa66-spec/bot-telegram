from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters, CallbackQueryHandler
)
from datetime import time
import pytz
import os

# ====== TOKEN ======
TOKEN = os.getenv("BOT_TOKEN")  # pakai env (AMAN)

# ====== TIMEZONE GMT+8 ======
timezone = pytz.timezone("Asia/Makassar")

# ====== DATA USER ======
USERS = {
    "220051100518": "NI MADE MEGA SISWANTI",
    "220240605152": "MUHAMMAD RAVI MAHENDRA",
    "220230204615": "ANISA FAEDATUL WAROHMAH",
    "220240605150": "MUHAMMAD TAUFIK ENLIANA PUTRA",
    "220250205531": "PRITA ASMINITYA SARI",
    "220230604695": "DESHINTA SELLA WOTULUNG",
    "220230604696": "LYGIA SYALOOMITA MESOINO",
    "220250205534": "MUHAMMAD IQBAL FALDI",
    "219940400200": "LELY FARIAL",
    "220230604692": "LITA TIARA PUTRI",
    "220240605157": "AFRIZA RAMADHONA PATIENCE",
    "220250205533": "RIZKY DARMAWAN",
    "220250205535": "INNE FEBBIYA DEWI",
    "220230604694": "SULISTI RIYANI",
    "220250205536": "AHKLIS SUKMA PRANESTI",
    "220240605160": "HESTI PEBRIANI",
    "220240605161": "DHITA SEPTIANTI KHAIRUNISA",
    "220240605156": "MISBATUL AMANAH",
    "220250205529": "ELSHYA ARIS PARENDEN",
    "220230604698": "FEBY TRI AMANDA",
    "220240104960": "AYU ARIFIANTI SAFITRI",
    "220240605149": "HESTI DWI PUTERI HASANAH IRMAN",
    "220240605151": "FELLY NABILLA FARADILLA",
    "220240605158": "NURUL AINI",
    "220240605155": "MASRURO",
    "220230604699": "ROSA OCTAVIANI",
    "220250205537": "NURUL",
    "220240605162": "MERLIN BEKA",
    "220240605159": "YESSY ALFA CHRISTOFFEL",
    "220240605154": "ELLA OKTAVIANI",
    "220250205532": "DIKY FIRMANSYAH",
    "220230204616": "YAYANG DWI SETIYA MINARTI"
}

# ====== LOGIN SESSION ======
logged_in_users = set()

# ====== TOMBOL ======
def generate_buttons():
    keyboard = [
        [InlineKeyboardButton("SiKEPI", url="https://sikepi.bankaltimtara.co.id/"),
         InlineKeyboardButton("SIMBADA", url="http://172.16.100.14/")],
        [InlineKeyboardButton("HCIS", url="http://172.16.98.11/"),
         InlineKeyboardButton("DGBO", url="https://dgbo.bankaltimtara.co.id/")],
        [InlineKeyboardButton("ASKRIDA", url="http://10.30.100.141/monitoring_asuransi/login.php"),
         InlineKeyboardButton("QUIZ", url="http://172.16.100.10/quiz/front/index.php?page=login&aksi=login_proses")],
        [InlineKeyboardButton("TRIC", url="http://172.16.100.10/tric/"),
         InlineKeyboardButton("SP2DOL", url="https://sipd-sp2d.bankaltimtara.co.id/user-management/auth/login")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== START ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo! Silakan masukkan Nomor User kamu:")

# ====== LOGIN ======
async def verify_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nomor = update.message.text.strip()
    chat_id = update.effective_chat.id

    if nomor in USERS:
        logged_in_users.add(chat_id)
        await update.message.reply_text(
            f"Selamat datang, {USERS[nomor]}!",
            reply_markup=generate_buttons()
        )
    else:
        await update.message.reply_text("Nomor tidak valid, coba lagi:")

# ====== COMMAND TOMBOL ======
async def tombol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id in logged_in_users:
        await update.message.reply_text("Menu:", reply_markup=generate_buttons())
    else:
        await update.message.reply_text("Silakan login dulu.")

# ====== LOGOUT ======
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logged_in_users.discard(chat_id)
    await update.message.reply_text("Kamu sudah logout.")

# ====== REMINDER PAGI ======
async def morning_reminder(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in logged_in_users:
        await context.bot.send_message(chat_id, "Apakah anda sudah absen pagi ini?")

# ====== REMINDER BULANAN ======
async def end_month_reminder(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in logged_in_users:
        await context.bot.send_message(
            chat_id,
            "Sudah akhir bulan nih, apakah anda memiliki berkas lemburan yang belum di selesaikan?"
        )

# ====== REMINDER SORE + RATING ======
async def evening_check(context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("⭐1", callback_data="rate_1"),
        InlineKeyboardButton("⭐2", callback_data="rate_2"),
        InlineKeyboardButton("⭐3", callback_data="rate_3"),
        InlineKeyboardButton("⭐4", callback_data="rate_4"),
        InlineKeyboardButton("⭐5", callback_data="rate_5"),
    ]]
    for chat_id in logged_in_users:
        await context.bot.send_message(
            chat_id,
            "Berapa level bahagiamu hari ini?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ====== HANDLE RATING ======
async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    rating = query.data.split("_")[1]
    await query.edit_message_text(f"Terima kasih! Kamu memilih ⭐{rating}")

# ====== ERROR HANDLER ======
async def error_handler(update, context):
    print("Error:", context.error)

# ====== MAIN ======
if __name__ == "__main__":
    app = ApplicationBuilder().token(8651214459:AAEGFEpZjXz6GBAn9lijvN1esIpywkFFfu4).build()

    # Handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tombol", tombol))
    app.add_handler(CommandHandler("logout", logout))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), verify_user))
    app.add_handler(CallbackQueryHandler(handle_rating))

    app.add_error_handler(error_handler)

    # ====== SCHEDULER ======
    app.job_queue.run_daily(
        morning_reminder,
        time=time(7, 0, tzinfo=timezone),
        days=(0,1,2,3,4)
    )

    app.job_queue.run_monthly(
        end_month_reminder,
        when=time(7, 0, tzinfo=timezone),
        day=28
    )

    app.job_queue.run_daily(
        evening_check,
        time=time(17, 0, tzinfo=timezone),
        days=(0,1,2,3,4)
    )

    print("Bot berjalan...")
    app.run_polling()