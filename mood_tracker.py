from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse
from kivy.metrics import dp, sp
import calendar
from datetime import datetime
from collections import Counter
from user_store import user_store 
from kivy.metrics import dp,sp

# Load file desain
Builder.load_file('screen/mood_tracker.kv')

# --- 1. CLASS KALENDER (MOOD TRACKER) ---
class MoodTrackerScreen(Screen):
    current_month = NumericProperty(datetime.now().month)
    current_year = NumericProperty(datetime.now().year)
    dominant_mood_text = StringProperty("Belum ada data")
    
    # Palet Warna
    mood_colors = {
        'Anger': [1, 0.4, 0.4, 1], 'Anxiety': [1, 0.85, 0.2, 1],
        'Joy': [1, 0.96, 0.6, 1], 'Sadness': [0.5, 0.8, 1, 1],
        'Envy': [0.5, 0.8, 0.7, 1], 'Fear': [0.8, 0.6, 0.8, 1],
        'Disgust': [0.6, 0.8, 0.6, 1], 'Embarrassment': [0.9, 0.6, 0.7, 1],
        'Ennui': [0.6, 0.6, 0.8, 1], 'Unknown': [0.9, 0.9, 0.9, 1]
    }

    def on_pre_enter(self):
        self.update_calendar()

    def update_calendar(self):
        # Update Judul Bulan
        month_name = calendar.month_name[self.current_month]
        self.ids.month_label.text = f"{month_name} {self.current_year}"
        
        # Ambil Data
        self.monthly_data = {}
        mood_counts = []
        str_month = f"{self.current_month:02d}"
        str_year = str(self.current_year)
        
        for key in user_store.keys():
            if key.startswith('curhat_'):
                data = user_store.get(key)
                date_str = data.get('date', '')
                try:
                    parts = date_str.split('/')
                    if len(parts) == 3 and parts[1] == str_month and parts[2] == str_year:
                        day_int = int(parts[0])
                        mood = data.get('feeling', 'Unknown')
                        self.monthly_data[day_int] = mood
                        mood_counts.append(mood)
                except: pass

        # Update Dominant Text
        if mood_counts:
            most_common = Counter(mood_counts).most_common(1)[0]
            self.dominant_mood_text = f"Dominant: {most_common[0]} ({most_common[1]} hari)"
        else:
            self.dominant_mood_text = "Data kosong bulan ini"

        # Gambar Grid
        grid = self.ids.calendar_grid
        grid.clear_widgets()
        
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for d in days:
            grid.add_widget(Label(text=d, color=(0.5,0.5,0.5,1), bold=True))
            
        first_day_weekday, num_days = calendar.monthrange(self.current_year, self.current_month)
        start_gap = (first_day_weekday + 1) % 7
        
        for _ in range(start_gap):
            grid.add_widget(Label(text=""))
            
        for day in range(1, num_days + 1):
            mood = self.monthly_data.get(day)
            bg = self.mood_colors.get(mood, [1, 1, 1, 0]) if mood else [1, 1, 1, 0]
            grid.add_widget(CalendarDay(text=str(day), bg_color=bg))

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar()
        
    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()
        
    def go_back(self):
        self.manager.current = 'menu'

    def go_to_stats(self):
        # Pindah ke layar Chart
        if self.manager.has_screen('mood_stats'):
            stats_screen = self.manager.get_screen('mood_stats')
            stats_screen.target_month = self.current_month
            stats_screen.target_year = self.current_year
            stats_screen.load_chart()
            self.manager.current = 'mood_stats'

# --- 2. CLASS CHART LINGKARAN (DONUT) ---
class DonutChart(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {}
        self.colors = {}
        self.bind(pos=self.draw_chart, size=self.draw_chart)

    def set_data(self, data, color_map):
        self.data = data
        self.colors = color_map
        self.draw_chart()

    def draw_chart(self, *args):
        self.canvas.clear()
        if not self.data: return

        total = sum(self.data.values())
        if total == 0: return

        center_x, center_y = self.center_x, self.center_y
        # Radius menyesuaikan ukuran layar (agar tidak kepotong)
        radius = (min(self.width, self.height) / 2) - dp(10)
        thickness = dp(35) # Ketebalan donat
        angle_start = 0
        
        with self.canvas:
            for mood, count in self.data.items():
                if count == 0: continue
                portion = (count / total) * 360
                angle_end = angle_start + portion
                
                col = self.colors.get(mood, [0.5, 0.5, 0.5, 1])
                Color(*col)
                Line(circle=(center_x, center_y, radius, angle_start, angle_end), width=thickness, cap='none')
                angle_start = angle_end

# --- 3. CLASS SCREEN STATISTIK ---
class MoodStatScreen(Screen):
    target_month = NumericProperty(0)
    target_year = NumericProperty(0)
    mood_colors = MoodTrackerScreen.mood_colors 

    def load_chart(self):
        try: month_name = calendar.month_name[self.target_month]
        except: month_name = ""
        if self.ids.title_lbl:
            self.ids.title_lbl.text = f"Statistik {month_name} {self.target_year}"
        
        # Ambil Data
        mood_counts = Counter()
        str_month = f"{self.target_month:02d}"
        str_year = str(self.target_year)
        
        for key in user_store.keys():
            if key.startswith('curhat_'):
                data = user_store.get(key)
                date_str = data.get('date', '')
                try:
                    parts = date_str.split('/')
                    if len(parts) == 3 and parts[1] == str_month and parts[2] == str_year:
                        mood = data.get('feeling', 'Unknown')
                        mood_counts[mood] += 1
                except: pass
        
        # Bersihkan & Gambar Ulang
        self.ids.chart_area.clear_widgets()
        self.ids.legend_container.clear_widgets()
        
        if not mood_counts:
            self.ids.chart_area.add_widget(Label(text="Belum ada data.", color=(0,0,0,0.5)))
            return

        # Masukkan Donut Chart
        donut = DonutChart()
        self.ids.chart_area.add_widget(donut)
        donut.set_data(mood_counts, self.mood_colors)
        
        # Masukkan Legend (Keterangan)
        for mood, count in mood_counts.most_common():
            color = self.mood_colors.get(mood, [0.5,0.5,0.5,1])
            self.ids.legend_container.add_widget(LegendItem(mood_name=mood, count_text=f"{count} hari", dot_color=color))

    def go_back(self):
        self.manager.current = 'mood_tracker'

# --- 4. WIDGET PENDUKUNG ---
class CalendarDay(Button):
    bg_color = ListProperty([0, 0, 0, 0])

class LegendItem(BoxLayout):
    mood_name = StringProperty("")
    count_text = StringProperty("")
    dot_color = ListProperty([0,0,0,1])