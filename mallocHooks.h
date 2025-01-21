//
// Created by mitch on 4/2/24.
//

#ifndef MODULE2TEST_MALLOCHOOKS_H
#define MODULE2TEST_MALLOCHOOKS_H

void* my_malloc(size_t size, const char* file, int line);
void my_free(void* ptr, const char* file, int line);
void* my_calloc(int num_elements, size_t size, const char* file, int line);
void* my_realloc(void* ptr, size_t new_size, const char* file, int line);
void write_to_file(void* ptr, size_t size, const char* file, int line, char* type);

#endif //MODULE2TEST_MALLOCHOOKS_H
