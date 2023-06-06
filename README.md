# CDPA Simulator

The CDPA is an attack on a device which performs `k`-bit arithmetical addition `X+W`, with the result of the addition replacing `Y`, where `X` and `Y` are `k`-bit secret values, and `W` is a known pseudo-random `k`-bit input. Both `X+W` and `Y` are represented as an XOR of `n` shares. The leakage model assumes that the Hamming distance between the `kn` bits of the representation of `X+W` and the `kn` bits of the representation of `Y` leaks. Optionally, a normally distributed random noise is added. The attack is successful if it correctly recovers (1) the `k-1` least significant bits of both `X` and `Y` and (2) the XOR of their most significant bits. (The best possible result is finding the XOR of these bits, because a simultaneous flip of the most significant bits of `X` and `Y` does not affect the Hamming distance between them.)

The repository contains two folders:

* `src` - The Python code that implements the attack
* `results` - Statistical data produced using this code

Folder `src` contains the following files:

* `cdpa_trace_generation.py` - generates traces for the CDPA attack
* `cdpa_attack.py` - mounts the CDPA attack of an arbitrary order
* `cdpa_end_to_end.py` - calls the trace generation function from `cdpa_trace_generation.py`, calls the attack function from `cdpa_attack.py`, and evaluates the result
* `test_cdpa.py` - a command line utility which performs the CDPA in a loop using `cdpa_end_to_end.py` and collects statistics

Folder `results` contains the following files:

* `cdpa_stats.xlsx` - a Microsoft Excel file containing the metrics M<sub>1</sub>, M<sub>2</sub>, M<sub>3</sub> described in Section 2.3.5 of the CDPA paper measured for different configurations, and the graph based on this data shown in Figure 12 of the CDPA paper
* `res(M1).csv, lsb(M2).csv, bit(M3).csv` - the three sheets of `cdpa_stats.xlsx` exported to the `csv` text format

## Usage of `test_cdpa_attack.py`

`test_cdpa_attack.py [-h] [-b BIT_COUNT ] [-s SHARE_COUNT] [-t TRACE_COUNT] [-n NOISE] [-e EXPERIMENT_COUNT] [-r RANDOM_SEED] [-v] [-l]`

- `-h` - Help.
- `-b` - Bit size of the secrets (1-64). Default value 32.
- `-s` - Number of shares. Default value 1.
- `-t` - Number of traces in one experiment. Default value 100K.
- `-n` - Amplitude of normally distributed noise added to the traces. Default value 0 (no noise).
- `-e` - Number of experiments. Default value 1.
- `-r` - Random seed. If no random seed is provided, the experiments are not reproducible, since each time different random values are used. If a random seed is provided, the experiments are reproducible, and the same command line always produces the same result.
- `-v` - Verbose. Permissible only if the number of experiments is 1 (which is the default). Outputs a summary of the rounds corresponding to bits 0-7 (or less if the bit size is less than 8).
- `-l` - Long printout. Permissible only if the number of experiments is 1 (which is the default). Outputs the same summary as with `-v` (so it is not required to use `-v` when `-l` is used), prepended by several lines, a line per trace, with more detailed information about each trace.

The printout of `test_cdpa_attack.py` includes three lines:

```text
xx.xx% correct answers
yy.yy% correct least significant bits
zz.zz% correct bits
```

These three lines reflect the estimations of metrics M<sub>1</sub>, M<sub>2</sub>, M<sub>3</sub> described in Section 2.3.5 of the CDPA paper, based on the performed set of experiments. When option `-l` or `-v` is used, additional lines are printed. They are described in detail in Section 2.3.6 of the CDPA paper.

## Reproducing the Results from the CDPA Paper

In order to exactly reproduce Figure 3 (the toy example), use the following command line:

```bash
python.exe ./test_cdpa_attack.py -b 8 -t 24 -r 55 -l
```

In order to exactly reproduce Figure 4 (successful CDPA with 100K traces), use the following command line:

```bash
python.exe ./test_cdpa_attack.py -b 64 -t 100000 -r 3 -v
```

Table 1 is based on the data in file `results/cdpa_stats.xlsx`, sheet `res(M1)`. For example, the upper left entry (2<sup>9</sup> for 32 bits, first order, noise 0) reflects the fact that the first entry in row 3 of this sheet (32 bits, first order, noise 0) which is greater that 50% is in cell G3, corresponding to 512=2<sup>9</sup> traces.

All the values in `results/cdpa_stats.xlsx` can be reproduced using `test_cdpa_attack.py`. For example, in order to reproduce cell G3 in all three sheets of `results/cdpa_stats.xlsx`, use, e.g., the following command line:

```bash
python.exe ./test_cdpa_attack.py -b 32 -s 1 -n 0 -t 512 -e 1000
```

The number of experiments (parameter `-e`) can be chosen arbitrarily, taking into account that both the precision and the run time increase as the number of experiments increases. The results may slightly deviate from the data in `results/cdpa_stats.xlsx`, since the metrics are estimated on a randomly chosen finite set of experiments.

## Environment Requirements

* Python of version `>= 3.8`.

## Installation of Dependencies

The codebase of the attack has a few dependencies.

The simplest way to install them is by using the [pip](https://pip.pypa.io/en/stable/) package manager.
The list of dependencies is contained within the `requirements.txt` file.

To install the dependencies run the `pip install` command:

```bash
python -m pip install -r requirements.txt
```

For more details on installation refer to the `pip` [user guide](https://pip.pypa.io/en/stable/user_guide/#requirements-files).

Note that in case of unmet [environment requirements](#environment-requirements) an error message will appear after running the command above, and the dependencies will not be installed. An appropriate version of a Python interpreter should be installed to fix the problem.
