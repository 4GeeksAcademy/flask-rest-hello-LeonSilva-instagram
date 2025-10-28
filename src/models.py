from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(80), nullable=False)
    lastname: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    following: Mapped[list['Follower']] = relationship(
        'Follower',
        foreign_keys=[lambda: Follower.follower_id],
        back_populates='follower'
    )

    followers: Mapped[list['Follower']] = relationship(
        'Follower',
        foreign_keys=[lambda: Follower.followed_id],
        back_populates='followed'
    )

    posts: Mapped[list['Post']] = relationship(back_populates='user')
    comments: Mapped[list['Comment']] = relationship(back_populates='author')

class Follower(db.Model):
    __tablename__ = 'follower'

    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    followed_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    follower: Mapped['User'] = relationship(
        'User',
        foreign_keys=[follower_id],
        back_populates='following'
    )

    followed: Mapped['User'] = relationship(
        'User',
        foreign_keys=[followed_id],
        back_populates='followers'
    )

class Post(db.Model):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='posts')

    media: Mapped[list['Media']] = relationship(back_populates='post')
    comments: Mapped[list['Comment']] = relationship(back_populates='post')

class Media(db.Model):
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum('image', 'video', 'audio', name='media_type'))
    url: Mapped[str] = mapped_column(String(255))

    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    post: Mapped['Post'] = relationship(back_populates='media')

class Comment(db.Model):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(1000))
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    author: Mapped['User'] = relationship(back_populates='comments')
    post: Mapped['Post'] = relationship(back_populates='comments')
