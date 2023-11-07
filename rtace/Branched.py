import uuid
import logging
from rtace.Tree import Tree


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Branched:
    current_branch: str = None
    branch_propagation: bool = True

    def __init__(self, branching_id: int = None):
        if branching_id is None:
            self.branching_id = int(str(uuid.uuid4().int)[:8])
            logger.debug(f'Generated new branching ID: {self.branching_id}')
        self.branching_id = branching_id
        logger.debug('Set branching ID: {}'.format(self.branching_id))

    def __getattribute__(self, name):
        try:
            attr = object.__getattribute__(self, name)

            if (attr is not None and attr.__class__.__name__ in ["method", "builtin_function_or_method"] and
                    (attr.__name__ == "__reduce_ex__" or attr.__name__ == "__getstate__")):
                return attr

            if callable(attr) and object.__getattribute__(self, "branch_propagation"):
                def intercept(*args, **kwargs):
                    try:
                        logger.debug(f'Branch off called with name {name}, args: {args}, kwargs: {kwargs}')
                        Tree().branch_off(self, attr, args, kwargs)
                        result = attr(*args, **kwargs)
                        return result
                    except Exception as ex:
                        logger.exception(f'Exception raised in intercept method {ex}')
                        raise ex

                return intercept
            else:
                return attr
        except Exception as e:
            raise e
