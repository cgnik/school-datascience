import os
from argparse import ArgumentParser
from enum import Enum, auto
import pandas as pd


class ElectionType(Enum):
    SPECIAL = auto()
    PRIMARY = auto()
    GENERAL = auto()


def sample_file(file):
    file_parts = os.path.splitext(file)
    return f"{file_parts[0]}_sample{os.path.extsep}{file_parts[1]}"


def sample(file_name: str, sample_size=10000):
    sample_file_name = sample_file(file_name)
    if os.path.exists(sample_file_name):
        return pd.read_csv(sample_file_name)
    full = pd.read_csv(file_name, compression='gzip', encoding='ISO-8859-1')
    samp = full.sample(n=sample_size)
    samp.to_csv(sample_file_name)
    return samp


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('vote_file')
    args = parser.parse_args()

    cm = lambda x: lambda y: y.startswith(x)  # find matching column names
    vote = sample(args.vote_file)
    elec_cols = {et.name: list(filter(cm(et.name), vote.columns)) for et in ElectionType}
