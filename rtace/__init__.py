from rtace.Tree import Tree as InternalTree
from rtace.Branch import Branch
from rtace.Branched import Branched


class Tree(InternalTree):
    def rebuild(self, branch_id: str):
        return super().rebuild(self.branches[branch_id])

    def data(self, branch_id: str):
        return self.branches[branch_id].data_copy
