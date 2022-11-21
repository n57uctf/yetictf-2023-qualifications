# Secure Drive

### Разработчики: Елисеев Никита, Малахов Егор

### Контакты(discord): Никитa#8022, BëḳöṠä#9151

**Суть таска:**

Веб приложение для работы с файлами в базе данных. Регистрируемся, логинимся в только что созданный аккаунт. Чтобы зарегаться, надо залогиниться в несуществующего пользователя (любые данные логина и пароля на форме авторизации, не важно какие). После логина, сверху видны данные текущего пользователя: его отпечаток в SHA-256 и его логин. Есть возможность выгружать любые файлы в базу данных, размер которых не превышает 30 мб, они будут шифроваться AES паролем пользователя и храниться в бд в зашифрованном виде. Для скачивания выбранного файла в расшифрованном виде необходимо ввести пароль пользователя, в противном случае, если поле для ввода пароля будет пустым, или будет содержать неправильный пароль, файл скачается в зашифрованном виде. Для получения флага необходимо подменить куки пользователя скриптиком и так мы попадем под админа. В данном случае используется уязвимость самопдописанных JWT с помощью kid параметра в хедере самого JWT, а подписывать подмененный JWT будет файл /dev/null. Админ создается при первом запуске приложения, и содержит в себе единственный файлик - архив с текстовиком, в котором лежит флаг. Когда зашли под админа через подмену куки, видим сверху отпечаток его пароля в SHA-256. Брутим по радужным таблицам, вводим пароль и скачиваем архив, флаг внутри.

**Ссылка на репо/архив:** 

### Запуск:
```
docker-compose build
docker-compose up
```

### Врайтап
Ссылка на скриптик - [https://github.com/ticarpi/jwt_tool/](https://github.com/ticarpi/jwt_tool/)
Ну либо как-нибудь сами, если нельзя скачать скрипт :)

```
python3 jwt_tool.py JWT -I -hc kid -hv "../../../../../../../../dev/null" -pc login -pv admin -S hs256 -p ""
```
+ JWT - куки пользователя, которые мы вытащили из браузера, либо другим скриптом
+ -hc - header claim, какой параметр меняем в хедере
+ -hv - header value, какое значение туда пихаем, а пихаем мы конкретно файл по пути /dev/null, который и подпишет наш файл, но до файла еще надо дойти, поэтому поднимаемся по директориям наверх 7-8 раз, этого, наверное, будет достаточно, чтобы попась в корень 
+ -pc - payload claim - если немного пошариться по страничке сервиса, то можно заметить, что поле для ввода логина называется login
+ -pv - payload value - а значением логина будет наш пользователь admin
+ -S - алгоритм JWT
+ -p - payload, в данном случае он пустой, можно и здесь предполагать на какие поля какие значения передавать для формирования токена

После запуска скрипта, он выдает нам JWT, куки, вставляем их в браузер, попадаем под админа.
Смотрим хэш по радужным таблицам, заходим в admin находим флаг


### Описание



### Флаг

```
YetiCTF{L1v3_l1kE_a_f1dg37}
```

