import os
from subprocess import check_output
import qrcode


AIRPORT_PATH = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"


def get_SSID(s):
    """
    # the input example:
    # 
    #       agrCtlRSSI: -44
    #       agrExtRSSI: 0
    #       agrCtlNoise: -89
    #       agrExtNoise: 0
    #       state: running
    #       op mode: station
    #       lastTxRate: 867
    #       maxRate: 867
    #       lastAssocStatus: 0
    #       802.11 auth: open
    #       link auth: wpa2-psk
    #       BSSID:
    #       SSID: ROOM-503
    #       MCS: 9
    #       guardInterval: 800
    #       NSS: 2
    #       channel: 36,80

    # return a dict
    """
    lines = [a.split(":") for a in s.split("\n") if a]
    d = {i[0].strip(): i[1].strip() for i in lines}
    return d

def get_current_wifi():
    if not os.path.isfile(AIRPORT_PATH):
        print("airport not found!")
        return

    # use airport to retrieve current SSID
    
    res = check_output(f'{AIRPORT_PATH} -I', shell=True)
    
    airport_info = get_SSID(res.decode())
    if "SSID" not in airport_info:
        print("SSID not found, please check the WIFI connection")
        return 

    # find the password in the keythain
    res = check_output(f'security find-generic-password -wa "{airport_info["SSID"]}"', 
                       shell=True)
    pwd = res.decode().strip()
    if not pwd:
        print("password not found!")
        return 

    return airport_info["SSID"], pwd,airport_info["link auth"]

def show_wifi_qr(ssid, password, auth_type, hidden=False):
    code = f'WIFI:T:{auth_type};S:{ssid};P:{password};H:{hidden};;'
    qr = qrcode.QRCode()
    qr.add_data(code)
    qr.print_ascii()


if __name__ == "__main__":
    ssid, pwd, link_auth = get_current_wifi()

    # auth_type is WPA3, WPA2, WPA and WEP
    # the value of link_auth is like "wpa2-psk"
    auth_type = link_auth.split("-")[0]
    show_wifi_qr(ssid, pwd, auth_type.upper())
