from common.data_utils import DataUtils, PostgreSQL
from common.logger_config import logger_config
from common.config_variables import postgreSQL_server_connection_data, log_file


class User:
    """
    A class to handle user-related operations such as registration, login,
    data change, message sending, and message retrieval.

    Attributes:
    ----------
    username : str
        The username of the user.
    __password : str
        The password of the user (private).
    admin_role : bool
        Flag indicating if the user has admin role.
    data_utils : DataUtils
        Utility for data-related operations.
    logger : logging.Logger
        Logger for user-related messages.
    postgresql_utils : PostgreSQL
        Utility for interacting with PostgreSQL database.
    """

    def __init__(self):
        """
        Initializes the User with default values and necessary utilities.
        """
        self.username = None
        self.__password = None
        self.admin_role = False
        self.data_utils = DataUtils()
        self.logger = logger_config("User", log_file, "server_logs.log")
        self.postgresql_utils = PostgreSQL(**postgreSQL_server_connection_data)

    def register_user(self, user_data):
        """
        Registers a new user with the provided data.

        Parameters:
        ----------
        user_data : dict
            The data of the user to register, containing 'username' and 'password'.

        Returns:
        -------
        bool
            True if registration is successful, False otherwise.
        """
        username = user_data["username"]
        try:
            validate_username = self.postgresql_utils.validate_username(username)
            if validate_username is False:
                password = user_data["password"]
                self.postgresql_utils.register_user_to_db(username, password)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False

    def login_user(self, user_data):
        """
        Logs in a user with the provided data.

        Parameters:
        ----------
        user_data : dict
            The data of the user to log in, containing 'username' and 'password'.

        Returns:
        -------
        bool
            True if login is successful, False otherwise.
        """
        username, password = user_data["username"], user_data["password"]
        try:
            validate_data = self.postgresql_utils.validate_credentials(username, password)
            if validate_data:
                self.username, self.__password = username, password
            return validate_data
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False

    def change_user_data(self, user_data):
        """
        Changes the user's data.

        Parameters:
        ----------
        user_data : dict
            The new data for the user, containing 'username' and 'password'.

        Returns:
        -------
        bool
            True if data change is successful, False otherwise.
        """
        new_username = user_data["username"]
        try:
            validate_username = self.postgresql_utils.validate_username(new_username)
            if validate_username is False:
                new_password = user_data["password"]
                self.postgresql_utils.update_user_data(new_username, new_password, self.username)
                self.username, self.__password = new_username, new_password
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False

    def delete_user(self, user_confirmation):
        """
        Deletes the user's account based on their confirmation.

        Parameters:
        ----------
        user_confirmation : str
            Confirmation from the user to delete the account.

        Returns:
        -------
        bool
            True if account deletion is successful, False otherwise.
        """
        if user_confirmation != "y":
            return False
        try:
            self.postgresql_utils.delete_user_from_db(self.username)
            return True
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False

    def check_message_length(self, message):
        """
        Checks if the message length is within the allowed limit.

        Parameters:
        ----------
        message : str
            The message to check.

        Returns:
        -------
        bool
            True if the message length is valid, False otherwise.
        """
        if len(message) > 255:
            return False
        return True

    def check_recipient_mailbox(self, recipient, unread_messages_bool):
        """
        Checks if the recipient's mailbox can receive more messages.

        Parameters:
        ----------
        recipient : str
            The recipient's username.
        unread_messages_bool : bool
            Flag indicating whether to check unread messages.

        Returns:
        -------
        bool
            True if the recipient's mailbox can receive more messages, False otherwise.
        """
        try:
            verify_recipient_mailbox = len(self.postgresql_utils.user_messages_list(recipient, unread_messages_bool))
            if verify_recipient_mailbox < 5:
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False

    def send_message(self, data):
        """
        Sends a message to the specified recipient.

        Parameters:
        ----------
        data : dict
            The data containing 'recipient' and 'mail' (message).

        Returns:
        -------
        bool or None
            True if the message is sent successfully,
            False if there is an error,
            None if the recipient does not exist.
        """
        recipient = data["recipient"]
        try:
            validate_recipient = self.postgresql_utils.validate_username(recipient)
            if validate_recipient:
                message = data["mail"]
                verify_message_length = self.check_message_length(message)
                verify_recipient_mailbox = self.check_recipient_mailbox(recipient, False)
                if verify_message_length and verify_recipient_mailbox:
                    self.postgresql_utils.save_message_to_db(recipient, self.username, message)
                    return True
                else:
                    return False
            return None
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False

    def show_unread_messages(self):
        """
        Retrieves the list of unread messages for the user.

        Returns:
        -------
        list
            A list of unread messages.
        """
        try:
            user_messages_list = self.postgresql_utils.user_messages_list(self.username, False)
            self.postgresql_utils.archive_messages(self.username)
            return user_messages_list
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return []

    def show_archived_messages(self):
        """
        Retrieves the list of archived messages for the user.

        Returns:
        -------
        list
            A list of archived messages.
        """
        try:
            archived_messages = self.postgresql_utils.user_messages_list(self.username, True)
            return archived_messages
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return []

    def __str__(self):
        """
        Returns a string representation of the user.

        Returns:
        -------
        str
            A string with the user's username and admin role status.
        """
        return f"Username: {self.username}, Admin role: {self.admin_role}"


