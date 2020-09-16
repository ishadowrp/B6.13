import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def check_album(params):
    """
    Ищет в БД альбом с идентичными параметрами и возвращает количество совпадений. Если количество не равно нулю, то функция вернет ложь
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.year == params["year"], Album.artist == params["artist"], Album.genre == params["genre"], Album.album == params["album"]).count()
    if albums == 0:
        return True
    else:
        return False    

def add(params):
    """
    Добавляет в БД нового исполнителя, название альбома и т.п.
    """

    session = connect_db()

    new_data = Album(year=params["year"], artist=params["artist"], genre=params["genre"], album=params["album"])
    session.add(new_data)
    session.commit()
    result = "Новые данные добавлены."

    return result