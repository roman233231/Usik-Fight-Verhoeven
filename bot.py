import os
import asyncio
import logging
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get('TELEGRAM_TOKEN')
TARGET_LINK = "https://t.me/+MKhgI6IVr083NGIy"   # Ваше посилання на канал

# ========== ОБРОБНИК ЗАПИТІВ НА ПРИЄДНАННЯ ==========
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user = request.from_user
    user_name = user.first_name
    user_chat_id = request.user_chat_id

    logging.info(f"📥 Новий запит від {user_name} (ID: {user.id})")

    try:
        # Повідомлення 1
        await context.bot.send_message(
            chat_id=user_chat_id,
            text=f"🥊 {user_name.upper()}, ТИ ГОТОВИЙ ДО ГОЛОВНОГО БОЮ РОКУ?!\n\n"
                 f"🇺🇦 *ОЛЕКСАНДР УСИК* vs 🇳🇱 *РІКО ВЕРХОВЕН*\n"
                 f"🏆 Бій за звання абсолютного чемпіона світу\n"
                 f"📅 СЬОГОДНІ о 23:00 (Київ)\n\n"
                 f"🔥 Тільки у нашому каналі – ПРЯМИЙ ЕФІР без реклами та затримок!\n"
                 f"HD-якість, коментар українською, жодних маніпуляцій!",
            parse_mode='Markdown'
        )
        await asyncio.sleep(2.5)

        # Відправка фото (локальне або за замовчуванням)
# Кнопка під фото
photo_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("👉 ПЕРЕЙТИ В КАНАЛ", url=TARGET_LINK)]
])

# Відправка фото (локальне або за замовчуванням)
try:
    with open("Phot.jpg", "rb") as photo_file:
        await context.bot.send_photo(
            chat_id=user_chat_id,
            photo=photo_file,
            caption="🥊 *Усик vs Верховен – битва титанів!*\n👇 *ДИВИСЬ ТРАНСЛЯЦІЮ ТУТ* 👇",
            reply_markup=photo_keyboard,
            parse_mode='Markdown'
        )
except FileNotFoundError:
    try:
        with open("Phot.png", "rb") as photo_file:
            await context.bot.send_photo(
                chat_id=user_chat_id,
                photo=photo_file,
                caption="🥊 *Усик vs Верховен – битва титанів!*\n👇 *ДИВИСЬ ТРАНСЛЯЦІЮ ТУТ* 👇",
                reply_markup=photo_keyboard,
                parse_mode='Markdown'
            )
    except:
        await context.bot.send_message(
            chat_id=user_chat_chat_id,
            text="📸 *Постер бою Усик – Верховен*\n👉 [Перейти в канал з трансляцією]({})".format(TARGET_LINK),
            parse_mode='Markdown'
        )
        await asyncio.sleep(2)

        # Повідомлення 2
        await context.bot.send_message(
            chat_id=user_chat_id,
            text="🇺🇦 *ЧОМУ ТИ ПОВИНЕН ЦЕ ПОДИВИТИСЬ?*\n\n"
                 "✅ Прямий ефір у найкращій якості\n"
                 "✅ Безкоштовно та без реєстрації\n"
                 "✅ Коментатор – відомий спортивний журналіст\n"
                 "✅ Запис бою одразу після завершення\n\n"
                 "🎁 *БОНУС:* перші 500 глядачів отримають відео з найкращими моментами та аналітику.",
            parse_mode='Markdown'
        )
        await asyncio.sleep(2.5)

        # Повідомлення 3 (кнопка)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚨 ОТРИМАТИ ДОСТУП ДО ЕФІРУ 🚨", url=TARGET_LINK)]
        ])
        await context.bot.send_message(
            chat_id=user_chat_id,
            text="⏰ *ДО ПОЧАТКУ БОЮ ЗАЛИШИЛОСЬ МЕНШЕ ГОДИНИ!*\n\n"
                 "❗ Посилання активне ТІЛЬКИ 15 хвилин після старту\n"
                 "❗ Канал закриється після набору 10 000 глядачів\n"
                 "❗ Не натиснеш зараз – пропустиш історичний бій!\n\n"
                 "👇 *ТИСНИ ТУТ І ЗАБИРАЙ СВОЄ МІСЦЕ* 👇",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        await asyncio.sleep(2)

        # Повідомлення 4 (останнє)
        await context.bot.send_message(
            chat_id=user_chat_id,
            text="💣 *ОСТАННЄ ПОПЕРЕДЖЕННЯ!*\n\n"
                 "За 5 хвилин до початку ми видаляємо всіх, хто не підтвердив перегляд.\n"
                 "Ти втратиш шанс побачити:\n"
                 "❌ Нокаут року\n"
                 "❌ Емоції Усика після перемоги\n"
                 "❌ Історичний пояс абсолютного чемпіона\n\n"
                 "🔥 *ЗАРАЗ АБО НІКОЛИ!* 🔥\n"
                 "👉 [ПЕРЕЙТИ В КАНАЛ]({})".format(TARGET_LINK),
            parse_mode='Markdown'
        )

        logging.info(f"✅ Агітаційний спам про бій Усик–Верховен надіслано {user_name}")

    except Exception as e:
        logging.warning(f"❌ Не вдалося надіслати {user_name}: {e}")

# ========== ФЛask ДЛЯ HEALTH CHECK ==========
flask_app = Flask(__name__)

@flask_app.route('/')
@flask_app.route('/healthz')
def health_check():
    return "OK", 200

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    flask_app.run(host='0.0.0.0', port=port, threaded=False)

# ========== ОСНОВНА ФУНКЦІЯ ==========
def main():
    # Запускаємо Flask в окремому потоці (щоб він не блокував бота)
    threading.Thread(target=run_flask).start()

    # ВИПРАВЛЕННЯ ПОМИЛКИ ЦИКЛУ ПОДІЙ
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    # Telegram бот
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    logging.info("🚀 Бот запущено. Агітуємо за бій Усик – Верховен!")
    app.run_polling()

if __name__ == "__main__":
    main()
