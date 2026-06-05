from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from user_store import user_store

class EmotionButton(FloatLayout):
    feeling_name = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_touch_down(self, touch):
        # Cek apakah touch ada di dalam area widget ini
        if self.collide_point(*touch.pos):
            if self.feeling_name:
                print(f"✓ {self.feeling_name} diklik!")
                
                # Simpan feeling ke storage
                user_store.put('current_feeling', feeling=self.feeling_name)
                
                # Pindah ke curhat screen
                # Cari screen manager dari parent hierarchy
                screen = self.parent
                while screen and not hasattr(screen, 'manager'):
                    screen = screen.parent
                
                if screen and hasattr(screen, 'manager'):
                    screen.manager.current = 'curhat'
                
                return True  # Konsumsi touch event
        
        return super().on_touch_down(touch)