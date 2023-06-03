
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
```
```bash
pkg install python
```
```bash
termux-setup-storage
```
```bash
cd ~/storage/shared/osu\!droid/
```bash
git clone https://github.com/unclem2/osu-droid-collections
```
```bash
cd osu-droid-collections
```
Получите osu!api ключ на сайте https://osu.ppy.sh/home/account/edit#new-oauth-application

```bash
nano api_key.txt
```
Создайте новое приложение. Укажите ссылку на репозиторий в поле URL. Вставьте osu!api ключ в файл и сохраните его.
Переместите коллекцию в репозиторий.
## Использование
```python
python menu.py
```

--- Доступные скрипты ---
1. Конвертация коллекции
2. Загрузчик карт по коллекции
3. Экспорт коллекций
4. Объединение json файлов
5. Очистка дубликатов карт

