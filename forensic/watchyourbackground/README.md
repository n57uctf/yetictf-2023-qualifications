__Category__: 
* Forensic

__Author__: 
* @slyshay6

__Description__: 
И кстати, в прошлом существовали какие-то "NFT", они тоже могут стоить хороших денег. Прапрадед говорит, как раз что-то подобное стояло на рабочем столе этой системы. Можешь достать эту картинку?/

Dump URLs:/
[Google Drive](https://drive.google.com/file/d/15godaZAKrOc88G88D5qsLLoTtokgoFjn/view?usp=share_link)/
[Yandex Disk](https://disk.yandex.ru/d/HKhD0aqIlMZAHA)/
[MEGA](https://mega.nz/file/9hdDmBYb#Q7NwMduJ7vwfpxtz9Nk1ny8i53bv8G2hdA6H3RxQRWE)/

MD5:/
0bb1f733f6e92c55f69b155f6cf1cc89  warning_dump.gz/
16b79fcd47c62f25127d3676bf6290ea  warning_dump

__Flag__:
* YetiCTF{wh3n_n0st4lg14_h1ts_h4rd}

__Files__:
* warning_dump

__Writeup__:
1. volatility3 windows.filescan, grepом находим Wallpaper1.bmp
2. дампим образ при помощи плагина windows.dumpfiles, получаем картинку с флагом