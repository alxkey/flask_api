select name, count(article_like.users_id)
from articles
inner join article_like
on articles.id = article_like.articles_id
where article_like.is_deleted = false
group by name
order by count desc;

update article_like set is_deleted = true;

update article_like set is_deleted = true where articles_id in
(select id from articles where name = 'Seventh artikle')
and users_id in
(select id from users where name ='ivashka');
select * from article_like;

select articles.name, users.name
from articles
inner join article_like
on article_like.articles_id = articles.id
inner join users
on article_like.users_id = users.id
where articles.id = 5 and is_deleted = false;

select articles.name, users.name
from articles
inner join article_like
on article_like.articles_id = articles.id
inner join users
on article_like.users_id = users.id
where articles.name = 'Двенадцатая' and is_deleted = false;

select articles.name, users.name, comments.comment_text
from articles
inner join comments
on comments.articles_id = articles.id
inner join users
on comments.users_id = users.id;

select articles.name, users.name, comments.comment_text
from articles
inner join comments
on comments.articles_id = articles.id
inner join users
on comments.users_id = users.id
where articles.id =15
and articles.is_deleted = false
and comments.is_deleted = false;

insert into comments(aricles_id, users_id, comment_text)
values('{data['article_id']}', '{data['user_id']}', '{data['comment']}');



