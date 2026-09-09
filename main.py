import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import random
import string
import discord
from discord.ext import commands
import asyncio
import time
from datetime import datetime

class DiscordUsernameChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Username Checker v2.0 - Bot Edition")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)
        
        # Переменные
        self.is_running = False
        self.username_count = 0
        self.available_count = 0
        self.taken_count = 0
        self.bot_token = ""
        self.bot = None
        self.guild_id = None
        
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
            text="🔍 Discord Username Checker v2.0 - Bot Edition",
            font=("Arial", 16, "bold"),
            bg="#2C2F33",
            fg="#7289DA"
        )
        title_label.pack()
        
        # Панель авторизации бота
        auth_frame = tk.LabelFrame(self.root, text="🤖 Авторизация Discord Bot", padx=10, pady=10, fg="#7289DA")
        auth_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(auth_frame, text="Discord Bot Token:").grid(row=0, column=0, sticky="w")
        self.token_entry = tk.Entry(auth_frame, width=50, show="*")
        self.token_entry.grid(row=0, column=1, sticky="ew", padx=5)
        
        tk.Label(auth_frame, text="ID Сервера (Guild ID):").grid(row=1, column=0, sticky="w", pady=5)
        self.guild_entry = tk.Entry(auth_frame, width=50)
        self.guild_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        self.connect_btn = tk.Button(
            auth_frame,
            text="🔗 Подключить Бота",
            command=self.connect_bot,
            bg="#43B581",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        )
        self.connect_btn.grid(row=0, column=2, rowspan=2, padx=10)
        
        self.status_label = tk.Label(auth_frame, text="❌ Бот не подключен", fg="#F04747", font=("Arial", 10, "bold"))
        self.status_label.grid(row=2, column=0, columnspan=3, pady=5)
        
        auth_frame.columnconfigure(1, weight=1)
        
        # Панель управления
        control_frame = tk.LabelFrame(self.root, text="⚙️ Настройки", padx=10, pady=10)
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
            pady=8,
            state=tk.DISABLED
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
        stats_frame = tk.LabelFrame(self.root, text="📊 Статистика", padx=10, pady=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Проверено: 0 | Свободных: 0 | Занято: 0",
            font=("Arial", 11, "bold"),
            fg="#43B581"
        )
        self.stats_label.pack()
        
        # Лог
        log_frame = tk.LabelFrame(self.root, text="📝 Лог результатов", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            width=120,
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
        self.log_text.tag_config("success", foreground="#43B581")
    
    def connect_bot(self):
        """Подключить Discord бота"""
        token = self.token_entry.get().strip()
        guild_id_str = self.guild_entry.get().strip()
        
        if not token:
            messagebox.showerror("Ошибка", "Введите Discord Bot Token!")
            return
        
        if not guild_id_str.isdigit():
            messagebox.showerror("Ошибка", "Guild ID должен быть числом!")
            return
        
        self.bot_token = token
        self.guild_id = int(guild_id_str)
        
        # Запустить подключение в отдельном потоке
        thread = threading.Thread(target=self.bot_connect_thread, daemon=True)
        thread.start()
    
    def bot_connect_thread(self):
        """Поток для подключения бота"""
        try:
            self.log_message("🔄 Подключение к Discord...", "info")
            
            # Создаем бота
            intents = discord.Intents.default()
            self.bot = commands.Bot(command_prefix="!", intents=intents)
            
            @self.bot.event
            async def on_ready():
                self.log_message(f"✅ Бот подключен как {self.bot.user}", "success")
                self.status_label.config(text=f"✅ Бот подключен: {self.bot.user}", fg="#43B581")
                self.start_btn.config(state=tk.NORMAL)
                self.connect_btn.config(state=tk.DISABLED)
            
            # Запуск бота в цикле
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.bot.start(self.bot_token))
            
        except discord.errors.LoginFailure:
            self.log_message("❌ Ошибка: Неверный Discord Bot Token!", "error")
            self.status_label.config(text="❌ Ошибка авторизации", fg="#F04747")
        except Exception as e:
            self.log_message(f"❌ Ошибка подключения: {str(e)}", "error")
            self.status_label.config(text="❌ Ошибка подключения", fg="#F04747")
    
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
    
    async def check_username_with_bot(self, username):
        """Проверить доступность username через Discord Bot API"""
        try:
            if not self.bot or not self.bot.user:
                return None
            
            # Пытаемся найти пользователя по username
            # Если найдем - значит занято, если нет - свободно
            try:
                user = await self.bot.fetch_user(username)
                return False  # Занято
            except discord.NotFound:
                return True  # Свободно
            except Exception as e:
                self.log_message(f"Ошибка при проверке '{username}': {str(e)}", "error")
                return None
                
        except Exception as e:
            self.log_message(f"Критическая ошибка: {str(e)}", "error")
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
        
        self.log_message("-" * 100, "info")
        
        while self.is_running:
            try:
                username = self.generate_username()
                
                # Запускаем async функцию
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(self.check_username_with_bot(username))
                loop.close()
                
                self.username_count += 1
                
                if result is True:
                    self.available_count += 1
                    self.log_message(f"✅ СВОБОДЕН: {username}", "available")
                elif result is False:
                    self.taken_count += 1
                    self.log_message(f"❌ ЗАНЯТ: {username}", "taken")
                else:
                    self.log_message(f"⚠️  ОШИБКА: {username}", "error")
                
                self.update_stats()
                time.sleep(1)  # Задержка между запросами
                
            except Exception as e:
                self.log_message(f"Критическая ошибка: {str(e)}", "error")
                time.sleep(2)
    
    def start_checking(self):
        """Запустить проверку"""
        if self.is_running:
            messagebox.showwarning("Предупреждение", "Проверка уже запущена!")
            return
        
        if not self.bot or not self.bot.user:
            messagebox.showerror("Ошибка", "Сначала подключите Discord бота!")
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
        self.log_message("-" * 100, "info")
    
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
