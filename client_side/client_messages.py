import getpass
from common.message_template import MessageTemplate


class ClientRequests:
    """
    A class to handle client requests and input for server communication.

    Attributes:
    ----------
    message_template : MessageTemplate
        Template for formatting client messages.
    """

    def __init__(self):
        """
        Initializes the ClientRequests with a message template.
        """
        self.message_template = MessageTemplate("REQUEST")

    def user_data_input(self):
        """
        Prompts the user to input their username and password.

        Returns:
        -------
        dict
            A dictionary containing the 'username' and 'password'.
        """
        username = input("(New) Username: ")
        while not username.strip():
            print("Username cannot be empty. Please try again.")
            username = input("(New) Username: ")
        password = getpass.getpass("(New) Password: ")
        while not password.strip():
            print("Password cannot be empty. Please try again.")
            password = getpass.getpass("(New) Password: ")
        return {"username": username, "password": password}

    def user_data_handling(self, command):
        """
        Handles user data input for specific commands.

        Parameters:
        ----------
        command : str
            The command requiring user data input.

        Returns:
        -------
        dict
            A formatted message template with the command and user data.
        """
        user_data = self.user_data_input()
        return self.message_template.template(message=command, data=user_data)

    def delete_account_confirmation_input(self, command):
        """
        Prompts the user to confirm account deletion.

        Parameters:
        ----------
        command : str
            The command for deleting an account.

        Returns:
        -------
        dict
            A formatted message template with the command and user decision.
        """
        decision = input("Do you really want to delete your account? Y/N ").lower()
        return self.message_template.template(message=command, data=decision)

    def send_message_input(self, command):
        """
        Prompts the user to input recipient and message details.

        Parameters:
        ----------
        command : str
            The command for sending a message.

        Returns:
        -------
        dict
            A formatted message template with the command and mail details.
        """
        recipient = input("Who do you want to send the message to? ")
        message = input("Message: ")
        mail = {"recipient": recipient, "mail": message}
        return self.message_template.template(message=command, data=mail)

    def request_to_server(self):
        """
        Prompts the user to input a command and handles the request accordingly.

        Returns:
        -------
        dict
            A formatted message template based on the user input command.
        """
        command = input("REQUEST: ").lower()
        if command in ["register", "login", "change data"]:
            return self.user_data_handling(command)
        elif command == "delete":
            return self.delete_account_confirmation_input(command)
        elif command == "send message":
            return self.send_message_input(command)
        return self.message_template.template(message=command)

