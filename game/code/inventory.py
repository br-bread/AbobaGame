class Inventory:
    def __init__(self):
        self.items = {
            'money': Item('Мелочь', 5, 'Несколько монет, лежащих в кармане'),
            'keyD': Item('Ключ', 1, 'Ключ от комнаты Дениса'),
            'candy': Item('Конфета', 0, 'Довольно вкусная'),
            'chocolate': Item('Шоколадка', 0, 'Стандартная плитка молочного шоколада')
        }


class Item:
    def __init__(self, name, count, description='', img=None):
        self.name = name
        self.count = count
        self.description = description
        self.img = img

    def add(self, count=1):
        self.count += count

    def remove(self, count=1):
        self.count -= count


inventory = Inventory()
