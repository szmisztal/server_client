class MessageTemplate:
    def __init__(self, instance):
        self.instance = instance

    def template(self, message = None, data = None):
        template = {
            "status": self.instance,
            "message": message,
            "data": data,
        }
        return template
