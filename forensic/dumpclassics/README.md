__Category__: 
* Forensic

__Author__: 
* @slyshay6

__Description__: 
Видимо все предыдущие попытки навариться на цифровом прошлом прапрадеда были тщетными. Что старые спекулятивные монеты, что этот "NFT" больше никому не нужны. Однако у меня есть последняя идея. Попробуй достать пароль от дефолтной учетной записи администратора./
(Флаг - пароль, все буквы в верхнем регистре. Пример: pAssw0R4 -> YetiCTF{PASSW0R4})/

Dump URLs:/
[Google Drive](https://drive.google.com/file/d/15godaZAKrOc88G88D5qsLLoTtokgoFjn/view?usp=share_link)/
[Yandex Disk](https://disk.yandex.ru/d/HKhD0aqIlMZAHA)/
[MEGA](https://mega.nz/file/9hdDmBYb#Q7NwMduJ7vwfpxtz9Nk1ny8i53bv8G2hdA6H3RxQRWE)/

MD5:/
0bb1f733f6e92c55f69b155f6cf1cc89  warning_dump.gz/
16b79fcd47c62f25127d3676bf6290ea  warning_dump

__Flag__:
* YetiCTF{4S34SY4SC4NB3}

__Files__:
* warning_dump

__Writeup__:
1. volatility3 windows.hashdump, достаем NTLM пользователя Administrator
2. крякером получаем пароль (http://rainbowtables.it64.com/)