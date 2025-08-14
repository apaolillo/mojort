#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void computeLPSArray(char *pattern, int m, int *LPS) {
    int length = 0;
    LPS[0] = 0;
    int i = 1;

    while (i < m) {
        if (pattern[i] == pattern[length]) {
            length++;
            LPS[i] = length;
            i++;
        } else {
            if (length != 0) {
                length = LPS[length - 1];
            } else {
                LPS[i] = 0;
                i++;
            }
        }
    }
}

int* KMP(char *pattern, char *text, int *matchCount) {
    int m = strlen(pattern);
    int n = strlen(text);

    int *LPS = (int *)malloc(sizeof(int) * m);
    computeLPSArray(pattern, m, LPS);

    int *ans = (int *)malloc(sizeof(int) * n);  // max possible matches is n
    *matchCount = 0;

    int i = 0;
    int j = 0;
    while (i < n) {
        if (pattern[j] == text[i]) {
            i++;
            j++;
        }

        if (j == m) {
            ans[(*matchCount)++] = i - j;
            j = LPS[j - 1];
        } else if (i < n && pattern[j] != text[i]) {
            if (j != 0)
                j = LPS[j - 1];
            else
                i++;
        }
    }

    free(LPS);
    return ans;
}

int main(int argc, char *argv[]) {
    FILE *file = fopen("../the_bible.txt", "r");
    if (file == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    // Read the whole line (assuming one-line file for now)
    char *text = (char *)malloc(4500000); // adjust size based on your data
    fgets(text, 4500000, file);
    fclose(file);

    double p = atof(argv[1]);
    int len = strlen(text);
    int newlen = (int)(len * p);
    text[newlen] = '\0';  // truncate the string

    char pattern[] = "God";

    clock_t start = clock();
    int matchCount = 0;
    int *ans = KMP(pattern, text, &matchCount);
    clock_t end = clock();

    if (matchCount > 0)
        printf("%d\n", ans[matchCount - 1]);

    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("runtime: %d µs\n", (int)(time_taken * 1e6));

    // Optional: Print all match indices
    /*
    printf("Pattern Found at Indexes: ");
    for (int i = 0; i < matchCount; i++)
        printf("%d ", ans[i]);
    printf("\n");
    */

    free(ans);
    free(text);
    return 0;
}
