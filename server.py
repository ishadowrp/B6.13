from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album
"""
Веб-сервис вывода списка альбомов
"""
@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Список альбомов {}:<br>".format(artist)
        result += "<br>".join(album_names)
    return result

"""
Веб-сервис добавления новой строки в БД
"""
@route("/albums", method="POST")
def add_new_data():
    new_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    """
    Валидация года на предмет правильного типа данных
    """
    try: 
        new_data["year"] = int(new_data["year"])
        if new_data["year"] >= 1000 and new_data["year"]<=2020:
            """
            Проверка на предмет дублирования данных в БД
            """
            if album.check_album(new_data):
                result = album.add(new_data)
            else:    
                message = "Запись с таким альбомом уже существует!"
                result = HTTPError(409, message)
        else:
            message = "Неверный тип данных в запросе: проверьте значение поля 'year'"
            result = HTTPError(400, message)
    except ValueError:
        message = "Неверный тип данных в запросе: проверьте значение поля 'year'"
        result = HTTPError(400, message)

    return result

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)