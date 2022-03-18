import datetime

d = datetime.date(2022, 3, 17)
print(d)
keys = ('name', 'text', 'date')
values = ('Двенадцатая', '1234567890987654321', datetime.date(2022, 3, 17))
dict_from_db = dict(zip(keys, values))
print(dict_from_db)

d = {"id": "15", "name": "Статья №1","text": "12345678909"}
d_from ={"id": "15", "name": "Статья №1", "text": "1234", "date": "11.03.2022"}
d_for ={**d_from, **d}
print(d_for)