class MessageTemplate:
    """
    A class to create message templates for client-server communication.

    Attributes:
    ----------
    instance : str
        The instance type (e.g., 'REQUEST' or 'RESPONSE') to include in the template.
    """

    def __init__(self, instance):
        """
        Initializes the MessageTemplate with the specified instance type.

        Parameters:
        ----------
        instance : str
            The instance type for the message template.
        """
        self.instance = instance

    def template(self, message=None, data=None):
        """
        Creates a message template with the provided message and data.

        Parameters:
        ----------
        message : str, optional
            The message content (default is None).
        data : any, optional
            Additional data to include in the template (default is None).

        Returns:
        -------
        dict
            A dictionary representing the message template.
        """
        template = {
            "status": self.instance,
            "message": message,
            "data": data,
        }
        return template

