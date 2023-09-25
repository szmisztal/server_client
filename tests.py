import unittest
import io
from unittest.mock import Mock, patch, mock_open
from datetime import datetime as dt
from client import Client
from server import Server
from data_utils import DataUtils
from communication_utils import CommunicationUtils
from users_utils import User


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @patch("builtins.input", side_effect = ["test_username", "test_password"])
    def test_make_register_request(self, mock_input):
        result = self.client.make_request_to_server("register")
        self.assertIsInstance(result, dict)
        self.assertIn("Register", result)

    @patch("builtins.input", side_effect = ["test_username", "test_password"])
    def test_make_login_request(self, mock_input):
        result = self.client.make_request_to_server("login")
        self.assertIsInstance(result, dict)
        self.assertIn("Login", result)

    @patch("builtins.input", side_effect = ["test_username", "test_password"])
    def test_make_change_data_request(self, mock_input):
        result = self.client.make_request_to_server("change data")
        self.assertIsInstance(result, dict)
        self.assertIn("New data", result)

    @patch("builtins.input", side_effect = ["test_request"])
    def test_make_request(self, mock_input):
        result = self.client.make_request_to_server("test_request")
        self.assertIsInstance(result, dict)
        self.assertIn("Request", result)

    @patch("builtins.input", side_effect = ["test_username", "test_password"])
    def test_user_data_input(self, mock_input):
        result = self.client.user_data_input()
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {"username": "test_username", "password": "test_password"})

    @patch("builtins.input", side_effect = ["test_recipient", "test_message"])
    def test_send_message_input(self, mock_input):
        result = self.client.send_message_input()
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {"Recipient": "test_recipient", "Message": "test_message"})

    @patch("builtins.input", side_effect = ["yes"])
    def test_delete_user_input(self, mock_input):
        result = self.client.delete_user_input()
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {"Delete confirmation": "yes"})

    @patch("sys.stdout", new_callable = io.StringIO)
    def test_read_server_response_dict(self, mock_stdout):
        data = {"key1": "value1", "key2": "value2"}
        json_data = self.client.data_utils.serialize_to_json(data)
        self.client.read_server_response(json_data)
        output = mock_stdout.getvalue()
        self.assertIn(">>> key1: value1", output)
        self.assertIn(">>> key2: value2", output)

    @patch("sys.stdout", new_callable = io.StringIO)
    def test_read_server_response_empty_list(self, mock_stdout):
        data = []
        json_data = self.client.data_utils.serialize_to_json(data)
        self.client.read_server_response(json_data)
        output = mock_stdout.getvalue()
        self.assertIn("You don`t have any messages to read", output)

    @patch("sys.stdout", new_callable = io.StringIO)
    def test_read_server_response_message_list(self, mock_stdout):
        data = [("Sender1", "Test_text_1"), ("Sender2", "Test_text_2")]
        json_data = self.client.data_utils.serialize_to_json(data)
        self.client.read_server_response(json_data)
        output = mock_stdout.getvalue()
        self.assertIn("Message from: Sender1", output)
        self.assertIn("Text: Test_text_1", output)
        self.assertIn("Message from: Sender2", output)
        self.assertIn("Text: Test_text_2", output)

    def test_stop(self):
        data = {"Server status": "Shutting down"}
        json_data = self.client.data_utils.serialize_to_json(data)
        self.client.stop(json_data)
        self.assertFalse(self.client.is_running)


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server()

    @patch("sys.stdout", new_callable = io.StringIO)
    def test_first_message_to_client(self, mock_stdout):
        message = self.server.first_message_to_client()
        self.assertIn("Client status", message)
        self.assertIn("Type 'help'", message)

    def test_read_client_request_request(self):
        data = {"Request": "test_request"}
        json_data = self.server.data_utils.serialize_to_json(data)
        result = self.server.read_client_request(json_data)
        self.assertEqual(result, "test_request")

    def test_read_client_request_user_data(self):
        data = {"username": "test_username", "password": "test_password"}
        json_data = self.server.data_utils.serialize_to_json(data)
        result = self.server.read_client_request(json_data)
        self.assertEqual(result, data)

    @patch("sys.stdout", new_callable = io.StringIO)
    def test_stop(self, mock_stdout):
        result = self.server.stop()
        self.assertFalse(self.server.is_running)
        self.assertEqual(result, {"Server status": "Shutting down"})
        output = mock_stdout.getvalue()
        self.assertIn("SERVER CLOSED...", output)


class TestDataUtils(unittest.TestCase):
    def setUp(self):
        self.data_utils = DataUtils()

    def test_serialize_to_json(self):
        dict_data = {"key1": "value1", "key2": "value2"}
        json_data = self.data_utils.serialize_to_json(dict_data)
        self.assertIsInstance(json_data, bytes)

    def test_deserialize_json(self):
        json_data = b'{"key1": "value1", "key2": "value2"}'
        dict_data = self.data_utils.deserialize_json(json_data)
        self.assertIsInstance(dict_data, dict)
        self.assertEqual(dict_data, {"key1": "value1", "key2": "value2"})

    def test_write_and_read_to_json_file(self):
        filename = "test_file.json"
        data = {"key1": "value1", "key2": "value2"}
        self.data_utils.write_to_json_file(filename, data)
        read_data = self.data_utils.read_json_file(filename)
        self.assertIsInstance(read_data, dict)
        self.assertEqual(read_data, data)


class TestCommunicationUtils(unittest.TestCase):
    def setUp(self):
        self.server = Mock()
        self.communication_utils = CommunicationUtils(self.server)
        self.user = Mock()
        self.user.logged_in = True

    def test_uptime(self):
        self.server.server_start_time = dt(2023, 8, 12)
        result = self.communication_utils.uptime()
        self.assertIsInstance(result, dict)
        self.assertIn("Server uptime time", result)

    def test_help_logged_in(self):
        self.user.logged_in = True
        result = self.communication_utils.help(self.user)
        self.assertIsInstance(result, dict)
        self.assertIn("Uptime", result)
        self.assertIn("Info", result)
        self.assertIn("Help", result)
        self.assertIn("Change data", result)
        self.assertIn("Send message", result)
        self.assertIn("Mailbox", result)
        self.assertIn("Archives", result)
        self.assertIn("Logout", result)
        self.assertIn("Delete", result)
        self.assertIn("Stop", result)

    def test_help_not_logged_in(self):
        self.user.logged_in = False
        result = self.communication_utils.help(self.user)
        self.assertIsInstance(result, dict)
        self.assertIn("Register", result)
        self.assertIn("Login", result)
        self.assertIn("Stop", result)

    def test_info(self):
        self.server.server_start_date = "12.08.2023"
        self.server.server_version = "0.2.8"
        result = self.communication_utils.info()
        self.assertIsInstance(result, dict)
        self.assertIn("Server start date:", result)
        self.assertIn("Server version:", result)

    def test_unknown_command(self):
        client_request = "unknown_command"
        result = self.communication_utils.unknown_command(client_request)
        self.assertIsInstance(result, dict)
        self.assertIn("Unknown command", result)

    def test_response_to_client_uptime(self):
        self.user.logged_in = True
        self.server.server_start_time = dt(2023, 8, 12)
        result = self.communication_utils.response_to_client("uptime", self.user)
        self.assertIsInstance(result, dict)
        self.assertIn("Server uptime time", result)

    def test_response_to_client_info(self):
        self.user.logged_in = True
        result = self.communication_utils.response_to_client("info", self.user)
        self.assertIsInstance(result, dict)
        self.assertIn("Server start date:", result)
        self.assertIn("Server version:", result)

    def test_response_to_client_help_logged_in(self):
        self.user.logged_in = True
        result = self.communication_utils.response_to_client("help", self.user)
        self.assertIsInstance(result, dict)
        self.assertIn("Uptime", result)
        self.assertIn("Info", result)
        self.assertIn("Help", result)
        self.assertIn("Change data", result)
        self.assertIn("Send message", result)
        self.assertIn("Mailbox", result)
        self.assertIn("Archives", result)
        self.assertIn("Logout", result)
        self.assertIn("Delete", result)
        self.assertIn("Stop", result)

    def test_response_to_client_help_not_logged_in(self):
        self.user.logged_in = False
        result = self.communication_utils.response_to_client("help", self.user)
        self.assertIsInstance(result, dict)
        self.assertIn("Register", result)
        self.assertIn("Login", result)
        self.assertIn("Stop", result)

    def test_response_to_client_change_user_data(self):
        self.user.change_user_data.return_value = {"Success": f"Your new data: username: {self.user.username}, password: {self.user.password}"}
        client_request = {"New data": {"new_username": "new_password"}}
        result = self.communication_utils.response_to_client(client_request, self.user)
        self.assertIsInstance(result, dict)
        self.assertIn("Success", result)

    def test_response_to_client_send_message(self):
        self.user.send_message.return_value = {"Message": "Send successfully"}
        client_request = {"Recipient": "test_recipient", "Message": "test_message"}
        result = self.communication_utils.response_to_client(client_request, self.user)
        self.assertIsInstance(result, dict)
        self.assertIn("Message", result)

    def test_response_to_client_show_new_messages(self):
        self.user.show_new_messages.return_value = [{"Message from": "sender", "Text": "text"}]
        result = self.communication_utils.response_to_client("mailbox", self.user)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_response_to_client_show_archived_messages(self):
        self.user.show_archived_messages.return_value = [{"Message from": "sender", "Text": "text"}]
        result = self.communication_utils.response_to_client("archives", self.user)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_response_to_client_logout(self):
        self.user.logout.return_value = {"Logout": "You was successfully log out"}
        result = self.communication_utils.response_to_client("logout", self.user)
        self.assertIsInstance(result, dict)
        self.assertIn("Logout", result)

    def test_response_to_client_delete(self):
        self.user.delete_user.return_value = {"Delete": "You have been deleted from database"}
        client_request = {"Delete confirmation": "Yes"}
        result = self.communication_utils.response_to_client(client_request, self.user)
        self.assertIsInstance(result, dict)
        self.assertIn("Delete", result)

    def test_response_to_client_unknown_command(self):
        client_request = "unknown_command"
        result = self.communication_utils.response_to_client(client_request, self.user)
        self.assertIsInstance(result, dict)
        self.assertIn("Unknown command", result)

    def test_response_to_client_not_logged_in(self):
        self.user.logged_in = False
        result = self.communication_utils.response_to_client("logout", self.user)
        self.assertIsInstance(result, dict)
        self.assertIn("Error", result)
        self.assertIn("You have to sign in first to see available commands", result["Error"])

    def test_response_to_client_stop(self):
        self.server.stop.return_value = {"Server status": "Shutting down"}
        result = self.communication_utils.response_to_client("stop", self.user)
        self.assertIsInstance(result, dict)
        self.assertIn("Server status", result)
        self.assertEqual(result["Server status"], "Shutting down")


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User("test_username", "test_password")
        self.test_user_data = {"username": f"{self.user.username}", "password": f"{self.user.password}"}
        self.data_utils = DataUtils()

    @patch("builtins.open", new_callable = mock_open, read_data = "[]")
    def test_register_user(self, mock_file):
        user_data = {"username": "register_username", "password": "register_password"}
        result = self.user.register_user(user_data)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["User"], "register_username registered successfully")

    def test_register_user_with_used_username(self):
        user_data = {"username": "test_username", "password": "test_password"}
        result = self.user.register_user(user_data)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["Username"], "In use, choose another")

    def test_login_user(self):
        user_data = {"username": "test_username", "password": "test_password"}
        result = self.user.login_user(user_data)
        self.assertIsInstance(result, dict)
        self.assertIn("User 'test_username'", result)
        self.assertEqual(result["User 'test_username'"], "Sign in successfully")

    def test_login_user_with_incorrect_data(self):
        user_data = {"username": "test_password", "password": "test_username"}
        result = self.user.login_user(user_data)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["Incorrect data"], "Try again")

    def test_logout(self):
        result = self.user.logout()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["Logout"], "You was successfully log out")

    @patch("builtins.open", new_callable = mock_open, read_data = "[]")
    def test_change_user_data(self, mock_file):
        new_user_data = {"username": "new_username", "password": "new_password"}
        result = self.user.change_user_data(new_user_data)
        self.assertIsInstance(result, dict)
        self.assertIn("Success", result)
        self.assertEqual(result["Success"], "Your new data: username: new_username, password: new_password")

    def test_change_data_with_incorrect_username(self):
        new_user_data = {"username": "test_username", "password": "new_password"}
        result = self.user.change_user_data(new_user_data)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["Username"], "In use, choose another")

    @patch("os.path.exists", return_value = False)
    def test_show_new_messages(self, mock_file):
        test_messages = [
            {"Message from": "Sender_1", "Text": "Test_message_1"},
            {"Message from": "Sender_2", "Text": "Test_message_2"}
        ]
        self.data_utils.write_to_json_file(f"{self.user.username}_new_messages.json", test_messages)
        messages_to_read = self.user.show_new_messages()
        self.assertEqual(messages_to_read, test_messages)

    @patch("os.path.exists", return_value = False)
    def test_show_archived_messages(self, mock_file):
        test_archived_messages = [
            {"Message from": "Sender_1", "Text": "Test_message_1"},
            {"Message from": "Sender_2", "Text": "Test_message_2"}
        ]
        self.data_utils.write_to_json_file(f"{self.user.username}_archived_messages.json", test_archived_messages)
        archived_messages = self.user.show_archived_messages()
        self.assertEqual(archived_messages, test_archived_messages)

    def test_str(self):
        expected_str = f"Username: {self.user.username}, Password: {self.user.password}, Login status: {self.user.logged_in}, Admin role: {self.user.admin_role}"
        self.assertEqual(str(self.user), expected_str)


if __name__ == "__main__":
    unittest.main()
