from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.core.window import Window
from kivy.metrics import dp
import random
import os

from user_store import user_store 

# Load KV
current_dir = os.path.dirname(os.path.abspath(__file__))
# Pastikan file kv ada dan namanya benar
kv_path = os.path.join(current_dir, 'bubble_game.kv')
if os.path.exists(kv_path):
    Builder.load_file(kv_path)

class FallingBubble(ButtonBehavior, Image):
    speed = NumericProperty(2) 
    is_popped = BooleanProperty(False)
    
    image_source = StringProperty('bubble.png') 
    
    img_intact = 'bubble.png'
    img_popped = 'popped.png'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image_source = self.img_intact
        # Ukuran random pakai dp agar responsif
        random_size = dp(random.randint(60, 100))
        self.size = (random_size, random_size)

    def on_press(self):
        # 1. Cek apakah sudah meletus?
        if self.is_popped:
            return

        # 2. Cek apakah Game sedang berjalan?
        p = self.parent
        screen = None
        while p:
            if isinstance(p, BubbleGameScreen):
                screen = p
                break
            p = p.parent
        
        if screen:
            # Kalau Game Over/Stop, bubble jadi batu
            if not screen.is_playing:
                return 
            
            # Kalau aman, letuskan!
            self.pop()
            screen.increase_score()

    def pop(self):
        self.is_popped = True
        self.image_source = self.img_popped
        
        try:
            sound = SoundLoader.load('pop.wav')
            if sound:
                sound.pitch = random.uniform(0.9, 1.3)
                sound.volume = 0.8
                sound.play()
        except:
            pass 

        anim = Animation(size=(self.width*1.2, self.height*1.2), opacity=0, duration=0.2)
        anim.bind(on_complete=self.remove_self)
        anim.start(self)

    def remove_self(self, *args):
        if self.parent:
            self.parent.remove_widget(self)

class BubbleGameScreen(Screen):
    current_score = NumericProperty(0)
    high_score = NumericProperty(0)
    is_playing = BooleanProperty(False)
    is_game_over = BooleanProperty(False)
    
    spawn_event = None
    game_loop_event = None

    def on_enter(self):
        if user_store.exists('highscore'):
            self.high_score = user_store.get('highscore')['score']
        else:
            self.high_score = 0
        self.is_game_over = False

    def on_leave(self):
        self.stop_game()

    def toggle_game(self):
        if self.is_playing:
            self.stop_game()
        else:
            self.start_game()

    def start_game(self):
        self.is_playing = True
        self.is_game_over = False
        self.current_score = 0
        
        self.clear_bubbles()
        
        # Spawn bubble setiap 0.8 detik
        self.spawn_event = Clock.schedule_interval(self.spawn_bubble, 0.8)
        self.game_loop_event = Clock.schedule_interval(self.update_bubbles, 1.0/60.0)

    def stop_game(self):
        self.is_playing = False
        if self.spawn_event: self.spawn_event.cancel()
        if self.game_loop_event: self.game_loop_event.cancel()
        self.clear_bubbles()

    def trigger_game_over(self):
        self.is_playing = False
        self.is_game_over = True
        
        if self.spawn_event: self.spawn_event.cancel()
        if self.game_loop_event: self.game_loop_event.cancel()
        
        print("GAME OVER!")

    def clear_bubbles(self):
        game_area = self.ids.game_area
        bubbles_to_remove = [child for child in game_area.children if isinstance(child, FallingBubble)]
        for bubble in bubbles_to_remove:
            game_area.remove_widget(bubble)

    def spawn_bubble(self, dt):
        bubble = FallingBubble()
        
        max_x = Window.width - bubble.width
        if max_x < 0: max_x = 0
        bubble.x = random.randint(0, int(max_x))
        bubble.y = Window.height
        
        score = self.current_score
        
        # LOGIKA KECEPATAN (Bertahap) dengan dp agar konsisten
        if score < 5:
            bubble.speed = dp(random.randint(2, 4))   # Lambat
        elif score < 15:
            bubble.speed = dp(random.randint(4, 6))   # Sedang
        elif score < 30:
            bubble.speed = dp(random.randint(6, 9))   # Cepat
        else:
            bubble.speed = dp(random.randint(8, 13))  # Ngebut
            new_size = dp(random.randint(50, 70))
            bubble.size = (new_size, new_size)
        
        self.ids.game_area.add_widget(bubble)

    def update_bubbles(self, dt):
        game_area = self.ids.game_area
        
        for child in game_area.children:
            if isinstance(child, FallingBubble) and not child.is_popped:
                child.y -= child.speed
                
                # Game over jika bubble lewat batas bawah
                if child.y < dp(-10):
                    self.trigger_game_over()
                    return 

    def increase_score(self):
        self.current_score += 1
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            user_store.put('highscore', score=self.high_score)