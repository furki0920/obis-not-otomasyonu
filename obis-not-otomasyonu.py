import time
import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- YAPILANDIRMA ---
OBIS_URL = "https://obis.adu.edu.tr/GIRIS"
USER_ID = "" # #obis kullanıcı adı
PASSWORD = "" #obis parola
TELEGRAM_TOKEN = "" #telegram token
CHAT_ID = "" #chat id

# Kesin ID'ler
DONEM_ARROW_ID = "ctl00_ctl00_cphMain_cphContent_cmbDonem_Arrow"
DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
JSON_FILE = os.path.join(DESKTOP, "notlar_hafiza.json")

def telegram_mesaj_gonder(mesaj):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mesaj}"
        requests.get(url, timeout=10)
    except: pass

def hafizayi_yukle():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {}
    return {}

def hafizayi_kaydet(veriler):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(veriler, f, ensure_ascii=False, indent=4)

def not_kontrol_et():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new") #otomasyon sürecini gözlemlemek için bu satırı yorum satırı yapabilirsiniz. 
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)
    
    try:
        print(f"  > [1/4] 🌐 OBİS Ana sayfası yükleniyor...")
        driver.get(OBIS_URL)
        time.sleep(3)

        # --- AŞAMA 1: GİRİŞ ---
        basarili_giris = False
        for deneme in range(1, 5):
            print(f"  > 🔍 Sayfa durumu kontrol ediliyor (Deneme #{deneme})...")
            
            if len(driver.find_elements(By.XPATH, "//*[contains(text(), 'Not/Sınav')]")) > 0:
                print(f"  > ✨ Teyit: Zaten içerideyiz, giriş adımları geçiliyor.")
                basarili_giris = True
                break
            
            login_formu_acik = len(driver.find_elements(By.ID, "ctl00_ctl00_cphMain_cphContent_loginRecaptcha_UserName")) > 0
            
            if not login_formu_acik:
                print(f"  > 🔘 Giriş paneli kapalı. 'Öğrenci Girişi' butonu aranıyor...")
                try:
                    ogrenci_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Öğrenci Girişi'] | //*[text()='Öğrenci Girişi']")))
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ogrenci_btn)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", ogrenci_btn)
                    print(f"  > ✅ 'Öğrenci Girişi' butonuna tıklandı. Form bekleniyor...")
                    time.sleep(4)
                except:
                    print(f"  > ⚠️ Buton bulunamadı, sayfa yenileniyor...")
                    driver.refresh()
                    time.sleep(3)
                    continue

            try:
                print(f"  > ✍️ Kullanıcı bilgileri yazılıyor...")
                user_f = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_ctl00_cphMain_cphContent_loginRecaptcha_UserName")))
                user_f.clear()
                user_f.send_keys(USER_ID)
                
                pass_f = driver.find_element(By.ID, "ctl00_ctl00_cphMain_cphContent_loginRecaptcha_Password")
                pass_f.clear()
                pass_f.send_keys(PASSWORD)
                
                print(f"  > 🖱️ Giriş Yap butonuna basılıyor...")
                login_btn = driver.find_element(By.XPATH, "//input[contains(@id, 'login') and @type='submit'] | /html/body/form/div[6]/div[2]/div[1]/div[1]/div[5]/div/table/tbody/tr/td/div/div[7]/span/input[1]")
                driver.execute_script("arguments[0].click();", login_btn)
                
                print(f"  > ⏳ Giriş onayı bekleniyor (8 sn)...")
                time.sleep(8)
                
                if len(driver.find_elements(By.XPATH, "//*[contains(text(), 'Not/Sınav')]")) > 0:
                    print(f"  > [2/4] 🎉 Giriş Başarılı! Sisteme tam erişim sağlandı.")
                    basarili_giris = True
                    break
                else:
                    print(f"  > ⚠️ Giriş reddedildi veya sayfa yüklenemedi.")
                    driver.refresh()
            except Exception as e:
                print(f"  > ❌ Form hatası: {str(e)[:40]}")
                driver.refresh()

        if not basarili_giris:
            raise Exception("4 denemeye rağmen OBİS giriş aşaması geçilemedi.")

        # --- AŞAMA 2: NAVİGASYON ---
        print("  > 📂 'Not/Sınav' menüsü açılıyor...")
        try:
            menu_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Not/Sınav')] | /html/body/form/div[10]/div/div[1]/ul/li[4]/div/a")))
            driver.execute_script("arguments[0].click();", menu_btn)
            
            time.sleep(3)
            print("  > 🔗 'Öğrenci Not Görüntüle' butonu aranıyor...")
            not_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Öğrenci Not Görüntüle')]")))
            driver.execute_script("arguments[0].click();", not_link)
            print("  > ✅ Not sayfası başarıyla yüklendi.")
        except Exception as e:
            raise Exception(f"Navigasyon hatası: {str(e)[:40]}")

        # --- AŞAMA 3: DÖNEM SEÇİMİ ---
        print(f"  > [3/4] 🎯 Dönem seçim oku (Arrow) açılıyor...")
        try:
            time.sleep(5)
            donem_oku = wait.until(EC.element_to_be_clickable((By.ID, DONEM_ARROW_ID)))
            driver.execute_script("arguments[0].click();", donem_oku)
            
            time.sleep(2)
            en_ust = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'rcbItem')][1]")))
            driver.execute_script("arguments[0].click();", en_ust)
            print("  > ✅ Dönem başarıyla seçildi.")
        except Exception as e:
            raise Exception(f"Dönem seçimi hatası: {str(e)[:40]}")

        # --- AŞAMA 4: VERİ OKUMA ---
        print("  > [4/4] 📊 Tablo taranıyor...")
        time.sleep(7)
        satirlar = driver.find_elements(By.TAG_NAME, "tr")
        current = {}
        for s in satirlar:
            txt = s.text.strip()
            if "Vize:" in txt or "Final:" in txt:
                anahtar = "Vize:" if "Vize:" in txt else "Final:"
                parca = txt.split(anahtar)
                ders_adi = parca[0].strip()
                not_degeri = anahtar + parca[1].strip()
                current[ders_adi] = not_degeri
                print(f"    - Okundu: {ders_adi} -> {not_degeri}")
        
        if not current:
            print("  > ⚠️ Tablo bulundu ama ders verisi ayıklanamadı.")
            
        print(f"  > ✨ İşlem tamamlandı. {len(current)} ders güncellendi.")
        return current

    except Exception as e:
        hata_mesaji = str(e)
        print(f"  > 🆘 AKSAMA BİLDİRİSİ: {hata_mesaji[:100]}")
        telegram_mesaj_gonder(f"⚠ osimhen uyarısı: Nöbet sırasında bir aksama yaşandı!\n\nDetay: {hata_mesaji[:100]}")
        return None
    finally:
        driver.quit()

# --- ANA DÖNGÜ ---
last_saved_grades = hafizayi_yukle()
is_first_run = True if not last_saved_grades else False
print("\n🚀 osimhen v4.8.1 BAŞLATILDI")
telegram_mesaj_gonder("🚀 osimhen v4.8.1 Yayında! Tam raporlama aktif.")

while True:
    zaman = time.strftime('%H:%M:%S')
    print(f"\n[{zaman}] Nöbetçi kontrolü başlatıyor...")
    
    yeni = not_kontrol_et()
    
    if yeni and len(yeni) > 0:
        degisiklik_var = False
        for d, n in yeni.items():
            if d not in last_saved_grades or last_saved_grades[d] != n:
                telegram_mesaj_gonder(f"🔔 NOT GÜNCELLEMESİ!\n\n📚 {d}\n📝 {n}")
                last_saved_grades[d] = n
                degisiklik_var = True
        
        if degisiklik_var or is_first_run:
            hafizayi_kaydet(last_saved_grades)
            if is_first_run:
                telegram_mesaj_gonder(f"✅ Sistem başarıyla bağlandı! {len(yeni)} ders izleniyor.")
                is_first_run = False
                print(f"[{zaman}] ✅ Başarılı: Veriler hafızaya kaydedildi.")
    
    bekleme_zamani = time.strftime('%H:%M:%S', time.localtime(time.time() + 900))
    print(f"[{zaman}] 💤 İşlem bitti. Bir sonraki kontrol saati: {bekleme_zamani}")
    time.sleep(900)