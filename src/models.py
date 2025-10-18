from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user' 
    id: Mapped[int] = mapped_column(primary_key = True)
    firstname: Mapped[str] = mapped_column(String(80),nullable = False)
    lastname: Mapped[str] = mapped_column(String(80),nullable = False) 
    email: Mapped[str] = mapped_column(String(120), unique = True, nullable = False)
    password: Mapped[str] = mapped_column(nullable = False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    # USUARIOS QUE ESTE SIGUE
    following: Mapped[list['Follower']] = relationship('Follower', 
        foreign_keys = [lambda: Follower.user_from_id],
        back_populates = 'user_id') 
    
    # USUARIOS QUE SIGUEN A ESTE USUARIO
    followers: Mapped[list['Follower']] = relationship('Follower',
        foreign_keys = [lambda: Follower.user_followed_by],
        back_populates = 'user_followed')

    posted: Mapped[list['Post']] = relationship(back_populates = 'user')
    comment_relation_author: Mapped['Comment'] = relationship(back_populates = 'author_relation')
    


class Follower(db.Model):
    __tablename__ = 'follower'
    # USUARIO QUE SIGUE A ALGUIEN O NADIE
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user_id: Mapped['User'] = relationship('User',
        foreign_keys = [user_from_id],
        back_populates= 'following')
    
    # A QUE USUARIOS SIGUE ESE USUARIO
    user_followed_by: Mapped[int] = mapped_column(ForeignKey('user.id')) 
    user_followed: Mapped['User'] = relationship('User',
        foreign_keys = [user_followed_by],
        back_populates= 'followers')

class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] =  mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates = 'posted')
    media_relation: Mapped[list['Media']] = relationship(back_populates = 'post_relation')
    Comment_relation_post: Mapped['Comment'] = relationship(back_populates = 'post_relation')

class Media(db.Model):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key = True)
    type: Mapped[str] = mapped_column(Enum('image','video','audio', name = 'media_type'))
    url: Mapped[str] = mapped_column(String(80))
    
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    post_relation: Mapped['Post'] = relationship(back_populates = 'media_relation')    

class Comment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key = True)
    comment_text: Mapped[str] = mapped_column(String(1000))
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    author_relation: Mapped['User'] = relationship(back_populates = 'comment_relation_author')
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    post_relation: Mapped['Post'] = relationship(back_populates = 'comment_relation_post' )