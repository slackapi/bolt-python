def _is_used_without_argument(args):
    """Tests if a decorator invocation is without () or (args).
    :param args: arguments
    :return: True if it's an invocation without args
    """
    return len(args) == 1
