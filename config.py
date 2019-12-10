from os import environ
import json


def load_config(fallback, space=None, config_name=None):
    ''' takes a dictionary of values to populate and name of configuration space
    First looks for json file {base_name}_config.json file
        grabs 'default' values then {config_name} values
    Next looks for {BASE_NAME}_{KEY} environment variables
    Each level overrides the previous
    '''
    
    config = fallback.copy()
    # look for and load info from config.json
    try:
        with open(f'{space}_config.json') as cf:
            config_json = json.loads(cf.read())
            config.update(config_json['default'])
            if config_name:
                config.update(config_json[config_name])
    except FileNotFoundError:
        # move on if file doesn't exist
        pass
    # override with environment variables
    for key in config.keys():
        override = environ.get(f'{config_name.upper()}_{key.upper()}')
        if override:
            config[key] = override
    return config
