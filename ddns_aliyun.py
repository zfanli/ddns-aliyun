import pprint
import json
import yaml

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


def get_ip():
    """get current public ip"""
    return requests.get("http://ip.cip.cc").text.strip()


# def database():
#     """connect to sqlite and get a cursor to execute sql"""
#     conn = sqlite3.connect("ip.db")
#     return conn


# def ensure_database():
#     """ensure ip table exists"""
#     conn = database()
#     cursor = conn.cursor()
#     cursor.execute(
#         "select count(*) from sqlite_master where type='table' and name = 'ip'"
#     )
#     if cursor.fetchall()[0][0] == 0:
#         cursor.execute(
#             """CREATE TABLE `ip` (
#                 `ip` varchar(15) NOT NULL,
#                 `current` var(1) NOT NULL,
#                 `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
#                 PRIMARY KEY (`ip`)
#             )"""
#         )
#     cursor.close()
#     return conn


# def is_current_ip(conn, ip):
#     cursor = conn.cursor()
#     cursor.execute(f"select count(*) from ip where ip='{ip}' and current='1'")
#     result = cursor.fetchall()[0][0] == 1
#     cursor.close()
#     return result


# def write_new_ip(conn, ip):
#     cursor = conn.cursor()
#     cursor.execute("UPDATE ip SET current='0' WHERE current='1'")
#     cursor.execute(f"INSERT INTO ip (IP, CURRENT) VALUES('{ip}', '1')")
#     conn.commit()
#     cursor.close()


# def is_ip_changed(ip):
#     conn = ensure_database()
#     result = False
#     if not is_current_ip(conn, ip):
#         write_new_ip(conn, ip)
#         result = True
#     conn.close()
#     return result


def query_domain_records(client):
    """query for all domain records"""
    request = DescribeDomainRecordsRequest()
    request.set_accept_format("json")

    request.set_DomainName(config["domain"])

    return client.do_action_with_exception(request)


def update_domain_record(client, ip, record):
    """update specific domain record"""
    request = UpdateDomainRecordRequest()
    request.set_accept_format("json")

    request.set_RecordId(record["RecordId"])
    request.set_RR(record["RR"])
    request.set_Type(record["Type"])
    request.set_Value(ip)

    return client.do_action_with_exception(request)


def make_client():
    """create an api client with config"""
    return AcsClient(config["id"], config["secret"], config["loc"])


if __name__ == "__main__":
    # read config
    config = read_config()
    rr_list = config["rr_list"]
    config = config["config"]

    # setup client
    client = make_client()

    ip = get_ip()
    # if is_ip_changed(ip):
    #     # query domain records
    #     records = query_domain_records(client)
    #     records = json.loads(records)["DomainRecords"]["Record"]
    #     for r in records:
    #         if r["RR"] in rr_list:
    #             update_domain_record(client, ip, r)
    #             print(r["RR"])

    # query domain records
    records = query_domain_records(client)
    records = json.loads(records)["DomainRecords"]["Record"]
    for r in records:
        if r["Type"] == "A" and r["RR"] in rr_list and r["Value"] != ip:
            update_domain_record(client, ip, r)
            print(r["RR"])

