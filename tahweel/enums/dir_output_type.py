from enum import Enum


class DirOutputType(Enum):
  TREE_TO_TREE = 'tree_to_tree'
  SIDE_BY_SIDE = 'side_by_side'

  def __str__(self):
    return self.value
