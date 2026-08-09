from nba_api.stats.endpoints.playbyplayv3 import PlayByPlayV3

game_id = "0022300061"

pbp = PlayByPlayV3(game_id=game_id)

df = pbp.get_data_frames()[0]

print(df.head())
print(df.shape)