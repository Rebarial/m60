# m60
Бэкэнд для сайта м60

## Реализовано
 - админка http://127.0.0.1:8000/admin/
 - апи видео http://127.0.0.1:8000/api/viedo/{id}/
 - телеграм бот для оповещений о новых заказах


## Установка
Необходим docker и docker-copose

``` bash
git clone https://github.com/Rebarial/m60

cd m60

docker-compose up --build --force-recreate -d
```


## Структура
 - м60 – папка с настройками django проекта и celary 
 - main_page – папка с моделями и админкой для основной страницы
 - telegram_bot – папка с телеграм ботом, его функциями и моделью телеграм подписчик
   - managment
     - commands
       - runbot – модуль запуска телеграмм бота
