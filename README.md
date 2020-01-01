# Bitwarden bwcli(1) Wrapper

## About

A wrapper for `bwcli(1)` to simplify interacting with organization collections

## Install

```
pip install .
bwpy --version
```

## Usage

```
# create an item called 'item0' - fail if it already exists
bwpy -o my_org -c secrets push -i item0

# create or update an item called 'item0', set login and password fields
bwpy -o my_org -c secrets push -i item0 -f -j '{"login":{ "username":"rob", "password":"password"}}'

# update of password field for item 'item0'
bwpy -o my_org -c secrets push -i item0 -f -j '{"login":{ "password":"new_password"}}'

# fetch all items in collection
bwpy -o my_org -c secrets pull | jq .

# fetch a specific item from collection
bwpy -o my_org -c secrets pull -i item0| jq .

# pull items and format in 'key = "value"' format
bwpy -o my_org -c secrets pull | jq -r '.[] | "\(.name) = \"\(.login.password)\""'
```
