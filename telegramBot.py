import requests

def send_alert(file,caption):
    res = requests.post(f'https://api.telegram.org/bot6913219075:AAEEfFIS-r4xsCSv1PF2_AlaV6bSzDdZeRw/sendPhoto?chat_id=-4108671775&caption={caption}',files =file)
    return res

# file = {'photo': open('upstox_login.png', 'rb')}
# send_alert(file,"shoonya")


