from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from auth import mysql_user, mysql_pass, mysql_host, mysql_port
from imgur_funcs import get_imglink, dog, cat

engine = create_engine(f"mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/imgs_links", echo=True)

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

Base.metadata.create_all(engine)

def fill_db():
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    query = session.query(Imgs_dog).delete(synchronize_session=False)
    query = session.query(Imgs_cat).delete(synchronize_session=False)

    for x in range(0, 5):
        dog_link = get_imglink(dog)
        cat_link = get_imglink(cat)

        dog_img = Imgs_dog(link=dog_link)
        cat_img = Imgs_cat(link=cat_link)

        session.add(dog_img)
        session.add(cat_img)

    session.commit()

def main():

    fill_db()

if(__name__ == "__main__"):
    main()