import numpy as np
import pandas as pd
import plotly.graph_objects as go

SHOW_IMAGE = True


def fetch_marimekko_chart_data():
    df = pd.read_csv('dataset/data.csv', sep=',')
    df = df[['home_fouls', 'away_fouls', 'result']]
    df = pd.melt(df, id_vars='result', value_vars=['home_fouls', 'away_fouls'])
    df = df.rename(columns={'variable': 'team', 'value': 'num_of_fouls'})
    df['victory'] = df.apply(lambda x: x.result in x.team, axis=1)
    mean = round(df['num_of_fouls'].mean())
    df['aggressive'] = False
    df.loc[df['num_of_fouls'] >= mean, 'aggressive'] = True
    df = df.drop(columns=['result', 'team', 'num_of_fouls'])
    aggressive_games_count = df['aggressive'].value_counts().to_numpy()
    aggressive_wins_count = df[df['aggressive']]['victory'].value_counts().to_numpy().astype(float)
    non_aggressive_wins_count = df[df['aggressive'] == False]['victory'].value_counts().to_numpy().astype(float)
    for i in range(0, 2):
        aggressive_wins_count[i] = aggressive_wins_count[i] / aggressive_games_count[1]
        non_aggressive_wins_count[i] = non_aggressive_wins_count[i] / aggressive_games_count[0]
    return aggressive_games_count, aggressive_wins_count, non_aggressive_wins_count


def create_marimekko_chart():
    aggressive_games_count, aggressive_wins_count, non_aggressive_wins_count = fetch_marimekko_chart_data()
    x_labels = ['Aggressive', 'Non-aggressive']
    widths = np.array([aggressive_games_count[1], aggressive_games_count[0]])
    data = {
        "Wins": [aggressive_wins_count[1] * 100, non_aggressive_wins_count[1] * 100],
        "Non-wins": [aggressive_wins_count[0] * 100, non_aggressive_wins_count[0] * 100]
    }
    x = np.cumsum(widths) - widths
    data = [
        go.Bar(name='Wins', y=data['Wins'], x=x, customdata=np.round(data['Wins'], 0),
               texttemplate="%{customdata}%<br>win rate", width=widths, offset=0, textposition="inside",
               textfont_color="white",
               marker=dict(color=['#cf443f', '#919191'])),
        go.Bar(name='Non-wins', y=data['Non-wins'], x=x, width=widths, offset=0, textposition="inside",
               textfont_color="white", marker=dict(color=['#ed8380', '#d1cfcf']))
    ]
    layout = go.Layout(
        barmode='stack',
        showlegend=False,
        font=dict(
            size=22
        )
    )
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(
        range=[0, widths[0] + widths[1]],
        showline=True, linecolor='black',
        tickvals=np.cumsum(widths) - widths / 2,
        ticktext=["%s<br>%d" % (length, width) for length, width in zip(x_labels, widths)]
    )
    fig.update_yaxes(range=[0, 100], showticklabels=False)
    if SHOW_IMAGE:
        fig.show()
    fig.write_image(file='./plot/1_mekko.png', scale=3)


if __name__ == '__main__':
    create_marimekko_chart()
