#include <stdio.h>
#include <string.h>
#include <malloc.h>

#define SUCCESS_EXIT (0)
#define ERROR_EXIT   (1)

#define LIC_MAX_SIZE (20)

#define RESET        ("\033[0m")
#define RED          ("\033[1;31m")
#define GREEN        ("\033[1;32m")
#define SEA_COLOR    ("\033[1;36m")
#define FLASHING     ("\033[1;5m")

#define HYPHEN       (36)
#define ALPHABET_END (25)

static char alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-\0";

static int my_license_generator(char * my_super_lic)
{
    if (NULL == my_super_lic)
    {
        return ERROR_EXIT;
    }

    int i = 0, j = 0;
    while (1)
    {
        if (j == 20) break;

        if ((0 == (j % 5)) && (j != 0))
        {
            my_super_lic[j++] = alphabet[HYPHEN];
            continue;
        }

        if (j < 5)
        {
            my_super_lic[j++] = alphabet[ALPHABET_END+1];
            continue;
        }

        if (j < 10)
        {
            my_super_lic[j++] = alphabet[ALPHABET_END];
            continue;
        }

        if (j < 15)
        {
            my_super_lic[j++] = alphabet[HYPHEN-1];
            continue;
        }

        if (j < 20)
        {
            my_super_lic[j++] = alphabet[i];
            continue;
        }
    }
    
    return SUCCESS_EXIT;
}

int compare_two_numbers(int a, int b)
{
    int r_code = (a == b) ? 0 : 1;
    return r_code;
}

int main(int argc, char * argv[])
{
    printf("%sYetiCTF Quals 2023 %s%sSuper License Checker 2%s\n", GREEN, RED, FLASHING, RESET);

    int i = 0, license_key = 0, user_key = 0;
    char * user_license_key = malloc(LIC_MAX_SIZE * sizeof(char));
    char * my_license_key = malloc(LIC_MAX_SIZE * sizeof(char));

    if (my_license_generator(my_license_key))
    {
        free(user_license_key);
        free(my_license_key);
        return ERROR_EXIT;
    }
    printf("%sMy license initialized !%s\n\n", SEA_COLOR, RESET);

    printf("%sEnter your license-key: %s", SEA_COLOR, RESET);
    fgets(user_license_key, LIC_MAX_SIZE+1, stdin);
    fflush(stdin);

    printf("\n%sComparing user's license-key and my super secret license !%s\n", SEA_COLOR, RESET);
    for (; i < LIC_MAX_SIZE; i++)
    {
        license_key += (int)my_license_key[i];
	    user_key += (int)user_license_key[i];
    }
 
    if (0 == compare_two_numbers(license_key, user_key))
    {
        printf("%s[+] Congrats, u are find my super-super secret license !%s\n", SEA_COLOR, RESET);
        printf("%s[+] YetiCTF{%s}%s\n", RED, my_license_key, RESET);
    }
    else
    {
        printf("%s[-] Try again =(%s\n", RED, RESET);
    }

    free(user_license_key);
    free(my_license_key);
    return SUCCESS_EXIT;
}
