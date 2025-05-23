from osu_db import OsuDb
import os


osu_db_path = f'C:/Users/{os.getlogin}/AppData/Local/osu!/osu!.db'

osu_data = OsuDb.from_file(osu_db_path)

for beatmap in osu_data.beatmaps:
    print(f"Beatmap: {beatmap.song_title.value} [{beatmap.difficulty.value}]")

    pairs = beatmap.star_rating_osu.pairs

    for pair in pairs:
        pairs = beatmap.star_rating_osu.pairs
        print(f"Mods: {pair.mods}, Star Rating: {pair.rating}")



    print("-" * 20)



