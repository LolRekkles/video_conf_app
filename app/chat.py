class Chat:
    def __init__(self):
        self.clients = []
        self.history = []

    def broadcast_message(self, message, msg_type='text'):
        formatted_message = {'type': msg_type, 'content': message}
        self.history.append(formatted_message)
        for client in self.clients:
            client.send(message)

    def add_client(self, client):
        self.clients.append(client)

    def get_history(self):
        return self.history
