from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty  # Tambah ini buat bind warna
from user_store import user_store
from datetime import datetime
from kivy.metrics import dp,sp

Builder.load_file('screen/curhat_screen.kv')

class CurhatScreen(Screen):
    character_bg_color = ObjectProperty([0.53, 0.81, 0.92, 1])  # Default biru muda, bisa diubah
    
    def __init__(self, **kwargs):
        super(CurhatScreen, self).__init__(**kwargs)
        self.current_feeling = None
        self.current_username = None
    
    def on_pre_enter(self):
        """Dipanggil sebelum screen ditampilkan"""
        print("=== CurhatScreen on_pre_enter ===")
        
        # Ambil nama user
        self.current_username = "Kamu"
        if user_store.exists('user'):
            self.current_username = user_store.get('user')['name']
            print(f"Username ditemukan: {self.current_username}")
        else:
            print("Username tidak ditemukan, menggunakan default: Kamu")
        
        # Ambil feeling yang dipilih
        self.current_feeling = "Unknown"
        if user_store.exists('current_feeling'):
            self.current_feeling = user_store.get('current_feeling')['feeling']
            print(f"Feeling ditemukan: {self.current_feeling}")
        else:
            print("Feeling tidak ditemukan")
        
        # Update UI
        self.update_ui()
    
    def on_enter(self):
        """Dipanggil saat screen sudah ditampilkan"""
        print("=== CurhatScreen on_enter ===")
        
        # Clear text input
        self.ids.curhat_input.text = ""
        self.ids.curhat_input.hint_text = 'Ceritakan perasaanmu disini...'
        
        print(f"Screen siap - User: {self.current_username}, Feeling: {self.current_feeling}")
    
    def update_ui(self):
        """Update semua elemen UI"""
        # Update greeting
        greeting_text = f"Hello, {self.current_username}!"
        self.ids.greeting_label.text = greeting_text
        print(f"Greeting updated: {greeting_text}")
        
        # Mapping feeling ke file gambar
        feeling_images = {
            'Anger': 'ang.png',
            'Anxiety': 'anx.png',
            'Joy': 'joy.png',
            'Disgust': 'dgs.png',
            'Envy': 'env.png',
            'Sadness': 'sad.png',
            'Embarrassment': 'emb.png',
            'Fear': 'fear.png',
            'Ennui': 'enn.png'
        }
        
        # Mapping feeling ke warna background
        feeling_colors = {
            'Anger': [1, 0.4, 0.4, 1],           # Merah
            'Anxiety': [1, 0.7, 0.4, 1],         # Orange
            'Joy': [1, 1, 0.4, 1],               # Kuning
            'Disgust': [0.6, 1, 0.4, 1],         # Hijau muda
            'Envy': [0.4, 1, 0.9, 1],            # Cyan
            'Sadness': [0.5, 0.7, 1, 1],         # Biru
            'Embarrassment': [1, 0.5, 0.9, 1],   # Pink
            'Fear': [0.8, 0.6, 1, 1],            # Ungu muda
            'Ennui': [0.5, 0.5, 1, 1]            # Biru ungu
        }
        
        # Update gambar karakter
        if self.current_feeling in feeling_images:
            image_file = feeling_images[self.current_feeling]
            self.ids.character_image.source = image_file
            print(f"Image updated: {image_file}")
        else:
            print(f"Feeling '{self.current_feeling}' tidak ditemukan dalam mapping")
            self.ids.character_image.source = 'joy.png'  # Default
        
        # Update warna background karakter via ObjectProperty (AMAN, gak crash)
        if self.current_feeling in feeling_colors:
            self.character_bg_color = feeling_colors[self.current_feeling]  # Ubah property, KV otomatis update
            print(f"Background color updated for: {self.current_feeling}")
    
    def go_back(self):
        """Kembali ke Today Feeling screen"""
        print("Tombol back ditekan - kembali ke Today Feeling")
        self.manager.current = 'tdy'
    
    def save_curhat(self):
        """Simpan curhat ke storage"""
        curhat_text = self.ids.curhat_input.text.strip()
        
        print(f"=== Menyimpan Curhat ===")
        print(f"Text: {curhat_text}")
        
        if not curhat_text:
            print("ERROR: Curhat kosong!")
            self.ids.curhat_input.hint_text = "Ceritakan perasaanmu dulu yuk!"
            self.ids.curhat_input.hint_text_color = [1, 0, 0, 1]
            return
        
        # Buat ID unik berdasarkan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        curhat_id = f"curhat_{timestamp}"
        
        # Data yang akan disimpan
        curhat_data = {
            'username': self.current_username,
            'feeling': self.current_feeling,
            'text': curhat_text,
            'date': datetime.now().strftime("%d/%m/%Y"),
            'time': datetime.now().strftime("%H:%M"),
            'timestamp': timestamp
        }
        
        # Simpan ke storage
        try:
            user_store.put(curhat_id, **curhat_data)
            print(f"✓ Curhat berhasil disimpan dengan ID: {curhat_id}")
            print(f"  User: {curhat_data['username']}")
            print(f"  Feeling: {curhat_data['feeling']}")
            print(f"  Date: {curhat_data['date']} {curhat_data['time']}")
            print(f"  Text length: {len(curhat_text)} characters")
            
            # Verifikasi data tersimpan
            saved = user_store.get(curhat_id)
            print(f"✓ Verifikasi: Data berhasil dibaca kembali")
            
            # Feedback visual ke user
            self.ids.curhat_input.text = ""
            self.ids.curhat_input.hint_text = "✓ Curhat berhasil disimpan!"
            self.ids.curhat_input.hint_text_color = [0, 0.7, 0, 1]
            
        
            
        except Exception as e:
            print(f"ERROR saat menyimpan curhat: {e}")
            self.ids.curhat_input.hint_text = "Error! Gagal menyimpan."
            self.ids.curhat_input.hint_text_color = [1, 0, 0, 1]
    
    def go_to_menu(self):
        """Kembali ke menu utama"""
        print("Kembali ke menu utama")
        self.manager.current = 'menu'

    def go_to_history(self):
        """Pindah ke screen history"""
        print("Pindah ke History Screen")
        self.manager.current = 'history'