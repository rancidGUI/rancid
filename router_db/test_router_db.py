import unittest
import router_db


# Classe de test pour les methodes de router_db.py
class TestParser(unittest.TestCase):

    def test_get_machine_index(self):
        machines = [
            ['127.0.0.1', 'cisco', 'down'],
            ['127.0.0.10', 'cisco', 'up'],
            ['127.0.0.100', 'cisco', 'down']
        ]

        self.assertEqual(1, router_db.get_machine_index(machines, '127.0.0.10'))

    def test_remove_machine(self):
        machines = [
            ['127.0.0.1', 'cisco', 'down'],
            ['127.0.0.10', 'cisco', 'up']
        ]
        machines_after_remove = [
            ['127.0.0.1', 'cisco', 'down']
        ]

        self.assertEqual(machines_after_remove, router_db.remove_machine(machines, 1))

    def test_update_machine(self):
        old_machine = [
            ['127.0.0.10', 'cisco', 'up']
        ]
        new_machine = [
            ['84.32.154.10', 'cisco', 'up']
        ]
        self.assertEqual(new_machine, router_db.update_machine(old_machine, '127.0.0.10', '84.32.154.10'))

    def test_update_type(self):
        old_type = [
            ['127.0.0.10', 'cisco', 'up']
        ]
        new_type = [
            ['127.0.0.10', 'extreme', 'up']
        ]
        self.assertEqual(new_type, router_db.update_type(old_type, '127.0.0.10', 'extreme'))

    def test_update_status(self):
        old_status = [
            ['127.0.0.10', 'cisco', 'up']
        ]
        new_status = [
            ['127.0.0.10', 'cisco', 'down']
        ]
        self.assertEqual(new_status, router_db.update_status(old_status, '127.0.0.10', 'down'))

if __name__ == '__main__':
    unittest.main()
