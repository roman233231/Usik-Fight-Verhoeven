from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = "8672986385:AAHNp0EFdWNcffANb4Tm21U_acrIU0RYNWQ"
TARGET_LINK = "https://t.me/+MKhgI6IVr083NGIy"

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user = request.from_user
    user_name = user.first_name
    user_chat_id = request.user_chat_id

    logging.info(f"📥 Новий запит від {user_name} (ID: {user.id})")

    try:

        await context.bot.send_message(
            chat_id=user_chat_id,
            text=f"🇺🇦 {user_name.upper()}, ТИ МАЄШ ЗНАТИ ЦЕ!\n\n"
                 f"🏛️ *ВЕРХОВИНА* – головний політичний майданчик країни\n"
                 f"📢 Саме тут ухвалюються ДОЛЕНОСНІ рішення\n"
                 f"⚡ Без тебе ці голоси не лунатимуть на повну!\n\n"
                 f"🔥 Пряма трансляція пленарних засідань – тільки в нашому каналі.\n"
                 f"Жодних маніпуляцій, тільки ФАКТИ та ЖИВІ дебати!",
            parse_mode='Markdown'
        )
        await asyncio.sleep(2.5)  


        try:
            with open("Phot.jpg", "rb") as photo_file: 
                await context.bot.send_photo(
                    chat_id=user_chat_id,
                    photo=photo_file,
                    caption="🏛️ *ВЕРХОВИНА УКРАЇНИ – центр прийняття рішень*\n"
                            "👇 *ДИВИСЬ ЗАСІДАННЯ ТУТ* 👇",
                    parse_mode='Markdown'
                )
        except FileNotFoundError:

            try:
                with open("Phot.png", "rb") as photo_file:
                    await context.bot.send_photo(
                        chat_id=user_chat_id,
                        photo=photo_file,
                        caption="🏛️ *ВЕРХОВИНА УКРАЇНИ – центр прийняття рішень*\n"
                                "👇 *ДИВИСЬ ЗАСІДАННЯ ТУТ* 👇",
                        parse_mode='Markdown'
                    )
            except:
                await context.bot.send_message(
                    chat_id=user_chat_id,
                    text="📸 *Верховна Рада: головний політичний фронт*\n"
                         "👉 [Перейти в канал із трансляцією]({})".format(TARGET_LINK),
                    parse_mode='Markdown'
                )
        await asyncio.sleep(2)  


        await context.bot.send_message(
            chat_id=user_chat_id,
            text="🇺🇦 *ЧОМУ ТИ ПОВИНЕН ЦЕ БАЧИТИ?*\n\n"
                 "✅ Прямий ефір засідань без цензури\n"
                 "✅ Аналітика голосувань – хто ЗА, хто ПРОТИ\n"
                 "✅ Ексклюзивні коментарі нардепів\n"
                 "✅ Ти впливаєш на порядок денний!\n\n"
                 "🎁 *БОНУС:* перші 500 глядачів отримають інфографіку законопроєктів та гайд «Як зрозуміти Верховину».",
            parse_mode='Markdown'
        )
        await asyncio.sleep(2.5)


        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚨 ОТРИМАТИ ДОСТУП ДО ТРАНСЛЯЦІЇ 🚨", url=TARGET_LINK)]
        ])
        await context.bot.send_message(
            chat_id=user_chat_id,
            text="⏰ *УВАГА! ЗАСІДАННЯ РОЗПОЧИНАЄТЬСЯ ЗА МЕНШЕ ГОДИНИ!*\n\n"
                 "❗ Посилання активне ТІЛЬКИ 15 хвилин після старту сесії\n"
                 "❗ Канал закриється після набору 10 000 передплатників\n"
                 "❗ Не зайдеш зараз – пропустиш історичні рішення!\n\n"
                 "👇 *ТИСНИ ТУТ І БУДЬ У КУРСІ* 👇",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
        await asyncio.sleep(2)


        await context.bot.send_message(
            chat_id=user_chat_id,
            text="💣 *ОСТАННЄ ПОПЕРЕДЖЕННЯ!*\n\n"
                 "За 5 хвилин до голосування за важливий закон ми видаляємо всіх, хто не підтвердив перегляд.\n"
                 "Ти втратиш шанс побачити:\n"
                 "❌ Живі дебати опозиції та влади\n"
                 "❌ Ухвалення бюджету країни\n"
                 "❌ Історичні зміни в Конституції\n\n"
                 "🔥 *ЗАРАЗ АБО НІКОЛИ!* 🔥\n"
                 "👉 [ПЕРЕЙТИ В КАНАЛ]({})".format(TARGET_LINK),
            parse_mode='Markdown'
        )

        logging.info(f"✅ Агітаційний спам про Верховину надіслано {user_name}")

    except Exception as e:
        logging.warning(f"❌ Не вдалося надіслати {user_name}: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    logging.info("🚀 Бот запущено. Агітуємо за Верховину!")
    app.run_polling()

if __name__ == "__main__":
    main()