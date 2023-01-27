import pandas as pd


def generate_second_plot_data():
    history_len = 5
    df = pd.read_csv('dataset/streak-data.csv', sep=',')
    result_df = df.filter(regex='^.*(?:result).*$', axis=1)
    home_result_df = pd.DataFrame(data={'team': 'home', 'result': result_df['result']})
    away_result_df = pd.DataFrame(data={'team': 'away', 'result': result_df['result']})
    df = pd.concat([home_result_df, away_result_df], axis=0)
    df['win'] = df.apply(lambda x: 1 if x.result in x.team else 0, axis=1)
    df = df.drop(columns=['team', 'result'])
    nested_array = df.values.reshape(-1, history_len + 1, df.shape[1])
    return nested_array


def second_plot():
    df = generate_second_plot_data()
    pass


if __name__ == '__main__':
    second_plot()
