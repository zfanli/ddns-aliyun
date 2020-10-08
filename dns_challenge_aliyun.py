import pprint
import json
import yaml
import sys

# import sqlite3
import requests

# import api utils

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import (
    DescribeDomainRecordsRequest,
)
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import (
    UpdateDomainRecordRequest,
)

# global variables
config = {}


def read_config():
    """read config from file"""
    with open("config.yml", "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def update_domain_record(client, rid, value):
    """update specific domain record"""
    request = UpdateDomainRecordRequest()
    request.set_accept_format("json")

    request.set_RecordId(rid)
    request.set_RR("_acme-challenge")
    request.set_Type("TXT")
    request.set_Value(value)

    return client.do_action_with_exception(request)


def make_client():
    """create an api client with config"""
    return AcsClient(config["id"], config["secret"], config["loc"])


def query_domain_records(client):
    """query for all domain records"""
    request = DescribeDomainRecordsRequest()
    request.set_accept_format("json")

    request.set_DomainName(config["domain"])

    return client.do_action_with_exception(request)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} challenge-value")
        exit(-1)

    value = sys.argv[1]

    # read config
    config = read_config()
    config = config["config"]

    # setup client
    client = make_client()

    # query records
    records = query_domain_records(client)
    records = json.loads(records)["DomainRecords"]["Record"]
    rid = ""
    for r in records:
        if r["RR"] == "_acme-challenge":
            rid = r["RecordId"]
    # print(rid)

    # update challenge record
    print("Update challenge to", value)
    update_domain_record(client, rid, value)

