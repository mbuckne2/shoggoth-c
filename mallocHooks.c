//
// Created by mitch on 4/2/24.
//


#include <stdio.h>
#include <stdlib.h>
#include "mallocHooks.h"

char* OUTPUT_FILE = "malloc_log.csv";

void* my_malloc(size_t size, const char* file, int line) {
    void* ptr = malloc(size);

    if(ptr != NULL) {
        write_to_file(ptr, size, file, line, "MALLOC");
    } else {
        fprintf(stderr, "malloc failed in file %s at line %d\n", file, line);
    }
    return ptr;
}

//note: size is set to 0, free doesn't really have a size (and I don't think it should matter)
void my_free(void* ptr, const char* file, int line) {

    write_to_file(ptr, 0, file, line, "FREE");
    free(ptr);
}

void* my_calloc(int num_elements, size_t size, const char* file, int line) {
    void* ptr = calloc(num_elements, size);

    if(ptr != NULL) {
        write_to_file(ptr, num_elements * size, file, line, "CALLOC");
    } else {
        fprintf(stderr, "calloc failed in file %s at line %d\n", file, line);
    }
    return ptr;

}

void* my_realloc(void* ptr, size_t new_size, const char* file, int line) {
    ptr = realloc(ptr, new_size);

    if(ptr != NULL) {
        write_to_file(ptr, new_size, file, line, "REALLOC");
    } else {
        fprintf(stderr, "calloc failed in file %s at line %d\n", file, line);
    }
    return ptr;

}

void write_to_file(void* ptr, size_t size, const char* file, int line, char* type) {
    FILE * outputFile = fopen(OUTPUT_FILE,"a");
    if(outputFile == NULL) {
        printf("Unable to save current data");
    } else {
        fprintf(outputFile, "%s,%p,%zu,%d,%s\n", type, ptr, size, line, file);
        fclose(outputFile);
    }

}