#  Copyright © 2022 FortifyIQ, Inc.
#
#  All Rights Reserved.
#
#  All information contained herein is, and remains, the property of FortifyIQ, Inc.
#  Dissemination of this information or reproduction of this material, in any medium,
#  is strictly forbidden unless prior written permission is obtained from FortifyIQ, Inc.

import numpy as np
from scipy.stats import moment
from termcolor import cprint


def cdpa_attack(data, traces, bit_count, share_count, verbose, list_traces):
    """CDPA attack on a pair of secrets X, Y.
    Parameters:
        data - array of input words W[i]
        traces - array of side channel leakage values, corresponding to the input words.
            Each side leakage value is the Hamming distance between X+W[i] and Y, where
            both X+W[i] and Y are randomly represented as an XOR of several shares.
            A normally distributed noise may be optionally added to this Hamming distance.
        bit_count - the bit size of the secrets X, Y and of the input words W[i]
        share_count - the order of the moment to be used for the attack. It should
            match the number of shares used to generate the side channel leakage data.
        verbose - if True, outputs a short report of steps 0-7 of the attack. (The number
            of steps is limited in order to keep reasonable line lengths.)
        list_traces - if True, outputs a more detailed report, including the individual
            traces and splitting of the set of all traces into subsets at steps 0-7 of
            the attack.
    Returns recovered values of X and Y. The attack is considered successful if the XOR
    of the most significant bits of X and Y and all the remaining individual bits of both
    X and Y are guessed correctly.
    """

    # Step 0 (two subsets)
    traces_count = traces.shape[0]
    subsets = [data & 1 == i for i in range(2)]
    moments = [moment(traces[t], moment=share_count)
               if share_count > 1 else np.average(traces[t]) for t in subsets]
    moment_trace, leaps_trace = [moments], []
    # The guessed values. At step 0, guess x_0^y_0 and store it into y_0.
    # x is initialized with 0.
    x, y = 0, int((moments[0] < moments[1]) ^ (share_count & 1))

    # The remaining steps. i == step_index - 1
    for i in range(bit_count - 1):
        subsets = [((data + x) >> i) & 3 == j for j in range(4)]
        moments = [moment(traces[t], moment=share_count)
                   if share_count > 1 else np.average(traces[t]) for t in subsets]
        moment_trace.append(moments)
        leaps = (
            moments[0] - moments[1] - moments[2] + moments[3],
            moments[1] - moments[2] - moments[3] + moments[0],
        )
        leaps_trace.append(leaps)
        bit0 = int(abs(leaps[0]) > abs(leaps[1]))  # The position of the d2L maximal by absolute value
        bit1 = int((leaps[not bit0] < 0) ^ (share_count & 1))  # Its sign
        case = bit0 + (bit1 << 1)
        x ^= bit0 << i  # Store the guessed x_i
        y ^= case << i  # Correct y_i and store the guessed x_{i+1} ^ y_{i+1} into y_{i+1}

    if verbose or list_traces:
        nibble_count = ((bit_count - 1) >> 2) + 1
        data_fmt = '{{:0{:d}x}}'.format(nibble_count)
        space = ' ' * (nibble_count - 1) if list_traces else ' '
        if bit_count > 8:
            bit_count = 8
        print(space + ' ' * 7
              + '  '.join('Step {}'.format(i) for i in range(bit_count)))
        if list_traces:
            print(space + 'W   HD    W&1 '
                  + ' '.join('((W+{:2x})'.format(x & ((1 << i) - 1)) for i in range(bit_count - 1)))
            print(space + ' ' * 15
                  + '  '.join('>>{})&3'.format(i) for i in range(bit_count - 1)))
            for i in range(traces_count):
                print((data_fmt + '   {:2d}  ').format(data[i], traces[i]), end='')
                print('   M{}      '.format(int(data[i]) & 1), end='')
                print((' ' * 6).join('M{}'.format(
                    ((int(data[i]) + (x & ((1 << j) - 1))) >> j) & 3) for j in range(bit_count - 1)))
            print()
        for j in range(4):
            print('L(M{})   '.format(j) + space, end='')
            if j >= 2:
                print(' ' * 5, end='')
            else:
                print('{:5.2f}'.format(moment_trace[0][j]), end='')
            for i in range(1, bit_count):
                print('   {:5.2f}'.format(moment_trace[i][j]), end='')
            print()
        print()
        for j in range(2):
            print('dL(M{})  '.format(j) + space, end='')
            if j >= 1:
                print(' ' * 5, end='')
            else:
                dif = moment_trace[0][1] - moment_trace[0][0]
                cprint('{:5.2f}'.format(dif), 'white', 'on_blue' if dif > 0 else 'on_yellow', end='')
            for i in range(1, bit_count):
                print('   {:5.2f}'.format(moment_trace[i][j + 2] - moment_trace[i][j]), end='')
            print()
        print()
        for j in range(2):
            print('d2L(M{})      '.format(j) + space, end='')
            for i in range(0, bit_count - 1):
                cur = leaps_trace[i][j]
                print('   ', end='')
                if abs(cur) > abs(leaps_trace[i][1 - j]):
                    cprint('{:5.2f}'.format(cur),
                           'white', 'on_blue' if cur < 0 else 'on_yellow', end='')
                else:
                    print('{:5.2f}'.format(cur), end='')
            print()
        print()
        print('(X^Y)[i]    ' + space, end='')
        for i in range(0, bit_count):
            print('{}       '.format(((x ^ y) >> i) & 1), end='')
        print()
        print('X[i-1]              ' + space, end='')
        for i in range(1, bit_count):
            print('{}       '.format((x >> (i - 1)) & 1), end='')
        print()
        print()
        print('X[i-1:0]     ' + space, end='')
        for i in range(1, bit_count):
            formatter = '{:02x}' if i > 4 else '{:2x}'
            print('      ' + formatter.format(x & ((1 << i) - 1)), end='')
        print()
        print('Y[i-1:0]     ' + space, end='')
        for i in range(1, bit_count):
            formatter = '{:02x}' if i > 4 else '{:2x}'
            print('      ' + formatter.format(y & ((1 << i) - 1)), end='')
        print()

    # The most significant bit of x is always 0.
    # The most significant bit of y contains the guessed XOR of the most significant bits of x and y.
    return x, y
