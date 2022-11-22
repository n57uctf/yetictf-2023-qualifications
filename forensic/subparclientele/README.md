__Category__: 
* Forensic

__Author__: 
* @slyshay6

__Description__: 
Видимо криптокошельки на системе не хранились. Но прапрадед сказал: "Не знаю на кой ляд тебе этот кошелек сдался, но поможешь найти домен, откуда малварь стянулась, и мы в расчете."/
(Формат флага: YetiCTF{*domain*_*ip*})/

Dump URLs:/
[Google Drive](https://drive.google.com/file/d/15godaZAKrOc88G88D5qsLLoTtokgoFjn/view?usp=share_link)/
[Yandex Disk](https://disk.yandex.ru/d/HKhD0aqIlMZAHA)/
[MEGA](https://mega.nz/file/9hdDmBYb#Q7NwMduJ7vwfpxtz9Nk1ny8i53bv8G2hdA6H3RxQRWE)/

MD5:/
0bb1f733f6e92c55f69b155f6cf1cc89  warning_dump.gz/
16b79fcd47c62f25127d3676bf6290ea  warning_dump/

__Flag__:
* YetiCTF{seniorhotelplaza.com_192.168.40.77}

__Files__:
* warning_dump

__Writeup__:
1. grep bonzi, в строках будет URL с доменом seniorhotelplaza.com
2. grep seniorhotelplaza.com, в строках будет адрес 192.168.40.77
3. альтернативно можно просканить подключения connscan volatility2 и найти сначала адрес, потом найти домен прогрепав адрес