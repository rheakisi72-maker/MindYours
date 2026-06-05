from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from user_store import user_store 

# Pastikan path ini benar
Builder.load_file('screen/menu_screen.kv')

class MenuScreen(Screen):
    def on_enter(self):
        """Dipanggil otomatis saat screen dibuka"""
        print("=== MenuScreen on_enter dipanggil ===")
        
        # Update greeting text dengan nama user
        if user_store.exists('user'):
            username = user_store.get('user')['name']
            # Saya persingkat sedikit biar muat di header
            greeting_text = f"Hai {username},\nPilih yang Kamu Butuh :3"
            print(f"DEBUG: Username ditemukan = {username}")
        else:
            greeting_text = "Hai Bestie,\nPilih yang Kamu Butuh :3"
            print("DEBUG: Username tidak ditemukan")
        
        self.ids.greeting_label.text = greeting_text

    def go_to_today_feeling(self):
        print("Navigasi ke Today Feeling")
        self.manager.current = 'tdy'
    
    def go_to_motivation(self):
        print("Navigasi ke Motivation")
        self.manager.current = 'motivation'
    
    def go_to_mood_tracker(self):
        print("Navigasi ke Mood Tracker")
        self.manager.current = 'mood_tracker'

    # --- FITUR BARU ---
    def go_to_mini_game(self):
        print("Navigasi ke Mini Game (Bubble)")
        # Pastikan di main.py screen gamenya dinamai 'bubble_game'
        self.manager.current = 'bubble_game'