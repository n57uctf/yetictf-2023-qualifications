#include <stdio.h>
#include <malloc.h>
#include <string.h>

#define LIC_MAX_SIZE (64)
#define SUCCESS_EXIT (0)
#define ERROR_EXIT   (1)
#define RESET        ("\033[0m")
#define RED          ("\033[1;31m")
#define GREEN        ("\033[1;32m")
#define FLASHING     ("\033[1;5m")

#define ALPHABET_END (26)
#define NUMBERS_END  (10)
#define HYPHEN       (36)

static char alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-\0";

static int my_license_generator(char * my_super_lic)
{
    if (NULL == my_super_lic)
    {
        return ERROR_EXIT;
    }

    int i, j = 0;
    for (i = 0; i < ALPHABET_END/4; i++)
    {
        my_super_lic[j++] = alphabet[i];
    }
    my_super_lic[j++] = alphabet[HYPHEN];

    for (i = (ALPHABET_END+4); i < HYPHEN-1; i++)
    {
        my_super_lic[j++] = alphabet[i];
    }
    my_super_lic[j++] = alphabet[HYPHEN];

    for (i = ALPHABET_END/4; i < ALPHABET_END/2 - 1; i++)
    {
        my_super_lic[j++] = alphabet[i];
    }
    my_super_lic[j++] = alphabet[HYPHEN];

    for (i = HYPHEN-1; i > (ALPHABET_END+4); i--)
    {
        my_super_lic[j++] = alphabet[i];
    }

    return SUCCESS_EXIT;
}

int main(int argc, char * argv[])
{
    printf("%sYetiCTF Quals 2023 %sSuper License Checker #1%s\n", GREEN, RED, RESET);
    if (argc < 2)
    {
        printf("Usage: ./SuperLicenseChecker1 %s<License-Key>%s\n", FLASHING, RESET);
        return ERROR_EXIT;
    }

    char user_lic[LIC_MAX_SIZE] = {0};
    strcpy(user_lic, argv[1]);

    char my_super_lic[LIC_MAX_SIZE] = {0};
    if (my_license_generator(my_super_lic)) return ERROR_EXIT;
    
    if (0 == strcmp(user_lic, my_super_lic))
    {
        printf("%s%sACCESS GRANTED !%s\n", GREEN, FLASHING, RESET);
        printf("Your flag: %sYetiCTF{%s}%s\n", RED, my_super_lic, RESET);
    }

    return SUCCESS_EXIT;
}
