"""Warnings by Bolt for Python

Developers can ignore the following warning categories as necessary.
see also: https://docs.python.org/3/library/warnings.html#default-warning-filter
"""


class BoltCodeWarning(UserWarning):
    """Warning to help developers notice their coding errors.
    This warning should not be used for informing configuration errors in the App/AsyncApp constructor.
    """
