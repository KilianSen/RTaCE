# RTaCE Reversible Traceable Automatic Code Execution 

A small project to demonstrate the use of the Python `__getattribute__` and `__setattr__` methods to create a simple
tool for tracing the state of an object and its method calls.


## Example

```python
import copy
import logging
from rtace import *


logging.basicConfig(level=logging.INFO)


class TestCase(Branched):
    value = 0

    def add_one(self):
        self.value += 1


if __name__ == '__main__':
    test_object = TestCase()

    branch_id = None
    test_branch_id = 0

    first_object = copy.copy(test_object)
    first_branch = test_object.current_branch
    for i in range(100):
        branch_id = test_object.current_branch

        if i == 69:
            test_branch_id = test_object.current_branch

        test_object.add_one()

    reconstructed_object = Tree().rebuild(test_branch_id)
    reconstructed_object2 = Tree().rebuild(test_branch_id)

    print()
    print('Conducting test')
    print('----------------------')
    print(f'Newest Branch {branch_id}\nTest branch   {test_branch_id}\nFirst branch  {test_branch_id}')
    print('----------------------')
    print(f'First State         {first_object} {first_object.value}')
    print(f'Current State       {test_object} {test_object.value}')
    print(f'Reconstructed State {reconstructed_object} {reconstructed_object.value}')
    print(f'Reconstructed State {reconstructed_object2} {reconstructed_object2.value}')


    del test_object
```
