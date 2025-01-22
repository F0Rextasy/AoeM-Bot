import pyautogui
import os
from pynput import mouse
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkFont
import customtkinter
import pygetwindow as gw
import json
import subprocess
import bot
import sys
import time
import threading
from datetime import datetime


class BotGUI:
    def __init__(self, root):
        ctk.set_appearance_mode("dark")  # Karanlık mod
        ctk.set_default_color_theme("dark-blue")  # Varsayılan renk teması
        # Pencereyi her zaman üstte tutacak özellik ekleyin
        root.attributes("-topmost", True)
        root.iconbitmap('ikon.ico')
        self.root = root
        self.selected_window = None  # Seçilen pencereyi tutan değişken
        self.root.title("AoeM - bot © 2024 v2")
        # Genişliği 600, yüksekliği 400 olarak ayarlandı
        self.root.geometry("600x300")
        self.root.resizable(False, False)  # Boyutlandırmayı sabit tut
        self.is_running = False  # Botun çalışma durumu
        self.settings = {
            "asker_egit": ctk.BooleanVar(value=False),
            "bina": ctk.BooleanVar(value=False),
            "erzak": ctk.BooleanVar(value=False),
            "ittifakyardim": ctk.BooleanVar(value=False),
            "ittifakteknoloji": ctk.BooleanVar(value=False),
            "sure": 10,
            "mapodun": ctk.BooleanVar(value=False),
            "maptas": ctk.BooleanVar(value=False),
            "mapyiyecek": ctk.BooleanVar(value=False),
            "maptas": ctk.BooleanVar(value=False),
            "mapaltin": ctk.BooleanVar(value=False),
            "basla": ctk.BooleanVar(value=True),
            "language": "TR"  # Default language is Turkish
        }

        self.lang_data = self.load_language_data()

        # GUI öğelerinin oluşturulması (butonlar, sekmeler, vb.)
        self.create_gui()

        # Ayarları otomatik olarak içe aktar
        self.import_settings()

    def load_language_data(self):
        # Dil dosyasını yükler
        try:
            with open("lang.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Dil dosyası bulunamadı, varsayılan dil kullanılacak.")
            return {"TR": {}, "EN": {}}  # Varsayılan boş veri döndürür

    def change_language(self, lang):
        self.settings["language"] = lang
        self.save_settings()
        self.update_gui_language()
        self.update_tab_names()

    def update_gui_language(self):
        lang = self.settings["language"]
        lang_dict = self.lang_data.get(lang, {})

        # Butonlar ve metinler burada güncellenir
        self.scan_button.configure(
            text=lang_dict.get("scan_window", "Pencere Tara"))
        self.select_button.configure(text=lang_dict.get("select", "Seç"))
        self.start_stop_button.configure(text=lang_dict.get("start", "BAŞLAT"))
        self.stop_button.configure(text=lang_dict.get("stop", "DURDUR"))
        self.status_label.configure(
            text=lang_dict.get("f2_message", "{F2} ya da"))
        self.save_settings_button.configure(
            text=lang_dict.get("save", "Kaydet"))
        self.import_settings_button.configure(
            text=lang_dict.get("import", "İçe Aktar"))
        self.bina_checkbox.configure(text=lang_dict.get("building", "Bina"))
        self.erzak_checkbox.configure(text=lang_dict.get("food", "Erzak"))
        self.odun_checkbox.configure(text=lang_dict.get("odun", "Odun"))
        self.yiyecek_checkbox.configure(
            text=lang_dict.get("yiyecek", "Yiyecek"))
        self.altin_checkbox.configure(text=lang_dict.get("altin", "Altın"))
        self.tas_checkbox.configure(text=lang_dict.get("tas", "Taş"))
        self.basla_checkbox.configure(
            text=lang_dict.get("oto_basla", "Oto Başla"))
        self.asker_checkbox.configure(
            text=lang_dict.get("train_soldiers", "Asker Eğit"))
        self.ittifak_checkbox.configure(
            text=lang_dict.get("alliance_help", "İttifak Yardımı"))
        self.teknoloji_checkbox.configure(
            text=lang_dict.get("technology_points", "Teknoloji Puanı"))
        self.sure_label.configure(text=lang_dict.get("time", "Süre (sn):"))
        self.update_tab_names()
        self.selected_window.set(lang_dict.get(
            "selected_window", "Pencere Seçin"))
        self.language_menu.set(lang)

    def update_tab_names(self):
        lang = self.settings.get("language", "TR")
        lang_dict = self.lang_data.get(lang, {})
        # Yeni sekme isimleri
        new_tab_names = {
            "Basit": lang_dict.get("basit", "Basit"),
            "Toplama": lang_dict.get("toplama", "Toplama"),
            "İttifak": lang_dict.get("ittifak", "İttifak"),
        }

        # CTkTabview içindeki butonların metinlerini güncelle
        for old_name, new_name in new_tab_names.items():
            for button in self.tabview._segmented_button.winfo_children():
                if button.cget("text") == old_name:
                    button.configure(text=new_name)

    def create_gui(self):
        # Pencere Tara kısmı
        self.window_frame = ctk.CTkFrame(self.root)
        self.window_frame.pack(pady=10, fill="x")

        self.scan_button = ctk.CTkButton(
            self.window_frame,
            text="Pencere Tara",
            command=self.scan_windows,
            width=80)
        self.scan_button.pack(side=tk.LEFT, padx=5)

        self.selected_window = ctk.StringVar(
            value="Pencere Seçin")  # Varsayılan değer
        self.window_list = ctk.CTkComboBox(
            self.window_frame, variable=self.selected_window, values=[])
        self.window_list.pack(side=tk.LEFT, padx=5)

        self.select_button = ctk.CTkButton(
            self.window_frame,
            text="Seç",
            command=self.select_window,
            width=80)
        self.select_button.pack(side=tk.LEFT, padx=5)

        # Butonlar ve diğer bileşenler burada tanımlanacak
        self.start_stop_button = customtkinter.CTkButton(
            self.window_frame, text="BAŞLAT", command=self.toggle_start_stop, width=50)
        self.start_stop_button.pack(
            side=tk.RIGHT)  # Pack ile yerleştirme

        self.stop_button = customtkinter.CTkButton(
            self.root, fg_color="red", text="DURDUR",  command=self.toggle_start_stop)
        self.stop_button.pack_forget()  # Başlangıçta gizli

        self.process = None

        # "F2 ile durdurabilirsin" yazısı
        self.status_label = ctk.CTkLabel(self.window_frame, text="{F2} ya da", font=("Arial", 14, "bold"),  # Kalın yazı
                                         anchor="w")  # Sağ tarafa yaslama
        self.status_label.pack_forget()  # Başlangıçta gizli

        # Ana çerçeveyi ayarla
        # Burada self.main_frame tanımlanıyor
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Sol çerçeve (tabview ve süre giriş alanını içerir)
        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill="y", expand=True)

        # Sağ çerçeve (konsol alanını içerir)
        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.pack(side=tk.TOP, fill="both", expand=True)

        #  Tabview
        self.tabview = ctk.CTkTabview(self.left_frame, height=1)
        self.tabview.pack(fill="both", expand=True, padx=5, pady=5)

        # Basit sekmesi
        self.features_tab = self.tabview.add("Basit")

        self.bina_checkbox = ctk.CTkCheckBox(
            self.features_tab, text="Bina", variable=self.settings["bina"])
        self.bina_checkbox.grid(row=0, column=0, sticky="w", padx=10, pady=2)

        self.erzak_checkbox = ctk.CTkCheckBox(
            self.features_tab, text="Erzak", variable=self.settings["erzak"])
        self.erzak_checkbox.grid(row=0, column=1, sticky="w", padx=10, pady=2)

        self.asker_checkbox = ctk.CTkCheckBox(
            self.features_tab, text="Asker Eğit", variable=self.settings["asker_egit"])
        self.asker_checkbox.grid(row=1, column=0, sticky="w", padx=10, pady=2)

        # Yan yana yerleştirme için bir alt çerçeve oluşturuyoruz
        self.sure_frame = ctk.CTkFrame(self.left_frame)
        self.sure_frame.pack(anchor="w", padx=10, pady=5, fill="x")

        # Süre Giriş Alanı (Tabview'in altına, sol çerçeveye)
        self.sure_label = ctk.CTkLabel(self.sure_frame, text="Süre (sn):")
        self.sure_label.pack(side="left", padx=(0, 5))

        validate_command = (self.root.register(self.validate_sure_entry), '%P')
        self.sure_entry = ctk.CTkEntry(
            self.sure_frame, validate="key", validatecommand=validate_command, width=50)
        self.sure_entry.pack(side="left")
        self.custom_font = CTkFont(size=11)  # Yazı boyutunu küçülttük
        # Otomatik Başlatma
        self.basla_checkbox = ctk.CTkCheckBox(
            self.sure_frame, text="Oto Başla", variable=self.settings["basla"])
        self.basla_checkbox.pack(side="right", padx=(0, 5))
        # Toplama Sekmesi
        self.features_tab1 = self.tabview.add("Toplama")

        # Checkbox'lar
        self.odun_checkbox = ctk.CTkCheckBox(
            self.features_tab1, text="Odun", variable=self.settings["mapodun"])
        self.odun_checkbox.grid(row=0, column=0, sticky="w", padx=10, pady=2)

        self.yiyecek_checkbox = ctk.CTkCheckBox(
            self.features_tab1, text="Yiyecek", variable=self.settings["mapyiyecek"])
        self.yiyecek_checkbox.grid(
            row=0, column=1, sticky="w", padx=10, pady=2)

        self.tas_checkbox = ctk.CTkCheckBox(
            self.features_tab1, text="Taş", variable=self.settings["maptas"])
        self.tas_checkbox.grid(
            row=1, column=0, sticky="w", padx=10, pady=2)

        self.altin_checkbox = ctk.CTkCheckBox(
            self.features_tab1, text="Altın", variable=self.settings["mapaltin"])
        self.altin_checkbox.grid(row=1, column=1, sticky="w", padx=10, pady=2)

        # Toplama Sekmesi
        self.features_tab2 = self.tabview.add("İttifak")

        self.ittifak_checkbox = ctk.CTkCheckBox(
            self.features_tab2, text="İttifak Yardımı", variable=self.settings["ittifakyardim"])
        self.ittifak_checkbox.grid(
            row=0, column=0, sticky="w", padx=10, pady=2)

        self.teknoloji_checkbox = ctk.CTkCheckBox(
            self.features_tab2, text="Teknoloji Puanı", variable=self.settings["ittifakteknoloji"])
        self.teknoloji_checkbox.grid(
            row=1, column=0, sticky="w", padx=10, pady=2)

        # Konsol Alanı
        # Sağ çerçeve (konsol için)
        self.console_text = ctk.CTkTextbox(
            self.right_frame, font=self.custom_font, height=20, width=300)
        self.console_text.pack(side=tk.TOP, fill="both",
                               expand=True, padx=(5, 0))

        # Import ayarları butonu
        self.import_settings_button = ctk.CTkButton(
            self.window_frame, text="İçe Aktar", command=self.import_settings, width=45)
        self.import_settings_button.pack(side=tk.RIGHT, padx=5)

        # Save ayarları butonu
        self.save_settings_button = ctk.CTkButton(
            self.window_frame, text="Kaydet", command=self.save_settings, width=50)
        self.save_settings_button.pack(side=tk.RIGHT, padx=0)

        # Footer Alanı
        footer_frame = tk.Frame(self.root, bg="#2E3B4E", height=40)
        footer_frame.pack(side="bottom", fill="x", padx=10, pady=5)

        footer_label = tk.Label(footer_frame,
                                text="F0Rextasy © AoeM-bot 2024",
                                font=("Helvetica", 10, "bold"),
                                fg="#FFD700",
                                bg="#2E3B4E",
                                relief="solid",
                                bd=1,
                                padx=10, pady=5)
        # Footer label sol tarafa yerleştirildi
        footer_label.pack(fill="both", expand=True, side=tk.LEFT)

        # Dil Seçimi (Footer'a eklenip en sağa yerleştirildi)
        self.language_menu = ctk.CTkOptionMenu(
            footer_frame, values=["TR", "EN", "ES", "FR", "DE", "ID", "PT", "IT", "TH", "AR", "RU", "ZH-TW", "ZH-CN", "JA", "KO"],  command=self.change_language)
        self.language_menu.set(self.settings["language"])
        # Sağ tarafa yerleştirildi
        self.language_menu.pack(side=tk.RIGHT, padx=5)

        # F2 tuşuna basıldığında toggle_start_stop fonksiyonunu çağırıyoruz
        self.root.bind("<F2>", self.toggle_start_stop_from_key)

    def toggle_start_stop_from_key(self, event=None):
        self.toggle_start_stop()

    def toggle_start_stop(self):
        # Mevcut dili ve dil ayarlarını al
        lang = self.settings.get("language", "TR")  # Varsayılan dil TR
        lang_dict = self.lang_data.get(lang, {})

        # Dil sözlüğünden buton metinlerini çek
        start_text = lang_dict.get("start", "BAŞLAT")
        stop_text = lang_dict.get("stop", "DURDUR")

        if self.start_stop_button.cget("text") == start_text:
            # Buton metnini DURDUR olarak güncelle
            self.start_stop_button.configure(text=stop_text)
            self.start_bot_in_thread()

            # Pencereyi küçült
            self.root.geometry("280x350+0+0")

            # Tabview ve diğer butonları gizle
            self.tabview.pack_forget()
            self.scan_button.pack_forget()
            self.select_button.pack_forget()
            self.window_list.pack_forget()
            self.save_settings_button.pack_forget()
            self.import_settings_button.pack_forget()
            self.sure_frame.pack_forget()
            self.left_frame.pack_forget()
            self.language_menu.pack_forget()

            # Konsol varsa doğru yere yerleştir
            if not hasattr(self, 'console_text'):
                self.console_text = ctk.CTkTextbox(
                    self.right_frame, font=self.custom_font, height=20, width=300)
            self.console_text.pack(
                side=tk.TOP, fill="both", expand=True, padx=(5, 0))

            # "F2 ile durdurabilirsin" mesajını göster
            self.status_label.pack(anchor="e", padx=10)

        else:
            # Buton metnini BAŞLAT olarak güncelle
            self.start_stop_button.configure(text=start_text)
            self.stop_bot_in_thread()

            # Pencereyi eski haline getir
            self.root.geometry("600x300")

            # Tabview ve diğer butonları geri göster
            self.tabview.pack(fill="both", expand=True, padx=5, pady=5)
            self.scan_button.pack(side=tk.LEFT, padx=5)
            self.window_list.pack(side=tk.LEFT, padx=5)
            self.select_button.pack(side=tk.LEFT, padx=5)
            self.save_settings_button.pack(side=tk.RIGHT, padx=5)
            self.import_settings_button.pack(side=tk.RIGHT, padx=5)
            self.sure_frame.pack(anchor="w", padx=10, pady=5, fill="x")
            self.left_frame.pack(side=tk.LEFT, fill="y", expand=True)
            self.right_frame.pack(side=tk.RIGHT, fill="both", expand=True)
            self.language_menu.pack(side=tk.RIGHT, padx=5)

            # Konsolu sağ frame'e yeniden ekle
            if not hasattr(self, 'console_text'):
                self.right_frame = ctk.CTkFrame(self.main_frame)
                self.right_frame.pack(side=tk.TOP, fill="both", expand=True)
                self.console_text = ctk.CTkTextbox(
                    self.right_frame, font=self.custom_font)
                self.console_text.pack(side=tk.TOP, fill="both",
                                       expand=True, padx=(5, 0))

            # "F2 ile durdurabilirsin" mesajını gizle
            self.status_label.pack_forget()

    def start_bot_in_thread(self):
        self.process_thread = threading.Thread(target=self.start_bot)
        self.process_thread.start()

    def stop_bot_in_thread(self):
        # Bir iş parçacığı durdurmak için bir bayrak kullanıyoruz
        if self.process:
            self.process.terminate()  # Botu durdur
            self.process = None

    def start_bot(self):
        # bot.py dosyasının yolunu ayarlayın
        python_executable = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'bot.py')
        # Python çalıştırma komutu
        python_command = ['python', python_executable]
        # Odağı giriş alanından kaldırmak için root üzerine odaklanın
        self.root.focus()
        # Botu başlat
        try:
            self.process = subprocess.Popen(
                python_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.read_output()
        except Exception as e:
            self.console_text.insert(tk.END, f"Hata: {e}\n")

    def read_output(self):

        output = None  # Başlangıçta output'a None değeri veriyoruz
        if self.process:
            output = self.process.stdout.readline()
        if output:  # output'a bir değer atandıysa
            self.console_text.insert(tk.END, output)  # Konsola yazdır
            self.console_text.see(tk.END)  # En son satıra kaydır
        if self.process and self.process.poll() is None:  # Bot hala çalışıyorsa
            # Çıktıları okumaya devam et
            self.root.after(100, self.read_output)
        else:
            # Eğer process None ise, bot başlatılmadı veya durdurulmuş
            self.console_text.insert(
                tk.END, "Hata: Bot durduruldu veya başlatılmadı.\n")
            self.console_text.see(tk.END)

    def stop_bot(self):
        if self.process:
            self.process.terminate()  # Botu durdur
            self.process = None

    def print_with_timestamp(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        colored_message = f"{timestamp} - {message}"

        # Konsola zaman damgası ile mesaj yazdırma
        self.console_text.insert(tk.END, colored_message + "\n")
        self.console_text.yview(tk.END)  # En son satıra kaydırma

    def console(self, message):
        self.print_with_timestamp(message)

    def scan_windows(self):
        windows = gw.getAllTitles()
        self.window_list.configure(values=windows)
        self.console("Pencereler tarandı: \n " + ", ".join(windows))

    def select_window(self):
        selected_window = self.selected_window.get()
        if selected_window != "Pencere Seçin":
            # Seçilen pencereyi etkinleştir
            gw.getWindowsWithTitle(selected_window)[0].activate()
            # Seçilen pencereyi konsola yazdır
            self.console(f"Seçilen pencere: {selected_window}")
        else:
            self.console("Lütfen bir pencere seçin.")

    def validate_sure_entry(self, value):
        # Yalnızca sayı girildiğinden emin olur
        if value == "" or value.isdigit():
            return True
        else:
            self.console("Hata: Lütfen sadece sayı girin.")
            return False

    def import_settings(self):
        settings_path = 'ayarlar.json'

        if not os.path.exists(settings_path):
            self.console(f"Hata: Ayar dosyası bulunamadı: {settings_path}")
            return

        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content:
                self.console("Hata: Ayar dosyası boş.")
                return

        try:
            settings = json.loads(content)
        except json.JSONDecodeError as e:
            self.console(
                f"Hata: Ayar dosyası geçersiz JSON formatında. Hata: {e}")
            return

        for key, var in self.settings.items():
            if key in settings:
                if key == "sure":
                    self.sure_entry.delete(0, tk.END)
                    self.sure_entry.insert(0, str(settings[key]))
                elif hasattr(var, 'set'):
                    var.set(settings[key])
                else:
                    self.settings[key] = settings[key]
            else:
                self.console(
                    f"Hata: '{key}' anahtarı ayar dosyasında bulunamadı.")

        # Dil ayarını güncelle
        # Varsayılan olarak "TR" dilini al
        language = settings.get("language", "TR")
        self.change_language(language)  # Dil değişikliğini uygula

        self.console(f"Ayarlar içe aktarıldı: {settings_path}")

    def save_settings(self):
        # Ayarları kaydet
        sure_value = self.sure_entry.get()
        if not sure_value:
            self.console("Hata: Lütfen süreyi girin.")
            return

        # Odağı giriş alanından kaldırmak için root üzerine odaklanın
        self.root.focus()

        settings_path = 'ayarlar.json'
        with open(settings_path, 'w', encoding='utf-8') as f:
            # Süre ayarını sayıya çevirip settings'e ekle
            self.settings["sure"] = int(sure_value)

            json.dump(
                {key: (var.get() if hasattr(var, 'get') else var)
                 for key, var in self.settings.items()},
                f, ensure_ascii=False, indent=4
            )
        self.console(f"Ayarlar kaydedildi: {settings_path}")


if __name__ == "__main__":
    root = ctk.CTk()  # CTk ana penceresini oluşturuyoruz
    app = BotGUI(root)  # GUI'yi başlatıyoruz
    root.mainloop()
