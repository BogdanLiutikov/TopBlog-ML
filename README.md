# Кейс по сбору аналитических данных блога

Проект «ТопБЛОГ» – это конкурс и образовательная программа для блогеров и SMM-специалистов. В рамках конкурсной части
проекта заданием для участников является выполнение поставленных KPI за определенный период. Важность решения кейса –
автоматизация человеческого труда, что дает повышение уровня эффективности и креативности, а также облегчение труда
сотрудников.

Участникам хакатона предстоит создать программный модуль фотоаналитики по распознаванию необходимых показателей и
корректное их распределение в заданную форму (таблицу).

## Команда: 52 SQUAD

**Проблематика:**

- Монотонная работа
- Смещение фокуса с обучения
- Отсутствие процессов
- Человеческий фактор

**Мы предлагаем:**

- Автоматизация распознавания метрик
- Автоматическое заполнение excel-таблиц
- MVP

**Краткое описание**: Приложение позволяет автоматически сохранять необходимые метрики (подписчики, просмотры и т.д.) из
скриншота студента в excel-таблицу для отслеживания прогресса блога. Модель искусственного интеллекта избавляет куратора
от монотонной работы, что позволяет ему больше времени уделять студентам.

Модель ищет весь текст со скриншота, далее по ключевым словам находит расположение метрики и в конце ищет
соответствующее значение метрик вблизи с ключевым словом.

Стэк: Python, EasyOCR, FastAPI

Для локального запуска с сервером необходимо клонировать проект, а также запустить следующие команды (необходимо наличие зависимостей из requirements.txt
):

```
    git clone https://github.com/BogdanLiutikov/TopBlog-ML
    uvicorn server:app --host 127.0.0.1 --port 8080
```

Для проверки с локальным файлом можно просто запустить `ml.py` указав в нем путь до нужного файла и площадку скриншота(tg,vk,yt,zn).