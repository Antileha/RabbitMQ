# Документация проекта: Микросервисная архитектура для обработки данных модели машинного обучения

## Описание проекта

Проект реализует микросервисную архитектуру для обработки данных, связанных с моделью машинного обучения. Каждый сервис выполняет определённую задачу: генерация данных, предсказания модели, логирование метрик и визуализация. Взаимодействие между микросервисами осуществляется через брокер сообщений RabbitMQ.

---

## Архитектура проекта

Проект состоит из следующих компонентов:

1. **features**:
   - Генерирует данные: вектор признаков и истинные значения (y_true).
   - Отправляет данные в очереди RabbitMQ (`features` и `y_true`).

2. **model**:
   - Получает данные из очереди `features`.
   - Делает предсказание с использованием загруженной модели.
   - Отправляет предсказания в очередь `y_pred`.

3. **metric**:
   - Читает данные из очередей `y_true` и `y_pred`.
   - Вычисляет абсолютные ошибки между истинными значениями и предсказаниями.
   - Записывает данные (id, y_true, y_pred, absolute_error) в файл `logs/metric_log.csv`.

4. **plot**:
   - Периодически читает файл `logs/metric_log.csv`.
   - Строит гистограмму распределения абсолютных ошибок.
   - Сохраняет график в файл `logs/error_distribution.png`.

5. **rabbitmq**:
   - Брокер сообщений для обеспечения взаимодействия между микросервисами.

---

## Системные требования

Для запуска проекта необходимы следующие инструменты:
- **Docker**: Версия 20.10 и выше.
- **Docker Compose**: Версия 1.29 и выше.

---

## Установка и запуск

### 1. Клонирование репозитория

Склонируйте репозиторий проекта:

 bash
git clone <URL_вашего_репозитория>
cd <название_папки_с_проектом>
2. Создание директории для логов
Создайте локальную директорию logs, если она ещё не существует:

bash
Копировать код
mkdir -p logs
3. Сборка и запуск контейнеров
Запустите проект через Docker Compose:

bash
Копировать код
docker-compose up --build
Для запуска в фоновом режиме:

bash
Копировать код
docker-compose up --build -d
Структура проекта
plaintext
Копировать код
.
├── docker-compose.yml         # Конфигурация Docker Compose
├── logs/                      # Директория для логов и графиков
│   ├── metric_log.csv         # CSV файл с метриками
│   ├── error_distribution.png # График распределения ошибок
├── features/
│   ├── Dockerfile             # Dockerfile для сервиса features
│   ├── src/
│       └── features.py        # Код сервиса features
├── model/
│   ├── Dockerfile             # Dockerfile для сервиса model
│   ├── src/
│       └── model.py           # Код сервиса model
├── metric/
│   ├── Dockerfile             # Dockerfile для сервиса metric
│   ├── src/
│       └── metric.py          # Код сервиса metric
├── plot/
│   ├── Dockerfile             # Dockerfile для сервиса plot
│   ├── src/
│       └── plot.py            # Код сервиса plot
└── README.md                  # Основная документация проекта

## Логика микросервисов

1. features
Генерирует случайный вектор признаков и истинное значение из встроенного датасета load_diabetes.
Отправляет данные в очереди RabbitMQ:
Очередь features: для признаков.
Очередь y_true: для истинных значений.

2. model
Получает данные из очереди features.
Делает предсказание, используя предобученную модель (файл myfile.pkl).
Отправляет предсказания в очередь y_pred.

3. metric
Подписывается на очереди y_true и y_pred.
Сохраняет входящие данные в файл logs/metric_log.csv.
Вычисляет абсолютную ошибку:
absolute_error=∣y_true−y_pred∣

4. plot
Считывает файл logs/metric_log.csv каждые 10 секунд.
Строит гистограмму распределения абсолютных ошибок.
Сохраняет график в файл logs/error_distribution.png.
Пример данных
Пример содержимого metric_log.csv:
csv
id,y_true,y_pred,absolute_error
1669147134.196809,295.0,221.77392889122234,73.22607110877766
1669147136.824343,153.0,118.44344405446542,34.55655594553458
1669147141.035324,189.0,204.06083656673704,15.060836566737038
1669147148.42061,173.0,200.44085356158348,27.44085356158348
1669147162.280003,154.0,159.34185386962795,5.341853869627954

Пример гистограммы (error_distribution.png):

Гистограмма абсолютных ошибок обновляется каждые 10 секунд:


Проблемы и их решения
Проблема: FileNotFoundError для файла metric_log.csv
Решение:
Убедитесь, что директория logs/ создана в корневой директории проекта.
Проверьте, что volume настроен в docker-compose.yml.

Проблема: Не удаётся подключиться к RabbitMQ
Решение:

Убедитесь, что сервис rabbitmq запущен.
Проверьте подключение к RabbitMQ из контейнеров.
Дополнительные команды
Остановка всех контейнеров:

bash
docker-compose down
Перезапуск всех контейнеров:

bash
docker-compose up --build
Просмотр логов конкретного контейнера:

bash
docker logs <имя_контейнера>