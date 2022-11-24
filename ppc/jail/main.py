import os


flag = os.environ['FLAG']

data = input('>>> ')

if len(data) > 14 or 'flag' in data:
    print('Good bye\n')
else:
    try:
        eval(data)
    except:
        print('Good bye\n')
