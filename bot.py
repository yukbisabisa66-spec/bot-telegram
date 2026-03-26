import os
import logging
from datetime import time, datetime
from zoneinfo import ZoneInfo

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN") or "TOKEN_BOT_KAMU"

# ====== DAFTAR USER (TIDAK DIUBAH) ======
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

# ====== STORAGE ======
logged_in_users = {}
user_states = {}

# ====== MENU ======
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

# ====== BUTTON TAMBAHAN ======
def absen_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Sudah", callback_data="absen_sudah"),
         InlineKeyboardButton("❌ Belum", callback_data="absen_belum")]
    ])

def lembur_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Ya", callback_data="lembur_ya"),
         InlineKeyboardButton("Tidak", callback_data="lembur_tidak")]
    ])

def rating_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⭐1", callback_data="rate_1"),
            InlineKeyboardButton("⭐2", callback_data="rate_2"),
            InlineKeyboardButton("⭐3", callback_data="rate_3"),
            InlineKeyboardButton("⭐4", callback_data="rate_4"),
            InlineKeyboardButton("⭐5", callback_data="rate_5"),
        ]
    ])

# ====== START ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if chat_id in logged_in_users:
        nama = logged_in_users[chat_id]
        await update.message.reply_text(
            f"Halo {nama}, kamu sudah login.",
            reply_markup=generate_buttons()
        )
    else:
        await update.message.reply_text("Masukkan Nomor User:")

# ====== LOGIN ======
async def verify_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nomor = update.message.text.strip()
    chat_id = update.effective_chat.id

    if nomor in USERS:
        nama = USERS[nomor]
        logged_in_users[chat_id] = nama
        user_states[chat_id] = {"absen": False}

        await update.message.reply_text(
            f"Selamat datang {nama} 👋",
            reply_markup=generate_buttons()
        )
    else:
        await update.message.reply_text("Nomor tidak valid!")

# ====== HANDLE BUTTON ======
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    data = query.data

    if data == "absen_sudah":
        user_states[chat_id]["absen"] = True
        await query.edit_message_text("✅ Selamat bekerja dengan semangat 💪")

    elif data == "absen_belum":
        user_states[chat_id]["absen"] = True
        await query.edit_message_text("⚠️ Mohon absen terlebih dahulu")

    elif data == "lembur_ya":
        await query.edit_message_text("Silakan menyelesaikan berkasnya 👍")

    elif data == "lembur_tidak":
        await query.edit_message_text("Baik, terima kasih 😊")

    elif data.startswith("rate"):
        await query.edit_message_text("Terima kasih atas penilaiannya 🙏")

# ====== RESET ABSEN ======
async def reset_absen(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in user_states:
        user_states[chat_id]["absen"] = False

# ====== ABSEN LOOP ======
async def broadcast_absen(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(ZoneInfo("Asia/Makassar"))

    if now.weekday() >= 5:
        return

    for chat_id in logged_in_users:
        if not user_states.get(chat_id, {}).get("absen", False):
            await context.bot.send_message(
                chat_id=chat_id,
                text="Apakah anda sudah absen hari ini?",
                reply_markup=absen_buttons()
            )

# ====== LEMBUR ======
async def broadcast_lembur(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(ZoneInfo("Asia/Makassar"))

    if now.day == 28:
        for chat_id in logged_in_users:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Apakah anda memiliki berkas lemburan bulan ini?",
                reply_markup=lembur_buttons()
            )

# ====== RATING ======
async def broadcast_rating(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(ZoneInfo("Asia/Makassar"))

    if now.weekday() < 5:
        for chat_id in logged_in_users:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Berapa bintang untuk hari ini?",
                reply_markup=rating_buttons()
            )

# ====== MAIN ======
if __name__ == "__main__":
    app = ApplicationBuilder().token("8651214459:AAHcuHXpdi85t9Z_54gctt-h5kqTfvnfhFA").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), verify_user))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    tz = ZoneInfo("Asia/Makassar")

    # ABSEN LOOP
    for m in range(0, 31, 5):
        app.job_queue.run_daily(
            broadcast_absen,
            time=time(hour=7, minute=m, tzinfo=tz)
        )

    # RESET
    app.job_queue.run_daily(
        reset_absen,
        time=time(hour=0, minute=0, tzinfo=tz)
    )

    # LEMBUR
    app.job_queue.run_daily(
        broadcast_lembur,
        time=time(hour=10, minute=0, tzinfo=tz)
    )

    # RATING
    app.job_queue.run_daily(
        broadcast_rating,
        time=time(hour=17, minute=0, tzinfo=tz)
    )

    print("Bot berjalan...")
    app.run_polling()
