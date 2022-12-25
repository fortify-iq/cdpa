# Copyright © 2022-present FortifyIQ, Inc. All rights reserved. 
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

import numpy as np


def hd(x, y=0):
    m1 = 0x5555555555555555
    m2 = 0x3333333333333333
    m4 = 0x0f0f0f0f0f0f0f0f
    h01 = 0x0101010101010101
    t = x ^ y
    t -= (t >> 1) & m1
    t = (t & m2) + ((t >> 2) & m2)
    t = (t + (t >> 4)) & m4
    return ((t * h01) >> 56) & 0x7f


def generate_traces(trace_count, bit_count, share_count, noise, seed):
    mask = np.uint64((1 << bit_count) - 1)
    state = np.random.RandomState(seed)
    x, y = tuple(state.randint(1 << bit_count, size=2, dtype=np.uint64))
    data = state.randint(1 << bit_count, size=trace_count, dtype=np.uint64)
    delta_y = (x + data) & mask
    y_array = np.full(trace_count, y)
    x_shares = state.randint(1 << bit_count, size=(share_count - 1, trace_count), dtype=np.uint64)
    y_shares = state.randint(1 << bit_count, size=(share_count - 1, trace_count), dtype=np.uint64)
    traces = np.zeros(trace_count, dtype=np.uint64)
    for i in range(share_count - 1):
        traces += hd(x_shares[i], y_shares[i])
        delta_y ^= x_shares[i]
        y_array ^= y_shares[i]
    traces += hd(delta_y, y_array)
    if noise:
        traces = traces.astype(float)
        traces += np.random.normal(scale=noise, size=trace_count)

    return data, traces, int(x), int(y)
