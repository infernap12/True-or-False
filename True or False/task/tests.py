import datetime
import difflib
import os
import threading
from time import sleep
from urllib.error import URLError
from urllib.request import urlopen

from hstest import CheckResult, StageTest, dynamic_test, TestedProgram

from test.simple_http_server import simple_server

welcome_msg = "Welcome to the True or False Game!\n"

main_menu_msg = """0. Exit
1. Play a game
2. Display scores
3. Reset scores
Enter an option:
"""

today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
player_scores = f"""Player scores
User: hyper, Score: 40, Date: {today}
User: jet, Score: 20, Date: {today}"""
scores_file_content = [f"User: hyper, Score: 40, Date: {today}\n", f"User: jet, Score: 20, Date: {today}\n"]

invalid_option_msg = "Invalid option!\n"
farewell_msg = "See you later!\n"
file_not_found_msg = "File not found or no scores in it!\n"
ask_name_msg = "What is your name?\n"
correct_response = ["Perfect!\n", "Awesome!\n", "You are a genius!\n", "Wow!\n", "Wonderful!\n"]
deletion_msg = "File deleted successfully!\n"

DELAY = 0.09
FILES_TO_DELETE = ["ID_card.txt", "cookie.txt", "scores.txt"]
URL = "http://0.0.0.0:8000/health"

# Testing invalid option and non scores
test_data_1 = [
    {
        "expected_start": f"{welcome_msg}{main_menu_msg}",
        "test_values": [
            {"case": "7", "expected": f"{invalid_option_msg}{main_menu_msg}"},
            {"case": "0", "expected": farewell_msg}
        ]
    },
    {
        "expected_start": f"{welcome_msg}{main_menu_msg}",
        "test_values": [
            {"case": "2", "expected": f"{file_not_found_msg}{main_menu_msg}"},
            {"case": "0", "expected": farewell_msg}
        ]
    },
    {
        "expected_start": f"{welcome_msg}{main_menu_msg}",
        "test_values": [
            {"case": "3", "expected": f"{file_not_found_msg}{main_menu_msg}"},
            {"case": "0", "expected": farewell_msg}
        ]
    },
]

# Testing gameplay
test_data_2 = [
    {
        "expected_start": f"{welcome_msg}{main_menu_msg}",
        "test_values": [
            {"case": "1", "expected": f"{ask_name_msg}"},
            {
                "case": "hyper",
                "expected": "Pong is the first commercially successful video game\nTrue or False?\n",
                "alternatives": None,
            },
            {
                "case": "True",
                "expected": f"The first mechanical computer - The Babbage Difference Engine - was designed by Charles Babbage in 1922\nTrue or False?\n",
                "alternatives": correct_response,
            },
            {
                "case": "False",
                "expected": f"Rihanna is a rugby player\nTrue or False?\n",
                "alternatives": correct_response,
            },
            {
                "case": "False",
                "expected": f"Bright brothers had invented the first successful airplane\nTrue or False?\n",
                "alternatives": correct_response,
            },
            {
                "case": "False",
                "expected": f"The heaviest land mammal is the African bush elephant\nTrue or False?\n",
                "alternatives": correct_response,
            },
            {
                "case": "False",
                "expected": f"Wrong answer, sorry!\nhyper you have 4 correct answer(s).\nYour score is 40 points.\n{main_menu_msg}",
            },
            {"case": "1", "expected": f"{ask_name_msg}"},
            {
                "case": "jet",
                "expected": "The International Space Station circles the globe every 900 minutes\nTrue or False?\n",
                "alternatives": None,
            },
            {
                "case": "False",
                "expected": f"The Sun is 109 times wider than Earth\nTrue or False?\n",
                "alternatives": correct_response,
            },
            {
                "case": "True",
                "expected": f"John Bardeen - Walter Brattain - William Shockley invented the first working transistors at Bell Labs\nTrue or False?\n",
                "alternatives": correct_response,
            },
            {
                "case": "False",
                "expected": f"Wrong answer, sorry!\njet you have 2 correct answer(s).\nYour score is 20 points.\n{main_menu_msg}"
            },
            {"case": "0", "expected": farewell_msg}
        ]
    },
]

# Tests scores
test_data_3 = [
    {
        "expected_start": f"{welcome_msg}{main_menu_msg}",
        "test_values": [
            {"case": "2", "expected": f"{player_scores}\n{main_menu_msg}\n"},
            {"case": "0", "expected": farewell_msg}
        ]
    },
]

# Tests deletion of scores
test_data_4 = [
    {
        "expected_start": f"{welcome_msg}{main_menu_msg}",
        "test_values": [
            {"case": "3", "expected": f"{deletion_msg}{main_menu_msg}"},
            {"case": "0", "expected": farewell_msg}
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
        expected = dict_["expected_start"]

        if len(output) < len(expected):
            sleep(DELAY)
            output += t.get_output()

        if output.replace("\n", "") not in expected.replace("\n", ""):
            return CheckResult.wrong(
                f"\nYour program should output:\n{expected}\ninstead of:\n{output}")

        for item in dict_["test_values"]:
            output = t.execute(item["case"])
            expected = item["expected"]

            if len(output) < len(expected):
                sleep(DELAY)
                output += t.get_output()

            if output.replace("\n", "") not in expected.replace("\n", ""):
                return CheckResult.wrong(
                    f"\nYour program should output:\n{expected}\ninstead of:\n{output}")

        return CheckResult.correct()

    @staticmethod
    def case_test_partial(dict_):
        """Tests case/expected"""
        t = TestedProgram()
        output = t.start()
        expected = dict_["expected_start"]

        if len(output) < len(expected):
            sleep(DELAY)
            output += t.get_output()

        if expected.replace("\n", "") not in output.replace("\n", ""):
            return CheckResult.wrong(
                f"\nYour program should output:\n{expected}\ninstead of:\n{output}")

        for item in dict_["test_values"]:
            output = t.execute(item["case"])
            expected = item["expected"]
            alternatives = item.get("alternatives")

            if len(output) < len(expected):
                sleep(DELAY)
                output += t.get_output()

            if expected.replace("\n", "") not in output.replace("\n", ""):
                return CheckResult.wrong(
                    f"\nThe output:\n{output}\nDoes not contain:\n{expected}\n")

            if alternatives:
                alternative_found = any(
                    [True for alternative in alternatives if alternative.replace("\n", "") in output.replace("\n", "")])
                if not alternative_found:
                    return CheckResult.wrong(
                        f"\nThe output:\n{output}\nDoes not contain one of these:\n{''.join(alternatives)}")

        return CheckResult.correct()

    @staticmethod
    def file_exists_test(file_name):
        """Tests existence of a file"""
        if not os.path.exists(file_name):
            return CheckResult.wrong(
                f"'{file_name}' does not exist!")
        return CheckResult.correct()

    @staticmethod
    def file_not_exists_test(file_name):
        """Tests non-existence of a file"""
        if os.path.exists(file_name):
            return CheckResult.wrong(
                f"'{file_name}' should not exist!")
        return CheckResult.correct()

    @staticmethod
    def file_content_test(test_file_data, output_file):
        """Tests the contents of files line by line"""
        try:
            with open(output_file) as file:
                output_file_data = file.readlines()

            # Converting generator object to list
            wrong_lines = [line for line in difflib.unified_diff(
                test_file_data, output_file_data, fromfile="file1",
                tofile="file2", lineterm='\n')]
        except:
            return CheckResult.wrong("Test or output file does not found!")

        if not wrong_lines:
            return CheckResult.correct()

        return CheckResult.wrong(
            f"Wrong line(s) found in '{output_file}'\n"
            f"{''.join(wrong_lines)}"
        )

    @staticmethod
    def file_content_equality_test(test_file_data, output_file):
        """Tests if the contents of files are equal"""
        try:
            with open(output_file, mode="rb") as file:
                output_file_data = file.read()
        except:
            return CheckResult.wrong("Test or output file does not found!")
        else:
            if output_file_data != test_file_data:
                return CheckResult.wrong(f"{output_file} content is incorrect!")
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
        """Tests invalid option,
        non scores messages
        """
        return ToFTest.case_test(dict_)

    @dynamic_test(data=test_data_2)
    def test3(self, dict_):
        """Tests gameplay
        """
        return ToFTest.case_test_partial(dict_)

    @dynamic_test(data=test_data_3)
    def test4(self, dict_):
        """Tests scores
        """
        return ToFTest.case_test(dict_)

    @dynamic_test()
    def test5(self):
        """Tests if file exists"""
        return ToFTest.file_exists_test("cookie.txt")

    @dynamic_test()
    def test6(self):
        """Tests if file exists"""
        return ToFTest.file_exists_test("scores.txt")

    @dynamic_test()
    def test7(self):
        """Tests content of scores.txt"""
        return ToFTest.file_content_test(scores_file_content, "scores.txt")

    @dynamic_test(data=test_data_4)
    def test8(self, dict_):
        """Tests deletion of scores
        """
        return ToFTest.case_test(dict_)

    @dynamic_test()
    def test9(self):
        """Tests non-existence of scores.txt
        """
        return ToFTest.file_not_exists_test("scores.txt")


if __name__ == '__main__':
    ToFTest().run_tests()
