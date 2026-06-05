from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform
from kivy.app import App
import os

class SmartUserStore:
    """
    Class 'Pintar' pengganti JsonStore biasa.
    Dia otomatis mendeteksi apakah sedang di Android atau Windows,
    dan memilih lokasi penyimpanan yang aman agar tidak crash.
    """
    _store = None

    def _get_actual_store(self):
        # Fungsi ini hanya dijalankan saat data benar-benar dibutuhkan
        if self._store is None:
            if platform == 'android':
                # --- LOGIKA KHUSUS ANDROID ---
                try:
                    # Ambil folder aman khusus aplikasi di Android
                    app = App.get_running_app()
                    data_dir = app.user_data_dir
                    storage_path = os.path.join(data_dir, 'user_data.json')
                    print(f"[UserStore] Android detected. Saving to: {storage_path}")
                except Exception as e:
                    # Fallback darurat jika terjadi error aneh (jarang terjadi)
                    print(f"[UserStore] Error getting android path: {e}")
                    storage_path = 'user_data.json'
            else:
                # --- LOGIKA WINDOWS/PC ---
                # Tetap simpan di folder project seperti biasa
                storage_path = 'user_data.json'
                print(f"[UserStore] PC detected. Saving to: {storage_path}")

            self._store = JsonStore(storage_path)
        
        return self._store

    def put(self, key, **kwargs):
        # Saat file lain memanggil user_store.put(...), kode ini yang jalan
        return self._get_actual_store().put(key, **kwargs)

    def get(self, key):
        # Saat file lain memanggil user_store.get(...), kode ini yang jalan
        return self._get_actual_store().get(key)

    def exists(self, key):
        return self._get_actual_store().exists(key)

    def delete(self, key):
        return self._get_actual_store().delete(key)

    def keys(self):
        return self._get_actual_store().keys()
    
    def count(self):
        return self._get_actual_store().count()

    def clear(self):
        return self._get_actual_store().clear()

# Inisialisasi variabel global
# File lain (main.py, screens) akan menganggap ini adalah JsonStore biasa
user_store = SmartUserStore()

print("user_store module loaded successfully (Android Ready)")