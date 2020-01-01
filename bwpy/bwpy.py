#!/usr/bin/env python

import json
from sh import bw
from .bitwarden.item import BitwardenItem
from .bitwarden.collection import BitwardenCollection


def pull(args):
    bw.sync()

    collection = BitwardenCollection(
        org_name=args.org, collection_name=args.collection,
    )

    print(collection.json(filter=args.item))


def push(args):
    item = BitwardenItem(
        org_name=args.org, collection_name=args.collection, item_name=args.item
    )

    json_data = json.loads(args.json)

    bw.sync()

    if args.force:
        result = item.upsert(json_data)
    else:
        result = item.insert(json_data)

    if not args.silent:
        print(f"successfully pushed item: {args.item} ({result['id']})")

    bw.sync()
