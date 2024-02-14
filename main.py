from difflib import SequenceMatcher

from pyrogram import Client, filters

from config import API_ID, API_HASH, WORD_SIMILARITY_COEFFICIENT
from database import DataBase

app = Client("session", api_id=API_ID, api_hash=API_HASH)

db = DataBase()


def message_for_resended(text):
    text = text or ""
    for word in text.split():
        searched = []
        for search_word in db.get('search_words', []):
            ratio = SequenceMatcher(
                None,
                word.lower(),
                search_word.lower()
            ).ratio()
            searched.append(ratio)

        if any([search >= WORD_SIMILARITY_COEFFICIENT for search in searched]):
            return True

    return False


@app.on_message(filters.command(['set_forward_chat']) & filters.me)
async def forward_chat_handler(client, message):
    db.set('chat_id_for_forward', message.chat.id)
    db.set('excluded_chats', [message.chat.id])
    await message.reply_text('В этот чат теперь будут пересылаться сообщения')


@app.on_message(filters.command(['add_words']) & filters.me)
async def add_word_handler(client, message):
    args = (message.text or message.caption or "").split()
    if len(args) <= 1:
        await message.reply_text('Неверное кол-во аргументов')
        return

    add_commands = args[1:]
    commands = db.get('search_words', [])
    commands.extend(add_commands)
    db.set('search_words', commands)

    await message.reply_text('Слово добавлено!')


@app.on_message(filters.command(['delete_words']) & filters.me)
async def delete_word(client, message):
    args = (message.text or message.caption or "").split()
    if len(args) <= 1:
        await message.reply_text('Неверное кол-во аргументов')
        return

    delete_words = args[1:]
    commands = db.get('search_words', [])
    for word in delete_words:
        if word not in commands:
            await message.reply_text(f'Этого слова нет в списке: {word}')
        else:
            commands.remove(word)

    db.set('search_words', commands)

    await message.reply_text('Слова удалены!')


@app.on_message(filters.command(['words']) & filters.me)
async def words_handler(client, message):
    await message.reply_text('Слова для поиска:\n' + '\n'.join(db.get('search_words', [])))


@app.on_message()
async def hello(client, message):
    if message.chat.id in db.get('excluded_chats', []):
        return

    if message_for_resended(message.text or message.caption):
        await client.forward_messages(
            db.get('chat_id_for_forward'),
            message.chat.id,
            message.id
        )


if __name__ == '__main__':
    app.run()
