# Compact Frequency Estimators in Adversarial Environments CCS '23 Artifacts Evaluation 

This repository contains code and experimental artifacts related to the [ACM CCS '23](https://www.sigsac.org/ccs/CCS2023/) paper titled **Compact Frequency Estimators in Adversarial Environments.** The ACM Reference format for our paper is below.

```
Sam A. Markelon, Mia Filić, and Thomas Shrimpton. 2023. 
Compact Frequency Estimators in Adversarial Environments. 
In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security (CCS ’23), November 26–30, 2023, Copenhagen, Denmark. 
ACM, New York, NY, USA, 15 pages. https://doi.org/10.1145/3576915.3623216
```

## Adversarial CFE Experiment Artifacts

This directory contains artifacts used to produce the experimental results in the paper **Compact Frequency Estimators in Adversarial Environments**. All subdirectories in the `experiments` directory correspond to an experiment in a specific section or subsection in the paper. Each subdirectory is self-contained in that you can run the particular experiment as is from within the directory. The steps for running experiments and reproducing results are outlined below. The data produced from these experiments that appear as results in the paper are presented in summary form as `.csv` files or as inline comments in the source code in each directory. 

The only requirement to run these experiments is to be able to run Python scripts from a terminal. We used Python 3.9.7, but in theory any Python version 3.6+ should suffice. The terminal commands we provide are in a *nix like syntax, but should also work in PowerShell if tested on Windows (with perhaps some slight syntactic differences). We provide an estimate the compute time for each experiment. We ran these experiments on an Apple M1 machine with 16GB of RAM. Compute times may vary slightly depending on hardware, but specialized or high performance computing machinery is not required. 

To install simply clone the GitHub repository at the artifact tag and install the necessary dependencies using pip. This should take less than 5 minutes of human time (depending on internet speed.)

```console
git clone https://github.com/smarky7CD/cfe-in-adv-envs.git

pip3 install numpy
pip3 install matplotlib
cd cfe-in-adv-envs
git checkout tags/AE -b CCS23-AE
```

As a basic test one can run the following and expect to see the following output. This takes about 10 seconds of compute time. 

```
cd cfes/
python3 test.py
```

Expected output:

```console
CK test qry is (1, 'cntUBx = cntLBx')
CMS test qry is 1
HK test qry is 1
```

In addition, an image scatter plot should pop up on one's display to ensure the `numpy` and `matplotlib` are installed and functioning correctly. One can simply close the window after it appears. 


### CFE Implementations

We present the source code of the Python 3 implementations of Count-Keeper (CK), Count-min Sketch (CMS), and HeavyKeeper (HK) in `/cfes`. The implementations are functionally one to one with their respective presentations in the paper (Figure 5, Figure 2, and Figure 3). The built-in Python `__init__` function acts as `REP` and all structures have a method called `qry(x)` and `up(x)` equivalent to their functional definitions in the paper. We also have a common `Hasher` class that is used across all structures for computing row position hash functions and to produce fingerprints of elements for CK and HK. The `Hasher` classes uses the BLAKE2b cryptographic hash function as described in Section 6.4 of our paper. 

These implementations (or a slight modification of them to allow for added behaviors) are used in every experiment. Note that these implementations are not tuned for performance, but rather ease of collecting data concerning correctness and behavior under adversarial conditions of these structures.. 

### Quick Functionality Test

### Streams

In `/streams` we present each stream described in Section 6.4 Data Streams as `{stream_name}/{stream_name}_stream.txt`. Each stream's subdirectory `{stream_name}` also contains a `{stream_name}_stream_size.txt` file and a `{stream_name}_stream_info.csv` file. The `{stream_name}_stream_size.txt` file contains the domain size and total stream length of each stream. The `{stream_name}_stream_info.csv` file is a two-column `.csv` file containing the item ID and its corresponding frequency ordered from least frequent to most frequent. These file was produced by running `/stream_info.py` in the `/streams` directory. The domain size and total stream length is output to `stdout` when this script is run. This will take about 30 seconds of compute time. 

The `kosorak` stream and `retail` stream subdirectory contain a `{stream_name}_unprocessed.txt` file. These are the original anonymized data collections from [the frequent item mining dataset repository](http://fimi.uantwerpen.be/data/). To get the `{stream_name}_stream.txt` that we use in our experiments we simply flatten this raw data such that there is one entry per line and randomize the order. This can be reproduced by running the script `process_stream.py` in the `/streams` directory. It will output a `test_kosorak_stream.txt` and a `test_retail_stream.txt` in their respective subdirectories. We append `test` to the output to avoid overwriting the original stream files. This will take about 30 seconds of compute time. 

The `novel` stream was created by processing the individual words in sequential order of the Project Gutenburg eBook plaintext edition of 1851 English-language novel [Moby-Dick; or, The Whale](https://www.gutenberg.org/cache/epub/2701/pg2701.txt) by Herman Melville. We map words to integers corresponding to their frequency rank - this mapping and more stream info can be seen in `novel_stream_verbose.csv` file in the `novel` subdirectory. 

We also provide code to reproduce the plots in Figure 6 in `/streams/stream_plots.` The code produces plots that map the top 35% probability mass of each stream using the `{stream_name}_stream_info.csv` files. To run requires the [numpy](https://pypi.org/project/numpy/) package and the [matplotlib](https://pypi.org/project/matplotlib/).

To install these packages (if not already done in the setup instructions) and run the script, the following can be executed in the `\stream_plots` subdirectory.

```console
pip3 install numpy
pip3 install matplotlib
python3 stream_plots.py
```

This takes about 30 seconds of compute time. The plots that appear in Figure 6 in Section 6.4 will be output in the newly created `stream_plots/plots` subdirectory. The probability mass that is plotted can be changed by altering the `percents` variable on line 32 of the `stream_plots.py#L32` file. 

### Honest Setting Performance Experiments

The code for honest setting performance experiments that appear in Table 1 in Section 6.4 of the paper are in `experiments/test-cfes`. The data file for the results that appear in the paper are included in `/data/papaer_results.csv`. This experiment is randomized on each trial on the particular choice of hash functions used for each structure and the order in which the stream is processed. Therefore, the exact results that appear in the paper will not be reproduced, but they will be close on an average over all the trials. 

We ran 1000 trials for each structure, stream, and parameter triplet for the results that appear in the paper. Due to the high overhead of memory accesses to retrieve the stream items, update the structures, and write out the data this took about 2 days of compute on a high performance machine. Therefore, for the artifacts review we change this 50 to trials for each triplet. This takes about 8 hours of compute on a laptop. This change will potentially introduce more variability in the results.

To run the experiments and summarize the results you can run the following from the `/experiments` directory.

```console
cd test-cfes/
python3 run_experiments.py
cd data/
python3 analyze_data.py
```

First a directory for each `{structure}_{parameter}_{stream}` triplet is created in the `\data` subdirectory. A per trial data `{trial_num}.csv` file is created in each of these subdirectories as a trial is completed. It logs the `Item ,True Frequency, Estimated Frequency, Absolute Error,Percent Error` for each item in the stream for a given structure and selection of parameters. While running `Stream {stream_name}, Trial {trial_number}` will be output to `stdout`. For the artifact review experiment setup this will go through the three streams up to trial 50 twice - as we have a standard parameter set and a constrained parameter set. 

After the experiment is finished running, we go to the `\data` subdirectory and run the `analyze_data.py` script. This outputs the analysis results to `stdout` and creates a summary file of our results averaged over the trials for each triplet. It is output as `total_results.csv`. This takes about 30 seconds of human time and 1 minute of compute time. 

The headers of `total_results.csv` are `structure,params,stream,avg heavy_match,avg jaccard_i,avg minimal_l,perecent_err` which correspond to the structure, parameters of the structure, the stream, the SIS, the Jaccard Index, the MCT, and the ARE as described in Section 6.4 of our paper. Matching the reported results in Table 1 and those produced by running the experiment shows a tight agreement. 

### Attack Experiments

The attack comparison experiments that appear in Table Section 6.5 of that paper are in `/experiments/attacks`. The attacks we implement and test are one to one with those described in sections 5.2, 5.3, and 6.5 of our paper. The results that appear in the paper are given as inline comments at the end of the `public_public.py` and `/private_private.py` files.

To run the attack experiments and reproduce the results you can run the following from the `/experiments` directory.

```console
cd attacks/
python3 public_public.py
python3 private_private.py 
```

Results will be printed to `stdout` after each script is run. 100 trials are performed for each structure and parameter pairing listed in the table. We report the average over these 100 trials for each pairing. The `public_public.py` attack takes about 200 minutes of compute time and the `private_private.py` takes about 220 minutes of compute time. 

The output looks like the below.

```console
private, private: q_U=2^20, trials=100
CMS: m=2048,k=4
Avg |I|, Avg rs. ins., Avg Q, Avg |C|, Avg Err
4189.98, 18768.62, 11808.56, 3.99, 260936.17
CMS m=4096, k=8
Avg |I|, Avg rs. ins., Avg Q, Avg |C|, Avg Err
11431.88, 33566.96, 33503.45, 8.0, 126894.19
.
.
.
```
The first line shows the attack setting (either public hash or private hash and private representation), the query budget, and the number of trials per structure and parameter pairing. Then each structure parameter pairing is printed along with the following statistics `Avg q_H, Avg |I|, Avg |C|, Avg Err` (in the public hash case) or `Avg |I|, Avg rs. ins., Avg Q, Avg |C|, Avg Err` (in the private hash case).  `q_H` corresponds to the number of offline hash computations in the public case. `|I|` is the size of the initial insertions to find a cover (or items that were hashed offline in the public hash case). `rs. ins.` are the total number of insertions to find and minimize the cover set before insertions are solely used to accumulate error in the private case. `Q` is the number of queries made in the private hash case. `|C|` is the size of the cover set the is found, and `Err` is the error produced according to our attack model in Figure of our paper. 

 Matching the reported results in Table 2 and those produced by running the experiment shows a tight agreement. Moreover, the data backs our claim that the attacks against CK generate about half the amount of error as opposed to the CMS attacks, and about `q_U - q_U/2k` less the amount of error as opposed to the HK attacks for an adversary with a fixed amount of resources. 

### CK Robustness Experiments

The experiments that showcase the CK flag raising ability that appear in the text of Section 6.6 of the paper are in `/experiments/flag-ck/`. The adversarial flag raising results are summarized as an inline comment at the end of the `attack_experiments.py` file. The non-adversarial flag raising results that appear in the paper are available in `/flag-ck/data/paper_results.csv`.

To run the flag raising attack experiments and reproduce the results you can run the following from the `/experiments` directory.

```console
cd flag-ck/
python3 attack_experiments.py 
```

100 trials are run the results are reported as an average over those trials. The compute time for this experiment takes about 2 minutes. Results will be printed to `stdout`.

The output of the below form.

```console
Trial 0
.
.
.
Trial 98
9536, 2384, 8, 8192, 1, 0
Trial 99
4016, 1004, 8, 8192, 1, 0


Avg q_H, Avg |I|, Avg |C|, Avg Err, x Flags Raised, Cover Flags Raised
13727.8, 3431.95, 8.0, 8192.0, 1.0, 0.0
```

The summary line averages the results across the trials. Looking at the `x Flags Raised = 1.0` tells us that a flag was raised on every target element, and the `Cover Flags Raised = 0.0` tells us that no flags were raised on any of the cover elements (as expected). This corresponds to the claims in our paper in section 6.6 about being able to flag suspicious estimates while keeping false positives low. 

To run the flag raising non-adversarial experiments and reproduce the results you can run the following from the `/experiments` root directory. This will take about 5 compute hours to run the experiment and about 2 minutes of compute to analyze the data. 

```console
cd flag-ck/
python3 run_honest_experiments.py
cd data/
python3 analyze_data.py
```

A summary data file called `total_results.csv` in the `data` subdirectory will be produced with the same information as the honest setting experiments. The total flags raised over the 100 trials ran for each stream will be printed to `stdout` (which is the data we care about). The output is of the form below.

```console
.
.
.
ck 1024x4 novel


Total Flags Raised...novel : 1
ck 1024x4 kosarak


Total Flags Raised...kosarak : 0
ck 1024x4 retail

```

This data shows that false positive flags are very rare per the claim in Section 6.6