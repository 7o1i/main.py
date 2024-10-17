from telegram import Update
from telegram.ext import ContextTypes
import time
from config import GROUP_CHAT_ID

# تخزين بيانات المستخدمين
users = {}
last_message_time = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {'messages': []}
        last_message_time[user_id] = 0  # تعيين الوقت الأولي لآخر رسالة
        await update.message.reply_text(
            "🌟 مرحبًا بك في بوت الأسرار! 🌟\n\n"
            "✅ تم إنشاء حسابك بنجاح!\n"
            "يمكنك الآن مشاركة أسرارك معي.\n\n"
            "✨ فقط اكتب ما تود مشاركته هنا، وسأرسله إلى المجموعة: https://t.me/arsal_7"
        )
    else:
        await update.message.reply_text("⚠️ لديك حساب بالفعل! يمكنك الآن مشاركة الأسرار.")

async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user is None:
        return  # تجاهل الرسائل التي لا تحتوي على مستخدم فعال

    user_id = update.effective_user.id
    current_time = time.time()

    if user_id in users:
        # تحقق من الوقت منذ آخر رسالة
        if current_time - last_message_time[user_id] < 7200:  # 7200 ثانية = ساعتين
            remaining_time = 7200 - (current_time - last_message_time[user_id])
            remaining_hours = int(remaining_time // 3600)
            remaining_minutes = int((remaining_time % 3600) // 60)

            await update.message.reply_text(
                f"❌ يمكنك فقط إرسال رسالة واحدة كل ساعتين!\n"
                f"يتبقى لك: {remaining_hours}:{remaining_minutes:02d}."
            )
            return

        secret_message = update.message.text
        last_message_time[user_id] = current_time

        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=f"🗣️: {secret_message}")
        await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=".")
        await update.message.reply_text("✅ تم إرسال سرك إلى المجموعة!")
    else:
        await update.message.reply_text("❌ لم يتم العثور على حسابك! ابدأ باستخدام /start.")
