import os

def show_beatmaps_menu(osu_path_songs):

    os.system('cls' if os.name == 'nt' else 'clear')

    print("[Beatmaps]\n")

    beatmap_index = 1
    available_beatmaps = []

    for file in os.listdir(osu_path_songs):
        available_beatmaps.append(file)
        file = file.split(" ", 1)[1]

        print(f"{beatmap_index}- {file}")
        beatmap_index += 1

    print("\n[i] Press Ctrl + F to search (Legacy Console only)")
    print('[i] Right-click the top bar and select "Find" to search\n')

    beatmap_option = int(input(" >>"))
    beatmap = available_beatmaps[beatmap_option - 1]
    osu_beatmap_path = os.path.join(osu_path_songs, beatmap)

    os.system('cls' if os.name == 'nt' else 'clear')

    beatmap_dificulties = []

    print("[Beatmap difficulties]\n")

    num = 1
    for file in os.listdir(osu_beatmap_path):
        if file.endswith(".osu"):
            beatmap_dificulties.append(file)
            file = file.split("[")[1].split("]")[0]
            print(f"{num}- {file}")
            num += 1

    print("\n[!] Difficulties are not sorted by star rate\n")

    map_difficulty_index = int(input(" >>"))

    map_difficulty = beatmap_dificulties[map_difficulty_index - 1]

    return [os.path.join(osu_beatmap_path, map_difficulty), osu_beatmap_path  ]