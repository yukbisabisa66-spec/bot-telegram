from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ====== DAFTAR USER ======
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

# ====== LOGIN USER (SIMPAN NAMA) ======
logged_in_users = {}

# ====== TOMBOL MENU ======
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
    chat_id = update.effective_chat.id

    if chat_id in logged_in_users:
        nama = logged_in_users[chat_id]
        await update.message.reply_text(
            f"Halo {nama}, kamu sudah login. Silakan pilih menu:",
            reply_markup=generate_buttons()
        )
    else:
        await update.message.reply_text(
            "Hallo, silakan masukkan Nomor User kamu:"
        )

# ====== VERIFIKASI USER ======
async def verify_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nomor = update.message.text.strip()
    chat_id = update.effective_chat.id

    if nomor in USERS:
        nama = USERS[nomor]
        logged_in_users[chat_id] = nama

        await update.message.reply_text(
            f"Selamat datang, {nama}! Kamu sekarang bisa menggunakan menu di bawah.",
            reply_markup=generate_buttons()
        )
    else:
        await update.message.reply_text(
            "Nomor tidak valid. Silakan masukkan nomor user lagi:"
        )

# ====== COMMAND INFO ======
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if chat_id in logged_in_users:
        nama = logged_in_users[chat_id]

        await update.message.reply_text(
            f"Halo {nama}, silakan pilih menu:",
            reply_markup=generate_buttons()
        )
    else:
        await update.message.reply_text(
            "Silakan login dulu dengan memasukkan Nomor User."
        )

# ====== MAIN ======
if __name__ == "__main__":
    app = ApplicationBuilder().token("8651214459:AAE4kaN2hWPZxkR0whp03WVBY2oALssRX80").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), verify_user))

    print("Bot berjalan...")
    app.run_polling()
