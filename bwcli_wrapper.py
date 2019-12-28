#!/usr/bin/env python
# pylint: skip-file


from dataclasses import dataclass
from pprint import pprint
import json
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
            str(
                bw.list(
                    "org-collections", "--organizationid", self.org_id(self.org_name)
                )
            )
        )


@dataclass
class BitwardenCollection(BitwardenOrg):
    collection_name: str

    def collection_id(self):
        for collection in self.org_collections(self.org_name):
            if collection["externalId"] == self.collection_name:
                return collection["id"]
        return None

    def collection_items(self):
        # FIXME: check for exit status and print out stderr/stdout
        return json.loads(
            str(
                bw.list.items(
                    "--collectionid",
                    self.collection_ids(self.org_name, self.collection_name),
                )
            )
        )

    def __str__(self):
        for item in self.collection_items(self.org_name, collection_id()):
            print(f"{item['login']['username']} = \"{item['login']['password']}\"")


@dataclass
class BitwardenItem(BitwardenCollection):
    item_name: str

    @staticmethod
    def item_template():
        return json.loads(str(bw.get.template.item()))

    @staticmethod
    def login_template():
        # FIXME: check for exit status and print out stderr/stdout
        return json.loads(str(bw.get.template("item.login")))

    def new_item(self, item_name, password):
        login_template = login_template()
        login_template["username"] = item_name
        login_template["password"] = password
        login_template["totp"] = ""

        item_template = self.item_template()
        item_template["login"] = login_template
        item_template["name"] = item_name
        item_template["notes"] = ""

        return item_template

    def create_item(self, item):
        result = bw.create.item(bw.encode(echo(json.dumps(item))))
        # FIXME: check for exit status and print out stderr/stdout
        return json.loads(str(result.stdout, "utf-8").rstrip())

    def edit_item(self, new_item_data, existing_item_id):
        result = bw.edit.item(
            existing_item_id, bw.encode(echo(json.dumps(new_item_data)))
        )
        # FIXME: check for exit status and print out stderr/stdout
        return json.loads(str(result.stdout, "utf-8").rstrip())

    def share_item(self, item):
        collection_ids = [collection_id(org_name, collection_name)]
        item_id = item["id"]
        # FIXME: check for exit status and print out stderr/stdout
        return bw.share(
            item_id, org_id(org_name), bw.encode(echo(json.dumps(collection_ids)))
        )

    def check_for_existing(self):
        items = collection_items(org_name, collection_name)
        item_names = [item for item in items if item["name"] == item_name]

        if item_names.count() > 1:
            raise Exception(f"multiple entries found for name: {item_name}")

    def upsert(self, item_key, item_value):

        # FIXME: split out into update / insert

        for item in collection_items(org_name, collection_name):
            if item["name"] == item_name:
                print(f"updating existing item: {item['id']}")
                new_item_data = self.new_item(item_name, password)
                new_item_data["login"] = item["login"]
                new_item_data["login"][item_key] = item_value
                result = self.edit_item(new_item_data, item["id"])
                return result

        print(f"creating new item..")
        item = self.create_item(new_item(item_name, password))
        result = self.share_item(item)
        return item


def main():
    org_name = ""
    collection_name = "terraform"
    item_name = "test_name"

    print(bw.sync())

    # print(upsert(org_name, collection_name, item_name, password))

    # item = BitwardenItem(
    #    org_name=org_name, collection_name=collection_name, item_name=item_name
    # )

    collection = BitwardenCollection(org_name=org_name, collection_name=collection_name)
    print(collection)

    # item.upsert("password", "test2")


if __name__ == "__main__":
    main()
