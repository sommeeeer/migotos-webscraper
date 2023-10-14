from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CatImage(Base):
    __tablename__ = "CatImage"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cat_id = Column(Integer, ForeignKey("Cat.id"), nullable=False)
    src = Column(String(255), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    cat = relationship("Cat", back_populates="images")
    blururl = Column(String(255), nullable=False)


class Cat(Base):
    __tablename__ = "Cat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    stamnavn = Column(String(255), nullable=False)
    pedigreeurl = Column(String(255))
    description = Column(String(255))
    birth = Column(String(255), nullable=False)
    gender = Column(String(255), nullable=False)
    fertile = Column(Boolean, nullable=False)
    father = Column(String(255), nullable=False)
    mother = Column(String(255), nullable=False)
    breeder = Column(String(255), nullable=False)
    owner = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    images = relationship("CatImage", back_populates="cat", lazy="dynamic")


class Kitten(Base):
    __tablename__ = "Kitten"

    id = Column(Integer, primary_key=True, autoincrement=True)
    litter_id = Column(Integer, ForeignKey("Litter.id"), nullable=False)
    name = Column(String(255), nullable=False)
    stamnavn = Column(String(255), nullable=False)
    gender = Column(String(255), nullable=False)
    info = Column(String(255))


class Litter(Base):
    __tablename__ = "Litter"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    born = Column(String(255), nullable=False)
    pedigreeurl = Column(String(255))
    mother_img = Column(String(255), nullable=False)
    father_img = Column(String(255), nullable=False)
    mother_name = Column(String(255), nullable=False)
    father_name = Column(String(255), nullable=False)
    mother_stamnavn = Column(String(255), nullable=False)
    father_stamnavn = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    litter_kittens = relationship("Kitten", backref="litter", lazy="dynamic")
    litter_pictures = relationship(
        "LitterPictureWeek", backref="litter", lazy="dynamic"
    )
    slug = Column(String(255))
    post_image = Column(String(255))
    tags = relationship("Tag", back_populates="litter")


class LitterPictureWeek(Base):
    __tablename__ = "LitterPictureWeek"

    id = Column(Integer, primary_key=True, autoincrement=True)
    litter_id = Column(Integer, ForeignKey("Litter.id"), nullable=False)
    name = Column(String(255), nullable=False)
    link = Column(String(255), nullable=False)
    images = relationship(
        "KittenPictureImage", backref="kitten_picture", lazy="dynamic"
    )


class KittenPictureImage(Base):
    __tablename__ = "KittenPictureImage"

    id = Column(Integer, primary_key=True, autoincrement=True)
    litter_picture_week = Column(
        Integer, ForeignKey("LitterPictureWeek.id"), nullable=False
    )
    title = Column(String(255))
    src = Column(String(255), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    blururl = Column(String(255), nullable=False)


class Tag(Base):
    __tablename__ = "Tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(255), nullable=False)
    litter_id = Column(Integer, ForeignKey("Litter.id"), nullable=False)
    litter = relationship("Litter", back_populates="tags")


class BlogPost(Base):
    __tablename__ = "BlogPost"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_date = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(String(255), nullable=False)
    image_url = Column(String(255), nullable=False)
    tags = relationship("BlogPostTag", back_populates="blog_post")


class BlogPostTag(Base):
    __tablename__ = "BlogPostTag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(255), nullable=False)
    blog_post_id = Column(Integer, ForeignKey("BlogPost.id"), nullable=False)
    blog_post = relationship("BlogPost", back_populates="tags")
