#!/usr/bin/env python

import json
from dataclasses import dataclass
from sh import bw
from .org import BitwardenOrg


@dataclass
class BitwardenCollection(BitwardenOrg):
    collection_name: str

    def collection_id(self):
        for collection in self.org_collections():
            if collection["externalId"] == self.collection_name:
                return collection["id"]
        raise KeyError(f"collection not found: {self.collection_name}")

    def collection_items(self):
        return json.loads(str(bw.list.items("--collectionid", self.collection_id())))

    def json(self, filter=None):
        items = []
        for item in self.collection_items():
            if (not filter) or (filter and filter == item["name"]):
                items.append(item)
        if not items:
            raise KeyError(
                f"no items found for collection: {self.collection_name}, filter: {filter}"
            )
        return json.dumps(items)
