import sys
import unittest
import random
from rtace import *


class BranchedModification(Branched):

    def __init__(self, value):
        super().__init__()
        self.value = value

    def modify(self):
        pass  # This method will be overridden by subclasses


class TestcaseAddition(BranchedModification):

    def __init__(self):
        super().__init__(0)

    def modify(self):
        self.value += 1


class TestcaseMultiplication(BranchedModification):

    def __init__(self):
        super().__init__(1)

    def modify(self):
        self.value *= 2


class TestcaseRandom(BranchedModification):

    def __init__(self):
        super().__init__(1)

    def modify(self):
        self.value *= random.randint(1, 5)


class TestcaseRandomWithSeed(BranchedModification):

    def __init__(self):
        super().__init__(1)
        self.rng_seed = random.randrange(sys.maxsize)

    def modify(self):
        self.value *= random.Random(self.rng_seed).randint(1, 5)


class TestBasic(unittest.TestCase):

    @staticmethod
    def check_reconstruction(test_object, should_value_change):
        branch_id = None
        test_branch_id = 0
        for i in range(100):
            branch_id = test_object.current_branch

            if i == 69:
                test_branch_id = test_object.current_branch

            test_object.modify()

        reconstructed_object = Tree().rebuild(test_branch_id)
        reconstructed_object2 = Tree().rebuild(test_branch_id)

        assert reconstructed_object != reconstructed_object2
        if should_value_change:
            assert reconstructed_object.value != reconstructed_object2.value
        else:
            assert reconstructed_object.value == reconstructed_object2.value

    def test_add_one(self):
        test_object = TestcaseAddition()
        self.check_reconstruction(test_object, False)

    def test_multi(self):
        test_object = TestcaseMultiplication()
        self.check_reconstruction(test_object, False)

    def test_fail_random(self):
        test_object = TestcaseRandom()
        self.check_reconstruction(test_object, True)

    def test_random_with_seed(self):
        test_object = TestcaseRandomWithSeed()
        self.check_reconstruction(test_object, False)


if __name__ == '__main__':
    unittest.main()