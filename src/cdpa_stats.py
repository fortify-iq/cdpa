from datetime import datetime

from test_cdpa import simulate


if __name__ == '__main__':
    with (
        open('res.csv', 'wt') as f_res,
        open('lsb.csv', 'wt') as f_lsb,
        open('bit.csv', 'wt') as f_bit
    ):
        prev_time = datetime.now()
        header = ',,,' + ','.join(str(1 << i) for i in range(6, 21))
        f_res.write(header)
        f_lsb.write(header)
        f_bit.write(header)
        for bit_count in (32, 64):
            for share_count in range(1, 4):
                start = 6
                for noise in (0, 4, 8, 16, 32, 64, 128):
                    line_header = '\n{},{},{:3d},'.format(bit_count, share_count, noise)
                    f_res.write(line_header)
                    f_lsb.write(line_header)
                    f_bit.write(line_header)
                    for trace_count_exp in range(6, 21):
                        if trace_count_exp < start:
                            f_res.write(',')
                            f_lsb.write(',')
                            f_bit.write(',')
                            continue
                        experiment_count = 1 << (min((34 - trace_count_exp) >> 1, 10))
                        cur_time = datetime.now()
                        print(
                            '{}\n{} {:2d} {:4d} '.format(
                                cur_time - prev_time,
                                line_header,
                                trace_count_exp,
                                experiment_count
                            ),
                            end=''
                        )
                        prev_time = cur_time
                        trace_count = 1 << trace_count_exp
                        result_sucess_ratio, lsb_success_ratio, bit_success_ratio = simulate(
                            trace_count, bit_count, share_count, experiment_count, None, noise
                        )
                        if lsb_success_ratio < 2:
                            start += 1
                        f_res.write('{},'.format(result_sucess_ratio))
                        f_lsb.write('{},'.format(lsb_success_ratio))
                        f_bit.write('{},'.format(bit_success_ratio))
                        f_res.flush()
                        f_lsb.flush()
                        f_bit.flush()
                        if result_sucess_ratio > 99:
                            break
