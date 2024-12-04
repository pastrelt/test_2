import os
import time
import pyautogui
import cv2
import numpy as np
import pygetwindow as gw

# Открываем приложение "Калькулятор" и ждем его загрузки
os.system('start calc')
time.sleep(2)

# Получаем окно калькулятора и его размеры
calc_window = gw.getWindowsWithTitle('Калькулятор')[0]
window_width, window_height = calc_window.width, calc_window.height
print(f"Размеры окна калькулятора: {window_width}x{window_height}")

# Количество отрезков по ширине и высоте
num_segments_width, num_segments_height = 18, 9

# Вычисляем размеры отрезков
segment_width, segment_height = window_width // num_segments_width, window_height // num_segments_height

# Словарь для сканов
scans = {}

# Сканируем каждый отрезок
for i in range(num_segments_height):
    for j in range(num_segments_width):
        x, y = calc_window.left + j * segment_width, calc_window.top + i * segment_height
        # Сканируем отрезок
        screenshot = pyautogui.screenshot(region=(x, y, segment_width, segment_height))
        scans[i * num_segments_width + j + 1] = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# Выводим координаты и сохраняем сканы
for index, (segment_image) in scans.items():
    cv2.imwrite(f'scan_segment_{index}.png', segment_image)

# Пример показа одного из сканов (опционально)
# cv2.imshow('Segment 1', scans[128])
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Задержка перед началом ввода
time.sleep(1)

# Функция для нажатия кнопки на калькуляторе
def click_button(image_name):
    button_location = pyautogui.locateOnScreen(image_name, confidence=0.9)
    if button_location:
        button_center = pyautogui.center(button_location)
        pyautogui.click(button_center)
        print(f"Нажата кнопка: {image_name} в координатах {button_center}.")
    else:
        print(f"Кнопка {image_name} не найдена.")

# Нажимаем кнопки для выполнения операции 12 + 7
buttons_to_click = [
    'scan_segment_128.png',  # Изображение кнопки "1"
    'scan_segment_131.png',  # Изображение кнопки "2"
    'scan_segment_137.png',  # Изображение кнопки "+"
    'scan_segment_92.png',   # Изображение кнопки "7"
    'scan_segment_155.png'   # Изображение кнопки "="
]

for button in buttons_to_click:
    click_button(button)

# Выводим информацию о текущем положении курсора
current_position = pyautogui.position()
print(f"Текущая позиция курсора: {current_position}")