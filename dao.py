import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from auth import mysql_user, mysql_pass, mysql_host, mysql_port
from imgur_funcs import get_imglink, dog, cat

db = 'imgs_links'

engine = create_engine(f"mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/{db}", echo=True)

Base = declarative_base()

class Imgs_dog(Base):
    __tablename__ = 'imgs_dog'

    id = Column(Integer, primary_key=True)
    link = Column(String(32))

    def __repr__(self):
        return f'Img_dog(link = {self.link})'


class Imgs_cat(Base):
    __tablename__ = 'imgs_cat'

    id = Column(Integer, primary_key=True)
    link = Column(String(32))

    def __repr__(self):
        return f'Img_cat(link = {self.link})'

def reset_db():
    Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    for x in range(0, 5):
        dog_link = get_imglink(dog)
        cat_link = get_imglink(cat)

        dog_img = Imgs_dog(link=dog_link)
        cat_img = Imgs_cat(link=cat_link)

        session.add(dog_img)
        session.add(cat_img)

    session.commit()

def get_rand_dog():
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    query = session.query(Imgs_dog).all()
    rand_id = random.randrange(1, len(query) + 1)

    return session.get(Imgs_dog, rand_id).link

def get_rand_cat():
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    query = session.query(Imgs_cat).all()
    rand_id = random.randrange(1, len(query) + 1)

    return session.get(Imgs_dog, rand_id).link

def main():
    reset_db()

if(__name__ == "__main__"):
    main()