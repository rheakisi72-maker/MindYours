from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from user_store import user_store  # Pakai user_store
from kivy.metrics import dp,sp

Builder.load_file('screen/main_screen1.kv')  # Pakai nama asli kamu: main_screen1.kv

class MainScreen(Screen):
    def on_enter(self):
        print("=== MainScreen on_enter ===")
        if user_store.exists('user'):  # Pakai user_store
            username = user_store.get('user')['name']
            welcome_text = f'Salam kenal {username},\nSekarang kenalan sama\nteman - teman Joy yuk!'
        else:
            welcome_text = 'Salam kenal,\nSekarang kenalan sama\nteman - teman Joy yuk!'
        
        self.ids.main_label.text = welcome_text
        print(f"DEBUG MainScreen: Text yang diset = {welcome_text}")
    
    def go_to_next_screen(self):
        print("Tombol Next ditekan - pindah ke menu")
        self.manager.current = 'menu'