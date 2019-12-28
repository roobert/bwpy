#!/usr/bin/env python

import json
from dataclasses import dataclass
from sh import bw, echo
from .bitwarden_org import BitwardenOrg


@dataclass
class BitwardenCollection(BitwardenOrg):
    collection_name: str

    def collection_id(self):
        for collection in self.org_collections():
            if collection["externalId"] == self.collection_name:
                return collection["id"]
        return None

    def collection_items(self):
        # FIXME: check for exit status and print out stderr/stdout
        return json.loads(str(bw.list.items("--collectionid", self.collection_id())))

    def __str__(self):
        lines = ""
        for item in self.collection_items():
            if not item["login"]["username"]:
                raise KeyError(f"missing 'username' key for item: {item['name']}")

            if not item["login"]["password"]:
                raise KeyError(f"missing 'password' key for item: {item['name']}")

            lines += f"{item['login']['username']} = \"{item['login']['password']}\"\n"
        return lines.rstrip()
