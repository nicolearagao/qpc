# Copyright (c) 2022 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 3 (GPLv3). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv3
# along with this software; if not, see
# https://www.gnu.org/licenses/gpl-3.0.txt.
#
"""Test openshift cred list in CLI."""
import json
import sys

from qpc.cli import CLI
from qpc.cred import CREDENTIAL_URI, OPENSHIFT_CRED_TYPE
from qpc.utils import get_server_location


class TestOpenShiftListCredential:
    """Class for testing OpenShift list credential."""

    def test_list_filtered_cred_data(
        self,
        capsys,
        requests_mock,
    ):
        """Test if cred list returns ocp creds."""
        url = get_server_location() + CREDENTIAL_URI
        openshift_cred_1 = {
            "id": 1,
            "name": "openshift_1",
            "cred_type": OPENSHIFT_CRED_TYPE,
            "token": "********",
        }
        openshift_cred_2 = {
            "id": 2,
            "name": "openshift_2",
            "cred_type": OPENSHIFT_CRED_TYPE,
            "token": "********",
        }
        results = [openshift_cred_1, openshift_cred_2]
        data = {"count": 2, "results": results}
        requests_mock.get(url, status_code=200, json=data)
        sys.argv = [
            "/bin/qpc",
            "cred",
            "list",
            "--type",
            OPENSHIFT_CRED_TYPE,
        ]
        CLI().main()
        expected_dict = [
            {
                "cred_type": "openshift",
                "id": 1,
                "name": "openshift_1",
                "token": "********",
            },
            {
                "cred_type": "openshift",
                "id": 2,
                "name": "openshift_2",
                "token": "********",
            },
        ]
        out, err = capsys.readouterr()
        out_as_dict = json.loads(out)
        assert out_as_dict == expected_dict
        assert err == ""