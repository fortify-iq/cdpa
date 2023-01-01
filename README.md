# CDPA Simulator

The CDPA is an attack on a device which performs k-bit arithmetical addition X+W, with the result of the addition replacing Y, where X and Y are k-bit secret values, and W is a known pseudo-random k-bit input. Both X+W and Y are represented as an XOR of n shares. The leakage model assumes that the leaked value is a sum (1) of the Hamming distance between the kn bits of the representation of X+W and the kn bits of the representation of Y and (2) of normally distributed noise. The attack is successful if it correctly recovers (1) the k-1 least significant bits of both X and Y and (2) the XOR of their most significant bits. (The best possible result is finding their XOR, because a simultaneous flip of the most significant bits of X and Y does not affect the Hamming distance between them.)

The repository contains two directories:
* `src` - Python code implementing the attack
* `docs` - Excel spreadsheets with statistical data produced by script `src/cdpa_stats.py`

Directory `src` contains the following files:

* `cdpa_trace_generation.py` - generator of traces for the CDPA attack
* `cdpa_attack.py` - the CDPA attack
* `TestCdpaAttack.py` - command line utility which generates traces using `CdpaTraceGeneration.py` and attacks them using `CdpaAttack.py`

Usage:
`TestCdpaAttack.py [-h] [-b BIT_COUNT ] [-s SHARE_COUNT] [-t TRACE_COUNT] [-n NOISE] [-e EXPERIMENT_COUNT] [-r RANDOM_SEED] [-v] [-l]`

- `-h` - Help.
- `-b` - Bit size of the secrets (1-64). Default value 32.
- `-s` - Number of shares. Default value 1.
- `-t` - Number of traces in one experiment. Default value 100K.
- `-n` - Amplitude of normally distributed noise added to the traces. 
- `-e` - Number of experiments. Default value 1.
- `-r` - Random seed (by default `None`). If no random seed is provided, the experiments are not reproducible, since each time different random values are used. If a random seed is provided, the experiments are reproducible, and the same command line always produces the same result.
- `-v` - Verbose. Permissible only if the number of experiments is 1 (which is the default). Outputs a summary of the rounds corresponding to bits 0-7 (or less if the bit size is less than 8).

- `-l` - Long printout. Permissible only if the number of experiments is 1 (which is the default). Outputs the same summary as with `-v` (so it is not required to use `-v` when `-l` is used), plus a line per trace with more detailed information about each trace.
