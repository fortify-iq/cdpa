# Copyright © 2022 FortifyIQ, Inc. All rights reserved. 
#
# This program, cdpa, is free software: you can redistribute it and/or modify
# it under the terms and conditions of FortifyIQ’s free use license (”License”)
# which is located at
# https://raw.githubusercontent.com/fortify-iq/cdpa/master/LICENSE.
# This license governs use of the accompanying software. If you use the
# software, you accept this license. If you do not accept the license, do not
# use the software.
#
# The License permits non-commercial use, but does not permit commercial use or
# resale. This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY OR RIGHT TO ECONOMIC DAMAGES; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# If you have any questions regarding the software of the license, please
# contact kreimer@fortifyiq.com

import warnings
import argparse

from cdpa_end_to_end import end_to_end_attack


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b',
        '--bit-count',
        type=int,
        choices=range(1, 65),
        default=32,
        help='Number of bits in the secret numbers (32 by default)',
    )
    parser.add_argument(
        '-s',
        '--share-count',
        type=int,
        default=1,
        help='Number of shares (1 by default)',
    )
    parser.add_argument(
        '-t',
        '--trace-count',
        type=int,
        default=100000,
        help='Number of traces to acquire for the attack (100K by default)',
    )
    parser.add_argument(
        '-n',
        '--noise',
        type=float,
        help='Standard deviation of the normally distributed noise '
        'added to the trace (0 by default)',
    )
    parser.add_argument(
        '-e',
        '--experiment-count',
        type=int,
        default=1,
        help='The number of experiments to perform (1 by default)',
    )
    parser.add_argument(
        '-r',
        '--random-seed',
        type=int,
        help='A random seed for the secret generation (None by default)',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Provide detailed printout',
    )
    parser.add_argument(
        '-l',
        '--list-of-traces',
        action='store_true',
        help='Print the list of traces',
    )

    args = parser.parse_args()
    args.verbose |= args.list_of_traces
    assert not args.verbose or args.experiment_count == 1, \
        '"-v" and "-l" are permitted only if the experiment count is 1 ("-e 1" or default)'

    return (
        args.trace_count,
        args.bit_count,
        args.share_count,
        args.experiment_count,
        args.random_seed,
        args.noise,
        args.verbose,
        args.list_of_traces,
    )


if __name__ == '__main__':
    # Parse the command line
    (
        trace_count,
        bit_count,
        share_count,
        experiment_count,
        seed,
        noise,
        verbose,
        list_traces,
    ) = parse()
    # Suppress expected overflows in addition and subtraction
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    result_ratio, lsb_success_ratio, bit_success_ratio = end_to_end_attack(
        trace_count, bit_count, share_count, experiment_count, seed, noise, verbose, list_traces
    )
    if not verbose:
        print('{:5.2f}% correct answers'.format(result_ratio))
        print('{:5.2f}% correct least significant bits'.format(lsb_success_ratio))
        print('{:5.2f}% correct bits'.format(bit_success_ratio))
