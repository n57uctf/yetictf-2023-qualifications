import subprocess, time

dictionary = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}"

patterns = []

while True:

    if patterns == []:

        for char in dictionary:
            p = subprocess.Popen(f'java -jar javlocker.jar {char}', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            output = p.communicate()[0].decode('utf-8')
            if not('No patterns' in output):
                patterns.append(char)
                print(char)

            #time.sleep(0.01)

    else:

        for idx, pattern in enumerate(patterns):
            for char in dictionary:
                p = subprocess.Popen(f'java -jar javlocker.jar {char}{pattern}', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                output = p.communicate()[0].decode('utf-8')
                if 'Fully matched' in output:
                    patterns[idx] = f"{char}{patterns[idx]}"
                    print(f"Fully matched: {patterns[idx]}")
                    del patterns[idx]
                    break

                if not('No patterns' in output):
                    patterns[idx] = f"{char}{patterns[idx]}"
                    print(patterns[idx])
                    break

                #time.sleep(0.01)