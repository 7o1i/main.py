import nest_asyncio
nest_asyncio.apply()

from telegram.ext import ApplicationBuilder
from handlers import start, receive_message
from config import TOKEN

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message))

    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())
