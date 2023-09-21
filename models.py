from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CatImage(Base):
    __tablename__ = "CatImage"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cat_id = Column(Integer, ForeignKey("Cat.id"), nullable=False)
    src = Column(String, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    cat = relationship("Cat", back_populates="images")


class Cat(Base):
    __tablename__ = "Cat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    stamnavn = Column(String, nullable=False)
    pedigreeurl = Column(String)
    description = Column(String)
    birth = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    fertile = Column(Boolean, nullable=False)
    father = Column(String, nullable=False)
    mother = Column(String, nullable=False)
    breeder = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    images = relationship("CatImage", back_populates="cat", lazy="dynamic")


class Kitten(Base):
    __tablename__ = "Kitten"

    id = Column(Integer, primary_key=True, autoincrement=True)
    litter_id = Column(Integer, ForeignKey("Litter.id"), nullable=False)
    name = Column(String, nullable=False)
    stamnavn = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    info = Column(String)


class Litter(Base):
    __tablename__ = "Litter"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    born = Column(String, nullable=False)
    pedigreeurl = Column(String)
    mother_img = Column(String, nullable=False)
    father_img = Column(String, nullable=False)
    mother_name = Column(String, nullable=False)
    father_name = Column(String, nullable=False)
    mother_stamnavn = Column(String, nullable=False)
    father_stamnavn = Column(String, nullable=False)
    description = Column(String, nullable=False)
    litter_kittens = relationship("Kitten", backref="litter", lazy="dynamic")
    litter_pictures = relationship(
        "LitterPictureWeek", backref="litter", lazy="dynamic"
    )
    slug = Column(String)
    post_image = Column(String)
    tags = relationship("Tag", back_populates="litter")


class LitterPictureWeek(Base):
    __tablename__ = "LitterPictureWeek"

    id = Column(Integer, primary_key=True, autoincrement=True)
    litter_id = Column(Integer, ForeignKey("Litter.id"), nullable=False)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    images = relationship(
        "KittenPictureImage", backref="kitten_picture", lazy="dynamic"
    )


class KittenPictureImage(Base):
    __tablename__ = "KittenPictureImage"

    id = Column(Integer, primary_key=True, autoincrement=True)
    litter_picture_week = Column(
        Integer, ForeignKey("LitterPictureWeek.id"), nullable=False
    )
    title = Column(String)
    src = Column(String, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)

class Tag(Base):
    __tablename__ = "Tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String, nullable=False)
    litter_id = Column(Integer, ForeignKey("Litter.id"), nullable=False)
    litter = relationship("Litter",  back_populates="tags")
          