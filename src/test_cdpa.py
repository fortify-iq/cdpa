#  Copyright © 2022 FortifyIQ, Inc.
#
#  All Rights Reserved.
#
#  All information contained herein is, and remains, the property of FortifyIQ, Inc.
#  Dissemination of this information or reproduction of this material, in any medium,
#  is strictly forbidden unless prior written permission is obtained from FortifyIQ, Inc.

import warnings
import argparse

from termcolor import cprint

from cdpa_attack import cdpa_attack
from cdpa_trace_generation import generate_traces


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


def simulate(
    trace_count,
    bit_count,
    share_count,
    experiment_count,
    seed=None,
    noise=None,
    verbose=False,
    list_traces=False,
):
    result_success_count, lsb_success_count, bit_success_count, mask = (
        0,
        0,
        0,
        (1 << (bit_count - 1)) - 1
    )
    for _ in range(experiment_count):
        # Generate the traces
        data, traces, x, y = generate_traces(trace_count, bit_count, share_count, noise, seed)
        if verbose:
            nibble_count = ((bit_count - 1) >> 2) + 1
            data_fmt = '{{:0{:d}x}}'.format(nibble_count)
            print('Secret values: X = ' + data_fmt.format(x) + ', Y = ' + data_fmt.format(y))
            print()
        res_x, res_y = cdpa_attack(data, traces, bit_count, share_count, verbose, list_traces)
        x_dif, y_dif = x ^ res_x, y ^ res_y
        highest_bit_match = ((x_dif ^ y_dif) >> (bit_count - 1)) == 0
        x_match_count = bit_count - 1 - (x_dif & mask).bit_count()
        y_match_count = bit_count - 1 - (y_dif & mask).bit_count()
        success = (
            highest_bit_match and x_match_count == bit_count - 1 and y_match_count == bit_count - 1
        )
        result_success_count += success
        bit_success_count += highest_bit_match + x_match_count + y_match_count
        if success:
            lsb_success_count += bit_count
        else:
            while x_dif & 1 == 0 and y_dif & 1 == 0:
                x_dif >>= 1
                y_dif >>= 1
                lsb_success_count += 1

    if verbose:
        nibble_count = ((bit_count - 1) >> 2) + 1
        data_fmt = '{{:0{:d}x}}'.format(nibble_count)
        print()
        print('Secret    values: X = ' + data_fmt.format(x) + ', Y = ' + data_fmt.format(y))
        print(
            'Recovered values: X = ' + data_fmt.format(res_x) + ', Y = ' + data_fmt.format(res_y)
        )
        cprint('Success' if success else 'Failure', 'green' if success else 'red')

    return (
        result_success_count / experiment_count * 100,
        lsb_success_count / experiment_count / bit_count * 100,
        bit_success_count / experiment_count / (2 * bit_count - 1) * 100
    )


if __name__ == '__main__':
    warnings.filterwarnings('ignore', category=RuntimeWarning)
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
    result_ratio, lsb_success_ratio, bit_success_ratio = simulate(
        trace_count, bit_count, share_count, experiment_count, seed, noise, verbose, list_traces
    )
    if not verbose:
        print('{:5.2f}% correct answers'.format(result_ratio))
        print('{:5.2f}% correct least significant bits'.format(lsb_success_ratio))
        print('{:5.2f}% correct bits'.format(bit_success_ratio))
