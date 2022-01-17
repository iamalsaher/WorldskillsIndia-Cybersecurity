#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

typedef struct string {
    unsigned length;
    char *data;
} string;

int main() {
    struct string* s = malloc(sizeof(string));
    puts("Length:");
    scanf("%u", &s->length);
    s->data = malloc(s->length + 1);
    memset(s->data, 0, s->length + 1);
    puts("Data:");
    read(0, s->data, s->length);

    free(s->data);
    free(s);

    char *s2 = malloc(16);
    memset(s2, 0, 16);
    puts("More data:");
    read(0, s2, 15);

    puts(s->data);

    return 0;
}