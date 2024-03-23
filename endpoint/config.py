import json
from pydantic import BaseModel

class Config(BaseModel):
    show_frames: bool
    ip_port: int

def loadConfig() -> Config | None:
    with open('config/config.json') as config_file:
        configDict = json.load(config_file)['config']
        return Config(**configDict)

config: Config = loadConfig()
