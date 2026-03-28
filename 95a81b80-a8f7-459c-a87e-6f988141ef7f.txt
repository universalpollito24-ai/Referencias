"""
Bot Unificado - Refes Bot + Gay/Hetero/Pan
Instalación: pip install python-telegram-bot==21.9 Pillow
Ejecutar:    python bot_unificado.py
"""

import logging
import random
import io
from datetime import datetime
from PIL import Image, ImageDraw
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# ─── CONFIGURACIÓN ───────────────────────────────────────────────
BOT_TOKEN  = "8730119287:AAHj1bUtqntoTVqcm39osQYP42grYZsieWA"
CHANNEL_ID = -1003553327894

URL_INFORMACION = "https://t.me/+Ws1jikVGAxQ3YTYx"
URL_ADQUIRIR    = "https://t.me/PollixUnivers"

PREFIJOS = [".", "/", ";", "!", "$", "#", "?", "-"]

USUARIO_ESPECIAL = 8332343166
# ─────────────────────────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ─── UTILIDADES ──────────────────────────────────────────────────

def get_keyboard():
    btn_info = InlineKeyboardButton("INFORMACION", url=URL_INFORMACION).to_dict()
    btn_info["style"] = "success"
    btn_info["icon_custom_emoji_id"] = "5458603043203327669"

    btn_adq = InlineKeyboardButton("ADQUIRIR!", url=URL_ADQUIRIR).to_dict()
    btn_adq["style"] = "danger"
    btn_adq["icon_custom_emoji_id"] = "5231005931550030290"

    return {"inline_keyboard": [[btn_info, btn_adq]]}

def time_str():
    return datetime.now().strftime("%I:%M:%S %p")

def get_message_text(msg) -> str:
    if msg.text:
        return msg.text
    if msg.caption:
        return msg.caption
    return ""

def es_comando(text: str, comando: str) -> bool:
    for prefijo in PREFIJOS:
        if text.startswith(prefijo + comando):
            return True
    return False

def porcentaje_gay(user_id: int) -> int:
    if user_id == USUARIO_ESPECIAL:
        return random.randint(0, 25)
    return random.randint(0, 100)

def porcentaje_hetero(user_id: int) -> int:
    if user_id == USUARIO_ESPECIAL:
        return random.randint(75, 100)
    return random.randint(0, 100)

def porcentaje_pan(user_id: int) -> int:
    if user_id == USUARIO_ESPECIAL:
        return random.randint(75, 100)
    return random.randint(0, 100)


# ─── GENERADORES DE IMAGEN ───────────────────────────────────────

def crear_bandera_gay() -> io.BytesIO:
    ancho, alto = 800, 400
    img = Image.new("RGB", (ancho, alto))
    draw = ImageDraw.Draw(img)
    colores = [
        (228, 3, 3),
        (255, 140, 0),
        (255, 237, 0),
        (0, 128, 38),
        (0, 76, 255),
        (115, 41, 130),
    ]
    franja_alto = alto // len(colores)
    for i, color in enumerate(colores):
        y0 = i * franja_alto
        y1 = y0 + franja_alto if i < len(colores) - 1 else alto
        draw.rectangle([0, y0, ancho, y1], fill=color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def crear_bandera_hetero() -> io.BytesIO:
    ancho, alto = 800, 400
    img = Image.new("RGB", (ancho, alto))
    draw = ImageDraw.Draw(img)
    colores = [
        (0, 0, 0),
        (64, 64, 64),
        (105, 105, 105),
        (128, 128, 128),
        (169, 169, 169),
        (211, 211, 211),
        (255, 255, 255),
    ]
    franja_alto = alto // len(colores)
    for i, color in enumerate(colores):
        y0 = i * franja_alto
        y1 = y0 + franja_alto if i < len(colores) - 1 else alto
        draw.rectangle([0, y0, ancho, y1], fill=color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def crear_imagen_pan() -> io.BytesIO:
    ancho, alto = 800, 500
    img = Image.new("RGB", (ancho, alto), (245, 222, 179))
    draw = ImageDraw.Draw(img)
    draw.ellipse([120, 270, 680, 430], fill=(160, 100, 40))
    draw.ellipse([100, 150, 700, 400], fill=(205, 133, 63))
    draw.ellipse([130, 130, 670, 320], fill=(222, 160, 70))
    draw.ellipse([200, 140, 500, 240], fill=(240, 195, 100))
    draw.arc([150, 180, 650, 370], start=200, end=340, fill=(150, 80, 30), width=8)
    draw.arc([110, 160, 350, 390], start=150, end=210, fill=(170, 95, 35), width=5)
    draw.arc([450, 160, 690, 390], start=330, end=390, fill=(170, 95, 35), width=5)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


# ─── HANDLERS ────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user     = update.effective_user
    username = f"@{user.username}" if user.username else user.full_name
    text = (
        "<b>❆ Welcome To #Refes_Bot!</b>\n\n"
        f"<b>[🇺🇸] Welcome ({username}) to my project's #official referral bot. If you're Black, please leave the chat. #Thank you. Stupid Nigga</b>\n"
        "<b>╸╸╸╸╸╸╸╸╸╸╸╸</b>\n"
        f'<b><a href="https://t.me/PollixUnivers">𖥻</a> Curret Time: </b><code>{time_str()}</code><b>  -  🌤</b>'
    )
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_keyboard(),
        disable_web_page_preview=True
    )


# Handlers dedicados para /gay /hetero /pan (comandos con /)
async def cmd_gay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id    = update.effective_user.id
    porcentaje = porcentaje_gay(user_id)
    caption    = f"*Woo\! Eres un total de* `{porcentaje}%` *\U0001f3f3\ufe0f\u200d\U0001f308*"
    await update.message.reply_photo(photo=crear_bandera_gay(), caption=caption, parse_mode="MarkdownV2")

async def cmd_hetero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id    = update.effective_user.id
    porcentaje = porcentaje_hetero(user_id)
    caption    = f"*Eres un* `{porcentaje}%` *Hetero \U0001f3f3\ufe0f*"
    await update.message.reply_photo(photo=crear_bandera_hetero(), caption=caption, parse_mode="MarkdownV2")

async def cmd_pan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id    = update.effective_user.id
    porcentaje = porcentaje_pan(user_id)
    caption    = f"*Waos\! Eres* `{porcentaje}%` *pansito \U0001f35e*"
    await update.message.reply_photo(photo=crear_imagen_pan(), caption=caption, parse_mode="MarkdownV2")


async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message or not message.text:
        return

    text    = message.text.strip()
    textl   = text.lower()
    trigger = textl.split()[0]
    user_id = update.effective_user.id

    # ── refe ─────────────────────────────────────────────────────
    if es_comando(trigger, "refe"):
        user = update.effective_user
        if not message.reply_to_message:
            resp = (
                "<b>❆ Use it correctly #Nigga\n"
                "↳ Use Reply Message\n"
                "↳ Command: </b><code>$refe</code>"
            )
            await message.reply_text(resp, parse_mode=ParseMode.HTML, reply_markup=get_keyboard())
            return

        confirm = (
            "<b>❆ Use it correctly #Nigga\n"
            "• #YOUR REFERENCE HAS BEEN\n"
            "SUCCESSFULLY SENT, </b><code>PENDING  PAROVAL\n"
            "OR  DENIAL</code><b>. REMEMBER, IF YOU USE THE\n"
            "BOT WITH BAD INTENTIONS YOU WILL BE\n"
            "CUMMED</b>"
        )
        await message.reply_text(confirm, parse_mode=ParseMode.HTML, reply_markup=get_keyboard())

        target      = message.reply_to_message
        target_user = target.from_user
        mention     = f"@{target_user.username}" if target_user and target_user.username else (target_user.full_name if target_user else "Desconocido")
        msg_content = get_message_text(target) or "Message Not Found"

        canal_text = (
            "<b>( ✿ ) ¡Nueva Referencia! ( ✿ )\n"
            "────────────────────\n"
            f"( ★ ) Mensaje: {msg_content}\n"
            f"( ★ ) name: {mention}\n"
            f'<a href="https://t.me/PollixUnivers">𖥻</a> • Time: </b><code>{time_str()}</code><b> - ☀️\n'
            "────────────────────</b>"
        )

        try:
            if target.photo:
                await context.bot.send_photo(chat_id=CHANNEL_ID, photo=target.photo[-1].file_id, caption=canal_text, parse_mode=ParseMode.HTML, reply_markup=get_keyboard())
            elif target.video:
                await context.bot.send_video(chat_id=CHANNEL_ID, video=target.video.file_id, caption=canal_text, parse_mode=ParseMode.HTML, reply_markup=get_keyboard())
            elif target.document:
                await context.bot.send_document(chat_id=CHANNEL_ID, document=target.document.file_id, caption=canal_text, parse_mode=ParseMode.HTML, reply_markup=get_keyboard())
            elif target.sticker:
                await context.bot.forward_message(chat_id=CHANNEL_ID, from_chat_id=update.effective_chat.id, message_id=target.message_id)
                await context.bot.send_message(chat_id=CHANNEL_ID, text=canal_text, parse_mode=ParseMode.HTML, reply_markup=get_keyboard())
            else:
                await context.bot.send_message(chat_id=CHANNEL_ID, text=canal_text, parse_mode=ParseMode.HTML, reply_markup=get_keyboard())
            logger.info(f"Referencia publicada por {user.full_name}")
        except Exception as e:
            logger.error(f"Error al publicar: {e}")
            await message.reply_text(f"❌ Error al enviar al canal:\n<code>{e}</code>", parse_mode=ParseMode.HTML)

    # ── gay (prefijos no /) ───────────────────────────────────────
    elif es_comando(textl, "gay"):
        porcentaje = porcentaje_gay(user_id)
        caption    = f"*Woo\! Eres un total de* `{porcentaje}%` *\U0001f3f3\ufe0f\u200d\U0001f308*"
        await message.reply_photo(photo=crear_bandera_gay(), caption=caption, parse_mode="MarkdownV2")

    # ── hetero ───────────────────────────────────────────────────
    elif es_comando(textl, "hetero"):
        porcentaje = porcentaje_hetero(user_id)
        caption    = f"*Eres un* `{porcentaje}%` *Hetero \U0001f3f3\ufe0f*"
        await message.reply_photo(photo=crear_bandera_hetero(), caption=caption, parse_mode="MarkdownV2")

    # ── pan ──────────────────────────────────────────────────────
    elif es_comando(textl, "pan"):
        porcentaje = porcentaje_pan(user_id)
        caption    = f"*Waos\! Eres* `{porcentaje}%` *pansito \U0001f35e*"
        await message.reply_photo(photo=crear_imagen_pan(), caption=caption, parse_mode="MarkdownV2")


# ─── MAIN ────────────────────────────────────────────────────────
def main():
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .pool_timeout(30)
        .get_updates_read_timeout(30)
        .get_updates_write_timeout(30)
        .get_updates_connect_timeout(30)
        .build()
    )

    # Comandos con /
    app.add_handler(CommandHandler("start",  cmd_start))
    app.add_handler(CommandHandler("gay",    cmd_gay))
    app.add_handler(CommandHandler("hetero", cmd_hetero))
    app.add_handler(CommandHandler("pan",    cmd_pan))
    app.add_handler(CommandHandler("refe",   handle_all))

    # Mensajes de texto (para . $ ; ! etc)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all))

    logger.info("✅ Bot unificado iniciado")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        poll_interval=0.0,
        timeout=10
    )


if __name__ == "__main__":
    main()
    
