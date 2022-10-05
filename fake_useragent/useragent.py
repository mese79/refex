import random
import json
from pathlib import Path


class UserAgent():
    def __init__(self, json_file: str = None) -> None:
        if json_file is None:
            json_file = Path(__file__).parent.joinpath('user_agents_0.1.11.json')

        # load useragents
        with open(json_file, mode='r') as f:
            self.useragents = json.load(f)['browsers']

        # list of available browsers
        # repeated chrome and firefox to increase their chance to be selected.
        self.browsers = [
            'chrome', 'opera', 'firefox', 'chrome', 'internetexplorer', 'safari',
            'chrome', 'firefox'
        ]

        self.random = self.get_random()

    def get_random(self) -> str:
        browser = random.choice(self.browsers)
        return random.choice(self.useragents[browser])




if __name__ == '__main__':
    agent = UserAgent()
    print(agent.random())
    print(agent.random())
