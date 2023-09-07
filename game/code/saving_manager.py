import os.path
import pickle


class SavingManager:
    def __init__(self):
        self.extension = '.save'
        self.folder = '..\saves'

    def save_data(self, data, name):
        file = open(self.folder + '/' + name + self.extension, 'wb')
        pickle.dump(data, file)

    def load_data(self, name, default_value):
        if os.path.exists(self.folder + '/' + name + self.extension):
            file = open(self.folder + '/' + name + self.extension, 'rb')
            return pickle.load(file)
        else:
            return default_value

    def save_game_data(self, data, file_names):
        for i, file in enumerate(data):
            self.save_data(file, file_names[i])


