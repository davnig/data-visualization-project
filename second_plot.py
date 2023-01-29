import pandas as pd


def encode_match_result(team, home_team, away_team, result):
    if result == 'draw':
        return result
    if (home_team == team and result == 'home') or (away_team == team and result == 'away'):
        return 'win'
    return 'lose'


def generate_second_plot_data():
    def count_all_winning_streaks():
        def init_streak_data():
            for i in range(1, 21):
                streak_data['{}-streaks'.format(i)] = 0
                streak_data['{}-streak-win'.format(i)] = 0
                streak_data['{}-streak-draw'.format(i)] = 0
                streak_data['{}-streak-lose'.format(i)] = 0

        def count_team_winning_streaks():
            def save_last_streaks():
                streak_data['{}-streaks'.format(streak_count)] += 1
                streak_data['{}-streak-{}'.format(streak_count, value)] += 1
                for below_steak in range(streak_count - 1, 0, -1):
                    streak_data['{}-streaks'.format(below_steak)] += 1
                    streak_data['{}-streak-win'.format(below_steak, value)] += 1

            results = team_df.values.flatten()
            streak_count = 0
            for idx, value in enumerate(results):
                if value == 'win':
                    streak_count += 1
                    continue
                if streak_count > 0:
                    save_last_streaks()
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

    df = pd.read_csv('dataset/data.csv', sep=',')
    df = df.filter(regex='season|round|home_team|away_team|result', axis=1)
    winning_streaks = count_all_winning_streaks()
    return winning_streaks


def second_plot():
    streak_count = generate_second_plot_data()
    print(streak_count)
    pass


if __name__ == '__main__':
    second_plot()
