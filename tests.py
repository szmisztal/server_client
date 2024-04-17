import unittest
import io
import os
from unittest.mock import Mock, patch
from datetime import datetime as dt
from client import Client
from server import Server
from data_utils import DataUtils, SQLite
from communication_utils import ServerResponses
from users_utils import User
from config_variables import sqlite_test_database


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
        self.sqlite_utils = SQLite(sqlite_test_database)
        self.connection = self.sqlite_utils.create_connection()

    def tearDown(self):
        self.connection.close()

    def test_serialize_to_json(self):
        dict_data = {"key1": "value1", "key2": "value2"}
        json_data = self.data_utils.serialize_to_json(dict_data)
        self.assertIsInstance(json_data, bytes)

    def test_deserialize_json(self):
        json_data = b'{"key1": "value1", "key2": "value2"}'
        dict_data = self.data_utils.deserialize_json(json_data)
        self.assertIsInstance(dict_data, dict)
        self.assertEqual(dict_data, {"key1": "value1", "key2": "value2"})

    def test_register_user_to_db_and_update_user_data_and_delete_user_from_db_and_all_validate_methods(self):
        username = "user_test"
        password = "password_password"
        new_username = "new_username"
        new_password = "new_password"
        self.assertTrue(self.sqlite_utils.validate_username(username))
        self.sqlite_utils.register_user_to_db(username, password)
        self.assertFalse(self.sqlite_utils.validate_username(username))
        self.assertTrue(self.sqlite_utils.validate_credentials(username, password))
        self.assertFalse(self.sqlite_utils.validate_credentials(username, new_password))
        self.sqlite_utils.update_user_data(new_username, new_password, username, password)
        self.assertTrue(self.sqlite_utils.validate_credentials(new_username, new_password))
        self.assertFalse(self.sqlite_utils.validate_credentials(new_username, password))
        self.assertFalse(self.sqlite_utils.validate_username(new_username))
        self.sqlite_utils.delete_user_from_db(new_username, new_password)
        self.assertTrue(self.sqlite_utils.validate_username(username))

    def test_user_messages_list_with_boolean_condition__and_archive_messages_and_save_message_to_db_method(self):
        sender = "szymon"
        message = "test_message"
        message_2 = "test_message_2"
        username = "user_test"
        boolean_condition = False
        self.sqlite_utils.register_user_to_db(sender, "sender_password")
        self.assertFalse(self.sqlite_utils.validate_username(username))
        self.assertFalse(self.sqlite_utils.validate_username(sender))
        self.sqlite_utils.save_message_to_db(sender, message, username)
        self.sqlite_utils.save_message_to_db(sender, message_2, username)
        messages_list = self.sqlite_utils.user_messages_list(username, boolean_condition)
        self.assertTrue(len(messages_list) > 0)
        self.sqlite_utils.archive_messages(username)
        messages_list_2 = self.sqlite_utils.user_messages_list(username, True)
        self.assertTrue(len(messages_list_2) >= 2)

    def test_write_and_read_to_json_file(self):
        filename = "test_file.json"
        data = {"key1": "value1", "key2": "value2"}
        self.data_utils.write_to_json_file(filename, data)
        read_data = self.data_utils.read_json_file(filename)
        self.assertIsInstance(read_data, dict)
        self.assertEqual(read_data, data)
        if os.path.exists(filename):
            os.remove(filename)
        self.assertFalse(os.path.exists(filename))

    def test_hash_password(self):
        raw_password = "test_password"
        hashed_password = self.data_utils.hash_password(raw_password)
        self.assertTrue(hashed_password)

    def test_check_hashed_password(self):
        raw_password = "test_password"
        hashed_password = self.data_utils.hash_password(raw_password)
        is_valid = self.data_utils.check_hashed_password(raw_password, hashed_password)
        self.assertTrue(is_valid)
        is_invalid = self.data_utils.check_hashed_password("wrong_password", hashed_password)
        self.assertFalse(is_invalid)


class TestCommunicationUtils(unittest.TestCase):
    def setUp(self):
        self.server = Mock()
        self.communication_utils = ServerResponses(self.server)
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
        self.data_utils = DataUtils()
        self.sqlite_utils = SQLite(sqlite_test_database)

    def test_register_user_success(self):
        user_data = {"username": "test_username", "password": "test_password"}
        result = self.user.register_user(user_data)
        self.assertEqual(result, {"User": "test_username registered successfully"})
        self.sqlite_utils.delete_user_from_db(self.user.username, self.user.password)

    def test_register_user_with_used_username(self):
        user_data = {"username": self.user.username, "password": self.user.password}
        result = self.user.register_user(user_data)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["Username"], "In use, choose another")
        self.sqlite_utils.delete_user_from_db(self.user.username, self.user.password)

    def test_login_user(self):
        user_data = {"username": self.user.username, "password": self.user.password}
        self.user.register_user(user_data)
        log_result = self.user.login_user(user_data)
        self.assertIsInstance(log_result, dict)
        self.assertIn("User 'test_username'", log_result)
        self.assertEqual(log_result["User 'test_username'"], "Sign in successfully")
        self.sqlite_utils.delete_user_from_db(self.user.username, self.user.password)

    def test_login_user_with_incorrect_data(self):
        user_data = {"username": "test_password", "password": "test_username"}
        result = self.user.login_user(user_data)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["Incorrect data"], "Try again")

    def test_logout(self):
        result = self.user.logout()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["Logout"], "You was successfully log out")

    def test_delete_user_success(self):
        user_confirmation = "yes"
        result = self.user.delete_user(user_confirmation)
        self.assertEqual(result, {"Delete": "You have been deleted from database"})

    def test_delete_user_failure(self):
        user_confirmation = "no"
        result = self.user.delete_user(user_confirmation)
        self.assertEqual(result, {"Confirmation failed": "Your data will remain in the database"})

    def test_change_user_data_success(self):
        new_user_data = {"username": "new_username", "password": "new_password"}
        result = self.user.change_user_data(new_user_data)
        expected_message = {"Success": f"Your new data: username: new_username, password: new_password"}
        self.assertEqual(result, expected_message)
        self.sqlite_utils.delete_user_from_db(self.user.username, self.user.password)

    def test_change_user_data_failure(self):
        new_user_data = {"username": "szymon", "password": "new_password"}
        result = self.user.change_user_data(new_user_data)
        self.assertEqual(result, {"Username": "In use, choose another"})

    def test_send_message_user_not_found(self):
        recipient_data = "test_recipient"
        message_data = "Test message"
        result = self.user.send_message(recipient_data, message_data)
        self.assertEqual(result, {"Recipient": "User not found, try again"})

    def test_send_message_max_length_exceeded(self):
        recipient_data = "szymon"
        message_data = "A" * 256
        result = self.user.send_message(recipient_data, message_data)
        self.assertEqual(result, {"Failed": "Max message length = 255"})

    def test_send_message_mailbox_full(self):
        recipient_data = "user_test"
        message_1 = "Test message"
        message_2 = "Test message"
        message_3 = "Test message"
        message_4 = "Test message"
        message_5 = "Test message"
        message_6 = "Test message"
        self.user.send_message(recipient_data, message_1)
        self.user.send_message(recipient_data, message_2)
        self.user.send_message(recipient_data, message_3)
        self.user.send_message(recipient_data, message_4)
        self.user.send_message(recipient_data, message_5)
        result = self.user.send_message(recipient_data, message_6)
        self.assertEqual(result, {"Failed": "Recipient`s mailbox is full"})

    def test_send_message_success(self):
        user_data = {"username": "test_user_2", "password": "test_user_password_2"}
        self.user.register_user(user_data)
        recipient_data = "test_user_2"
        message_data = "Test message"
        result = self.user.send_message(recipient_data, message_data)
        self.assertEqual(result, {"Message": "Send successfully"})
        self.sqlite_utils.delete_user_from_db("test_user_2", "test_user_password_2")

    def test_str(self):
        expected_str = f"Username: {self.user.username}, Password: {self.user.password}, Login status: {self.user.logged_in}, Admin role: {self.user.admin_role}"
        self.assertEqual(str(self.user), expected_str)


if __name__ == "__main__":
    unittest.main()
