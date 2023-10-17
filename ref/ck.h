#ifndef __CK_H
#define __CK_H

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdint.h> 
#include <string.h>
#include <inttypes.h>
#include <sodium.h>

/* Struct types */

typedef struct{
    unsigned char key[crypto_generichash_KEYBYTES]; // key used for hashing
    size_t m; // width
    size_t k; // depth
    uint32_t *M; // CMS array
    uint32_t *A; // HK counter array
    uint32_t *F; // HK fingerprint array
    size_t n; // tracks stream length 
    float psi; // flag parameter
}ck;

typedef struct{
    uint32_t cnt; // count value
    bool flag; //flag value
} ck_qry_response;

/* Functions for hashing */

uint32_t truncate_hash(unsigned char *hash);

size_t row_hash(const unsigned char *key, const  char *x, size_t i, size_t m);

uint32_t fp_hash(const unsigned char *key, const char *x);

/* Core CK functionality */

ck* ck_initialize(size_t m, size_t k, float psi);

void ck_destroy(ck *CK);

void ck_up(ck *CK, const char *x);

/* Helper functions for qrys*/

uint32_t cms_qry(const unsigned char* key, const uint32_t *M, size_t m, size_t k, const char *x);

uint32_t hk_qry(const unsigned char* key, const uint32_t *A, const uint32_t *F, size_t m, size_t k, const char *x);

ck_qry_response ck_qry(const ck *CK, const char *x);


#endif