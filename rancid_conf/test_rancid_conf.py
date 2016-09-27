import unittest
import rancid_conf


# Classe de test pour les methodes de rancid_conf.py
class TestParser(unittest.TestCase):

    def test_get(self):
        content = """
        KEY=VALUE1
        LIST_OF_GROUPS="value1 value2"
        """
        self.assertEqual("value1 value2", rancid_conf.get_value(content, "LIST_OF_GROUPS"))

    def test_set(self):
        content_before = """
        KEY=VALUE1
        LIST_OF_GROUPS="value1 value2"
        """
        content_after = """
        KEY=VALUE1
        LIST_OF_GROUPS="value1 value2 value3"
        """
        ret = rancid_conf.set_value(content_before, "LIST_OF_GROUPS",
                                    rancid_conf.add_group(rancid_conf.get_value(content_before, "LIST_OF_GROUPS"),
                                                          "value3"))
        self.assertEqual(content_after, ret)

    def test_add_group(self):
        old_groups = "group1 group2"
        new_groups = "group1 group2 group3"

        ret = rancid_conf.add_group(old_groups, "group3")
        self.assertEqual(new_groups, ret)

    def test_remove_group(self):
        old_groups = "group1 group2 group3"
        new_groups = "group1 group2"

        ret = rancid_conf.remove_group(old_groups, "group3")
        self.assertEqual(new_groups, ret)

    def test_upade_group(self):
        old_groups = "group1 group2 group3"
        new_groups = "group1 groupTwo group3"

        ret = rancid_conf.update_group(old_groups, "group2", "groupTwo")
        self.assertEqual(new_groups, ret)

if __name__ == '__main__':
    unittest.main()
