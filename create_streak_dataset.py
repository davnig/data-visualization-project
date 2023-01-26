import pandas as pd

from data_manipulation import force_type_in_hist_df, fill_stat_values_in_hist_df
from utils import add_historic_data_of_last_n_matches_as_features

INPUT_CSV_NAME = '../dataset/data.csv'
OUTPUT_CSV_NAME = '../dataset/streak-data.csv'


def data_manipulation(df: pd.DataFrame):
    def convert_wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
        not_hist_columns = df.filter(regex='^(?!.*_[1-5]$).*$', axis=1).columns.tolist()
        # delete all matches not having a complete history of 5 games
        df = df.drop(df[df['home_season_5'] == '-'].index)
        # rename columns of current match as historic with #0 index and duplicate
        home_current = pd.DataFrame(data=df.filter(regex='^(?!.*_[1-5]$).*$', axis=1).values.tolist(),
                                    columns=[f'home_{col}_0' for col in not_hist_columns]).set_index(df.index)
        away_current = pd.DataFrame(data=df.filter(regex='^(?!.*_[1-5]$).*$', axis=1).values.tolist(),
                                    columns=[f'away_{col}_0' for col in not_hist_columns]).set_index(df.index)
        df = df.drop(columns=df.filter(regex='^(?!.*_[1-5]$).*$', axis=1).columns, inplace=False)
        df = pd.concat([home_current, away_current, df], axis=1)
        # re-insert 'result' column
        df.insert(loc=1, column='result', value=df['home_result_0'])
        # insert 'id' columns
        df.insert(loc=0, column='id', value=df.index)
        # convert wide to long
        df = pd.wide_to_long(df, stubnames=[f'{home_or_away}_{col}' for col in not_hist_columns for home_or_away in
                                            ['home', 'away']], i=['id', 'result'], j='time_idx', sep='_', suffix='\d+')
        # clean unwanted columns
        df = df.drop(columns=['home_result', 'away_result'], axis=1)
        df = df.reset_index()
        df = df.sort_values(by=['id', 'time_idx'], ascending=[True, True])
        df = df.reset_index(drop=True)
        df = df.drop(columns=['id', 'time_idx'])
        return df

    print('===> Phase 2: DATA MANIPULATION ')
    df['time'] = pd.to_datetime(df['time'], format="%H:%M")
    df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
    df = add_historic_data_of_last_n_matches_as_features(df)
    df = convert_wide_to_long(df)
    df = fill_stat_values_in_hist_df(df)
    # delete group of 5 match having a NaN value
    if len(df[df['away_season'] == '-'].index.tolist()) > 0:
        df = df.drop(
            df.iloc[
            df[df['away_season'] == '-'].index.tolist()[0] - 5:df[df['away_season'] == '-'].index.tolist()[0] + 1,
            :].index).reset_index(drop=True)
    # force correct type for all columns
    df = force_type_in_hist_df(df)
    print('===> Phase 2: DONE ')
    return df


if __name__ == '__main__':
    df = pd.read_csv(INPUT_CSV_NAME)
    df = data_manipulation(df)
    df.to_csv(OUTPUT_CSV_NAME, index=False)
    print(f'DONE. Final shape: {df.shape}')
