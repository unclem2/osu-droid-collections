
# osu-droid-collections

Конвертирует collections.db в favorite.json при помощи osu!api.



## Особенности

- Конвертация коллекций osu!stable в osu!droid
- Загрузчик карт по данным коллекции
- Полная(почти) совместимость с особенностями директории osu!droid
- Кроссплатформенность(Termux, PC)


# Установка и настройка
- Скачайте [Termux](https://github.com/termux/termux-app/releases/download/v0.118.0/termux-app_v0.118.0+github-debug_universal.apk) (обязательно с GitHub) 
```bash
pkg update
pkg upgrade
```
```bash
pkg install git
```
```bash
git clone https://github.com/unclem2/osu-droid-collections
```
```bash
cd osu-droid-collections
```
```bash
bash setup.sh
```
```bash
cp ~/osu-droid-collections -r ~/storage/shared/osu\!droid/ 
cd ..
cd ~/storage/shared/osu\!droid/osu-droid-collections
```
Получите osu!api ключ на сайте https://osu.ppy.sh/home/account/edit#new-oauth-application

```bash
nano api_key.txt
```
Создайте новое приложение. Укажите ссылку на репозиторий в поле URL. Вставьте osu!api ключ в файл и сохраните его.
Переместите коллекцию в репозиторий.
```python
python menu.py
```
## Использование
1. Обработка коллекций. Скрипт берет хэши карт из collections.db, обращается к osu!api и создает два файла: один с {beatmapsetid}, другой {beatmapsetid} {artist} {name}. Нужно запускать для корректной работы остальных скриптов
2. Загрузчик. Загружает карты по {beatmapsetid} через chimu api
3. Экспорт коллекций. Нужен для работы следующего скрипта, но также имеет и иное применение.
4. Слияние json файлов. Скрипт создает новую коллекцию с данными из экспортированной коллекцией и уже существующей в папке osu!droid/json/



