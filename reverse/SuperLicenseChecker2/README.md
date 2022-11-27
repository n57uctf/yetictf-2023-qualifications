# Super license checker

### Разработчик: Павел Чернов

### Контакты(tg): @K001rch

**Суть таска:**

Заводится два массива. `user_license_key` и `my_license_key`.
В `user_license_key` пишется пользовательская лицензия,
предварительно генерируется лицензия, которая сохраняется
в `my_license_key`. Далее пользовательская лицензия
сверяется со сгенерированной по суммам знаков, составляющих пользовательскую и
секретную лицензии соответсвенно. Если результат функции
compare_two_numbers = 0, значит - числа равны - выводится флаг,
содержимое которого равно сгенерированной ранее лицензии.

Бинарный упакован упаковщиком UPX. Перед началом дебага
необходимо распоковать его тем же упаковщиком. Понять,
что файл упакован можно при помощи просмотра исполняемого
файла в hex-редакторе.

**Ссылка на репо/архив:** 

### Запуск:

```
./SuperLicenseChecker2 
```

### Врайтап
 
```
╰─ ~/upx/./upx -d SuperLicenseChecker2 -o ./Sup2
╰─ gdb Sup2
gdb-peda$ disass main
// интересующий код
...
   0x00000000000014a9 <+400>:	call   0x12f7 <compare_two_numbers>
   0x00000000000014ae <+405>:	test   eax,eax
   0x00000000000014b0 <+407>:	jne    0x150b <main+498>
...
// видим, что если результат сравнения двух чисел
// не равен, то делаем jump на выход, пропуская большой
// кусок кода. Похоже на то, что мы таким образом пропускаем вывод флага
// проверим это.

// делаем тестовый запуск, чтобы проинициализировать оффсеты
gdb-peda$ r
Starting program: /home/k1rch/CTF/Yeti2023Quals/reverse/SuperLicenseChecker2/reverse2 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
YetiCTF Quals 2023 Super License Checker 2
My license initialized !

Enter your license-key: AAAA-AAAA-AAAA-AAAA

Comparing user's license-key and my super secret license !
[-] Try again =(
[Inferior 1 (process 69210) exited normally]
gdb-peda$ disass main
// оффсеты проинициализировались
   0x00005555555554a9 <+400>:	call   0x5555555552f7 <compare_two_numbers>
   0x00005555555554ae <+405>:	test   eax,eax
   0x00005555555554b0 <+407>:	jne    0x55555555550b <main+498>
....
// делаем точку останова на инструкцию по оффсету 0x00005555555554a9
gdb-peda$ b * 0x00005555555554a9
Breakpoint 1 at 0x5555555554a9
gdb-peda$ r
Starting program: /home/k1rch/CTF/Yeti2023Quals/reverse/SuperLicenseChecker2/reverse2 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
YetiCTF Quals 2023 Super License Checker 2
My license initialized !

Enter your license-key: AAAA-AAAA-AAAA-AAAA

Comparing user's license-key and my super secret license !
...
=> 0x00005555555554a9 <+400>:	call   0x5555555552f7 <compare_two_numbers>
   0x00005555555554ae <+405>:	test   eax,eax
   0x00005555555554b0 <+407>:	jne    0x55555555550b <main+498>
...
gdb-peda$ disass compare_two_numbers
Dump of assembler code for function compare_two_numbers:
   0x00005555555552f7 <+0>:	endbr64 
   0x00005555555552fb <+4>:	push   rbp
   0x00005555555552fc <+5>:	mov    rbp,rsp
   0x00005555555552ff <+8>:	mov    DWORD PTR [rbp-0x14],edi
   0x0000555555555302 <+11>:	mov    DWORD PTR [rbp-0x18],esi
   0x0000555555555305 <+14>:	mov    eax,DWORD PTR [rbp-0x14]
   0x0000555555555308 <+17>:	cmp    eax,DWORD PTR [rbp-0x18]
   0x000055555555530b <+20>:	setne  al
   0x000055555555530e <+23>:	movzx  eax,al
   0x0000555555555311 <+26>:	mov    DWORD PTR [rbp-0x4],eax
   0x0000555555555314 <+29>:	mov    eax,DWORD PTR [rbp-0x4]
   0x0000555555555317 <+32>:	pop    rbp
   0x0000555555555318 <+33>:	ret    
End of assembler dump.
gdb-peda$ b * 0x0000555555555308
Breakpoint 2 at 0x555555555308
gdb-peda$ c
Continuing.
// На самом деле флаг можно уже сейчас посмотреть в стеке
...
0048| 0x7fffffffde10 --> 0x5555555596b0 ("AAAA-AAAA-AAAA-AAAA\n")
0056| 0x7fffffffde18 --> 0x5555555596d0 ("00000-ZZZZ-9999-AAAA")
...
или тут:
gdb-peda$ x/60sx $rsp
0x7fffffffdde0:	0x20	0xde	0xff	0xff	0xff	0x7f	0x00	0x00
0x7fffffffdde8:	0xae	0x54	0x55	0x55	0x55	0x55	0x00	0x00
0x7fffffffddf0:	0x38	0xdf	0xff	0xff	0xff	0x7f	0x00	0x00
0x7fffffffddf8:	0xff	0xfb	0xeb	0xbf	0x01	0x00	0x00	0x00
0x7fffffffde00:	0x99	0xe2	0xff	0xff	0x14	0x00	0x00	0x00
0x7fffffffde08:	0xc7	0x04	0x00	0x00	0xa1	0x04	0x00	0x00
0x7fffffffde10:	0xb0	0x96	0x55	0x55	0x55	0x55	0x00	0x00
0x7fffffffde18:	0xd0	0x96	0x55	0x55

Однако пойдем другим путем:
доходим до инструкции:
=> 0x555555555317 <compare_two_numbers+32>:	pop    rbp
и изменяем код возврата с 1 на 0:
gdb-peda$ set $rax=0x0
gdb-peda$ c
Continuing.
[+] Congrats, u are find my super-super secret license !
[+] YetiCTF{00000-ZZZZ-9999-AAAA}
[Inferior 1 (process 69274) exited normally]
Warning: not running
gdb-peda$
```

### Описание

Я усложнил свою защиту лицензии, попытайтесь найти её ещё раз !

### Флаг
```
YetiCTF{00000-ZZZZ-9999-AAAA}
```