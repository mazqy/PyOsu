import configparser

config = configparser.ConfigParser()
config.read('config/osuData.cfg')

def get_setting(section, option, cast=str):
    value = config.get(section, option)
    if cast == bool:
        return value.lower() in ("True", "1", "yes", "on")
    return cast(value)

def save_setting(section, key, value):
    config[section][key] = str(value).strip()
    with open('config/osuData.cfg', 'w') as f:
        config.write(f)