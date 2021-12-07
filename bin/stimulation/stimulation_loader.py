import json
import os

from .stimulation import Stimulation


class StimulationLoader:
    @staticmethod
    def load_from_file(filename):
        print(os.listdir())
        with open(filename, "r") as f:
            data = json.load(f)
        output = Stimulation(data['num_of_pixels'])
        for duartion, img in data['phases']:
            output.add_phase(img, duartion)
        if 'loop' in data:
            output.loop = data['loop']
        return output

    @staticmethod
    def load_from_folder(folder_name):
        output = []
        files = os.listdir()
        for f in files:
            output.append(StimulationLoader.load_from_file(f))
        return output