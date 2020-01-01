#!/usr/bin/env python

import json
from dataclasses import dataclass
from sh import bw


@dataclass
class BitwardenOrg:
    org_name: str

    def __org_id(self):
        orgs = json.loads(str(bw.list.organizations()))
        for org in orgs:
            if org["name"] == self.org_name:
                return org["id"]
        raise KeyError(f"organization not found: {org['name']}")

    def __org_collections(self):
        return json.loads(
            str(bw.list("org-collections", "--organizationid", self.__org_id()))
        )
