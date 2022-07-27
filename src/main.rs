use std::collections::hash_map::DefaultHasher;
use std::env;
use std::hash::Hasher;
use std::io;
use std::io::Read;

const K: usize = 40;

#[derive(PartialEq)]
enum FastQState {
    Initial,
    GotAt,
    InSeq,
}

fn complement(b: u8) -> u8 {
    match b {
        b'A' => b'T',
        b'C' => b'G',
        b'G' => b'C',
        b'T' => b'A',
        _ => b' ',
    }
}

fn canonicalize_kmer<'a>(kmer_a: &'a [u8], kmer_b: &'a [u8]) -> &'a [u8] {
    for i in 0..K {
        if kmer_a[i] < kmer_b[i] {
            return kmer_a;
        } else if kmer_a[i] > kmer_b[i] {
            return kmer_b;
        }
    }
    kmer_a
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        print!("Usage: $0 N_BUCKETS");
        std::process::exit(1);
    }
    let n_buckets = args[1].parse::<usize>().unwrap();

    let mut state = FastQState::Initial;

    let mut kmer: [u8; K] = [0; K];
    let mut kmer_rc: [u8; K] = [0; K];
    let mut seq_idx = 0;

    let mut buckets: Vec<i32> = Vec::with_capacity(n_buckets);
    for _ in 0..n_buckets {
        buckets.push(0);
    }

    for b in io::stdin().lock().bytes() {
        let b = b.unwrap();

        if state == FastQState::InSeq && b != b'\n' && b != b'+' {
            if seq_idx < K {
                kmer[seq_idx] = b;
            } else {
                for i in 1..K {
                    kmer[i - 1] = kmer[i];
                }
                kmer[K - 1] = b;
                for i in 0..K {
                    kmer_rc[i] = complement(kmer[K - 1 - i]);
                }

                let canonical_kmer = canonicalize_kmer(&kmer, &kmer_rc);

                let mut hasher = DefaultHasher::new();
                hasher.write(&canonical_kmer);
                let hash = hasher.finish();
                let bucket = (hash % (n_buckets as u64)) as usize;
                buckets[bucket] = buckets[bucket].saturating_add(1);
            }

            seq_idx += 1;
        }

        match state {
            FastQState::Initial => {
                if b == b'@' {
                    state = FastQState::GotAt;
                }
            }

            FastQState::GotAt => {
                if b == b'\n' {
                    state = FastQState::InSeq;
                    seq_idx = 0;
                }
            }

            FastQState::InSeq => {
                if b == b'+' {
                    state = FastQState::Initial;
                }
            }
        }
    }

    for val in buckets {
        print!("{}\n", val);
    }
}
