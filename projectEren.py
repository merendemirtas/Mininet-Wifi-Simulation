#!/usr/bin/python

from mininet.node import OVSController
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
import matplotlib.pyplot as plt
import threading
import re

def topology():
    # En stabil iletisim ve cizim modu
    net = Mininet_wifi(controller=OVSController, link=wmediumd)

    print("Nodes olusturuluyor...")
    # Otomatik gecis (roaming) icin SSID'ler ayni
    ap1 = net.addAccessPoint('ap1', ssid='eren_wifi', mode='g', channel='1', position='50,80,0', range='40')
    ap2 = net.addAccessPoint('ap2', ssid='eren_wifi', mode='g', channel='6', position='150,80,0', range='40')
    
    # Istasyonlar
    sta1 = net.addStation('sta1', ip='10.0.0.1/8', position='30,80,0') 
    sta2 = net.addStation('sta2', ip='10.0.0.2/8', position='50,100,0')
    sta3 = net.addStation('sta3', ip='10.0.0.3/8', position='150,100,0')
    sta4 = net.addStation('sta4', ip='10.0.0.4/8', position='150,60,0')

    c1 = net.addController('c1', controller=OVSController)

    print("Ag yapilandiriliyor...")
    net.configureNodes()
    net.addLink(ap1, ap2)

    # Arayuzu baslat
    net.plotGraph(max_x=200, max_y=160)
    
    print("Simulasyon baslatiliyor...")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])

    print("\nIletisim analizi baslatildi (sta2 -> sta1 ping calisiyor)...")
    print("="*45)
    print("{:<10} | {:<12} | {:<15}".format("SANİYE", "DURUM", "GECİKME"))
    print("="*45)
    
    # Toplam ping 60 saniye surecek
    p = sta2.popen('ping -c 60 -O 10.0.0.1')
    ping_output = []

    # Saniye saniye okuma yapacak arka plan (tablo yazdirici)
    def monitor_ping():
        for line in iter(p.stdout.readline, b''):
            decoded_line = line.decode('utf-8').strip()
            ping_output.append(decoded_line)
            
            if "time=" in decoded_line:
                time_val = re.search(r'time=([\d\.]+)', decoded_line)
                seq_val = re.search(r'icmp_seq=(\d+)', decoded_line)
                if time_val and seq_val:
                    print("{:<10} | {:<12} | {} ms".format(seq_val.group(1), "BAŞARILI", time_val.group(1)))
            
            elif "no answer yet" in decoded_line:
                seq_val = re.search(r'icmp_seq=(\d+)', decoded_line)
                if seq_val:
                    print("{:<10} | {:<12} | -".format(seq_val.group(1), "KAYIP"))

    t = threading.Thread(target=monitor_ping)
    t.daemon = True
    t.start()

    # --- HAREKET VE BEKLEME SENARYOSU ---
    
    # Nokta 0
    print("\n>>> NOKTA 0: AP1 Ustunde (Baslangic). 10 sn bekleme... <<<\n")
    sta1.setPosition('50,80,0')
    plt.pause(10)

    # Nokta 1
    print("\n>>> NOKTA 1: AP1 Sinirina gidildi. 10 sn bekleme... <<<\n")
    sta1.setPosition('90,80,0')
    plt.pause(10)
    
    # Nokta 3
    print("\n>>> NOKTA 3: AP2 Sinirina gidildi. 10 sn bekleme... <<<\n")
    sta1.setPosition('110,80,0')
    plt.pause(10)
    
    # Nokta 4
    print("\n>>> NOKTA 4: AP2 Yanina gidildi. 20 sn bekleme... <<<\n")
    sta1.setPosition('150,80,0')
    plt.pause(20)
    
    # Donus
    print("\n>>> BITIS: Baslangic noktasina (Nokta 0) aninda donuluyor... <<<\n")
    sta1.setPosition('50,80,0')
    
    # ÇÖZÜM BURADA: Arayuzun aninda guncellenmesi ve kalan 10 saniyelik pingin (toplam 60) 
    # baslangic noktasinda atilmaya devam etmesi icin plt.pause ekledik.
    plt.pause(10) 
    
    print("\nVeriler isleniyor, pingin bitmesi bekleniyor...")
    p.wait() 
    
    res = "\n".join(ping_output)
    
    loss = re.findall(r'([\d\.]+)% packet loss', res)
    rtt = re.findall(r'rtt min/avg/max/mdev = [\d\.]+/([\d\.]+)/', res)
    
    print("\n" + "="*45)
    print("               ANALİZ SONUÇLARI              ")
    print("="*45)
    if loss:
        print("Ortalama Paket Kaybi : %" + loss[0])
        if loss[0] == '100' or loss[0] == '100.0' or loss[0] == '100.00':
            print("Ortalama Gecikme     : Ölçülemedi (Tam Kayıp)")
        elif rtt:
            print("Ortalama Gecikme     : " + rtt[0] + " ms")
        else:
            print("Ortalama Gecikme     : Okunamadı")
    else:
        print("Hata: Paket kaybi verisi okunamadi.")
    print("="*45 + "\n")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    topology()
