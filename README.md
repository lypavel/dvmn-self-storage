# Сервис SelfStorage

Сезонные вещи, занимающие много места в квартире не всегда удобно хранить, во многих случаях места в квартире для них нет, также бывает, что вещи надоедают, но избавляться от них жалко - они накапливаются и занимают все пространство, мешая жить. Аренда небольшого склада решит эту проблему.

## Запуск

1. Скачайте код из репозитория и установите [Python 3.10.12](https://www.python.org/downloads/release/python-31012/)
2. Если нужно, создайте [виртуальное окружение](https://docs.python.org/3/library/venv.html).
3. Установите зависимости командой `pip install -r requirements.txt`
4. Создайте `.env` файл со следующим содержимым
    ```env
    ALLOWED_HOSTS= список разрешённых хостов
    DEBUG= дебаг режим
    SECRET_KEY= секретный ключ

    EMAIL_HOST_USER= адрес google почты, с которого будет производиться рассылка уведомлений
    EMAIL_HOST_PASSWORD= ключ доступа к google аккаунту
    HOST_URL= адрес сайта для формирования ссылок

    CELERY_WORKER_LOCATION= адрес, на котором работает `redis`
    GEO_API_KEY= токен Яндекс геокодера
    ```
5. Примените миграции с помощью `python3 manage.py migrate`
6. Запустите сервер командой `python3 manage.py runserver 0:8000`
7. Сайт будет доступен по адресу [0.0.0.0:8000](http://0.0.0.0:8000/), админка [0.0.0.0:8000/admin](http://0.0.0.0:8000/admin/)

## Цели проекта

Код написан в учебных целях — это командный проект в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
