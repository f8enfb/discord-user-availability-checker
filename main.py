import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import random
import string
import requests
import time
from datetime import datetime

class DiscordUsernameChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Username Checker v1.0")
        self.root.geometry("900x750")
        self.root.resizable(False, False)
        
        # Переменные
        self.is_running = False
        self.username_count = 0
        self.available_count = 0
        self.taken_count = 0
        
        # Символы для генерации
        self.char_sets = {
            "Все": string.ascii_letters + string.digits + "!@#$%^&*_-+=[]{}|;:,.<>?",
            "Буквы + Цифры": string.ascii_letters + string.digits,
            "Только буквы": string.ascii_letters,
            "Только цифры": string.digits,
            "Буквы + спецсимволы": string.ascii_letters + "!@#$%^&*_-+=[]{}|;:,.<>?",
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        # Заголовок
        title_frame = tk.Frame(self.root, bg="#2C2F33")
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="🔍 Discord Username Checker",
            font=("Arial", 16, "bold"),
            bg="#2C2F33",
            fg="#7289DA"
        )
        title_label.pack()
        
        # Панель управления
        control_frame = tk.LabelFrame(self.root, text="Настройки", padx=10, pady=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Тип символов
        tk.Label(control_frame, text="Тип символов:").grid(row=0, column=0, sticky="w")
        self.char_var = tk.StringVar(value="Все")
        char_combo = ttk.Combobox(
            control_frame, 
            textvariable=self.char_var, 
            values=list(self.char_sets.keys()),
            state="readonly",
            width=25
        )
        char_combo.grid(row=0, column=1, sticky="w", padx=5)
        
        # Быстрое переключение длины
        tk.Label(control_frame, text="Длина username:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky="w", pady=10
        )
        
        length_frame = tk.Frame(control_frame)
        length_frame.grid(row=1, column=1, sticky="w", padx=5, pady=10)
        
        self.length_var = tk.IntVar(value=2)
        
        # Радиобаттоны для быстрого выбора
        tk.Radiobutton(
            length_frame,
            text="2 символа",
            variable=self.length_var,
            value=2,
            font=("Arial", 10),
            command=self.update_length_mode
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(
            length_frame,
            text="3 символа",
            variable=self.length_var,
            value=3,
            font=("Arial", 10),
            command=self.update_length_mode
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(
            length_frame,
            text="4 символа",
            variable=self.length_var,
            value=4,
            font=("Arial", 10),
            command=self.update_length_mode
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(
            length_frame,
            text="Произвольная",
            variable=self.length_var,
            value=0,
            font=("Arial", 10),
            command=self.update_length_mode
        ).pack(side=tk.LEFT, padx=10)
        
        # Произвольная длина (скрытая по умолчанию)
        custom_length_frame = tk.Frame(control_frame)
        custom_length_frame.grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        tk.Label(custom_length_frame, text="Мин. длина:").pack(side=tk.LEFT, padx=5)
        self.min_len_var = tk.StringVar(value="2")
        min_len_spin = ttk.Spinbox(
            custom_length_frame,
            from_=1,
            to=10,
            textvariable=self.min_len_var,
            width=5
        )
        min_len_spin.pack(side=tk.LEFT, padx=5)
        
        tk.Label(custom_length_frame, text="Макс. длина:").pack(side=tk.LEFT, padx=20)
        self.max_len_var = tk.StringVar(value="4")
        max_len_spin = ttk.Spinbox(
            custom_length_frame,
            from_=1,
            to=10,
            textvariable=self.max_len_var,
            width=5
        )
        max_len_spin.pack(side=tk.LEFT, padx=5)
        
        self.custom_length_frame = custom_length_frame
        self.custom_length_frame.pack_forget()  # Скрыть по умолчанию
        
        # Кнопки управления
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_btn = tk.Button(
            button_frame,
            text="▶ Запустить",
            command=self.start_checking,
            bg="#43B581",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹ Остановить",
            command=self.stop_checking,
            bg="#F04747",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑 Очистить",
            command=self.clear_log,
            bg="#7289DA",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Статистика
        stats_frame = tk.LabelFrame(self.root, text="Статистика", padx=10, pady=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Проверено: 0 | Свободных: 0 | Занято: 0",
            font=("Arial", 11, "bold"),
            fg="#43B581"
        )
        self.stats_label.pack()
        
        # Лог
        log_frame = tk.LabelFrame(self.root, text="Лог результатов", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            width=100,
            bg="#23272A",
            fg="#7289DA",
            font=("Courier", 9),
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Конфигурация тегов для цветов
        self.log_text.tag_config("available", foreground="#43B581")
        self.log_text.tag_config("taken", foreground="#F04747")
        self.log_text.tag_config("error", foreground="#FAA61A")
        self.log_text.tag_config("info", foreground="#7289DA")
    
    def update_length_mode(self):
        """Обновить режим длины"""
        if self.length_var.get() == 0:
            # Произвольная длина
            self.custom_length_frame.pack(fill=tk.X, padx=5, pady=5)
        else:
            # Фиксированная длина
            self.custom_length_frame.pack_forget()
    
    def log_message(self, message, tag="info"):
        """Добавить сообщение в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        self.log_text.see(tk.END)
        self.root.update()
    
    def update_stats(self):
        """Обновить статистику"""
        self.stats_label.config(
            text=f"Проверено: {self.username_count} | "
                 f"Свободных: {self.available_count} | "
                 f"Занято: {self.taken_count}"
        )
    
    def generate_username(self):
        """Генерировать случайный username"""
        char_set = self.char_sets[self.char_var.get()]
        
        if self.length_var.get() == 0:
            # Произвольная длина
            min_len = int(self.min_len_var.get())
            max_len = int(self.max_len_var.get())
        else:
            # Фиксированная длина
            min_len = max_len = self.length_var.get()
        
        length = random.randint(min_len, max_len)
        username = ''.join(random.choice(char_set) for _ in range(length))
        return username
    
    def check_username_availability(self, username):
        """Проверить доступность username"""
        try:
            # Попытка найти пользователя через Discord API (поиск)
            # Note: это косвенный метод проверки
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            
            # Метод 1: Проверка через Discord поиск
            url = f"https://discord.com/api/v10/users/search?query={username}"
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("users") and len(data["users"]) > 0:
                    for user in data["users"]:
                        if user.get("username", "").lower() == username.lower():
                            return False  # Занято
                return True  # Свободно
            
            # Если API не работает, пытаемся через другой метод
            time.sleep(0.1)  # Задержка для избежания rate limit
            return None  # Неизвестно
            
        except Exception as e:
            self.log_message(f"Ошибка при проверке '{username}': {str(e)}", "error")
            return None
    
    def checking_thread(self):
        """Поток для проверки username"""
        self.log_message("✅ Проверка запущена!", "info")
        
        if self.length_var.get() == 0:
            self.log_message(f"Параметры: {self.char_var.get()} | "
                            f"Длина: {self.min_len_var.get()}-{self.max_len_var.get()} (произвольная)", "info")
        else:
            self.log_message(f"Параметры: {self.char_var.get()} | "
                            f"Длина: {self.length_var.get()} символов", "info")
        
        self.log_message("-" * 80, "info")
        
        while self.is_running:
            try:
                username = self.generate_username()
                result = self.check_username_availability(username)
                
                self.username_count += 1
                
                if result is True:
                    self.available_count += 1
                    self.log_message(f"✅ СВОБОДЕН: {username}", "available")
                elif result is False:
                    self.taken_count += 1
                    self.log_message(f"❌ ЗАНЯТ: {username}", "taken")
                else:
                    self.log_message(f"⚠️  НЕИЗВЕСТНО: {username}", "error")
                
                self.update_stats()
                time.sleep(0.5)  # Задержка между запросами
                
            except Exception as e:
                self.log_message(f"Критическая ошибка: {str(e)}", "error")
                time.sleep(1)
    
    def start_checking(self):
        """Запустить проверку"""
        if self.is_running:
            messagebox.showwarning("Предупреждение", "Проверка уже запущена!")
            return
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Запустить поток
        thread = threading.Thread(target=self.checking_thread, daemon=True)
        thread.start()
    
    def stop_checking(self):
        """Остановить проверку"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log_message("⏹ Проверка остановлена!", "info")
        self.log_message("-" * 80, "info")
    
    def clear_log(self):
        """Очистить лог"""
        self.log_text.delete(1.0, tk.END)
        self.username_count = 0
        self.available_count = 0
        self.taken_count = 0
        self.update_stats()

if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordUsernameChecker(root)
    root.mainloop()
