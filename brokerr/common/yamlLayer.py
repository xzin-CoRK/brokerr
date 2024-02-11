import yaml

def get_config() -> dict:
    '''Returns a dict representation of the YAML config file'''
    with open("/config/config.yaml") as stream:
        try:
            config = yaml.safe_load(stream)
            
            if config and config['trackers']:
                for tracker_dict in config['trackers']:
                    tracker_name = list(tracker_dict.keys())[0]
                    tracker_dict.update({
                        "name": tracker_name
                    })
            
            return config

        except yaml.YAMLError as exc:
            print(exc)