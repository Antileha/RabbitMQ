import time
import pandas as pd
import matplotlib.pyplot as plt
import os

# Путь к файлу логов
log_file = './logs/metric_log.csv'
output_file = './logs/error_distribution.png'

# Функция для построения гистограммы
def plot_histogram():
    # Чтение данных из CSV файла
    if os.path.exists(log_file):
        df = pd.read_csv(log_file)

        # Вычисляем абсолютные ошибки, если они есть
        if 'absolute_error' in df.columns:
            # Строим гистограмму
            plt.figure(figsize=(10, 6))
            plt.hist(df['absolute_error'], bins=30, edgecolor='black', alpha=0.7)
            plt.title('Распределение абсолютных ошибок')
            plt.xlabel('Абсолютная ошибка')
            plt.ylabel('Частота')

            # Сохраняем изображение
            plt.savefig(output_file)
            plt.close()
            print(f"График сохранён в {output_file}")
        else:
            print("Ошибка: нет данных об абсолютных ошибках.")
    else:
        print(f"Ошибка: файл {log_file} не найден.")

# Бесконечный цикл для обновления графика
while True:
    plot_histogram()
    # Обновляем график каждые 10 секунд
    time.sleep(10)
