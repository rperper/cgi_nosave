#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void error(char *msg)
{
    printf("Content-Type:text/html;charset=iso-8859-1\r\n"
           "Status: 400 Bad Request\r\n\r\n"
           "<TITLE>ERROR</TITLE>\r\n"
           "<BOLD>%s</BOLD>\r\n", msg);
    exit(1);
}


int main(int argc, char **argv) {
    /* First read */
    char *cl;
    const int blocksize = 262144;
    char block[blocksize];
    time_t start, end;
    time(&start);
    if (!(cl = getenv("CONTENT_LENGTH")))
        error("No CONTENT_LENGTH");
    int icl = atoi(cl);
    int i = 0;
    while (i < icl)
    {
        int size = blocksize;
        if (i + size > icl)
            size = icl - i;
        fread(block, 1, size, stdin);
        i += size;
    }
    time(&end);
    char charssec[100];
    if (start >= end)
        sprintf(charssec,"%s","<B>infinite</B>");
    else 
        sprintf(charssec,"%d",icl / (end - start));
    /* Then respond */
    printf("Content-Type:text/html;charset=iso-8859-1\r\n"
           "Status: 200 Success\r\n\r\n"
           "<TITLE>Read Complete and Successful</TITLE>\r\n"
           "<BOLD>Read %d bytes, %s chars/sec in %d seconds</BOLD>\r\n", 
           icl, charssec, end-start);
    return 0;
}
