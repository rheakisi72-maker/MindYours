from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from user_store import user_store

Builder.load_file('screen/history_screen.kv')

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        self.username = "Kamu"
    
    def on_pre_enter(self):
        """Load data setiap kali screen dibuka"""
        print("\n=== HistoryScreen on_pre_enter ===")
        
        # Ambil username
        if user_store.exists('user'):
            self.username = user_store.get('user')['name']
        
        # Load semua catatan
        self.load_history()
    
    def load_history(self):
        """Load semua catatan curhat dari storage"""
        print("Loading history...")
        
        # Clear container
        container = self.ids.history_container
        container.clear_widgets()
        
        # Ambil semua key yang dimulai dengan 'curhat_'
        all_keys = user_store.keys()
        curhat_keys = [k for k in all_keys if k.startswith('curhat_')]
        
        print(f"Found {len(curhat_keys)} curhat entries")
        
        if len(curhat_keys) == 0:
            # Tampilkan pesan kosong
            empty_label = Label(
                text='Belum ada catatan.\nYuk curhat dulu!',
                font_size='16sp',
                color=(0.5, 0.5, 0.5, 1),
                halign='center',
                size_hint_y=None,
                height=200
            )
            container.add_widget(empty_label)
            return
        
        # Sort berdasarkan timestamp (terbaru dulu)
        curhat_keys.sort(reverse=True)
        
        # Mapping feeling ke emoji/image
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
        
        feeling_colors = {
            'Anger': [1, 0.4, 0.4, 1],
            'Anxiety': [1, 0.7, 0.4, 1],
            'Joy': [1, 1, 0.4, 1],
            'Disgust': [0.6, 1, 0.4, 1],
            'Envy': [0.4, 1, 0.9, 1],
            'Sadness': [0.5, 0.7, 1, 1],
            'Embarrassment': [1, 0.5, 0.9, 1],
            'Fear': [0.8, 0.6, 1, 1],
            'Ennui': [0.5, 0.5, 1, 1]
        }
        
        # Buat card untuk setiap catatan
        for key in curhat_keys:
            data = user_store.get(key)
            
            # Buat item card
            card = HistoryCard(
                curhat_id=key,
                feeling=data.get('feeling', 'Unknown'),
                date=data.get('date', ''),
                time=data.get('time', ''),
                text=data.get('text', ''),
                feeling_image=feeling_images.get(data.get('feeling'), 'joy.png'),
                feeling_color=feeling_colors.get(data.get('feeling'), [0.8, 0.8, 0.8, 1]),
                on_delete=self.delete_curhat
            )
            
            container.add_widget(card)
    
    def delete_curhat(self, curhat_id):
        """Hapus catatan curhat"""
        print(f"Deleting: {curhat_id}")
        
        if user_store.exists(curhat_id):
            user_store.delete(curhat_id)
            print(f"✓ Deleted: {curhat_id}")
            
            # Reload history
            self.load_history()
    
    def go_back(self):
        """Kembali ke menu"""
        print("Back to menu")
        self.manager.current = 'menu'


class HistoryCard(BoxLayout):
    """Widget untuk menampilkan satu catatan curhat (Fixed Version)"""
    
    def __init__(self, curhat_id, feeling, date, time, text, feeling_image, feeling_color, on_delete, **kwargs):
        super(HistoryCard, self).__init__(**kwargs)
        
        self.curhat_id = curhat_id
        self.feeling = feeling
        self.date = date
        self.time = time
        self.full_text = text
        self.feeling_image = feeling_image
        self.feeling_color = feeling_color
        self.on_delete_callback = on_delete
        self.is_expanded = False
        
        # Konfigurasi Container Utama
        self.orientation = 'vertical'
        self.size_hint_y = None
        # Tinggi awal hanya header + padding, nanti nambah kalau di-expand
        self.height = dp(100) 
        self.padding = dp(10)
        self.spacing = dp(5)
        
        # Background dengan rounded corners
        with self.canvas.before:
            Color(*feeling_color)
            self.bg_rect = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=[dp(15)]
            )
        
        # Bind agar background mengikuti ukuran kartu saat teks memanjang
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        self.build_layout()
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def build_layout(self):
        # --- BAGIAN ATAS (Header: Gambar, Info, Tombol) ---
        header_box = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=dp(80), # Tinggi area header fix
            spacing=dp(10)
        )
        
        # 1. Gambar Emosi (Kiri)
        emoji_img = Image(
            source=self.feeling_image,
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'center_y': 0.5}
        )
        header_box.add_widget(emoji_img)
        
        # 2. Info (Tengah: Tanggal & Preview Pendek)
        info_box = BoxLayout(
            orientation='vertical', 
            spacing=dp(2),
            pos_hint={'center_y': 0.5}
        )
        
        # Nama Perasaan
        feeling_label = Label(
            text=self.feeling,
            font_size=dp(16),
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(20),
            halign='left', valign='middle'
        )
        feeling_label.bind(size=feeling_label.setter('text_size')) # Agar align left jalan
        info_box.add_widget(feeling_label)
        
        # Tanggal
        datetime_label = Label(
            text=f"{self.date} • {self.time}",
            font_size=dp(11),
            color=(0.2, 0.2, 0.2, 0.7),
            size_hint_y=None,
            height=dp(15),
            halign='left', valign='middle'
        )
        datetime_label.bind(size=datetime_label.setter('text_size'))
        info_box.add_widget(datetime_label)

        # Preview Text (Hanya muncul saat collapsed)
        self.preview_text_label = Label(
            text=self.full_text[:40] + "..." if len(self.full_text) > 40 else self.full_text,
            font_size=dp(12),
            color=(0.1, 0.1, 0.1, 1),
            size_hint_y=1, # Isi sisa ruang di info_box
            halign='left', valign='top'
        )
        self.preview_text_label.bind(size=lambda instance, val: setattr(instance, 'text_size', (val[0], val[1])))
        info_box.add_widget(self.preview_text_label)
        
        header_box.add_widget(info_box)
        
        # 3. Tombol (Kanan)
        btn_box = BoxLayout(
            orientation='vertical', 
            size_hint_x=None, 
            width=dp(40),
            size_hint_y=None,
            height=dp(80),
            spacing=dp(15),
            pos_hint={'center_y': 0.5}
        )
        
        
        # Tombol Delete
        delete_btn = Button(
            size_hint=(None, None),
            size=(dp(24), dp(24)), 
            pos_hint={'center_x': 0.5},
            background_normal='trash.png',
            background_down='trash.png',
            border=(0,0,0,0)
            
        )
        delete_btn.bind(on_press=lambda x: self.on_delete_callback(self.curhat_id))
        
        # Tombol Expand (Panah)
        self.expand_btn = Button(
            size_hint=(None, None),
            size=(dp(16), dp(16)),
            pos_hint={'center_x': 0.5},
            background_normal='expand.png', 
            background_down='expand.png',
            border=(0, 0, 0, 0)
        )
        self.expand_btn.bind(on_press=self.toggle_expand)
        
        btn_box.add_widget(delete_btn)
        btn_box.add_widget(self.expand_btn)
        header_box.add_widget(btn_box)
        
        self.add_widget(header_box)
        
        # --- BAGIAN BAWAH (Full Text - Hidden by default) ---
        self.full_text_label = Label(
            text=self.full_text,
            font_size=dp(14),
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=0,   # Awalnya 0 (tersembunyi)
            opacity=0,  # Invisible
            markup=True
        )
        self.add_widget(self.full_text_label)

    def toggle_expand(self, instance):
        """Logika buka tutup kartu yang AMAN dari overflow"""
        self.is_expanded = not self.is_expanded
        
        if self.is_expanded:
            # Ganti icon panah
            self.expand_btn.text = ''
            
            # Sembunyikan preview pendek agar tidak dobel
            self.preview_text_label.opacity = 0
            
            # Setting Full Text
            self.full_text_label.opacity = 1
            # Text size mengikuti lebar kartu dikurangi padding (Dynamic Width!)
            self.full_text_label.text_size = (self.width - dp(20), None)
            self.full_text_label.texture_update()
            
            # Set tinggi label sesuai tekstur font
            self.full_text_label.height = self.full_text_label.texture_size[1] + dp(10)
            
            # Update tinggi Kartu utama
            self.height = dp(90) + self.full_text_label.height
            
        else:
            # Kembalikan ke mode ringkas
            self.expand_btn.text = ''
            self.preview_text_label.opacity = 1
            
            self.full_text_label.height = 0
            self.full_text_label.opacity = 0
            
            self.height = dp(100) # Kembali ke tinggi awal