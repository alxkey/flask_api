from dataclasses import dataclass

from datetime import date


@dataclass(frozen=True)
class Article:
    name: str
    text: str
    date: date
    user_id: str


@dataclass(frozen=True)
class ArticleUpdate:
    article_id: str
    text: str
    date: date
    name: str
    user_id: str


@dataclass(frozen=True)
class ArticleResult:
    article_id: int


@dataclass(frozen=True)
class User:
    name: str
    password: str
    first_name: str
    last_name: str
    age: int


@dataclass(frozen=True)
class UserUpdate:
    user_id: str
    name: str
    password: str
    first_name: str
    last_name: str
    age: int


@dataclass(frozen=True)
class UserGet:
    name: str
    first_name: str
    last_name: str
    age: int


@dataclass(frozen=True)
class UserResult:
    token: str
    user_id: str


@dataclass(frozen=True)
class Like:
    article_id: str
    user_id: str


@dataclass(frozen=True)
class LikeGet:
    article_name: str
    likes: int


@dataclass(frozen=True)
class LikeGetById:
    article_name: str
    user_name: str


@dataclass(frozen=True)
class Comment:
    article_name: str
    user_name: str
    comment: str


@dataclass(frozen=True)
class CommentCreate:
    article_id: str
    user_id: str
    comment: str


@dataclass(frozen=True)
class CommentById:
    article_id: str
    user_id: str


@dataclass(frozen=True)
class CommentByName:
    article_name: str
    user_name: str


def main():
    pass


if __name__ == '__main__':
    main()
