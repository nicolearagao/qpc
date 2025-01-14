"""SourceShowCommand is used to show sources for system scans."""

import sys
from logging import getLogger

from requests import codes

from qpc import messages, source
from qpc.clicommand import CliCommand
from qpc.request import GET
from qpc.translation import _
from qpc.utils import pretty_print

logger = getLogger(__name__)


# pylint: disable=too-few-public-methods
class SourceShowCommand(CliCommand):
    """Defines the show command.

    This command is for showing a source which can later be used with a scan
    to gather facts.
    """

    SUBCOMMAND = source.SUBCOMMAND
    ACTION = source.SHOW

    def __init__(self, subparsers):
        """Create command."""
        # pylint: disable=no-member
        CliCommand.__init__(
            self,
            self.SUBCOMMAND,
            self.ACTION,
            subparsers.add_parser(self.ACTION),
            GET,
            source.SOURCE_URI,
            [codes.ok],
        )
        self.parser.add_argument(
            "--name",
            dest="name",
            metavar="NAME",
            help=_(messages.SOURCE_NAME_HELP),
            required=True,
        )

    def _build_req_params(self):
        self.req_params = {"name": self.args.name}

    def _handle_response_success(self):
        json_data = self.response.json()
        count = json_data.get("count", 0)
        results = json_data.get("results", [])
        if count == 1:
            cred_entry = results[0]
            data = pretty_print(cred_entry)
            print(data)
        else:
            logger.error(_(messages.SOURCE_DOES_NOT_EXIST), self.args.name)
            sys.exit(1)
