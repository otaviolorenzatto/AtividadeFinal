
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

class AsyncConn:
    def __init__(self, id: str, channel_name: str) -> None:
        config = PNConfiguration()
        config.subscribe_key = 'sub-c-3c4dffb7-433f-4b29-adad-588e97e9c5ed'
        config.publish_key = 'pub-c-49753194-5bdb-4ebe-a1ed-d81012baf4af'
        config.user_id = id
        config.enable_subscribe = True
        config.daemon = True

        self.pubnub = PubNub(config)
        self.channel_name = channel_name

        print(f"Configurando conexão com o canal '{self.channel_name}'...")
        subscription = self.pubnub.channel(self.channel_name).subscription()
        subscription.subscribe()

    def publish(self, data: dict):
        print("tentando enviar uma mensagem")
        self.pubnub.publish().channel(self.channel_name).message(data).sync()

