import unittest
import os

class TestFileCoverate(unittest.TestCase):

    def testFileCoverage(self):
        for path, dirs, files in os.walk("."):
            # __foo__, foo, testFoo, bar
            file_set = set([filename for filename in files if filename.endswith(".py")])

            # foo, bar
            testable = filter(lambda x:not (x.startswith("_") or x.endswith("_test.py")), file_set)

            # testFoo, testBar
            testFileNames = map(lambda name: "_test.".join(name.split(".")) , testable)

            # expect testFoo and testBar in file_set
            for expectedTest in testFileNames:
                if expectedTest not in file_set:
                    self.fail("{} not found in {}".format(expectedTest, path))

if __name__ == '__main__':
   unittest.main()

