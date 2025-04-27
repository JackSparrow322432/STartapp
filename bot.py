from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# --- База данных ---
DATABASE_URL = "sqlite:///./appointments.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    parent_name = Column(String)
    child_age = Column(Integer)
    phone = Column(String)
    preferred_time = Column(String)

Base.metadata.create_all(bind=engine)

# --- Состояния разговора ---
ASKING, BOOKING_NAME, BOOKING_AGE, BOOKING_PHONE, BOOKING_TIME = range(5)

RESPONSES = {
    "речь": "Трудности с речью часто встречаются у детей с аутизмом. Занятия с логопедом помогают.",
    "поведение": "Коррекцию поведения можно проводить через ABA-терапию.",
    "социализация": "Социализация развивается через игры. Специалисты могут помочь.",
    "сенсорика": "Чувствительность к звукам, свету — обычное дело. Помогают сенсорные тренировки.",
}

# --- Функции бота ---
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Здравствуйте! Я помогу вам с вопросами об аутизме.\n"
        "Задайте вопрос или напишите /appointment для записи на консультацию."
    )
    return ASKING

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    for keyword, response in RESPONSES.items():
        if keyword in text:
            update.message.reply_text(response + "\nХотите записаться? Напишите /appointment")
            return ASKING
    update.message.reply_text("Спасибо за вопрос. Рекомендую консультацию. Напишите /appointment.")
    return ASKING

def appointment_start(update: Update, context: CallbackContext):
    update.message.reply_text("Как вас зовут?")
    return BOOKING_NAME

def appointment_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    update.message.reply_text("Сколько лет вашему ребенку?")
    return BOOKING_AGE

def appointment_age(update: Update, context: CallbackContext):
    context.user_data['age'] = update.message.text
    update.message.reply_text("Ваш номер телефона?")
    return BOOKING_PHONE

def appointment_phone(update: Update, context: CallbackContext):
    context.user_data['phone'] = update.message.text
    update.message.reply_text("Когда вам удобно связаться?")
    return BOOKING_TIME

def appointment_time(update: Update, context: CallbackContext):
    context.user_data['time'] = update.message.text
    db = SessionLocal()
    appointment = Appointment(
        parent_name=context.user_data['name'],
        child_age=int(context.user_data['age']),
        phone=context.user_data['phone'],
        preferred_time=context.user_data['time']
    )
    db.add(appointment)
    db.commit()
    db.close()
    update.message.reply_text("Спасибо! Мы свяжемся с вами в ближайшее время.")
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Отмена записи. Напишите /appointment, чтобы начать снова.")
    return ConversationHandler.END

# --- Основной запуск ---
def main():
    TOKEN = "7554507823:AAEZ10oZbH7Kz-8GI1rXM8McM6Jm_uWVNEs"  # ← сюда вставь свой токен!

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('appointment', appointment_start)],

        states={
            BOOKING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, appointment_name)],
            BOOKING_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, appointment_age)],
            BOOKING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, appointment_phone)],
            BOOKING_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, appointment_time)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()