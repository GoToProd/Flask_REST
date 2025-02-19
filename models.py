from passlib.hash import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base, relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta


engine = create_engine("sqlite:///test.db")

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()
Base.metadata.create_all(bind=engine)


class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(18), nullable=False)
    videos = relationship("Video", backref="user", lazy=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.password = bcrypt.hash(kwargs.get("password"))

    def get_token(self, expire_time=24):
        token = create_access_token(identity=str(self.id), expires_delta=timedelta(hours=expire_time))
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception("Invalid password")
        return user


if __name__ == "__main__":
    Base.metadata.create_all(engine)
