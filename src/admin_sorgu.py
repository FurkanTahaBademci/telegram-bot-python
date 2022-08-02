from src.cfg import YETKILI_ID
import numpy as np

def admin_sorgu(update,context):

    mesaj_atan_kisi_id = update.message.chat.id

    for i in np.array(YETKILI_ID):

        if mesaj_atan_kisi_id == i:
            yanit= "yes"
            break
        else:
            yanit = "no"

    if yanit == "no":
        update.message.reply_text(f'Sayın {update.message.chat.first_name}. Giriş yapmanız gerekmektedir. Lütfen şifrenizi giriniz .')
        return yanit
    elif yanit == "yes":
        return yanit
