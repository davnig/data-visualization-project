import numpy as np
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
    aggressive_games_count = df['aggressive'].value_counts().to_numpy()
    aggressive_wins_count = df[df['aggressive']]['victory'].value_counts().to_numpy().astype(np.float)
    non_aggressive_wins_count = df[df['aggressive'] == False]['victory'].value_counts().to_numpy().astype(np.float)
    for i in range(0, 2):
        aggressive_wins_count[i] = aggressive_wins_count[i] / aggressive_games_count[1]
        non_aggressive_wins_count[i] = non_aggressive_wins_count[i] / aggressive_games_count[0]
    return aggressive_games_count, aggressive_wins_count, non_aggressive_wins_count


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

    x_labels = ['Aggressive', 'Non-aggressive']
    widths = [aggressive_games_count[1], aggressive_games_count[0]]
    data = {
        "Wins": [aggressive_wins_count[1], non_aggressive_wins_count[1]],
        "Non-wins": [aggressive_wins_count[0], non_aggressive_wins_count[0]]
    }

    fig = go.Figure()
    for key in data:
        fig.add_trace(go.Bar(
            name=key,
            y=data[key],
            x=np.cumsum(widths) - widths,
            width=widths,
            offset=0,
            textposition="inside",
            textangle=0,
            textfont_color="white",
        ))

    # fig.update_xaxes(
    #    ticktext=["%s<br>%d" % (label, width) for label, width in zip(x_labels, widths)]
    # )

    fig.update_xaxes(range=[0, widths[0] + widths[1]])
    fig.update_yaxes(range=[0, 1])

    fig.update_layout(
        title_text="Marimekko Chart",
        barmode="stack",
        uniformtext=dict(mode="hide", minsize=10),
    )
    fig.show()
    pass


if __name__ == '__main__':
    first_plot_revised()
