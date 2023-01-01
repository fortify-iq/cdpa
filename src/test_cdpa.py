#  Copyright © 2022 FortifyIQ, Inc.
#
#  All Rights Reserved.
#
#  All information contained herein is, and remains, the property of FortifyIQ, Inc.
#  Dissemination of this information or reproduction of this material, in any medium,
#  is strictly forbidden unless prior written permission is obtained from FortifyIQ, Inc.

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
        help='The number of bits in the secret numbers',
    )
    parser.add_argument(
        '-s',
        '--share-count',
        type=int,
        default=1,
        help='The number of shares',
    )
    parser.add_argument(
        '-t',
        '--trace-count',
        type=int,
        default=100000,
        help='The number of traces to acquire for the attack',
    )
    parser.add_argument(
        '-n',
        '--noise',
        type=float,
        help='The standard deviation of normally distributed noise',
    )
    parser.add_argument(
        '-e',
        '--experiment-count',
        type=int,
        default=1,
        help='The number of experiments to perform',
    )
    parser.add_argument(
        '-r',
        '--random-seed',
        type=int,
        help='A random seed for the secret generation',
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
    result_ratio, lsb_success_ratio, bit_success_ratio = end_to_end_attack(
        trace_count, bit_count, share_count, experiment_count, seed, noise, verbose, list_traces
    )
