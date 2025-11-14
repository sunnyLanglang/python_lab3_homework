import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import pygame
import os

# 初始化pygame mixer
# Инициализация микшера pygame
pygame.mixer.init()

def close():
    # 停止音乐并退出
    # Остановить музыку и выйти
    pygame.mixer.music.stop()
    window.destroy()

def play_background_music():
    # 播放背景音乐
    # Воспроизвести фоновую музыку
    try:
        music_file = '03 - P.T. Adamczyk - The Rebel Path.mp3'
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # -1表示循环播放
            pygame.mixer.music.set_volume(0.5)  # 设置音量 (0.0 到 1.0)
        else:
            print(f"音乐文件未找到: {music_file}")
    except Exception as e:
        print(f"播放音乐时出错: {e}")

def toggle_music():
    #切换音乐播放/暂停
    # Переключить воспроизведение/паузу музыки
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        btn_music.config(text="Воспроизвести музыку", bg="#f39c12")
    else:
        pygame.mixer.music.unpause()
        btn_music.config(text="Приостановить музыку", bg="#3498db")

def animate_key_label():
    # 简单的缩放动画效果
    # Простая анимация масштабирования
    current_size = 14
    max_size = 18
    
    def scale_up(step=0):
        nonlocal current_size
        if step <= 5:
            new_size = current_size + (max_size - current_size) * (step / 5)
            lbl_key.config(font=("Consolas", int(new_size), "bold"))
            window.after(20, lambda: scale_up(step + 1))
        else:
            window.after(100, scale_down)
    
    def scale_down(step=0):
        nonlocal current_size
        if step <= 5:
            new_size = max_size - (max_size - current_size) * (step / 5)
            lbl_key.config(font=("Consolas", int(new_size), "bold"))
            window.after(20, lambda: scale_down(step + 1))
    
    scale_up()

def generate():
    # 生成两个不同的字母序号(1-26)
    # Генерация двух разных номеров букв (1-26)
    num1, num2 = random.randint(1, 26), random.randint(1, 26)
    while num2 == num1:
        num2 = random.randint(1, 26)
    
    # 确定字母区间
    # Определение интервала букв
    start_num, end_num = sorted([num1, num2])
    start_letter = chr(ord('A') + start_num - 1)
    end_letter = chr(ord('A') + end_num - 1)
    
    # 生成第二块的7个随机字母
    # Генерация 7 случайных букв для второго блока
    block2 = ''.join([chr(ord('A') + random.randint(start_num - 1, end_num - 1)) 
                      for _ in range(7)])
    
    # 格式化密钥
    # Форматирование ключа
    key = f"{start_num:02d} {block2} {end_num:02d}"
    
    # 更新显示并启动动画
    # Обновление отображения и запуск анимации
    lbl_key.configure(text=key)
    lbl_status.configure(text=f"Ключ сгенерирован! Интервал: {start_letter}-{end_letter}")
    
    # 启动动画效果
    # Запуск анимации
    animate_key_label()

def copy_key():
    key = lbl_key.cget("text")
    if key != "Ожидание генерации ключа":
        window.clipboard_clear()
        window.clipboard_append(key)
        lbl_status.configure(text="Ключ скопирован в буфер обмена!")
        window.after(2000, lambda: lbl_status.configure(text="Готов - можно " \
                     "генерировать новый ключ"))
        
        # 复制时也添加动画效果
        # Анимация при копировании тоже
        animate_key_label()
    else:
        messagebox.showwarning("Ошибка копирования", "Пожалуйста, сначала " \
                               "сгенерируйте действительный ключ")

# 创建主窗口
# Создание главного окна
window = tk.Tk()
window.title("Генератор ключей")
window.geometry("600x500")
window.resizable(False, False)

# 启动背景音乐
# Запустить фоновую музыку
play_background_music()

# 加载背景图片
# Загрузка фонового изображения
try:
    bg_image = ImageTk.PhotoImage(Image.open('preview.jpg').resize((600, 500), Image.Resampling.LANCZOS))
    tk.Label(window, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)
except:
    # 如果图片加载失败，使用纯色背景
    window.configure(bg='#2c3e50')

# 创建主框架
# Создание главного фрейма
frame = tk.Frame(window, bg='#34495e', bd=2, relief='ridge')
frame.place(relx=0.5, rely=0.5, anchor='center', width=390, height=380)

# 标题
# Заголовок
tk.Label(frame, text="Генератор ключей Cyberpunk2077", font=("Arial", 16, "bold"), fg="#f0f1ec", 
         bg="#34495e").grid(column=0, row=0, columnspan=3, pady=15)

# 密钥显示
# Отображение ключа
lbl_key = tk.Label(frame, text="Ожидание генерации ключа", font=("Consolas", 14, "bold"), 
                   width=25, justify="center", bg="#2c3e50", fg="#e74c3c", 
                   bd=2, relief="solid")
lbl_key.grid(column=0, row=1, columnspan=3, pady=20)

# 按钮框架
# Фрейм для кнопок
button_frame = tk.Frame(frame, bg="#34495e")
button_frame.grid(column=0, row=2, columnspan=3, pady=10)

# 主要功能按钮
# Основные функциональные кнопки
tk.Button(button_frame, text="Сгенерировать", font=("Arial", 12), bg="#3498db", 
          fg="white", width=12, command=generate).pack(side="left", padx=5)
tk.Button(button_frame, text="Копировать", font=("Arial", 12), bg="#2ecc71", 
          fg="white", width=12, command=copy_key).pack(side="left", padx=5)
tk.Button(button_frame, text="Выход", font=("Arial", 12), bg="#e74c3c", 
          fg="white", width=12, command=close).pack(side="left", padx=5)

# 音乐控制按钮
# Кнопка управления музыкой
btn_music = tk.Button(frame, text="Приостановить музыку", font=("Arial", 10), bg="#3498db", 
                     fg="white", width=17, command=toggle_music)
btn_music.grid(column=0, row=3, columnspan=3, pady=5)

# 状态和规则
# Статус и правило
lbl_status = tk.Label(frame, text="Нажмите кнопку генерации для начала", font=("Arial", 10), 
                      fg="#bdc3c7", bg="#34495e")
lbl_status.grid(column=0, row=4, columnspan=3, pady=10)

rules_text = "Формат: XX XXXXXXX XX\n1-й и 3-й блоки - номера букв\n2-й блок - " \
             "случайные буквы из интервала\nПример: A(01)иJ(10) → 01 DEBBHCI 10"
tk.Label(frame, text=rules_text, font=("Arial", 9), fg="#95a5a6", bg="#34495e", 
         justify="left").grid(column=0, row=5, columnspan=3, pady=10)

# 窗口关闭事件处理
# Обработка события закрытия окна
window.protocol("WM_DELETE_WINDOW", close)

window.mainloop()