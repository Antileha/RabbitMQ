import pika
import json
import csv
import os

# Путь к файлу логов
log_dir = './logs'
log_file = f'{log_dir}/metric_log.csv'

# Создаём директорию logs, если она не существует
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Если файл не существует, создаём его с заголовками
if not os.path.exists(log_file):
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'y_true', 'y_pred', 'absolute_error'])


# Словарь для хранения приходящих значений y_true и y_pred по ID
metrics = {}

# Функция для записи данных в CSV
def log_metric(message_id, y_true, y_pred, abs_error):
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([message_id, y_true, y_pred, abs_error])

try:
    # Создаём подключение по адресу rabbitmq:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очереди
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')

    # Создаём функцию callback для обработки данных из очереди
    def callback(ch, method, properties, body):
        message = json.loads(body)
        message_id = message['id']
        data = message['body']

        if method.routing_key == 'y_true':
            # Если пришло сообщение с y_true, сохраняем в словарь
            metrics[message_id] = {'y_true': data}
            print(f"Получено y_true с ID {message_id}: {data}")
        elif method.routing_key == 'y_pred':
            # Если пришло сообщение с y_pred, сохраняем в словарь
            if message_id in metrics:
                metrics[message_id]['y_pred'] = data
                print(f"Получено y_pred с ID {message_id}: {data}")

                # Если оба значения получены, рассчитываем абсолютную ошибку и записываем в лог
                if 'y_true' in metrics[message_id] and 'y_pred' in metrics[message_id]:
                    y_true = metrics[message_id]['y_true']
                    y_pred = metrics[message_id]['y_pred']
                    abs_error = abs(y_true - y_pred)

                    # Записываем метрику в CSV
                    log_metric(message_id, y_true, y_pred, abs_error)
                    print(f"Записана метрика для ID {message_id}: абсолютная ошибка = {abs_error}")

                    # Удаляем обработанный ID из словаря
                    del metrics[message_id]

    # Извлекаем сообщение из очереди y_true
    channel.basic_consume(
        queue='y_true',
        on_message_callback=callback,
        auto_ack=True
    )

    # Извлекаем сообщение из очереди y_pred
    channel.basic_consume(
        queue='y_pred',
        on_message_callback=callback,
        auto_ack=True
    )

    print('...Ожидание сообщений, для выхода нажмите CTRL+C')

    # Запускаем режим ожидания прихода сообщений
    channel.start_consuming()

except Exception as e:
    print(f'Не удалось подключиться к очереди: {e}')
