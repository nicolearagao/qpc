"""ScanListCommand is used to list system scans."""

import sys
import urllib.parse as urlparse
from logging import getLogger

from requests import codes

from qpc import messages, scan
from qpc.clicommand import CliCommand
from qpc.request import GET
from qpc.scan.utils import get_scan_object_id
from qpc.translation import _
from qpc.utils import pretty_print

logger = getLogger(__name__)


# pylint: disable=too-few-public-methods
class ScanJobCommand(CliCommand):
    """Defines the job command.

    This command is for listing the existing scan jobs for each scan.
    """

    SUBCOMMAND = scan.SUBCOMMAND
    ACTION = scan.JOB

    def __init__(self, subparsers):
        """Create command."""
        # pylint: disable=no-member
        CliCommand.__init__(
            self,
            self.SUBCOMMAND,
            self.ACTION,
            subparsers.add_parser(self.ACTION),
            GET,
            scan.SCAN_URI,
            [codes.ok],
        )
        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--name", dest="name", metavar="NAME", help=_(messages.SCAN_NAME_HELP)
        )
        group.add_argument(
            "--id", dest="id", metavar="ID", help=_(messages.SCAN_JOB_ID_HELP)
        )
        self.parser.add_argument(
            "--status",
            dest="status",
            choices=[
                scan.SCAN_STATUS_CREATED,
                scan.SCAN_STATUS_PENDING,
                scan.SCAN_STATUS_RUNNING,
                scan.SCAN_STATUS_PAUSED,
                scan.SCAN_STATUS_CANCELED,
                scan.SCAN_STATUS_COMPLETED,
                scan.SCAN_STATUS_FAILED,
            ],
            metavar="STATUS",
            help=_(messages.SCAN_STATUS_FILTER_HELP),
            required=False,
        )

    def _validate_args(self):
        """Validate the scan job arguments."""
        CliCommand._validate_args(self)
        if self.args.id and self.args.name:
            self.parser.print_usage()
            sys.exit(1)
        if self.args.id and self.args.status:
            logger.info(_(messages.SCAN_JOB_ID_STATUS))
            self.parser.print_usage()
            sys.exit(1)

    def _build_req_params(self):
        """Add filter by scan_type/state query param."""
        if "name" in self.args and self.args.name:
            found, scan_object_id = get_scan_object_id(self.parser, self.args.name)
            if found:
                self.req_path += scan_object_id + "jobs/"
            else:
                sys.exit(1)
        if "id" in self.args and self.args.id:
            self.req_path = scan.SCAN_JOB_URI + str(self.args.id) + "/"
        if "status" in self.args and self.args.status:
            self.req_params = {"status": self.args.status}

    def _handle_response_success(self):
        # pylint: disable=no-member
        if self.response.status_code in [codes.ok]:
            json_data = self.response.json()
            count = json_data.get("count", 0)
            results = json_data.get("results", [])
            if count == 0:
                # if GET is used for single scan job,
                # count doesn't exist and will be 0
                if "id" in self.args and self.args.id:
                    data = pretty_print(json_data)
                    print(data)
                else:
                    logger.error(_(messages.SCAN_LIST_NO_SCANS))
                    sys.exit(1)
            else:
                data = pretty_print(results)
                print(data)
            if json_data.get("next"):
                next_link = json_data.get("next")
                params = urlparse.parse_qs(urlparse.urlparse(next_link).query)
                page = params.get("page", ["1"])[0]
                if self.req_params:
                    self.req_params["page"] = page
                else:
                    self.req_params = {"page": page}
                input(_(messages.NEXT_RESULTS))
                self._do_command()
        else:
            logger.error(_(messages.SCAN_LIST_NO_SCANS))
            sys.exit(1)
