from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from user_store import user_store  # Pakai user_store biar konsisten
from kivy.metrics import dp,sp

Builder.load_file('screen/input_name_screen1.kv') 
class InputNameScreen(Screen):
    def save_and_next(self):
        username = self.ids.name_input.text.strip()
        
        print(f"DEBUG: Username yang diinput = '{username}'")
        
        if username:
            user_store.put('user', name=username)  # Pakai user_store
            print(f"DEBUG: Nama tersimpan = {username}")
            
            # CEK APAKAH BENAR TERSIMPAN
            saved_name = user_store.get('user')['name']
            print(f"DEBUG: Nama yang dibaca dari JSON = '{saved_name}'")
            
            self.manager.current = 'main'
        else:
            print("DEBUG: Username kosong!")
            self.ids.name_input.hint_text = 'Nama tidak boleh kosong!'
            self.ids.name_input.hint_text_color = (1, 0, 0, 1)