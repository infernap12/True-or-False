import os
import threading
from time import sleep
from urllib.error import URLError
from urllib.request import urlopen

from hstest import CheckResult, StageTest, dynamic_test, TestedProgram

from test.simple_http_server import simple_server

welcome_message = """Welcome to the True or False Game!
{"username": "rihanna", "password": "785bdf267c5244"}"""

DELAY = 0.09
FILES_TO_DELETE = ["ID_card.txt", "cookie.txt"]
URL = "http://0.0.0.0:8000/health"
ID_CARD = "ID_card.txt"

# Testing welcome message
test_data_1 = [
    {
        "expected_start": welcome_message,
        "error_response": 'Welcome to the True or False Game!\n{"username": "*******", "password": "**************"}',
        "test_values": [
        ]
    },
]


def is_connected():
    i = 0
    while True:
        try:
            if urlopen(URL).status == 200: return True
        except URLError as e:
            pass
        sleep(0.3)
        i += 1
        if i > 20: return False


class ToFTest(StageTest):
    """Tests True or False Project"""

    @staticmethod
    def delete_files(arr):
        """Deletes files in an array"""
        for file_name in arr:
            if os.path.exists(file_name):
                os.remove(file_name)

    @staticmethod
    def case_test(dict_):
        """Tests case/expected"""
        t = TestedProgram()
        output = t.start()
        if len(output) < len(dict_["expected_start"]):
            sleep(DELAY)
            output += t.get_output()
        expected = dict_["expected_start"]
        error_response = dict_["error_response"]
        if output.replace("\n", "") != expected.replace("\n", ""):
            return CheckResult.wrong(
                f"\nYour program should output:\n{error_response}\ninstead of:\n{output}")
        for item in dict_["test_values"]:
            output = t.execute(item["case"])
            if len(output) < len(item["expected"]):
                sleep(DELAY)
                output += t.get_output()
            expected = item["expected"]
            if output.replace("\n", "") != expected.replace("\n", ""):
                return CheckResult.wrong(
                    f"\nYour program should output:\n{expected}\ninstead of:\n{output}")
        return CheckResult.correct()

    @staticmethod
    def file_exists_test(file_name):
        """Tests existence of a file"""
        if not os.path.exists(file_name):
            return CheckResult.wrong(
                f"'{file_name}' does not exist!")
        return CheckResult.correct()

    def __init__(self, *args, **kwargs):
        """Creates HTTP Server"""
        super().__init__(*args, **kwargs)
        self._http_server = threading.Thread(daemon=True, target=simple_server)
        self._http_server.start()

    def after_all_tests(self):
        ToFTest.delete_files(FILES_TO_DELETE)

    @dynamic_test()
    def test1(self):
        """Tests connection to the HTTP Server"""
        if is_connected():
            return CheckResult.correct()
        return CheckResult.wrong("Connection is refused by the host!")

    @dynamic_test(data=test_data_1)
    def test2(self, dict_):
        """Tests connection, welcome message,
        and endpoint messages
        """
        return ToFTest.case_test(dict_)

    @dynamic_test()
    def test3(self):
        """Tests if file exists"""
        return ToFTest.file_exists_test(ID_CARD)


if __name__ == '__main__':
    ToFTest().run_tests()
