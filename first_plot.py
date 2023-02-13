import pandas as pd
import plotly.graph_objects as go


def generate_first_plot_data():
    df = pd.read_csv('dataset/data.csv', sep=',')
    df = df[['home_fouls', 'away_fouls', 'result']]
    df = pd.melt(df, id_vars='result', value_vars=['home_fouls', 'away_fouls'])
    df = df.rename(columns={'variable': 'team', 'value': 'num_of_fouls'})
    df = df[df.apply(lambda x: x.result in x.team, axis=1)]
    df = df.drop(columns=['result', 'team'])
    mean = round(df['num_of_fouls'].mean())
    non_aggressive_wins = df.query("num_of_fouls <= {}".format(mean)).sum()
    aggressive_wins = df.query("num_of_fouls > {}".format(mean)).sum()
    df = pd.DataFrame(
        data={'aggressiveness': ['non-aggressive', 'aggressive'], 'wins': [non_aggressive_wins[0], aggressive_wins[0]]})
    return df, mean


def generate_first_plot_revised_data():
    df = pd.read_csv('dataset/data.csv', sep=',')
    df = df[['home_fouls', 'away_fouls', 'result']]
    df = pd.melt(df, id_vars='result', value_vars=['home_fouls', 'away_fouls'])
    df = df.rename(columns={'variable': 'team', 'value': 'num_of_fouls'})
    df['victory'] = df.apply(lambda x: x.result in x.team, axis=1)
    mean = round(df['num_of_fouls'].mean())
    df['aggressive'] = False
    df.loc[df['num_of_fouls'] > mean, 'aggressive'] = True
    df = df.drop(columns=['result', 'team', 'num_of_fouls'])
    aggressive_games_count = df['aggressive'].value_counts()
    aggressive_victories_count = df[df['aggressive']]['victory'].value_counts()
    non_aggressive_victories_count = df[df['aggressive'] == False]['victory'].value_counts()
    return aggressive_games_count, aggressive_victories_count, non_aggressive_victories_count


def first_plot():
    df, mean = generate_first_plot_data()
    fig = go.Figure(
        data=[go.Pie(labels=df['aggressiveness'], values=df['wins'], marker=dict(colors=['lightgrey', '#e23d3d']))])
    # fig.show()
    # fig.write_image('./plot/1_pie.png')
    fig = go.Figure(data=[
        go.Bar(name='Aggressive', x=[15], y=[''], orientation='h'),
        go.Bar(name='Non-aggressive', x=[15], y=['aggressiveness'], orientation='h')
    ])
    fig.update_layout(barmode='stack')
    fig.update_yaxes(range=[0, 30])
    fig.show()


def first_plot_revised():
    aggressive_games_count, aggressive_wins_count, non_aggressive_wins_count = generate_first_plot_revised_data()
    pass


if __name__ == '__main__':
    first_plot_revised()
