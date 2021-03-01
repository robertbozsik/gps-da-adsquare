import pandas as pd


def list_from_affinities(aff_name: str) -> list:
    """Return a list created from the given user_affinity csv file"""
    aff_name = pd.read_csv(
        f"../assignment_data/affinities/{aff_name}.csv", header=None, names=[aff_name])
    aff_name = list(aff_name.iloc[:, 0])  # all rows, first column
    return aff_name
