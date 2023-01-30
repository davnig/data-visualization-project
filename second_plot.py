import pandas as pd
import plotly.express as px


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
    return normalized_streak_df


def second_plot():
    winning_streaks_df = generate_second_plot_data()
    fig = px.bar(winning_streaks_df, x='streak', y=['win', 'draw', 'lose'], title='test')
    fig.update_layout(barmode='group')
    fig.show()
    pass


if __name__ == '__main__':
    second_plot()
