import pandas as pd
import plotly.express as px


def generate_first_plot_df():
    df = pd.read_csv('dataset/data.csv', sep=',')
    df = df[['home_fouls', 'away_fouls', 'result']]
    df = pd.melt(df, id_vars='result', value_vars=['home_fouls', 'away_fouls'])
    df = df.rename(columns={'variable': 'team', 'value': 'num_of_fouls'})
    df['win'] = df.apply(lambda x: x.result in x.team, axis=1)
    df = df.drop(columns=['result', 'team'])
    mean = round(df['num_of_fouls'].mean())
    non_aggressive_series = df.query("num_of_fouls < {}".format(mean)).groupby(["num_of_fouls"]).sum().sum()
    aggressive_series = df.query("num_of_fouls >= {}".format(mean)).groupby(["num_of_fouls"]).sum().sum()
    non_aggressive_df = pd.DataFrame(non_aggressive_series, columns=['non_aggressive'])
    aggressive_df = pd.DataFrame(aggressive_series, columns=['aggressive'])
    return pd.concat([non_aggressive_df, aggressive_df], axis=1).transpose()


def first_plot():
    df = generate_first_plot_df()
    fig = px.bar(df, x=['aggressive', 'non_aggressive'], y='win',
                 title='Comparison of game victories when playing aggressively')
    fig.show()
    print('halo')


def second_plot():
    pass


if __name__ == '__main__':
    first_plot()
    second_plot()
