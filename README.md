# Mininet-WiFi Roaming & Communication Analysis

Bu proje, **Mininet-WiFi** emülatörü üzerinde iki Erişim Noktası (Access Point) ve hareketli bir istasyon (Station) arasındaki iletişim sürekliliğini analiz etmek için tasarlanmıştır.

## 📌 Proje Özeti
`projectEren.py` betiği, bir mobil cihazın (sta1) iki farklı AP arasında hareket ederken bağlantı durumunu, paket kaybını ve gecikme (latency) değerlerini gerçek zamanlı olarak ölçer.

### Özellikler:
* **Roaming Simülasyonu:** `sta1`, AP1 kapsama alanından AP2 kapsama alanına hareket eder.
* **Gerçek Zamanlı Analiz:** Ping sonuçları (ICMP) saniye saniye bir tablo formatında ekrana basılır.
* **Görselleştirme:** `matplotlib` kullanılarak düğümlerin konumu ve hareketleri grafiksel olarak gösterilir.
* **Özet Rapor:** Simülasyon sonunda ortalama paket kaybı ve gecikme verileri sunulur.

## 🛠 Kurulum ve Gereksinimler
Bu projeyi çalıştırmak için sisteminizde **Mininet-WiFi** kurulu olmalıdır.

```bash
# Mininet-WiFi kurulumu (Eğer sisteminizde yoksa)
git clone [https://github.com/intrig-unicamp/mininet-wifi](https://github.com/intrig-unicamp/mininet-wifi)
cd mininet-wifi
sudo util/install.sh -W

<img width="645" height="568" alt="Ekran Resmi 2026-05-13 13 03 19" src="https://github.com/user-attachments/assets/831777e6-7184-4dbd-bc11-0e9891bff159" />
