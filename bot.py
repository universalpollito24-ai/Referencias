"""
Bot de Telegram - Refes Bot
Instalación: pip install python-telegram-bot
Ejecutar:    python bot.py
"""

import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LinkPreviewOptions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# ─── CONFIGURACIÓN ───────────────────────────────────────────────────────────
BOT_TOKEN   = "8730119287:AAHj1bUtqntoTVqcm39osQYP42grYZsieWA"
CHANNEL_ID  = -1003553327894

URL_INFORMACION = "https://t.me/+Ws1jikVGAxQ3YTYx"
URL_ADQUIRIR    = "https://t.me/PollixUnivers"

REFE_TRIGGERS = {"/refe", ".refe", "$refe", "!refe", ";refe"}
# ─────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_keyboard():
    """Botones sin emoji de flecha, igual al original."""
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("INFORMACION", url=URL_INFORMACION),
        InlineKeyboardButton("ADQUIRIR!",   url=URL_ADQUIRIR),
    ]])


def time_str():
    return datetime.now().strftime("%I:%M:%S %p")


def get_message_text(msg) -> str:
    """Extrae el texto o caption de un mensaje. Si no tiene, devuelve vacío."""
    if msg.text:
        return msg.text
    if msg.caption:
        return msg.caption
    return ""


# ─── /start ──────────────────────────────────────────────────────────────────
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
        link_preview_options=LinkPreviewOptions(is_disabled=True)
    )


# ─── Manejador unificado para todos los triggers ──────────────────────────────
async def handle_refe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message or not message.text:
        return

    trigger = message.text.strip().split()[0].lower()
    if trigger not in REFE_TRIGGERS:
        return

    user = update.effective_user

    # ── Sin mensaje respondido ────────────────────────────────────────────────
    if not message.reply_to_message:
        text = (
            "<b>❆ Use it correctly #Nigga\n"
            "↳ Use Reply Message\n"
            "↳ Command: </b><code>$refe</code>"
        )
        await message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=get_keyboard())
        return

    # ── Confirmación en el grupo (igual al original) ──────────────────────────
    confirm = (
        "<b>❆ Use it correctly #Nigga\n"
        "• #YOUR REFERENCE HAS BEEN\n"
        "SUCCESSFULLY SENT, </b><code>PENDING  PAROVAL\n"
        "OR  DENIAL</code><b>. REMEMBER, IF YOU USE THE\n"
        "BOT WITH BAD INTENTIONS YOU WILL BE\n"
        "CUMMED</b>"
    )
    await message.reply_text(confirm, parse_mode=ParseMode.HTML, reply_markup=get_keyboard())

    # ── Armar plantilla del canal ─────────────────────────────────────────────
    target      = message.reply_to_message
    target_user = target.from_user

    # DEBUG: ver qué usuario está detectando
    logger.info(f"[DEBUG] Quien ejecutó /refe: {user.username} ({user.id})")
    logger.info(f"[DEBUG] from_user del mensaje respondido: {target_user}")
    if target.forward_origin:
        logger.info(f"[DEBUG] forward_origin: {target.forward_origin}")

    mention = f"@{target_user.username}" if target_user and target_user.username else f"{target_user.full_name if target_user else 'Desconocido'}"

    msg_content = get_message_text(target)
    if not msg_content:
        msg_content = "Message Not Found"

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
            await context.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=target.photo[-1].file_id,
                caption=canal_text,
                parse_mode=ParseMode.HTML,
                reply_markup=get_keyboard()
            )
        elif target.video:
            await context.bot.send_video(
                chat_id=CHANNEL_ID,
                video=target.video.file_id,
                caption=canal_text,
                parse_mode=ParseMode.HTML,
                reply_markup=get_keyboard()
            )
        elif target.document:
            await context.bot.send_document(
                chat_id=CHANNEL_ID,
                document=target.document.file_id,
                caption=canal_text,
                parse_mode=ParseMode.HTML,
                reply_markup=get_keyboard()
            )
        elif target.sticker:
            await context.bot.forward_message(
                chat_id=CHANNEL_ID,
                from_chat_id=update.effective_chat.id,
                message_id=target.message_id
            )
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=canal_text,
                parse_mode=ParseMode.HTML,
                reply_markup=get_keyboard()
            )
        else:
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=canal_text,
                parse_mode=ParseMode.HTML,
                reply_markup=get_keyboard()
            )

        logger.info(f"Referencia publicada por {user.full_name}")

    except Exception as e:
        logger.error(f"Error al publicar: {e}")
        await message.reply_text(
            f"❌ Error al enviar al canal:\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )


# ─── Main ─────────────────────────────────────────────────────────────────────
# Para que el bot NO se detenga al cerrar Termux, ejecútalo así:
#   1. Instala tmux:     pkg install tmux
#   2. Abre sesión:      tmux new -s bot
#   3. Corre el bot:     python bot.py
#   4. Sal sin cerrar:   Ctrl+B, luego D
#   5. Para volver:      tmux attach -t bot
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

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("refe",  handle_refe))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_refe))

    logger.info("Bot iniciado correctamente")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        poll_interval=0.0,
        timeout=10
    )


if __name__ == "__main__":
    main()
