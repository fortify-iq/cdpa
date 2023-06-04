# CDPA Simulator

The CDPA is an attack on a device which performs k-bit arithmetical addition X+W, with the result of the addition replacing Y, where X and Y are k-bit secret values, and W is a known pseudo-random k-bit input. Both X+W and Y are represented as an XOR of n shares. The leakage model assumes that the leaked value is a sum (1) of the Hamming distance between the kn bits of the representation of X+W and the kn bits of the representation of Y and (2) of normally distributed noise. The attack is successful if it correctly recovers (1) the k-1 least significant bits of both X and Y and (2) the XOR of their most significant bits. (The best possible result is finding their XOR, because a simultaneous flip of the most significant bits of X and Y does not affect the Hamming distance between them.)

The repository contains two directories:

* `src` - Python code implementing the attack
* `docs` - An Excel spreadsheets with statistical data

Directory `src` contains the following files:

* `cdpa_trace_generation.py` - generates traces for the CDPA attack
* `cdpa_attack.py` - mounts the CDPA attack of an arbitrary order
* `cdpa_end_to_end.py` - calls the traces generation function from `cdpa_trace_generation.py`, calls the attack function from `cdpa_attack.py`, and evaluates the result
* `test_cdpa_attack.py` - command line utility which performs the CDPA in a loop using `cdpa_end_to_end.py` and collects statistics

## Usage of `test_cdpa_attack.py`

`test_cdpa_attack.py [-h] [-b BIT_COUNT ] [-s SHARE_COUNT] [-t TRACE_COUNT] [-n NOISE] [-e EXPERIMENT_COUNT] [-r RANDOM_SEED] [-v] [-l]`

- `-h` - Help.
- `-b` - Bit size of the secrets (1-64). Default value 32.
- `-s` - Number of shares. Default value 1.
- `-t` - Number of traces in one experiment. Default value 100K.
- `-n` - Amplitude of normally distributed noise added to the traces. By default no noise (= amplitude 0).
- `-e` - Number of experiments. Default value 1.
- `-r` - Random seed (by default `None`). If no random seed is provided, the experiments are not reproducible, since each time different random values are used. If a random seed is provided, the experiments are reproducible, and the same command line always produces the same result.
- `-v` - Verbose. Permissible only if the number of experiments is 1 (which is the default). Outputs a summary of the rounds corresponding to bits 0-7 (or less if the bit size is less than 8).
- `-l` - Long printout. Permissible only if the number of experiments is 1 (which is the default). Outputs the same summary as with `-v` (so it is not required to use `-v` when `-l` is used), prepended by several lines, a line per trace, with more detailed information about each trace.

## Environment requirements

* Python of version `>= 3.8`.

## Installation of Dependencies

The codebase of the attack has a few dependencies.

The simplest way to install them is by using the [pip](https://pip.pypa.io/en/stable/) package manager.
The list of dependencies is contained within the `requirements.txt` file.

To install dependencies run `pip install` command:

```bash
python -m pip install -r requirements.txt
```

For more details on installation refer to pip [user guide](https://pip.pypa.io/en/stable/user_guide/#requirements-files).

Note that in case of unmet [environment requirements](#environment-requirements) the ignorance meassage is shown after running the command above. Appropriate version of Python interpreter should be installed to fix the problem.
