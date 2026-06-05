from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from user_store import user_store  # Import user_store biar diinisialisasi duluan

# Import semua Screen (TIDAK PERLU import EmoticonButton!)
from screen.splash_screen import SplashScreen
from screen.input_name_screen import InputNameScreen
from screen.main_screen import MainScreen
from screen.menu_screen import MenuScreen
from screen.tdy_screen import TodayFeelingScreen
from screen.curhat_screen import CurhatScreen
from screen.history_screen import HistoryScreen
from screen.motivation_screen import MotivationScreen
from screen.mood_tracker import MoodTrackerScreen, MoodStatScreen
from screen.bubble_game import BubbleGameScreen  


class MyApp(App):
    def build(self):
        #Window.size = (360, 640)
        
        sm = ScreenManager(transition=FadeTransition(duration=0.5)) 
        
        # Tambahkan HANYA Screen ke ScreenManager
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(InputNameScreen(name='input_name'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TodayFeelingScreen(name='tdy'))
        sm.add_widget(CurhatScreen(name='curhat'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(MotivationScreen(name='motivation'))
        sm.add_widget(MoodTrackerScreen(name='mood_tracker'))
        sm.add_widget(MoodStatScreen(name='mood_stats'))    
        sm.add_widget(BubbleGameScreen(name='bubble_game'))
        
        print("="*50)
        print("SEMUA SCREEN TERDAFTAR:")
        for screen in sm.screens:
            print(f"  - {screen.name}")
        print("="*50)
        
        
        return sm

if __name__ == '__main__':
    MyApp().run()