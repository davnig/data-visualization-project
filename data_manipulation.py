import pandas as pd

from utils import MATCH_STATS_COLUMNS


def fill_stat_values_in_hist_df(df: pd.DataFrame):
    """Fill missing stats values with 0 in historic dataframe"""
    for col in [f'{home_away}_{col}' for home_away in ['home', 'away'] for col in MATCH_STATS_COLUMNS]:
        df[col].replace(['-'], 0, inplace=True)
    return df


def fill_stat_values(df: pd.DataFrame):
    """Fill missing stats values with 0"""
    for col in MATCH_STATS_COLUMNS:
        df[col].replace(['-'], 0, inplace=True)
    return df


def force_type_in_hist_df(df: pd.DataFrame) -> pd.DataFrame:
    """Cast data to proper type in historic dataframe"""
    str_columns = ['season', 'date', 'time', 'home_team', 'away_team', 'referee']
    str_columns = [f'home_{col}' for col in str_columns] + [f'away_{col}' for col in str_columns]
    str_columns += ['result']
    int_columns = [x for x in df.columns if x not in str_columns]
    type_dict = {}
    for int_col in int_columns:
        type_dict[int_col] = 'int'
    for str_col in str_columns:
        type_dict[str_col] = 'str'
    return df.astype(type_dict)


def force_type(df: pd.DataFrame) -> pd.DataFrame:
    """Cast data to proper type"""
    str_columns = ['season', 'date', 'home_team', 'away_team', 'referee']
    str_columns += ['result']
    int_columns = [x for x in df.columns if x not in str_columns]
    type_dict = {}
    for int_col in int_columns:
        type_dict[int_col] = 'int'
    for str_col in str_columns:
        type_dict[str_col] = 'str'
    return df.astype(type_dict)


def remove_referees(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(df.filter(regex='referee', axis=1).columns, axis=1)


def remove_teams(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(df.filter(regex='team', axis=1).columns, axis=1)
