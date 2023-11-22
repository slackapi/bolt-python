import sys
from types import TracebackType
from typing import Optional

from slack_bolt.cli.error import CliError

RED = '\033[1;31m'
RESET_COLOR = '\033[m'

def excepthook(type: type[BaseException], value: BaseException, traceback: Optional[TracebackType]):
	if type == CliError:
		sys.stderr.write(f"{RED}error{RESET_COLOR}: {value}")
		traceback.tb_frame.
		if traceback
	else:
		sys.__excepthook__(type, value, traceback)

sys.excepthook = excepthook

