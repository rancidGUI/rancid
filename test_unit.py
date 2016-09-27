from rancid_conf import test_rancid_conf
from router_db  import test_router_db
import unittest

def suite():
   test_suite = unittest.TestSuite()
   test_suite.addTests(unittest.makeSuite(test_rancid_conf.TestParser))
   test_suite.addTests(unittest.makeSuite(test_router_db.TestParser))
   return test_suite

all_test = suite()

unittest.TextTestRunner(verbosity=2).run(all_test)
