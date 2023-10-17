#include "ck.h"

int main(){

    //create a new CK - t for test
    ck *t = ck_initialize(1024,4,0.0012);


    // insert the novel stream
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("novel_stream.txt", "r");

    while ((read = getline(&line, &len, fp)) != -1) {
        line[strcspn(line, "\n")] = 0;
        ck_up(t,line);
    }

    fclose(fp);
    if (line) free(line);
    
    // check query logic and up logic again

    // test some queries
    ck_qry_response a1 = ck_qry(t,"1");
    printf("Qry(1): %"PRIu32 ",%d\n",a1.cnt,a1.flag);
    ck_qry_response a379 = ck_qry(t,"379");
    printf("Qry(327): %"PRIu32 ",%d\n",a379.cnt,a379.flag);
    ck_qry_response a2219 = ck_qry(t,"2219");
    printf("Qry(2219): %"PRIu32 ",%d\n",a2219.cnt,a2219.flag);

    //destroy the CK
    ck_destroy(t);

return 0;
}