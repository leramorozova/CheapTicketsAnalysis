# Анализ данных по авиабилетам

## Сбор данных

*Данные*: авиабилеты небольших городов России с аэропортами.

*Список аэропортов*: получен из ресурса 
[unipage.net](https://www.unipage.net/ru/airports) путем парсинга HTML страниц.
Целевые аэропроты - размера S и M по классификации unipage.

*Авиабилеты*: для всех полученных аэропортов была собрана информация по 
авиабилетам за период с 2017 до 2022 года. Источник данных - [Avisales API](https://aviasales.docs.apiary.io/#).


### Зaпуск парсера

#### Настройка окружения

Для запуска вам необходимо добавить `AVIASALES_TOKEN` в переменные окружения. 
В переменной должен содержаться партнерский токен aviasales.
Получить его можно [тут](https://support.travelpayouts.com/hc/en-us/articles/203956083-Requirements-for-data-API-access).

#### Установка зависимостей

Спулльте репозиторий и установите зависимости из `requirements.txt`
```shell
git pull https://github.com/leramorozova/CheapTicketsAnalysis.git
cd CheapTicketsAnalysis
pip install -r requirements.txt
```

#### Скрипт парсинга

Скрипт параметризуем (узнать все параметры можно при помощи инструкции `help`),
но работает также и с дефолтными параметрами.
```shell
python3 parser/main.py --help
python3 parser/main.py --verbose
```

В результате выполнения скрипта будет получен датасет в формате csv.

## Анализ данных

## Алгоритм
После того, как датасет в формате csv был скачан, проверить, 
что путь до датасета совпадает с находящимся в переменной 'CURRENT_DATASET'
в модуле 'show_optimal_route.py'.

После этого перейдите в папку 'parser' и запустите скрипт следующим образом

```shell
python3 show_optimal_route.py -o <origin_city> -d <destination_city>
```

Результат работы скрипта - оптимальная цена и соответствующий ей маршрут
