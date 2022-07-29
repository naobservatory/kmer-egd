// Copyright (c) 2010, Paul Hsieh
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// * Redistributions of source code must retain the above copyright notice, this
//   list of conditions and the following disclaimer.
// * Redistributions in binary form must reproduce the above copyright notice,
//   this list of conditions and the following disclaimer in the documentation
//   and/or other materials provided with the distribution.
// * Neither my name, Paul Hsieh, nor the names of any other contributors to the
//   code use may not be used to endorse or promote products derived from this
//   software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

// Via https://chromium.googlesource.com/chromium/src/base/+/master/third_party/superfasthash/superfasthash.c
// See http://www.azillionmonkeys.com/qed/hash.html

#ifndef SUPER_FAST_HASH_H
#define SUPER_FAST_HASH_H

#include <stdint.h>

#undef get16bits
#if (defined(__GNUC__) && defined(__i386__)) || defined(__WATCOMC__) \
  || defined(_MSC_VER) || defined (__BORLANDC__) || defined (__TURBOC__)
#define get16bits(d) (*((const uint16_t *) (d)))
#endif

#if !defined (get16bits)
#define get16bits(d) ((((uint32_t)(((const uint8_t *)(d))[1])) << 8)\
                       +(uint32_t)(((const uint8_t *)(d))[0]) )
#endif

uint32_t SuperFastHash (const char * data, int len) {
    uint32_t hash = (uint32_t)len, tmp;
    int rem;

    if (len <= 0 || data == NULL) return 0;

    rem = len & 3;
    len >>= 2;

    /* Main loop */
    for (;len > 0; len--) {
        hash  += get16bits (data);
        tmp    = (uint32_t)(get16bits (data+2) << 11) ^ hash;
        hash   = (hash << 16) ^ tmp;
        data  += 2*sizeof (uint16_t);
        hash  += hash >> 11;
    }

    /* Handle end cases */
    switch (rem) {
        case 3: hash += get16bits (data);
                hash ^= hash << 16;
                hash ^=
                    (uint32_t)(((signed char)data[sizeof (uint16_t)]) << 18);
                hash += hash >> 11;
                break;
        case 2: hash += get16bits (data);
                hash ^= hash << 11;
                hash += hash >> 17;
                break;
        case 1: hash += (uint32_t)((signed char)*data);
                hash ^= hash << 10;
                hash += hash >> 1;
    }

    /* Force "avalanching" of final 127 bits */
    hash ^= hash << 3;
    hash += hash >> 5;
    hash ^= hash << 4;
    hash += hash >> 17;
    hash ^= hash << 25;
    hash += hash >> 6;

    return hash;
}

#define to16bits(a,b) (((uint32_t)(a) << 8) + (uint32_t)(b))

char complement(char b) {
  switch (b) {
  case 'A': return 'T';
  case 'C': return 'G';
  case 'G': return 'C';
  case 'T': return 'A';
  default: return ' ';
  }
}

// Compute a hash of the range from offset to offset-1, wrapping at K.  The
// hash should be identical for a sequence and its reverse complement.  The
// value for K must be a multiple of 4.
uint64_t HashGenomicCircularBuffer(const char* cb, uint32_t offset) {
  uint32_t hash_f = K;
  uint32_t hash_r = K;
  uint32_t tmp_f;
  uint32_t tmp_r;

  /* Main loop */
  for (int i = 0 ; i < (K >> 2); i++) {
    char location_f1 = cb[(offset + i*4 + 0) % K];
    char location_f2 = cb[(offset + i*4 + 1) % K];
    char location_f3 = cb[(offset + i*4 + 2) % K];
    char location_f4 = cb[(offset + i*4 + 3) % K];
      
    hash_f  += to16bits(location_f1, location_f2);
    tmp_f    = (uint32_t)(to16bits(location_f3, location_f4) << 11) ^ hash_f;
    hash_f   = (hash_f << 16) ^ tmp_f;
    hash_f  += hash_f >> 11;

    char location_r1 = complement(cb[(K + offset - i*4 - 1) % K]);
    char location_r2 = complement(cb[(K + offset - i*4 - 2) % K]);
    char location_r3 = complement(cb[(K + offset - i*4 - 3) % K]);
    char location_r4 = complement(cb[(K + offset - i*4 - 4) % K]);
      
    hash_r  += to16bits(location_r1, location_r2);
    tmp_r    = (uint32_t)(to16bits(location_r3, location_r4) << 11) ^ hash_r;
    hash_r   = (hash_r << 16) ^ tmp_r;
    hash_r  += hash_r >> 11;
  }
  
  // SuperFastHash switches K & 3 here, but we choose K to be a multiple of 4
  // and ensure that this isn't required.
  
  /* Force "avalanching" of final 127 bits */
  hash_f ^= hash_f << 3;
  hash_f += hash_f >> 5;
  hash_f ^= hash_f << 4;
  hash_f += hash_f >> 17;
  hash_f ^= hash_f << 25;
  hash_f += hash_f >> 6;

  hash_r ^= hash_r << 3;
  hash_r += hash_r >> 5;
  hash_r ^= hash_r << 4;
  hash_r += hash_r >> 17;
  hash_r ^= hash_r << 25;
  hash_r += hash_r >> 6;

  if (hash_f < hash_r) {
    return (uint64_t)hash_f << 32 | hash_r;
  } else {
    return (uint64_t)hash_r << 32 | hash_f;
  }
}

#endif // SUPER_FAST_HASH_H
