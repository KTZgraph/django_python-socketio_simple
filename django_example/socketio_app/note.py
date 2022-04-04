class Note:
    def __init__(self)->None:
        self.id = 1
        self.data = ''

    def update_body(self, data:str):
        self.data = data

    def to_dict(self):
        return {'_id': self.id, 'data': self.data}