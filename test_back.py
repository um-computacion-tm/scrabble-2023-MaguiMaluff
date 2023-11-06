import unittest
from unittest.mock import patch, builtins
from back import Back, InvalidTask

class TestBack(unittest.TestCase):
    @patch.object(builtins, 'print')
    @patch('builtins.input', side_effect = ["A", "C", "P", "a",])
    def test_get_task(self, mock_input, mock_print):
        back = Back()

        task = back.get_task()
        self.assertEqual(task, "A")
        task = back.get_task()
        self.assertEqual(task, "C")
        task = back.get_task()
        self.assertEqual(task, "P")
        task = back.get_task()
        self.assertEqual(task, "A")


if __name__ == '__main__':
    unittest.main()