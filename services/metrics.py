def efficiency(std_total, actual_avg):
    return (std_total / actual_avg) * 100


def bottleneck(eff_df, processes):
    avg = eff_df[processes].mean()
    return avg.idxmin(), avg.min()


def worst_product(eff_df, processes):
    return eff_df.set_index("SP")[processes].mean(axis=1).idxmin()
