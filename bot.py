import json
import time
from datetime import datetime
from pynput.mouse import Controller, Button
import pyautogui
from PIL import Image
from colorama import init


# Zaman damgası ile mesaj yazdıran fonksiyon
init(autoreset=True)
resource_cycle_index = 0


def print_with_timestamp(message):
    """Zaman damgası ekleyerek renkli yazı yazdırır"""
    print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - {message}")


def some_function_for_bot(app):
    """Bot işlemi sırasında GUI'ye mesaj gönderen fonksiyon"""
    app.print_with_timestamp(
        f"Bot işlemi başlatılıyor: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    time.sleep(2)
    app.print_with_timestamp(
        f"İşlem tamamlandı: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

# Ayarları yükleyen fonksiyon


def load_settings():
    with open("ayarlar.json", "r", encoding="utf-8") as file:
        settings = json.load(file)
    return settings


def find_and_click_image(image_path, confidence=0.6, timeout=5, max_retries=3, click_delay=None):
    """Belirli bir görüntüyü ekranda bulan ve tıklayan fonksiyon, zaman aşımı ve deneme sayısı eklenmiş."""

    # Eğer click_delay belirtilmemişse, settings.json'dan sure değeri alınır.
    if click_delay is None:
        settings = load_settings()  # Ayarları yükle
        # Eğer sure değeri yoksa varsayılan 10 saniye kullanılır.
        click_delay = settings.get("sure", 10)

    retries = 0  # Deneme sayısını başlatıyoruz.
    while retries < max_retries:
        try:
            location = pyautogui.locateCenterOnScreen(
                image_path, confidence=confidence)
            if location:
                mouse = Controller()
                mouse.position = location
                mouse.click(Button.left, 1)
                print_with_timestamp(
                    f"{image_path} tıklandı ({location[0]}, {location[1]}).")

                # Tıklama sonrası 5 saniye bekleme ve geri sayım
                for i in range(click_delay, 0, -1):
                    print_with_timestamp(
                        f"Tıklama sonrası {i} saniye bekleniyor...")
                    time.sleep(1)  # 1 saniye bekle
                # Resim bulundu ve tıklandı, işlem başarıyla tamamlandı.
                return True
            else:
                retries += 1  # Resim bulunamadığında denemeyi artırıyoruz.
                print_with_timestamp(
                    f"{image_path} bulunamadı, tekrar denenecek... (Deneme {retries}/{max_retries})")
                time.sleep(timeout)  # Belirtilen süre kadar bekle
        except pyautogui.ImageNotFoundException:
            print_with_timestamp(f"{image_path} ekranda bulunamadı.")
            retries += 1  # Resim bulunamazsa da denemeyi artırıyoruz.
            time.sleep(timeout)  # Resim bulunamazsa bekleme süresi

    # Max deneme sayısına ulaşıldıysa, resim bulunamadı demek.
    print_with_timestamp(f"{image_path} {max_retries} denemede de bulunamadı.")
    return False  # Max deneme sayısına ulaşıldı, resim hala bulunamadı.


def scroll_down():
    """Ekranı biraz aşağı kaydıran fonksiyon"""
    mouse = Controller()
    screen_width, screen_height = pyautogui.size()
    start_y = int(screen_height / 2)
    mouse.position = (screen_width // 2, start_y)
    mouse.press(Button.left)
    time.sleep(0.2)  # Kaydırma işlemini simüle etmek için kısa bekleme
    # Ekranın dörtte biri kadar aşağı kaydır
    mouse.move(0, int(screen_height * 0.25))
    mouse.release(Button.left)
    print_with_timestamp("Ekran aşağı kaydırıldı.")


def basla():
    # basla.png tıklanır
    if not find_and_click_image("ekran/basla.png"):
        print_with_timestamp("basla.png bulunamadı, işlem sonlanıyor.")
        return False
    print_with_timestamp("basla.png tıklandı.")
    time.sleep(2)  # bekleme süresi

    # aoe.png tıklanır
    if not find_and_click_image("ekran/aoe.png"):
        print_with_timestamp("aoe.png bulunamadı, işlem sonlanıyor.")
        return False
    print_with_timestamp("aoe.png tıklandı.")
    time.sleep(30)
    print_with_timestamp("Başla işlemi tamamlandı.")
    return True


def ittifak_teknoloji():
    print_with_timestamp("İttifak teknoloji fonksiyonu başlatıldı...")

    # ittifak.png tıklanır
    if not find_and_click_image("ekran/ittifak.png"):
        print_with_timestamp("ittifak.png bulunamadı, işlem sonlanıyor.")
        return False
    print_with_timestamp("ittifak.png tıklandı.")

    # teknoloji.png tıklanır
    if not find_and_click_image("ekran/teknoloji.png"):
        print_with_timestamp("teknoloji.png bulunamadı, işlem sonlanıyor.")
        return False
    print_with_timestamp("teknoloji.png tıklandı.")

    # yesil.png tıklanır
    if not find_and_click_image("ekran/yesil.png"):
        print_with_timestamp("yesil.png bulunamadı, cikis.png tıklanıyor...")
        # yesil.png bulunamazsa cikis.png tıklanır
        if not find_and_click_image("ekran/cikis.png"):
            print_with_timestamp("cikis.png bulunamadı, esc tuşuna basılıyor.")
            pyautogui.press('esc')  # cikis.png bulunamazsa esc tuşuna bas
            # cikis.png tekrar aranır
            if not find_and_click_image("ekran/cikis.png"):
                print_with_timestamp(
                    "cikis.png yine bulunamadı, tekrar esc tuşuna basılıyor.")
                # cikis.png yine bulunamazsa tekrar esc tuşuna bas
                pyautogui.press('esc')
            else:
                print_with_timestamp("cikis.png tıklandı.")
        else:
            print_with_timestamp("cikis.png tıklandı.")
    else:
        print_with_timestamp("yesil.png tıklandı.")

    # bagis.png resmine belirli bir sayıda hızlı tıklamak için
    click_count = 5  # Kaç kez tıklanmasını istediğiniz sayıyı belirleyin

    for i in range(click_count):
        if not find_and_click_image("ekran/bagis.png"):
            print_with_timestamp(
                f"{i+1}. tıklamada bagis.png bulunamadı, işlem sonlanıyor.")
            return False
        print_with_timestamp(
            f"bagis.png hızlı tıklandı ({i+1}/{click_count}).")

    # cikis.png tıklanır
    if not find_and_click_image("ekran/cikis.png"):
        print_with_timestamp("cikis.png bulunamadı, esc tuşuna basılıyor.")
        pyautogui.press('esc')  # cikis.png bulunamazsa esc tuşuna bas
        # cikis.png tekrar aranır
    if not find_and_click_image("ekran/cikis.png"):
        print_with_timestamp(
            "cikis.png yine bulunamadı, tekrar esc tuşuna basılıyor.")
        # cikis.png yine bulunamazsa tekrar esc tuşuna bas
        pyautogui.press('esc')
    if not find_and_click_image("ekran/cikis.png"):
        print_with_timestamp(
            "cikis.png yine bulunamadı, tekrar esc tuşuna basılıyor.")
        # cikis.png yine bulunamazsa tekrar esc tuşuna bas
        pyautogui.press('esc')
    else:
        print_with_timestamp("cikis.png tıklandı.")

    print_with_timestamp("İttifak teknoloji işlemi tamamlandı.")
    return True


def odun_toplama():
    # map.png ve ara.png tıklanır
    if not find_and_click_image("ekran/map.png"):
        print_with_timestamp(
            "map.png bulunamadı,f3 basılıyor ve işleme devam ediyor")
        pyautogui.press('f3')
    else:
        print_with_timestamp("map.png tıklandı.")
    time.sleep(2)
    if not find_and_click_image("ekran/ara.png"):
        print_with_timestamp("ara.png bulunamadı, işlem sonlanıyor.")
        return False
    print_with_timestamp("ara.png tıklandı.")
    time.sleep(2)
    # mapodun.png tıklanır
    if not find_and_click_image("ekran/mapodun.png"):
        print_with_timestamp("mapodun.png bulunamadı, işlem sonlanıyor.")
    else:
        print_with_timestamp("mapodun.png tıklandı.")

    # ara2.png tıklanır
    if not find_and_click_image("ekran/ara2.png"):
        print_with_timestamp("ara2.png bulunamadı, işlem sonlanıyor.")
    else:
        print_with_timestamp("ara2.png tıklandı.")

    # topla.png bulunana kadar tekrar ara2.png tıklanır
    while not find_and_click_image("ekran/topla.png"):
        print_with_timestamp("topla.png bulunamadı, eksi.png tıklanıyor...")
        if not find_and_click_image("ekran/eksi.png"):
            print_with_timestamp("eksi.png bulunamadı, işlem sonlanıyor.")
            return False
        print_with_timestamp("eksi.png tıklandı.")

        if not find_and_click_image("ekran/ara2.png"):
            print_with_timestamp(
                "ara2.png tekrar bulunamadı, işlem sonlanıyor.")
        else:
            print_with_timestamp("ara2.png tıklandı.")

    print_with_timestamp("topla.png tıklandı.")

    # konuslandir.png tıklanır
    if not find_and_click_image("ekran/konuslandir.png"):
        print_with_timestamp("konuslandir.png bulunamadı, işlem sonlanıyor.")
    else:
        print_with_timestamp("konuslandir.png tıklandı.")

    # iptal.png varsa tıklanır, sonra cikis2.png
    if find_and_click_image("ekran/iptal.png"):
        print_with_timestamp("iptal.png bulundu, tıklanıyor...")
        if not find_and_click_image("ekran/cikis2.png"):
            print_with_timestamp(
                "cikis2.png bulunamadı, esc tuşuna basılıyor.")
            pyautogui.press('esc')
    else:
        if not find_and_click_image("ekran/cikis2.png"):
            print_with_timestamp(
                "cikis2.png bulunamadı, esc tuşuna basılıyor.")
            pyautogui.press('esc')

    # mapdon.png ve kale.png tıklanır
    if not find_and_click_image("ekran/mapdon.png"):
        print_with_timestamp(
            "mapdon.png bulunamadı, f3 tuşuna basılıyor ve devam ediliyor.")
        pyautogui.press('f3')
    else:
        print_with_timestamp("mapdon.png tıklandı.")

    if not find_and_click_image("ekran/kale.png"):
        print_with_timestamp(
            "kale.png bulunamadı, f3 tuşuna basılıyor ve devam ediliyor.")
        pyautogui.press('f3')
    else:
        print_with_timestamp("kale.png tıklandı.")

    print_with_timestamp("Odun toplama işlemi tamamlandı.")
    return True


def yiyecek_toplama():
    # map.png ve ara.png tıklanır
    if not find_and_click_image("ekran/map.png"):
        print_with_timestamp(
            "map.png bulunamadı,f3 basılıyor ve işleme devam ediyor")
        pyautogui.press('f3')
    else:
        print_with_timestamp("map.png tıklandı.")
    time.sleep(2)
    if not find_and_click_image("ekran/ara.png"):
        print_with_timestamp("ara.png bulunamadı, işlem sonlanıyor.")
        return False
    print_with_timestamp("ara.png tıklandı.")
    time.sleep(2)
    # mapodun.png tıklanır
    if not find_and_click_image("ekran/mapyiyecek.png"):
        print_with_timestamp("mapyiyecek.png bulunamadı, işlem sonlanıyor.")
    else:
        print_with_timestamp("mapyiyecek.png tıklandı.")

    # ara2.png tıklanır
    if not find_and_click_image("ekran/ara2.png"):
        print_with_timestamp("ara2.png bulunamadı, işlem sonlanıyor.")
    else:
        print_with_timestamp("ara2.png tıklandı.")

    # topla.png bulunana kadar tekrar ara2.png tıklanır
    while not find_and_click_image("ekran/topla.png"):
        print_with_timestamp("topla.png bulunamadı, eksi.png tıklanıyor...")
        if not find_and_click_image("ekran/eksi.png"):
            print_with_timestamp("eksi.png bulunamadı, işlem sonlanıyor.")
            return False
        print_with_timestamp("eksi.png tıklandı.")

        if not find_and_click_image("ekran/ara2.png"):
            print_with_timestamp(
                "ara2.png tekrar bulunamadı, işlem sonlanıyor.")
        else:
            print_with_timestamp("ara2.png tıklandı.")

    print_with_timestamp("topla.png tıklandı.")

    # konuslandir.png tıklanır
    if not find_and_click_image("ekran/konuslandir.png"):
        print_with_timestamp("konuslandir.png bulunamadı, işlem sonlanıyor.")
    else:
        print_with_timestamp("konuslandir.png tıklandı.")

    # iptal.png varsa tıklanır, sonra cikis2.png
    if find_and_click_image("ekran/iptal.png"):
        print_with_timestamp("iptal.png bulundu, tıklanıyor...")
        if not find_and_click_image("ekran/cikis2.png"):
            print_with_timestamp(
                "cikis2.png bulunamadı, esc tuşuna basılıyor.")
            pyautogui.press('esc')
    else:
        if not find_and_click_image("ekran/cikis2.png"):
            print_with_timestamp(
                "cikis2.png bulunamadı, esc tuşuna basılıyor.")
            pyautogui.press('esc')

    # mapdon.png ve kale.png tıklanır
    if not find_and_click_image("ekran/mapdon.png"):
        print_with_timestamp(
            "mapdon.png bulunamadı, f3 tuşuna basılıyor ve devam ediliyor.")
        pyautogui.press('f3')
    else:
        print_with_timestamp("mapdon.png tıklandı.")

    if not find_and_click_image("ekran/kale.png"):
        print_with_timestamp(
            "kale.png bulunamadı, f3 tuşuna basılıyor ve devam ediliyor.")
        pyautogui.press('f3')
    else:
        print_with_timestamp("kale.png tıklandı.")

    print_with_timestamp("Yiyecek toplama işlemi tamamlandı.")
    return True


def tas_toplama():
    # map.png ve ara.png tıklanır
    if not find_and_click_image("ekran/map.png"):
        print_with_timestamp(
            "map.png bulunamadı,f3 basılıyor ve işleme devam ediyor")
        pyautogui.press('f3')
    else:
        print_with_timestamp("map.png tıklandı.")
    time.sleep(2)
    if not find_and_click_image("ekran/ara.png"):
        print_with_timestamp("ara.png bulunamadı, işlem sonlanıyor.")
        return False
    print_with_timestamp("ara.png tıklandı.")
    time.sleep(2)
    # mapodun.png tıklanır
    if not find_and_click_image("ekran/maptas.png"):
        print_with_timestamp("maptas.png bulunamadı, işlem sonlanıyor.")
    else:
        print_with_timestamp("maptas.png tıklandı.")

    # ara2.png tıklanır
    if not find_and_click_image("ekran/ara2.png"):
        print_with_timestamp("ara2.png bulunamadı, işlem sonlanıyor.")
    else:
        print_with_timestamp("ara2.png tıklandı.")

    # topla.png bulunana kadar tekrar ara2.png tıklanır
    while not find_and_click_image("ekran/topla.png"):
        print_with_timestamp("topla.png bulunamadı, eksi.png tıklanıyor...")
        if not find_and_click_image("ekran/eksi.png"):
            print_with_timestamp("eksi.png bulunamadı, işlem sonlanıyor.")
            return False
        print_with_timestamp("eksi.png tıklandı.")

        if not find_and_click_image("ekran/ara2.png"):
            print_with_timestamp(
                "ara2.png tekrar bulunamadı, işlem sonlanıyor.")
        else:
            print_with_timestamp("ara2.png tıklandı.")

    print_with_timestamp("topla.png tıklandı.")

    # konuslandir.png tıklanır
    if not find_and_click_image("ekran/konuslandir.png"):
        print_with_timestamp("konuslandir.png bulunamadı, işlem sonlanıyor.")
    else:
        print_with_timestamp("konuslandir.png tıklandı.")

    # iptal.png varsa tıklanır, sonra cikis2.png
    if find_and_click_image("ekran/iptal.png"):
        print_with_timestamp("iptal.png bulundu, tıklanıyor...")
        if not find_and_click_image("ekran/cikis2.png"):
            print_with_timestamp(
                "cikis2.png bulunamadı, esc tuşuna basılıyor.")
            pyautogui.press('esc')
    else:
        if not find_and_click_image("ekran/cikis2.png"):
            print_with_timestamp(
                "cikis2.png bulunamadı, esc tuşuna basılıyor.")
            pyautogui.press('esc')

    # mapdon.png ve kale.png tıklanır
    if not find_and_click_image("ekran/mapdon.png"):
        print_with_timestamp(
            "mapdon.png bulunamadı, f3 tuşuna basılıyor ve devam ediliyor.")
        pyautogui.press('f3')
    else:
        print_with_timestamp("mapdon.png tıklandı.")

    if not find_and_click_image("ekran/kale.png"):
        print_with_timestamp(
            "kale.png bulunamadı, f3 tuşuna basılıyor ve devam ediliyor.")
        pyautogui.press('f3')
    else:
        print_with_timestamp("kale.png tıklandı.")

    print_with_timestamp("Taş toplama işlemi tamamlandı.")
    return True


def altin_toplama():
    # map.png ve ara.png tıklanır
    if not find_and_click_image("ekran/map.png"):
        print_with_timestamp(
            "map.png bulunamadı,f3 basılıyor ve işleme devam ediyor")
        pyautogui.press('f3')
    else:
        print_with_timestamp("map.png tıklandı.")
    time.sleep(2)
    if not find_and_click_image("ekran/ara.png"):
        print_with_timestamp("ara.png bulunamadı, işlem sonlanıyor.")
        return False
    print_with_timestamp("ara.png tıklandı.")
    time.sleep(2)
    # mapodun.png tıklanır
    if not find_and_click_image("ekran/mapaltin.png"):
        print_with_timestamp("mapaltin.png bulunamadı, işlem sonlanıyor.")
    else:
        print_with_timestamp("mapaltin.png tıklandı.")

    # ara2.png tıklanır
    if not find_and_click_image("ekran/ara2.png"):
        print_with_timestamp("ara2.png bulunamadı, işlem sonlanıyor.")
    else:
        print_with_timestamp("ara2.png tıklandı.")

    # topla.png bulunana kadar tekrar ara2.png tıklanır
    while not find_and_click_image("ekran/topla.png"):
        print_with_timestamp("topla.png bulunamadı, eksi.png tıklanıyor...")
        if not find_and_click_image("ekran/eksi.png"):
            print_with_timestamp("eksi.png bulunamadı, işlem sonlanıyor.")
            return False
        print_with_timestamp("eksi.png tıklandı.")

        if not find_and_click_image("ekran/ara2.png"):
            print_with_timestamp(
                "ara2.png tekrar bulunamadı, işlem sonlanıyor.")
        else:
            print_with_timestamp("ara2.png tıklandı.")

    print_with_timestamp("topla.png tıklandı.")

    # konuslandir.png tıklanır
    if not find_and_click_image("ekran/konuslandir.png"):
        print_with_timestamp("konuslandir.png bulunamadı, işlem sonlanıyor.")
    else:
        print_with_timestamp("konuslandir.png tıklandı.")

    # iptal.png varsa tıklanır, sonra cikis2.png
    if find_and_click_image("ekran/iptal.png"):
        print_with_timestamp("iptal.png bulundu, tıklanıyor...")
        if not find_and_click_image("ekran/cikis2.png"):
            print_with_timestamp(
                "cikis2.png bulunamadı, esc tuşuna basılıyor.")
            pyautogui.press('esc')
    else:
        if not find_and_click_image("ekran/cikis2.png"):
            print_with_timestamp(
                "cikis2.png bulunamadı, esc tuşuna basılıyor.")
            pyautogui.press('esc')

    # mapdon.png ve kale.png tıklanır
    if not find_and_click_image("ekran/mapdon.png"):
        print_with_timestamp(
            "mapdon.png bulunamadı, f3 tuşuna basılıyor ve devam ediliyor.")
        pyautogui.press('f3')
    else:
        print_with_timestamp("mapdon.png tıklandı.")

    if not find_and_click_image("ekran/kale.png"):
        print_with_timestamp(
            "kale.png bulunamadı, f3 tuşuna basılıyor ve devam ediliyor.")
        pyautogui.press('f3')
    else:
        print_with_timestamp("kale.png tıklandı.")

    print_with_timestamp("Altın toplama işlemi tamamlandı.")
    return True


def upgrade_building():
    images = [
        "ekran/panel.png",
        "ekran/panel2.png",
        "ekran/panelinsaat.png",
        "ekran/git.png",
        "ekran/yukselt1.png",
        "ekran/yukselt2.png",
        "ekran/yardim.png",
        "ekran/cikis.png"
    ]

    for image in images:
        print_with_timestamp(f"Bina yükseltme işlemi - {image} aranıyor...")

        if image in ["ekran/panel.png", "ekran/panel2.png"]:
            if not find_and_click_image(image, max_retries=3):
                print_with_timestamp(
                    f"{image} bulunamadı, F1 tuşuna basılıyor...")
                pyautogui.press('f1')
                continue

        elif image == "ekran/git.png":
            if not find_and_click_image(image, max_retries=3):
                print_with_timestamp(
                    f"{image} bulunamadığı için işlem sonlandırılıyor.")
                # git.png bulunamadığında işlem sonlandırılır
                if not find_and_click_image("ekran/cikis2.png", max_retries=3):
                    print_with_timestamp(
                        "cikis2.png de bulunamadı, Esc tuşuna basılıyor...")
                    pyautogui.press('esc')
                return False  # İşlem bitirilir ve diğer fonksiyona geçilir

        elif image == "ekran/yukselt2.png":
            if not find_and_click_image(image, max_retries=3):
                print_with_timestamp(
                    f"{image} bulunamadı, dahafazla.png aranıyor...")
                if find_and_click_image("ekran/dahafazla.png", max_retries=3):
                    print_with_timestamp(
                        "dahafazla.png bulundu, tıklanıyor...")
                    if find_and_click_image("ekran/tumunukullan.png", max_retries=3):
                        print_with_timestamp(
                            "tumunukullan.png bulundu, tıklanıyor...")
                        if not find_and_click_image(image, max_retries=3):
                            print_with_timestamp(
                                "Tekrar yukselt2.png aranıyor fakat bulunamadı.")
                            if not find_and_click_image("ekran/cikis.png", max_retries=3):
                                print_with_timestamp(
                                    "cikis.png bulunamadı, Esc tuşuna basılıyor...")
                                pyautogui.press('esc')
                            return False
                    else:
                        print_with_timestamp(
                            "tumunukullan.png bulunamadı, işlem sonlandırılıyor...")
                        if not find_and_click_image("ekran/cikis.png", max_retries=3):
                            pyautogui.press('esc')
                        return False
                else:
                    print_with_timestamp(
                        "dahafazla.png bulunamadı, işlem sonlandırılıyor...")
                    if not find_and_click_image("ekran/cikis.png", max_retries=3):
                        pyautogui.press('esc')
                    return False

        elif not find_and_click_image(image, max_retries=3):
            print_with_timestamp(
                f"{image} bulunamadığı için bir sonraki resme geçiliyor.")
            continue

    print_with_timestamp("Bina yükseltme işlemi tamamlandı.")
    return True


def train_units():
    images = [
        "ekran/panel.png",
        "ekran/panel2.png",
        "ekran/panelegitim.png"
    ]

    # İlk olarak panel, panel2, panelegitim sırasıyla arama yapılır
    for image in images:
        print_with_timestamp(f"Asker eğitimi işlemi - {image} aranıyor...")

        # panel.png veya panel2.png bulunamazsa F1 tuşuna basılır
        if image in ["ekran/panel.png", "ekran/panel2.png"]:
            if not find_and_click_image(image):
                print_with_timestamp(
                    f"{image} bulunamadı, F1 tuşuna basılıyor...")
                pyautogui.press('f1')
                continue
        elif not find_and_click_image(image):
            print_with_timestamp(
                f"{image} bulunamadığı için bir sonraki resme geçiliyor.")
            continue

    print_with_timestamp("Eğitim paneli açıldı, asker eğitimi başlatılıyor...")

    # "panelegitim" açıldıktan sonra, önce "orduya katil" aratılır
    ordkatil_found = find_and_click_image("ekran/orduyakatil.png")
    if ordkatil_found:
        print_with_timestamp("Asker türü bulundu, eğitim başlatılıyor...")
        # ordkatil bulunduysa bile, git.png tekrar aranır
        if find_and_click_image("ekran/git.png"):
            print_with_timestamp("Git butonu tıklandı, eğitim başlatılıyor...")
    else:
        # "orduya katil" bulunamazsa "git" aranır
        if find_and_click_image("ekran/git.png"):
            print_with_timestamp("Git butonu tıklandı, eğitim başlatılıyor...")
        else:
            # Hem "orduya katil" hem de "git" bulunmazsa, ekran kaydırılır
            print_with_timestamp(
                "Asker türü bulunamadı, ekran kaydırılıyor...")
            scroll_up()  # Sayfa kaydırma işlemi
            time.sleep(5)  # Kaydırma sonrası bekleme

            # Kaydırmadan sonra tekrar "orduya katil" arar
            ordkatil_found_after_scroll = find_and_click_image(
                "ekran/orduyakatil.png")
            if ordkatil_found_after_scroll:
                print_with_timestamp(
                    "Asker türü bulundu, eğitim başlatılıyor...")
                # ordkatil bulunduysa bile, git.png tekrar aranır
                if find_and_click_image("ekran/git.png"):
                    print_with_timestamp(
                        "Git butonu tıklandı, eğitim başlatılıyor...")
            else:
                # Eğer yine bulunmazsa, "git" arar
                if find_and_click_image("ekran/git.png"):
                    print_with_timestamp(
                        "Git butonu tıklandı, eğitim başlatılıyor...")
                else:
                    print_with_timestamp(
                        "Ne asker türü ne de git butonu bulunamadı, işlem sona erdiriliyor.")
                    # Çıkış işlemi ve diğer fonksiyona geçiş
                    if not find_and_click_image("ekran/cikis2.png"):
                        print_with_timestamp(
                            "Cikis2.png bulunamadı, Esc tuşuna basılıyor...")
                        pyautogui.press('esc')
                    return False  # İşlem sonlanır ve diğer fonksiyona geçilir

    # Eğitim butonlarını tıklama
    if not find_and_click_image("ekran/egit.png"):
        print_with_timestamp("Eğit butonu bulunamadı, işlem sona erdiriliyor.")
        return False

    if not find_and_click_image("ekran/egit2.png"):
        print_with_timestamp(
            "İkinci eğit butonu bulunamadı, işlem sona erdiriliyor.")
        return False

    # Çıkış işlemi
    find_and_click_image("ekran/cikis.png")
    print_with_timestamp("Asker eğitimi tamamlandı.")
    return True


def ittifak_yardim():
    print_with_timestamp("İttifak yardımı fonksiyonu başlatıldı...")

    image_path = "ekran/ittifakyardim.png"

    if find_and_click_image(image_path):
        print_with_timestamp("İttifak yardımı yapıldı.")
        return True
    else:
        print_with_timestamp(
            "İttifak yardımı bulunamadı. Yeniden deneniyor...")
        if find_and_click_image(image_path):
            print_with_timestamp("İttifak yardımı yapıldı.")
            return True
        else:
            print_with_timestamp("İttifak yardımı yine bulunamadı.")
            return False


def gather_resources():
    resources = [
        "ekran/odun.png",
        "ekran/yiyecek.png",
        "ekran/tas.png",
        "ekran/altin.png"
    ]
    for resource in resources:
        print_with_timestamp(f"Erzak toplama işlemi - {resource} aranıyor...")
        if find_and_click_image(resource):
            return True
    return False


def scroll_up():
    # Ekranın ortasını bulmak için ekranın genişliğini ve yüksekliğini alıyoruz
    screen_width, screen_height = pyautogui.size()

    # Ekranın ortasına tıklıyoruz
    pyautogui.click(screen_width // 2, screen_height // 2)

    # Fareyi basılı tutarak yukarı kaydırıyoruz
    pyautogui.mouseDown()  # Fareyi basılı tutuyoruz
    pyautogui.move(0, -300, duration=1)  # Fareyi yukarıya doğru kaydırıyoruz
    pyautogui.mouseUp()  # Fareyi bırakıyoruz

    # Kaydırma sonrası biraz bekleyebiliriz
    # Kaydırma sonrası bekleme (isteğe bağlı)


def main():
    settings = load_settings()
    print_with_timestamp("Bot başlatılıyor...")

    # Ayarları konsola yazdır
    for key, value in settings.items():
        # Yalnızca aktif ayarları göster
        if value not in [False, "", None] and not (str(value).endswith(".png") or str(value).endswith(".txt")) and value != 0:
            print_with_timestamp(f"Ayar: {key} - {value}")
        sure = settings.get("sure")
    while True:
        print_with_timestamp("Kontrol başlatılıyor...")

        if settings.get("basla"):
            print_with_timestamp("Oyun başlatılıyor...")
            if basla():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("Oyun başlatıldı.")

        if settings.get("ittifakyardim"):
            print_with_timestamp("İttifak yardımı işlemi başlatılıyor...")
            if ittifak_yardim():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("İttifak yardımı tamamlandı.")

        if settings.get("ittifakteknoloji"):
            print_with_timestamp("İttifak teknoloji işlemi başlatılıyor...")
            if ittifak_teknoloji():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("İttifak teknoloji puanı tamamlandı.")

        if settings.get("maptas"):
            print_with_timestamp("Taş toplama işlemi başlatılıyor...")
            if tas_toplama():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("Taş toplama tamamlandı.")

        if settings.get("ittifakyardim"):
            print_with_timestamp("İttifak yardımı işlemi başlatılıyor...")
            if ittifak_yardim():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("İttifak yardımı tamamlandı.")

        if settings.get("erzak"):
            print_with_timestamp("Erzak toplama işlemi başlatılıyor...")
            if gather_resources():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("Erzak toplama tamamlandı.")

        if settings.get("ittifakyardim"):
            print_with_timestamp("İttifak yardımı işlemi başlatılıyor...")
            if ittifak_yardim():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("İttifak yardımı tamamlandı.")

        if settings.get("mapaltin"):
            print_with_timestamp("Altın toplama işlemi başlatılıyor...")
            if altin_toplama():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("Altın toplama tamamlandı.")

        if settings.get("ittifakyardim"):
            print_with_timestamp("İttifak yardımı işlemi başlatılıyor...")
            if ittifak_yardim():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("İttifak yardımı tamamlandı.")

        if settings.get("bina"):
            print_with_timestamp("Bina yükseltme işlemi başlatılıyor...")
            if upgrade_building():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("Bina yükseltme tamamlandı.")

        if settings.get("ittifakyardim"):
            print_with_timestamp("İttifak yardımı işlemi başlatılıyor...")
            if ittifak_yardim():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("İttifak yardımı tamamlandı.")

        if settings.get("mapyiyecek"):
            print_with_timestamp("Yiyecek toplama işlemi başlatılıyor...")
            if yiyecek_toplama():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("Yiyecek toplama tamamlandı.")

        if settings.get("ittifakyardim"):
            print_with_timestamp("İttifak yardımı işlemi başlatılıyor...")
            if ittifak_yardim():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("İttifak yardımı tamamlandı.")

        if settings.get("asker_egit"):
            print_with_timestamp("Asker eğitimi işlemi başlatılıyor...")
            if train_units():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("Asker eğitimi tamamlandı.")

        if settings.get("ittifakyardim"):
            print_with_timestamp("İttifak yardımı işlemi başlatılıyor...")
            if ittifak_yardim():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("İttifak yardımı tamamlandı.")

        if settings.get("mapodun"):
            print_with_timestamp("Odun toplama işlemi başlatılıyor...")
            if odun_toplama():  # İşlem tamamlanana kadar bekliyoruz
                print_with_timestamp("Odun toplama tamamlandı.")
        sure = settings.get("sure")
        print_with_timestamp(f"{sure} saniye bekleniyor...")
        time.sleep(sure)  # "sure" saniye bekle ve tekrar kontrol et


if __name__ == "__main__":
    main()
