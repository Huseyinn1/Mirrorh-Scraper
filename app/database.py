import logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Data(Base):
    __tablename__ = 'datas'
    id = Column(Integer, primary_key=True)
    attacker = Column(String)
    country = Column(String)
    url = Column(String)
    ip = Column(String)
    date = Column(String)
    leak_url = Column(String)

engine = create_engine('sqlite:///datas_posts.db')
Session = sessionmaker(bind=engine)
session = Session()

# Logger'ı yapılandır
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_table():
    Base.metadata.create_all(engine)


def is_data_exists(attacker,url):
    post = session.query(Data).filter_by(attacker=attacker, url=url).first()
    return post is not None

def insert_data(attacker, country, url, ip, date,leak_url):
    if not is_data_exists(attacker,url):
        post = Data(attacker=attacker, country=country, url=url, ip=ip, date=date,leak_url=leak_url)
        session.add(post)
        session.commit()
        logger.info(f"Data with URL '{url}' added successfully!")
        return True
    else:
        logger.warning(f"Data with URL '{url}' already exists!")
        return False

def delete_post(url):
    post = session.query(Data).filter_by(url=url).first()
    if post:
        session.delete(post)
        session.commit()
        logger.info(f"Data with URL '{url}' deleted successfully!")
    else:
        logger.warning(f"Data with URL '{url}' not found!")
