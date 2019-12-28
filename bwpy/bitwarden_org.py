#!/usr/bin/env python

import json
from dataclasses import dataclass
from sh import bw, echo


@dataclass
class BitwardenOrg:
    org_name: str

    def org_id(self):
        # FIXME: check for exit status and print out stderr/stdout
        orgs = json.loads(str(bw.list.organizations()))
        for org in orgs:
            if org["name"] == self.org_name:
                return org["id"]
        return None

    def org_collections(self):
        # FIXME: check for exit status and print out stderr/stdout
        return json.loads(
            str(bw.list("org-collections", "--organizationid", self.org_id()))
        )
