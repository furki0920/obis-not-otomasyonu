# ADÜ OBİS Not Takip Otomasyonu (osimhen v4.8.1)

Bu proje, Aydın Adnan Menderes Üniversitesi Öğrenci Bilgi Sistemi (OBİS) üzerindeki not değişikliklerini otomatik olarak takip eden ve güncellemeleri anlık olarak Telegram üzerinden kullanıcıya bildiren bir Python uygulamasıdır.

## 🚀 Özellikler
- **Web Otomasyonu:** Selenium ve WebDriver Manager kullanılarak OBİS sistemine güvenli giriş ve navigasyon.
- **Headless Çalışma:** Tarayıcı arayüzü olmadan (arka planda) düşük kaynak tüketimi ile çalışma.
- **Akıllı Hafıza:** Notları yerel bir JSON dosyasında saklayarak sadece yeni açıklanan veya değişen notlar için bildirim gönderme.
- **Telegram Entegrasyonu:** Telegram Bot API üzerinden anlık bildirim sistemi.
- **Hata Yönetimi:** Beklenmedik sistem kesintilerinde veya giriş hatalarında kullanıcıya bilgilendirme mesajı gönderimi.

## 🛠 Kullanılan Teknolojiler
- **Python 3.x**
- **Selenium:** Web otomasyonu ve veri çekme (Scraping).
- **Telegram API:** Bildirim servisi.
- **JSON:** Veri saklama ve hafıza yönetimi.
- **Requests:** HTTP istekleri yönetimi.

## ⚙️ Kurulum ve Kullanım

1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install selenium webdriver-manager requests
2. Kod içerisindeki yapılandırma alanlarını doldurun:

  USER_ID: OBİS kullanıcı adınız.

  PASSWORD: OBİS şifreniz.

  TELEGRAM_TOKEN: BotFather üzerinden alınan API token.

  CHAT_ID: Bildirimlerin gönderileceği Telegram sohbet kimliği.

3. Uygulamayı başlatın:
   ```bash
   python obis-not-otomasyonu.py

⚖️ Yasal Uyarı
Bu araç eğitim ve kişisel kullanım amaçlıdır. Sistemin aşırı kullanımından kaynaklanabilecek durumlarda sorumluluk kullanıcıya aittir.
