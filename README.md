# Count-Keeper: An Adversarially Robust Compact Frequency Estimator 

This repository contains implementation code and experimental artifacts related to the Count-Keeper data structure - an adversarially robust compact frequency estimator. 

The accompanying full paper text is available in `/paper/` (updated 2023-09-25). It is also available on [ePrint](https://eprint.iacr.org/2023/1366).

The conference proceedings version of the paper will appear at [ACM CCS '23](https://www.sigsac.org/ccs/CCS2023/). The ACM Reference format for our paper is below.

```
Sam A. Markelon, Mia Filić, and Thomas Shrimpton. 2023. 
Compact Frequency Estimators in Adversarial Environments. 
In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security (CCS ’23), November 26–30, 2023, Copenhagen, Denmark. 
ACM, New York, NY, USA, 15 pages. https://doi.org/10.1145/3576915.3623216
```


## Reference Implementation

A reference implementation of Count-Keeper (CK) written in C in available in `/ref`. It relies on [Sodium](https://doc.libsodium.org/) for keyed Blake2b hashing. 

There is a `test.c` file that explores how to use this reference implementation. A `Makefile` is included to build it. It requires updating pointers to the location of your libsodium install. 

## Adversarial CFE Experiment Artifacts

This directory contains artifacts used to produce the experimental results in the paper **Compact Frequency Estimators in Adversarial Environments**. All subdirectories correspond to an experiment in a specific section or subsection in the paper. Each subdirectory is self-contained in that you can run the particular experiment as is from within the directory. Moreover, the results that appear in the paper are presented in summary form as `.csv` files or as inline comments in the source code.

### CFE Implementations

We present the source code of the Python 3 implementations of CK, CMS, and HK in `/cfes`. We also have a common `Hasher` class that is used across all structures for row position hash functions and to produce fingerprints of elements for CK and HK. The implementation follow the description in Section 5.4 Results.

These implementations (or a slight modification to allow for added behaviors) are used in every experiment.

### Streams

In `/streams` we present each stream described in Section 5.4 Data Streams as `{stream_name}_stream.txt` as well as some data about the streams in each stream's subdirectory.

### Non-Adaptive Experiments

The code for non-adaptive experiments that appear in Section 5.4 of the paper are in `/test-cfes`. The results that appear in the paper are included in `/data/total_results.csv`.

To run the experiments and reproduce the results you can run the following from the `/experiments` directory.

```console
cd test-cfes/
cd data/
python3 create_data_dirs.py
cd ..
python3 run_experiments_standard.py
python3 run_experiments_constrained.py
cd data/
python3 analyze_data.py
```

A summary data file will be created. Be warned that we default to 1000 trials and the experiments will take a long time to run. 

### Attack Experiments

The attack comparison experiments that appear in Section 5.5 of that paper are in `/attacks`. The results that appear in the paper are summarized as inline comments at the end of the `public_public.py` and `/private_private.py` files.

To run the attack experiments and reproduce the results you can run the following from the `/experiments` directory.

```console
cd attacks/
python3 public_public.py
python3 private_private.py 
```

Results will be printed to `stdout`.

### CK Robustness Experiments

The experiments that showcase CK flag raising that appear in Section 5.6 of the paper are in `flag-ck/`. The adversarial flag raising results are summarized as an inline comment at the end of the `attack_experiments.py` file. The non-adversarial flag raising results are summarized in `/data/total_results.csv`.

To run the flag raising attack experiments and reproduce the results you can run the following from the `/experiments` directory.

```console
cd flag-ck/
python3 attack_experiments.py 
```

Results will be printed to `stdout`.

To run the flag raising non-adversarial experiments and reproduce the results you can run the following from the `/experiments` root directory.

```console
cd flag-ck/
cd data/
python3 create_data_dirs.py
cd ..
python3 run_honest_experiments.py
cd data/
python3 analyze_data.py
```

A summary data file will be produced. The total flags raised over the 100 trials ran for each stream will be printed to `stdout`.