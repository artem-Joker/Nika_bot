import os
import asyncio
import nest_asyncio
import together
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext

# Разрешаем асинхронный код в средах, которые его блокируют
nest_asyncio.apply()

# Получаем токены из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Проверяем, заданы ли переменные окружения
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN не задан! Укажите его в переменных окружения.")
if not TOGETHER_API_KEY:
    raise ValueError("❌ TOGETHER_API_KEY не задан! Укажите его в переменных окружения.")

# Настройка Together AI
together.api_key = TOGETHER_API_KEY

async def chat_with_gpt(update: Update, context: CallbackContext):
    user_message = update.message.text

    try:
        response = together.Complete.create(
            prompt=user_message,
            model="mistralai/Mistral-7B-Instruct",
            max_tokens=100
        )

        # Проверяем структуру ответа от Together AI
        bot_reply = response.get("output", {}).get("choices", [{}])[0].get("text", "Ответ не получен.")
    except Exception as e:
        bot_reply = f"Ошибка при запросе к Together AI: {str(e)}"

    await update.message.reply_text(bot_reply)

# Создаём Telegram-бота
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_gpt))

# Запуск бота
if __name__ == "__main__":
    print("✅ Бот с Together AI запущен!")
    asyncio.run(app.run_polling())