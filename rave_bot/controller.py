"""Telegram controller for the Rave Android app via Appium."""
import asyncio
import io
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from rave_android import RaveAndroid

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN", "")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "0"))
POLL_SECONDS = max(1.0, float(os.getenv("POLL_SECONDS", "3")))
COMMANDS = {"!ping": "pong", "!help": "Команды: !ping, !help"}
state = {"rave": None, "task": None, "room": None, "seen": set()}

def allowed(update: Update) -> bool:
    user = update.effective_user
    return bool(user) and user.id == ALLOWED_USER_ID

def match_command(text: str):
    lines = text.strip().lower().splitlines()
    if not lines or not lines[-1].split():
        return None
    return COMMANDS.get(lines[-1].split()[0])

async def ensure_app():
    if state["rave"] is None:
        state["rave"] = await asyncio.to_thread(RaveAndroid)

async def stop_watcher():
    task = state["task"]
    if task:
        task.cancel()
        state["task"] = None
        try:
            await task
        except asyncio.CancelledError:
            pass

async def watch_chat():
    while True:
        messages = await asyncio.to_thread(state["rave"].messages)
        for message in messages:
            if message in state["seen"]:
                continue
            state["seen"].add(message)
            if len(state["seen"]) > 500:
                state["seen"] = set(list(state["seen"])[-250:])
            reply = match_command(message)
            if reply:
                await asyncio.to_thread(state["rave"].send, reply)
        await asyncio.sleep(POLL_SECONDS)

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    await update.message.reply_text(
        "Rave Android-бот готов. Команды: /join <ссылка>, /say <текст>, "
        "/leave, /status, /screenshot, /dumpui.\n"
        "Чтение/отправка чата заработают только после настройки реальных селекторов в .env."
    )

async def cmd_join(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    if not ctx.args:
        await update.message.reply_text("Использование: /join https://rave.link/...")
        return
    try:
        await ensure_app()
        await stop_watcher()
        await asyncio.to_thread(state["rave"].join, ctx.args[0])
        state["room"] = ctx.args[0]
        state["seen"] = set()
        state["task"] = asyncio.create_task(watch_chat())
        await update.message.reply_text("Ссылка передана приложению Rave. Проверьте экран; чат заработает после настройки селекторов в .env.")
    except Exception as exc:
        await update.message.reply_text(f"Не удалось открыть комнату: {exc}")

async def cmd_say(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    if not state["rave"] or not state["room"]:
        await update.message.reply_text("Сначала используйте /join <ссылка>.")
        return
    message = " ".join(ctx.args).strip()
    if not message:
        await update.message.reply_text("Использование: /say <текст>")
        return
    try:
        await asyncio.to_thread(state["rave"].send, message)
        await update.message.reply_text("Команда отправки выполнена.")
    except Exception as exc:
        await update.message.reply_text(f"Не удалось отправить сообщение: {exc}")

async def cmd_leave(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    await stop_watcher()
    state["room"] = None
    if state["rave"]:
        await asyncio.to_thread(state["rave"].leave)
    await update.message.reply_text("Мониторинг остановлен. Приложение осталось открытым.")

async def cmd_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if allowed(update):
        await update.message.reply_text(
            f"Appium: {'подключён' if state['rave'] else 'не подключён'}\n"
            f"Комната: {state['room'] or 'не выбрана'}"
        )

async def cmd_screenshot(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    try:
        await ensure_app()
        png = await asyncio.to_thread(state["rave"].screenshot)
        await update.message.reply_photo(io.BytesIO(png))
    except Exception as exc:
        await update.message.reply_text(f"Ошибка скриншота: {exc}")

async def cmd_dumpui(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    try:
        await ensure_app()
        xml = await asyncio.to_thread(state["rave"].dump_ui)
        await update.message.reply_document(io.BytesIO(xml.encode("utf-8")), filename="rave_ui.xml", caption="XML интерфейса текущего экрана для настройки .env.")
    except Exception as exc:
        await update.message.reply_text(f"Не удалось получить интерфейс: {exc}")

def main():
    if not TOKEN or not ALLOWED_USER_ID:
        raise SystemExit("Укажите TELEGRAM_TOKEN и ALLOWED_USER_ID в .env")
    app = Application.builder().token(TOKEN).build()
    handlers = {
        "start": cmd_start, "join": cmd_join, "say": cmd_say,
        "leave": cmd_leave, "status": cmd_status,
        "screenshot": cmd_screenshot, "dumpui": cmd_dumpui,
    }
    for command, handler in handlers.items():
        app.add_handler(CommandHandler(command, handler))
    app.run_polling()

if __name__ == "__main__":
    main()
