import uuid
import copy
import logging

from rtace.TSSingleton import Singleton
from rtace.Branch import Branch


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Tree(Singleton):
    branches: {str: Branch} = {}

    def branch_off(self, instance, func: callable, args, kwargs):
        new_branch = uuid.uuid4().hex[:8]

        while new_branch in self.branches:
            new_branch = uuid.uuid4().hex[:8]

        logger.debug(f'Branch {new_branch} has been created.')

        self.branches[new_branch] = \
            Branch(
                Tree.branches[instance.current_branch] if instance.current_branch is not None else None,
                func, args, kwargs, copy.deepcopy(instance)
            )
        instance.current_branch = new_branch

    @staticmethod
    def rebuild(branch_instance: Branch):
        logger.info(f'Rebuilding {branch_instance}...')

        brb = branch_instance

        function_stack: [(callable, list, dict)] = []

        while isinstance(brb, Branch):
            function_stack.append((brb.function, brb.args, brb.kwargs))
            if not isinstance(brb.origin, Branch):
                brb = brb.data_copy
            else:
                brb = brb.origin

        primal = copy.copy(brb)
        logger.debug(f'{branch_instance} found primal {primal}')
        object.__setattr__(primal, "branch_propagation", True)

        backtracking_stack = list(reversed(function_stack))
        for f in backtracking_stack:
            f[0].__func__(primal, *f[1], **f[2])

        primal.branch_propagation = True
        logger.info(f'{branch_instance} has been rebuilt successfully.')

        return primal
