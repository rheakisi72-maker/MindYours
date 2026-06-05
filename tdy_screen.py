from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.lang import Builder
from user_store import user_store
from kivy.metrics import dp,sp

# Definisi EmotionButton SEBELUM load KV file
class EmotionButton(FloatLayout):
    feeling_name = StringProperty('')
    
    def on_touch_down(self, touch):
        # Cek apakah touch ada di dalam area widget ini
        if self.collide_point(*touch.pos):
            if self.feeling_name:
                print(f"✓ {self.feeling_name} diklik!")
                
                # Simpan feeling ke storage
                user_store.put('current_feeling', feeling=self.feeling_name)
                
                # Pindah ke curhat screen
                screen = self.parent
                while screen and not hasattr(screen, 'manager'):
                    screen = screen.parent
                
                if screen and hasattr(screen, 'manager'):
                    screen.manager.current = 'curhat'
                
                return True
        
        return super().on_touch_down(touch)

# Load KV file SETELAH EmotionButton didefinisikan
Builder.load_file('screen/tdy_screen.kv')

class TodayFeelingScreen(Screen):
    def go_to_back_screen(self):
        print("Kembali ke Menu")
        self.manager.current = 'menu'