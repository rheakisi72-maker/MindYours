from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from user_store import user_store 
from kivy.metrics import dp,sp

Builder.load_file('screen/splash_screen1.kv')

class SplashScreen(Screen):
    def on_enter(self):
        print("SplashScreen entered")
        Clock.schedule_once(self.go_to_next, 3.5)  # 3 detik splash
    
    def go_to_next(self, dt):
        print("Navigasi dari splash ke input_name")
        self.manager.current = 'input_name'
    