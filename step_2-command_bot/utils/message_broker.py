from abc import abstractmethod
from webexteamssdk import WebexTeamsAPI

class MessageBroker:
    @abstractmethod
    def send(self, message):
        pass

class WebexTeamsMessageBroker(MessageBroker):
    def __init__(self, token, target_id=None):
        self.api = WebexTeamsAPI(access_token=token)
        self.target_id = target_id

    def set_target_id(self, target_id):
        self.target_id = target_id

    def send(self, message):
        if self.target_id is not None:
            self.api.messages.create(roomId=self.target_id, markdown=message)

class StdOutMessageBroker(MessageBroker):
    def send(self, message):
        print("{}".format(message))
