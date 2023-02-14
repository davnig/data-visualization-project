import pandas as pd
import plotly.graph_objects as go

SHOW_IMAGE = True


def encode_match_result(team, home_team, away_team, result):
    if result == 'draw':
        return result
    if (home_team == team and result == 'home') or (away_team == team and result == 'away'):
        return 'win'
    return 'lose'


def generate_second_plot_data():
    def count_all_streaks():
        def init_streak_data():
            for i in range(0, 21):
                streak_data['{}-streaks'.format(i)] = 0
                streak_data['{}-streak-win'.format(i)] = 0
                streak_data['{}-streak-draw'.format(i)] = 0
                streak_data['{}-streak-lose'.format(i)] = 0

        def count_team_winning_streaks():
            def save():
                streak_data['0-streaks'] += 1
                streak_data['0-streak-{}'.format(value)] += 1

            def save_current_streak():
                if '{}-streaks'.format(streak_count) not in streak_data:
                    return
                streak_data['{}-streaks'.format(streak_count)] += 1
                streak_data['{}-streak-{}'.format(streak_count, value)] += 1
                for below_steak in range(streak_count - 1, 0, -1):
                    streak_data['{}-streaks'.format(below_steak)] += 1
                    streak_data['{}-streak-win'.format(below_steak, value)] += 1

            results = team_df.values.flatten()
            streak_count = 0
            for idx, value in enumerate(results):
                save()
                if value == 'win':
                    streak_count += 1
                    continue
                if streak_count > 0:
                    save_current_streak()
                    streak_count = 0

        all_seasons = df.season.unique()
        all_teams = pd.concat([df.home_team, df.away_team], axis=0).unique()
        streak_data = {}
        init_streak_data()
        for season in all_seasons:
            season_df = df[df['season'] == season]
            for team in all_teams:
                team_df = season_df[(season_df.home_team == team) | (season_df.away_team == team)]
                team_df['win'] = team_df.apply(lambda row:
                                               encode_match_result(team, row.home_team, row.away_team, row.result),
                                               axis=1)
                team_df = team_df[['win']].reset_index(drop=True).rename(columns={'win': 'result'})
                count_team_winning_streaks()
        return streak_data

    def remove_unwanted_streaks(max_streak=20):
        saved_max_streak = int(len(streaks) / 4)
        for i in range(0, saved_max_streak):
            if i > max_streak:
                streaks.pop('{}-streaks'.format(i))
                streaks.pop('{}-streak-win'.format(i))
                streaks.pop('{}-streak-draw'.format(i))
                streaks.pop('{}-streak-lose'.format(i))
        return streaks

    def normalize_winning_streak():
        normalized = {}
        num_of_streaks = int(len(streaks) / 4)
        for i in range(0, num_of_streaks):
            normalized['{}-win'.format(i)] = streaks['{}-streak-win'.format(i)] / streaks[
                '{}-streaks'.format(i)]
            normalized['{}-draw'.format(i)] = streaks['{}-streak-draw'.format(i)] / streaks[
                '{}-streaks'.format(i)]
            normalized['{}-lose'.format(i)] = streaks['{}-streak-lose'.format(i)] / streaks[
                '{}-streaks'.format(i)]
        return normalized

    def convert_streak_dict_to_df():
        streak_df = pd.DataFrame()
        streak_df['streak'] = range(0, int(len(streaks) / 4))
        streak_df['win'] = [normalized_streak_count[x] for x in normalized_streak_count if x.endswith('win')]
        streak_df['draw'] = [normalized_streak_count[x] for x in normalized_streak_count if x.endswith('draw')]
        streak_df['lose'] = [normalized_streak_count[x] for x in normalized_streak_count if x.endswith('lose')]
        streak_df['total'] = [streaks[x] for x in streaks if x.endswith('streaks')]
        return streak_df

    df = pd.read_csv('dataset/data.csv', sep=',')
    df = df.filter(regex='season|round|home_team|away_team|result', axis=1)
    streaks = count_all_streaks()
    streaks = remove_unwanted_streaks(max_streak=7)
    normalized_streak_count = normalize_winning_streak()
    normalized_streak_df = convert_streak_dict_to_df()
    total_ref = normalized_streak_df.iloc[1, 4]
    normalized_streak_df['total_norm'] = normalized_streak_df['total'] / total_ref
    return normalized_streak_df


def second_plot():
    winning_streaks_df = generate_second_plot_data()
    winning_streaks_df = winning_streaks_df.drop(index=0)
    win_percentages = ['35%', '40%', '45%', '51%', '57%', '74%', '76%']
    layout = go.Layout(
        plot_bgcolor='rgba(0,0,0,0)'
    )
    data = [
        go.Bar(name='streak count', x=winning_streaks_df.streak, y=winning_streaks_df.total_norm, offsetgroup=0,
               text=winning_streaks_df['total'], textposition='outside', marker=dict(color='#69c38f')),
        go.Bar(name='win', x=winning_streaks_df.streak, y=winning_streaks_df.win, offsetgroup=1,
               text=win_percentages, textposition='inside', marker=dict(color='#006d78')),
        go.Bar(name='draw', x=winning_streaks_df.streak, y=winning_streaks_df.draw, offsetgroup=1,
               base=winning_streaks_df.win, marker=dict(color='#929399')),
        go.Bar(name='lose', x=winning_streaks_df.streak, y=winning_streaks_df.lose, offsetgroup=1,
               base=winning_streaks_df.win + winning_streaks_df.draw, marker=dict(color='#cfd0d7'))
    ]
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(showline=True, linecolor='black', title_text='Winning streaks', title_font={'size': 20})
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(
        font=dict(
            size=24
        )
    )
    fig.update_layout(legend=dict(font=dict(size=20)))
    if SHOW_IMAGE:
        fig.show()
    # fig.write_image(file='./plot/plot2.png', width=2000, height=1000, scale=2)


if __name__ == '__main__':
    second_plot()
