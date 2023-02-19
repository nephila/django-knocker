from channels.generic.websocket import JsonWebsocketConsumer


class KnockerConsumer(JsonWebsocketConsumer):
    def websocket_connect(self, message):
        """
        Attach the consumer to the selected language
        """
        self.groups = self.get_groups()
        return super().websocket_connect(message)

    def get_groups(self):
        """
        Attach the consumer to the selected language
        """
        lang = self.scope["url_route"]["kwargs"].get("language")
        return [
            "knocker-%s" % lang,
        ]

    def knocker_saved(self, event):
        """
        This method handles messages sent to knocker.saved

        :param event: event object
        """
        self.send_json(content=event["message"])
