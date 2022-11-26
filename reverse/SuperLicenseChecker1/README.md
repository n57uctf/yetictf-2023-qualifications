# Super license checker

### Разработчик: Павел Чернов

### Контакты(tg): @K001rch

**Суть таска:**

Заводится два массива. `user_lic` и `my_super_lic`.
В `user_lic` пишется пользовательская лицензия,
предварительно генерируется лицензия, которая сохраняется
в `my_super_lic`. Далее пользовательская лицензия
сверяется со сгенерированной. Если результат функции
strncmp = 0, значит - строки равны - выводится флаг,
содержимое которого равно сгенерированной ранее лицензии.

Бинарный упакован упаковщиком UPX. Перед началом дебага
необходимо распоковать его тем же упаковщиком. Понять,
что файл упакован можно при помощи просмотра исполняемого
файла в hex-редакторе.

**Ссылка на репо/архив:** 

### Запуск:

```
./SuperLicenseChecker1 <License-key> 
```

### Врайтап
 
```
╰─ ~/upx/./upx -d SuperLicenseChecker1 -o ./Sup1
╰─ gdb Sup1 
gdb-peda$ disas main
   ...
   0x00000000004019e9 <+325>:	call   0x401745 <my_license_generator>
   ...
// далее можем открыть иду и посмотреть, как генерируется лицензия
// и понять, что в результате будет сгенерировано или же ...
gdb-peda$ b * 0x0000000000401a0a
gdb-peda$ r AAAA-AAAA-AAAA-AAAA
Смотрим значения регистров:
RAX: 0x7fffffffdcc0 ("AAAA-AAAA-AAAA-AAAA")
RBX: 0x7fffffffdf50 --> 0x7fffffffe2fd ("SYSTEMD_EXEC_PID=2616")
RCX: 0x4c5100 ("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-")
RDX: 0x7fffffffdd00 ("ABCDEF-45678-GHIJKL-98765")
...
// Видим, что в RDX лежит строка, похожая на лицензию
gdb-peda$ r ABCDEF-45678-GHIJKL-98765
Breakpoint 1, 0x0000000000401a0a in main ()
gdb-peda$ c
Continuing.
ACCESS GRANTED !
Your flag: YetiCTF{ABCDEF-45678-GHIJKL-98765}
[Inferior 1 (process 8353) exited normally]
Warning: not running
```

### Описание

Получи мою лицензию!

### Флаг

```
YetiCTF{ABCDEF-45678-GHIJKL-98765}
```
