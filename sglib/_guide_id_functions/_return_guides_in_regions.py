
# _return_guides_in_regions.py

__module_name__ = "_return_guides_in_regions.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


# package imports #
# --------------- #
import pandas as pd
import regex
import seq_toolkit


def _id_PAMs_in_sequence(sequence, PAM, motif_key="pam", verbose=True):

    PAM_df = seq_toolkit.query_motif(sequence, PAM, motif_key, verbose)
    return PAM_df


def _build_region_interval_idx(df, region_extension):

    RegionIntervals = []

    for i in range(len(df)):
        start = int(df.filter(regex="tart").iloc[i].values[0]) - region_extension
        end = int(df.filter(regex="nd").iloc[i].values[0]) + region_extension
        RegionIntervals.append(pd.Interval(left=start, right=end, closed="right"))

    return pd.IntervalIndex(RegionIntervals)


def _return_guides_in_regions(
    sequence,
    df,
    region_column=False,
    region_specification=False,
    PAM="NGG",
    global_start=0,
    region_extension=0,
):

    """"""
    
    if region_column:
        region_df = df.loc[df[region_column] == region_specification].reset_index(drop=True)
    else:
        region_df = df
                
    pam_df = _id_PAMs_in_sequence(sequence, PAM, motif_key="pam", verbose=True)

    region_df["range"] = ranges = _build_region_interval_idx(
        region_df, region_extension
    )
    pam_df['pam.start'] += global_start
    pam_df['pam.end'] += global_start
        
    pam_df["range"] = pd.cut(x=pam_df["pam.start"].values, bins=ranges)
    target_region_df = pd.merge(region_df, pam_df, on="range").drop("range", axis=1)

    return target_region_df