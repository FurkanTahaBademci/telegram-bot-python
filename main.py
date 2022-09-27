import logging
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from src.fiyat import get_current_data
from src.cfg import ADMIN_SIFRE, YETKILI_ID,BOT_TOKEN
from src.admin_sorgu import admin_sorgu
from src.screenshot import screenshot
from src.camera_shot import camera_shot
from src.video_kaydetme import video_record
import src.ses_keydetme as sess
import datetime
import os 
import sys
import pyautogui


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', 
                              '%m-%d-%Y %H:%M:%S')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('log/logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


ANA_SAYFA_MESAJ = ('/fiyat - Anlık fiyat\n\n/pc_kitle - Bilgisayarı kilitle\n\n/pc_uyku - Uykuya al\n\n/pc_kapat - Bilgisayarı kapat\n\n/pc_kapatma_iptali - Kapatma işlemi iptal et\n\n/ekran - Ekran resmi al\n\n/kamera - Kamera görüntüsü al\n\n/video - Video kaydı al \n\n /ses - Ses kaydı al\n\n/botu_durdur - Botu durdur')


def saat():

    global date_clock
    x = datetime.datetime.now()
    date_clock = (x.strftime("%d/%m/%Y  %H:%M"))


def giris(update,context):  # ATILAN TÜM MESAJLAR BURAYA DÜŞÜYOR 
    
    mesaj = (update.message.text)
    mesaj_atan_kisi_id = update.message.chat.id
    mesaj_atan_kisi = update.message.chat.first_name
    yanit = admin_sorgu(update,context)   # SİSTEMDE İD KAYITLI MI DİYE KONTROL YAPIYORUZ
    mesaj_sil(update,context)

    if mesaj == ADMIN_SIFRE and yanit== "no":  
        YETKILI_ID.append(mesaj_atan_kisi_id)   # YETKİLİ İD KAYIT İŞLEMİ 
        update.message.reply_text(f'{mesaj_atan_kisi} hoşgeldiniz. {mesaj_atan_kisi_id} ID ile giriş yapılmıştır.')
        update.message.reply_text(ANA_SAYFA_MESAJ)

    elif yanit== "yes":
        update.message.reply_text(f'{mesaj_atan_kisi_id} ID kayıtlıdır. Hoşgeldiniz')
        update.message.reply_text(ANA_SAYFA_MESAJ)


def start(update,context):
    
    mesaj_atan_kisi_id = update.message.chat.id
    yanit = admin_sorgu(update,context)
    mesaj_sil(update,context)

    if yanit== "yes":
        update.message.reply_text(f'{mesaj_atan_kisi_id} ID kayıtlıdır. Hoşgeldiniz')
        update.message.reply_text(ANA_SAYFA_MESAJ)


def fiyat(update,context):

    # mesaj_sil(update,context)
    
    yanit = admin_sorgu(update,context)
    if yanit== "yes":
        response = get_current_data(update)
        update.message.reply_text(response)


def pc_kitle(update,context):

    # mesaj_sil(update,context)
    yanit = admin_sorgu(update,context)

    if yanit== "yes":
        update.message.reply_text("Bilgisayarınız kilitlenmiştir")
        os.system("Rundll32.exe user32.dll,LockWorkStation")


def pc_uyku(update,context):

    # mesaj_sil(update,context)
    yanit = admin_sorgu(update,context)

    if yanit== "yes":
        update.message.reply_text("Bilgisayarınız uykuya geçmiştir")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")



def pc_kapat(update,context):

    # mesaj_sil(update,context)
    yanit = admin_sorgu(update,context)

    if yanit == "yes":
        update.message.reply_text("Bilgisayarınız 5 saniye içinde kapatılacaktır")
        os.system("shutdown -s -f -t 5")



def pc_kapatma_iptali(update,context):

    # mesaj_sil(update,context)
    yanit = admin_sorgu(update,context)

    if yanit == "yes":
        update.message.reply_text("Bilgisayarınızın kapatma işlemi yapılmıştır")
        os.system("shutdown -a")



def kamera(update,context):

    yanit = admin_sorgu(update,context)
    mesaj_atan_kisi_id = update.message.chat.id
    # mesaj_sil(update,context)
    if yanit == "yes":
        camera_shot()
        saat()
        bot.send_photo(
            chat_id = mesaj_atan_kisi_id, 
            caption = "Anlık kamera görüntüsü \n"+date_clock,
            photo = open('output/camera.jpg','rb')) 



def ekran(update,context):

    yanit = admin_sorgu(update,context)
    mesaj_atan_kisi_id = update.message.chat.id
    # mesaj_sil(update,context)

    if yanit == "yes":
        screenshot()  
        saat()
        bot.send_photo(
            chat_id = mesaj_atan_kisi_id, 
            caption = "Anlık ekran görüntüsü \n"+date_clock,
            photo = open('output/screen.jpg','rb')) 



def ses(update,context):
    yanit = admin_sorgu(update,context)
    mesaj_atan_kisi_id = update.message.chat.id
    # mesaj_sil(update,context)

    if yanit== "yes":

        update.message.reply_text("Ses kaydı başladı")
        sess.ses()
        saat()
        bot.send_audio(
            chat_id = mesaj_atan_kisi_id, 
            caption = "\n"+date_clock,
            audio = open('output/out.wav','rb')) 


def botu_durdur(update, context):

    yanit = admin_sorgu(update,context)

    if yanit == "yes":
        update.message.reply_text("Bot durduruldu")
        sys.exit()

def video(update, context):

    yanit = admin_sorgu(update,context)
    mesaj_atan_kisi_id = update.message.chat.id

    if yanit == "yes":
        update.message.reply_text("Video kaydı başladı")
        video_record()
        saat()
        bot.send_video(
            chat_id = mesaj_atan_kisi_id, 
            caption = "Anlık video görüntüsü\n"+date_clock,
            video = open('output/webcam.mp4','rb')
        )

def mesaj_sil(update,context):
    
    bot.deleteMessage(
    message_id = update.message.message_id,
    chat_id = update.message.chat.id
    )
    for i in range(1,5,1):
        try:
            bot.deleteMessage(
            message_id = update.message.message_id-i,
            chat_id = update.message.chat.id
            )
        except:
            pass

def yaz(update, context):

    yanit = admin_sorgu(update,context)
 
    if yanit == "yes":

        mess = update.message.text
        mess = mess[4:]
        pyautogui.write( mess , interval=0.01)
        update.message.reply_text("Mesajınız yazılmıştır. Mesaj içeriği : ",mess)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    global bot
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    bot = updater.bot

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("fiyat", fiyat))
    dp.add_handler(CommandHandler("pc_kitle", pc_kitle))
    dp.add_handler(CommandHandler("pc_uyku", pc_uyku))
    dp.add_handler(CommandHandler("pc_kapat", pc_kapat))
    dp.add_handler(CommandHandler("pc_kapatma_iptali", pc_kapatma_iptali))
    dp.add_handler(CommandHandler("kamera", kamera))
    dp.add_handler(CommandHandler("ekran", ekran))
    dp.add_handler(CommandHandler("video", video))
    dp.add_handler(CommandHandler("ses", ses))
    dp.add_handler(CommandHandler("yaz", yaz))

    dp.add_handler(CommandHandler("botu_durdur", botu_durdur))

    dp.add_handler(MessageHandler(Filters.text, giris))
    
    dp.add_error_handler(error) # log
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
