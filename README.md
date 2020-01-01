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
# force create an item called 'item0'
bwpy -o my_org -c secrets push -i item0 -j '{"login":{ "username":"rob", "password":"password"}}'

# force update of password field for item 'item0'
bwpy -o my_org -c secrets push -i item0 -f -j '{"login":{ "password":"new_password"}}'

# fetch all items in collection
bwpy -o my_org -c secrets pull | jq .

# fetch a specific item from collection
bwpy -o my_org -c secrets pull -i item0| jq .
```
