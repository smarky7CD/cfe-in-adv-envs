#include "ck.h"

/* Functions for hashing */

uint32_t truncate_hash(unsigned char *hash){
    uint32_t h;
    h = (uint32_t)hash[0] << 24 |
        (uint32_t)hash[1] << 16 |
        (uint32_t)hash[2] << 8  |
        (uint32_t)hash[3];
    return h;
}

size_t row_hash(const unsigned char *key, const  char *x, size_t i, size_t m)
{
    unsigned char hash[crypto_generichash_BYTES];
    crypto_generichash_state state;
    crypto_generichash_init(&state, key, sizeof key, sizeof hash);
    char istr[256];
    snprintf(istr, sizeof istr, "%zu", i);
    crypto_generichash_update(&state, (const unsigned char *) istr, strlen(istr));
    crypto_generichash_update(&state, (const unsigned char *) x, strlen(x));
    crypto_generichash_final(&state, hash, sizeof hash);
    uint32_t h = truncate_hash(hash);
    size_t j = (size_t) h % m;
    return j;
}

uint32_t fp_hash(const unsigned char *key, const char *x){
    #define FP ((const unsigned char *) "fp")
    #define FP_LEN 2
    unsigned char hash[crypto_generichash_BYTES];
    crypto_generichash_state state;
    crypto_generichash_init(&state, key, sizeof key, sizeof hash);
    crypto_generichash_update(&state, (const unsigned char *) FP, FP_LEN);
    crypto_generichash_update(&state, (const unsigned char *) x, strlen(x));
    crypto_generichash_final(&state, hash, sizeof hash);
    uint32_t fp = truncate_hash(hash);
    if (fp == 0) fp++;
    return fp;
}

/* Core CK functionality */

ck* ck_initialize(size_t m , size_t k, float psi){
    ck* CK = (ck*) malloc(sizeof(ck));
    randombytes_buf(CK->key, sizeof CK->key);
    CK->m = m;
    CK->k = k;
    CK->M = (uint32_t *) calloc((m*k), sizeof(uint32_t));
    CK->A = (uint32_t *) calloc((m*k), sizeof(uint32_t));
    CK->F = (uint32_t *) calloc((m*k), sizeof(uint32_t));
    CK->n = 0;
    CK->psi = psi;
    return CK;
}

void ck_destroy(ck *CK){
    free(CK->M);
    free(CK->A);
    free(CK->F);
    free(CK);
}


void ck_up(ck *CK, const char *x){
    CK->n++;
    uint32_t fpx = fp_hash(CK->key, x);
    for(size_t i=0; i<CK->k; i++){
        size_t xi = row_hash(CK->key,x,i,CK->m) + (CK->m * i); 
        CK->M[xi]++;
        uint32_t fpa = CK->F[xi];
        if (fpa == 0){
            CK->A[xi] = 1;
            CK->F[xi] = fpx;
        } else if (fpx == fpa)
        {
            CK->A[xi]++;
        } else{
            CK->A[xi]--;
            if (CK->A[xi] == 0){
                CK->A[xi]++;
                CK->F[xi] = fpx;
            }
        }
    }   
}

/* Helper functions for qrys */

uint32_t cms_qry(const unsigned char* key, const uint32_t *M, size_t m, size_t k, const char *x){
    uint32_t c = UINT32_MAX;
    for(size_t i=0; i<k; i++){
        size_t xi = row_hash(key,x,i,m) + (m * i);
        if (M[xi] < c) c = M[xi]; 
    }
    return c;
}

uint32_t hk_qry(const unsigned char* key, const uint32_t *A, const uint32_t *F, size_t m, size_t k, const char *x){
    uint32_t c = 0;
    uint32_t fpx = fp_hash(key, x);
     for(size_t i=0; i<k; i++){
        size_t xi = row_hash(key,x,i,m) + (m * i);
        if (A[xi] > c && F[xi] == fpx) c = A[xi]; 
    }
    return c;
}

ck_qry_response ck_qry(const ck *CK, const char* x){
    ck_qry_response a;
    uint32_t theta1 = UINT32_MAX;
    uint32_t theta2 =  UINT32_MAX;
    float delta = (float) UINT32_MAX;
    
    uint32_t cntUBx = cms_qry(CK->key,CK->M,CK->m,CK->k,x);
    uint32_t cntLBx = hk_qry(CK->key,CK->A,CK->F,CK->m,CK->k,x);

    if (cntUBx == cntLBx){
        a.cnt = cntUBx;
        a.flag = false;
        return a;
    }
    
    uint32_t fpx = fp_hash(CK->key, x);
    for(size_t i=0; i<CK->k; i++){
        size_t xi = row_hash(CK->key,x,i,CK->m) + (CK->m * i); 
        uint32_t fpa = CK->F[xi];
        if (fpa == 0){
            a.cnt = 0;
            a.flag = false;
            return a;
        } 
        if (fpx != fpa){
            uint32_t  theta1_n = (CK->M[xi] - CK->A[xi] + 1) / 2;
            if(theta1_n < theta1) theta1 = theta1_n;
            if(theta1_n < delta) delta = theta1_n;
        } else{
            uint32_t theta2_n = CK->A[xi] + ((CK->M[xi] - CK->A[xi]) / 2);
            uint32_t delta_n = theta2_n - CK->A[xi];
            if(theta2_n < theta2) theta2 = theta2_n;
            if(delta_n < delta) delta = delta_n;
        }
    }
    
    if(cntUBx < theta1 && cntUBx < theta2){
        a.cnt = cntUBx;
    }else if(theta1 < theta2)
    {
        a.cnt = theta1;
    }else{
        a.cnt = theta2;
    }

    if(delta >= (CK->psi * (float) CK->n)){
         a.flag = true;
    }else{
        a.flag = false;
    }
    
    return a;

}
