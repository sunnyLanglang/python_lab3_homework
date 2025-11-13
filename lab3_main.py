import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

def close():
    window.destroy()

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
    
    # 更新显示
    # Обновление отображения
    lbl_key.configure(text=key)
    lbl_status.configure(text=f"Ключ сгенерирован! Интервал: {start_letter}-{end_letter}")

def copy_key():
    key = lbl_key.cget("text")
    if key != "Ожидание генерации ключа":
        window.clipboard_clear()
        window.clipboard_append(key)
        lbl_status.configure(text="Ключ скопирован в буфер обмена!")
        window.after(2000, lambda: lbl_status.configure(text="Готов - можно " \
                     "генерировать новый ключ"))
    else:
        messagebox.showwarning("Ошибка копирования", "Пожалуйста, сначала " \
                               "сгенерируйте действительный ключ")

# 创建主窗口
# Создание главного окна
window = tk.Tk()
window.title("Генератор ключей")
window.geometry("600x500")
window.resizable(False, False)

# 加载背景图片
# Загрузка фонового изображения
bg_image = ImageTk.PhotoImage(Image.open('preview.jpg').resize((600, 500), Image.Resampling.LANCZOS))
tk.Label(window, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

# 创建主框架
# Создание главного фрейма
frame = tk.Frame(window, bg='#34495e', bd=2, relief='ridge')
frame.place(relx=0.5, rely=0.5, anchor='center', width=420, height=350)

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

# 按钮
# Кнопки
button_frame = tk.Frame(frame, bg="#34495e")
button_frame.grid(column=0, row=2, columnspan=3, pady=15)

tk.Button(button_frame, text="Сгенерировать", font=("Arial", 12), bg="#3498db", 
          fg="white", width=12, command=generate).pack(side="left", padx=10)
tk.Button(button_frame, text="Копировать", font=("Arial", 12), bg="#2ecc71", 
          fg="white", width=12, command=copy_key).pack(side="left", padx=10)
tk.Button(button_frame, text="Выход", font=("Arial", 12), bg="#e74c3c", 
          fg="white", width=12, command=close).pack(side="left", padx=10)

# 状态和规则
# Статус и правило
lbl_status = tk.Label(frame, text="Нажмите кнопку генерации для начала", font=("Arial", 10), 
                      fg="#bdc3c7", bg="#34495e")
lbl_status.grid(column=0, row=3, columnspan=3, pady=10)

rules_text = "Формат: XX XXXXXXX XX\n1-й и 3-й блоки - номера букв\n2-й блок - " \
             "случайные буквы из интервала\nПример: A(01)иJ(10) → 01 DEBBHCI 10"
tk.Label(frame, text=rules_text, font=("Arial", 9), fg="#95a5a6", bg="#34495e", 
         justify="left").grid(column=0, row=4, columnspan=3, pady=10)

window.mainloop()