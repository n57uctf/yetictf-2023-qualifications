__Category__: 
* Forensic

__Author__: 
* @slyshay6

__Description__: 
На другом жестком диске из вещей прапрадеда раскатана какая-то доисторическая ось, говорит что это одна из самых первых его систем. Думаю на этом дереликте может находится что-то интересное. Но мой нейрофайер орет, что там малвари и выдает этот дамп памяти. Найди, на что он может ругаться и отправь полный путь./
(Формат флага: YetiCTF{*path_in_lowercase*}. Разделяющий слэш - '/'./
Example: 'C:/My Documents/MalProc.bat' -> YetiCTF{/my documents/malproc.bat})/

Dump URLs:/
[Google Drive](https://drive.google.com/file/d/15godaZAKrOc88G88D5qsLLoTtokgoFjn/view?usp=share_link)/
[Yandex Disk](https://disk.yandex.ru/d/HKhD0aqIlMZAHA)/
[MEGA](https://mega.nz/file/9hdDmBYb#Q7NwMduJ7vwfpxtz9Nk1ny8i53bv8G2hdA6H3RxQRWE)/
/

MD5:/
0bb1f733f6e92c55f69b155f6cf1cc89  warning_dump.gz/
16b79fcd47c62f25127d3676bf6290ea  warning_dump

__Flag__:
* YetiCTF{/program files/bonzibuddy432/bonzibdy_35.exe}

__Files__:
* warning_dump

__Writeup__:
1. volatility3 windows.pstree вывести список процессов, найти BonziBDY_35.EXE
2. вывести все образы windows.filescan, взять grep BonziBDY_35.EXE
3. привести путь к виду: /program files/bonzibuddy432/bonzibdy_35.exe