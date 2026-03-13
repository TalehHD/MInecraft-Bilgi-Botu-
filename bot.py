import json
import random
from turtle import update
from urllib import response
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN = "BURAYA_TOKEN_YAZ"

# JSON yükleme
with open("data.json", "r", encoding="utf-8") as f:
    minecraft_data = json.load(f)


    minecraft_data = {key.lower(): value for key, value in minecraft_data.items()}


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba!\n"
        "Ben Minecraft Bilgi Botuyum.\n\n"
        "Bir Minecraft nesnesi yaz ve sana bilgi vereyim.\n"
        "Örnek: Creeper, Diamond"
    )


# HELP
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Botu başlat\n"
        "/help - Yardim\n"
        "/list - Tüm nesneler\n"
        "/mob - Sadece moblari goster\n"
        "/item- Sadece itemleri goster\n"
        "/block- Sadece bloklari goster\n"
        "/random - Rastgele nesne"
    )


# LIST
async def list_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = ", ".join(minecraft_data.keys())
    await update.message.reply_text(f"Mevcut nesneler:\n{items}")


# MOB LİSTESİ KOMUTU
async def list_mobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Sadece türü 'mob' olan anahtarları (key) filtreliyoruz
    mobs = [key for key, data in minecraft_data.items() if data.get('type').lower() == 'mob']
    
    if mobs:
        mesaj = "👾 **Mevcut Moblar:**\n" + ", ".join(mobs)
    else:
        mesaj = "Sistemde hiç mob bulunamadi."
        
    await update.message.reply_text(mesaj, parse_mode='Markdown')


    # ITEM LİSTESİ
async def list_items_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = [key for key, data in minecraft_data.items() if data.get('type').lower() == 'item']

    if items:
        mesaj = "📦 Mevcut Itemler:\n" + ", ".join(items)
    else:
        mesaj = "Sistemde hiç item bulunamadı."

    await update.message.reply_text(mesaj)


    # BLOCK LİSTESİ
async def list_blocks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    blocks = [key for key, data in minecraft_data.items() if data.get('type').lower() == 'block']

    if blocks:
        mesaj = "🧱 Mevcut Bloklar:\n" + ", ".join(blocks)
    else:
        mesaj = "Sistemde hiç blok bulunamadı."

    await update.message.reply_text(mesaj)


# RANDOM
async def random_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = random.choice(list(minecraft_data.keys()))
    data = minecraft_data[item]


    text = f"""
İsim: {data['name']}
Tür: {data['type']}
Açiklama: {data['description']}
Kullanim: {data['usage']}
"""

    await update.message.reply_text(text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text in minecraft_data:
        data = minecraft_data[text]

        reply = f"""
İsim: {data['name']}
Tür: {data['type']}
Açiklama: {data['description']}
Kullanim: {data['usage']}
"""
        await update.message.reply_text(reply)

    else:
        await update.message.reply_text("Bu nesneyi bulamadım.") 


# BOT BAŞLATMA
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("list", list_items))
app.add_handler(CommandHandler("mob", list_mobs))
app.add_handler(CommandHandler("item", list_items_type))
app.add_handler(CommandHandler("block", list_blocks))
app.add_handler(CommandHandler("random", random_item))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


print("Bot çalişiyor...")

app.run_polling()