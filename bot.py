import os
import asyncio
import logging
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get('TELEGRAM_TOKEN')

# ⬇️ ПОСИЛАННЯ (тепер 4)
TARGET_LINK1 = "https://t.me/+BGaqXaUv76cxMzI6"   # для кнопок у повідомленні №4
TARGET_LINK2 = "https://t.me/+XOEUvi8O2T41NmVi"   # для текстового лінка в №5
TARGET_LINK3 = "https://t.me/+uYn5wvOhlixiNDUx"   # для кнопки під фото в №2
TARGET_LINK4 = "https://t.me/+1YU558QhfZphMzJi"   # НОВЕ посилання для додаткового повідомлення

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user = request.from_user
    user_name = user.first_name
    user_chat_id = request.user_chat_id

    logging.info(f"📥 Новий запит від {user_name} (ID: {user.id})")

    try:
        # ---------- ПОВІДОМЛЕННЯ №1 (текст + ВСІ 4 ПОСИЛАННЯ) ----------
        await context.bot.send_message(
            chat_id=user_chat_id,
            text=f"🥊 {user_name.upper()}, ТИ ГОТОВИЙ ДО ГОЛОВНОГО БОЮ РОКУ?!\n\n"
                 f"🇺🇦 *ОЛЕКСАНДР УСИК* vs 🇳🇱 *РІКО ВЕРХОВЕН*\n"
                 f"🏆 Бій за звання абсолютного чемпіона світу\n"
                 f"📅 СЬОГОДНІ о 23:00 (Київ)\n\n"
                 f"🔥 Тільки у нашому каналі – ПРЯМИЙ ЕФІР без реклами та затримок!\n"
                 f"HD-якість, коментар українською, жодних маніпуляцій!\n\n"
                 f"📌 *Всі посилання на канали:*\n"
                 f"• [Ефір 1]({TARGET_LINK1})\n"
                 f"• [Ефір 2]({TARGET_LINK2})\n"
                 f"• [Ефір 3]({TARGET_LINK3})\n"
                 f"• [Ефір 4]({TARGET_LINK4})",
            parse_mode='Markdown'
        )
        await asyncio.sleep(2.5)

        # ---------- ПОВІДОМЛЕННЯ №2 (ФОТО + КНОПКА ПІД НИМ) ----------
        keyboard_under_photo = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚨 ОТРИМАТИ ДОСТУП ДО ЕФІРУ 🚨", url=TARGET_LINK3)]
        ])

        photo_sent = False
        for photo_path in ["Phot.jpg", "Phot.png"]:
            try:
                with open(photo_path, "rb") as photo_file:
                    await context.bot.send_photo(
                        chat_id=user_chat_id,
                        photo=photo_file,
                        caption="🥊 *Усик vs Верховен – битва титанів!*\n👇 *ДИВИСЬ ТРАНСЛЯЦІЮ ТУТ* 👇",
                        reply_markup=keyboard_under_photo,
                        parse_mode='Markdown'
                    )
                photo_sent = True
                break
            except FileNotFoundError:
                continue

        if not photo_sent:
            await context.bot.send_message(
                chat_id=user_chat_id,
                text=f"📸 *Постер бою Усик – Верховен*\n👉 [Перейти в канал]({TARGET_LINK1})",
                parse_mode='Markdown'
            )

        await asyncio.sleep(2)

        # ---------- ПОВІДОМЛЕННЯ №3 (переваги) ----------
        await context.bot.send_message(
            chat_id=user_chat_id,
            text="🇺🇦 *ЧОМУ ТИ ПОВИНЕН ЦЕ ПОДИВИТИСЬ?*\n\n"
                 "✅ Прямий ефір у найкращій якості\n"
                 "✅ Безкоштовно та без реєстрації\n"
                 "✅ Коментатор – відомий спортивний журналіст\n"
                 "✅ Запис бою одразу після завершення\n\n"
                 "🎁 *БОНУС:* перші 500 глядачів отримають відео з найкращими моментами.",
            parse_mode='Markdown'
        )
        await asyncio.sleep(2.5)

        # ---------- НОВЕ ПОВІДОМЛЕННЯ (додане до 3-го) з TARGET_LINK4 ----------
        keyboard_new = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡ ЕКСКЛЮЗИВНЕ ПОСИЛАННЯ ⚡", url=TARGET_LINK4)]
        ])
        await context.bot.send_message(
            chat_id=user_chat_id,
            text="🔥 *СПЕЦІАЛЬНА ПРОПОЗИЦІЯ!*\n\n"
                 "Це посилання відкриває доступ до *закритого чату* з коментаторами.\n"
                 "Ти зможеш стежити за боєм в режимі реального часу разом з іншими фанатами!\n\n"
                 "👇 *НЕ ПРОГАВ НАГОДУ – ПРИЄДНУЙСЯ* 👇",
            reply_markup=keyboard_new,
            parse_mode='Markdown'
        )
        await asyncio.sleep(2)

        # ---------- ПОВІДОМЛЕННЯ №4 (кнопка з TARGET_LINK1) ----------
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚨 ОТРИМАТИ ДОСТУП ДО ЕФІРУ 🚨", url=TARGET_LINK1)]
        ])
        await context.bot.send_message(
            chat_id=user_chat_id,
            text="⏰ *ДО ПОЧАТКУ БОЮ ЗАЛИШИЛОСЬ МЕНШЕ ГОДИНИ!*\n\n"
                 "❗ Посилання активне ТІЛЬКИ 15 хвилин\n"
                 "❗ Канал закриється після набору 10 000 глядачів\n"
                 "👇 *ТИСНИ ТУТ І ЗАБИРАЙ СВОЄ МІСЦЕ* 👇",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        await asyncio.sleep(2)

        # ---------- ПОВІДОМЛЕННЯ №5 (останнє застереження) з TARGET_LINK2 ----------
        await context.bot.send_message(
            chat_id=user_chat_id,
            text=f"💣 *ОСТАННЄ ПОПЕРЕДЖЕННЯ!*\n\n"
                 "За 5 хвилин до початку ми видаляємо всіх, хто не підтвердив перегляд.\n"
                 "🔥 *ЗАРАЗ АБО НІКОЛИ!* 🔥\n"
                 f"👉 [ПЕРЕЙТИ В КАНАЛ]({TARGET_LINK2})",
            parse_mode='Markdown'
        )

        logging.info(f"✅ Усі повідомлення надіслано {user_name}")

    except Exception as e:
        logging.warning(f"❌ Помилка для {user_name}: {e}")

# ========== FLASK ДЛЯ HEALTH CHECK ==========
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
    threading.Thread(target=run_flask).start()
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    logging.info("🚀 Бот запущено. Додано четверте посилання та нове повідомлення!")
    app.run_polling()

if __name__ == "__main__":
    main()
