#  Copyright © 2022-2023 [unidentified]
#
#  All Rights Reserved.

try:
    from termcolor import cprint
except ModuleNotFoundError:

    def cprint(x, y=None, z=None, **kwargs):
        print(x, **kwargs)


from cdpa_attack import cdpa_attack
from cdpa_trace_generation import generate_traces, hd


def end_to_end_attack(
    trace_count,
    bit_count,
    share_count,
    experiment_count,
    seed=None,
    noise=None,
    verbose=False,
    list_traces=False
):
    # Generate the traces
    result_success_count, lsb_success_count, bit_success_count, mask = (
        0,
        0,
        0,
        (1 << (bit_count - 1)) - 1
    )
    for _ in range(experiment_count):
        data, traces, x, y = generate_traces(trace_count, bit_count, share_count, noise, seed)
        if verbose:
            nibble_count = ((bit_count - 1) >> 2) + 1
            data_fmt = '{' + ':0{:d}x'.format(nibble_count) + '}'
            print('Secret values: X = ' + data_fmt.format(x) + ', Y = ' + data_fmt.format(y))
            print()
        res_x, res_y = cdpa_attack(data, traces, bit_count, share_count, verbose, list_traces)
        x_dif, y_dif = x ^ res_x, y ^ res_y
        highest_bit_match = ((x_dif ^ y_dif) >> (bit_count - 1)) == 0
        x_match_count = bit_count - 1 - hd(x_dif & mask)
        y_match_count = bit_count - 1 - hd(y_dif & mask)
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
        data_fmt = '{' + ':0{:d}x'.format(nibble_count) + '}'
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
