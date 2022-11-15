import argparse
import json
import random
import socket
import string

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from time import sleep

import requests
import sys

from sanity_util import COLLECTION, IVERSON, JOULE, WIN_INT_PORT, WIN_EXT_PORT, HOST_PORT, \
    EMB_INT_PORT, EMB_EXT_PORT, HOST_WIN_COL, HOST_LINUX_COL, EMB_COL, CONTAINER_DVWA, CONTAINER_MOCK, \
    CONTAINER_PORT_MOCK, CONTAINER_PORT_DVWA, KEPLER, OOB, AWS_COL, AWS_PORT, LAGRANGE

console_ip = ""
app_ip = ""
app_url = ""
defender_type = ""
offset = 0
latest_rule = {}
console_version = ""
IVERSON_VERSION = 2104439
JOULE_VERSION = 2201882
KEPLER_VERSION = 2201883
LAGRANGE_VERSION = 2210352
windows = False
customer_id = None
mock = False
oob_type = None
version = ""


def get_auth():
    if customer_id is None:
        return ('ashtrahman', 'Pa$$word1')
    else:
        return ('ahaytovich@paloaltonetworks.com', 'jEZ255V88Nyhxcr!')


def get_console_version():
    global console_version
    global latest_rule
    if customer_id is None:
        url = f"https://{console_ip}:8083/api/v1/version"
    else:
        url = f"https://staging-consoles.cloud.twistlock.com/{customer_id}/api/v1/version"
    response = requests.get(url, auth=get_auth(), verify=False)

    if response.status_code == 200:
        # version received like this '"yy.mm.xxx"' - convert it to a number yymmxxx
        version = response.text
        version = version[1:-1].rsplit(".")
        version_number = int("".join(version))

        if version_number > LAGRANGE_VERSION:
            latest_rule = json.loads(LAGRANGE)
        elif version_number > KEPLER_VERSION:
            latest_rule = json.loads(KEPLER)
        elif version_number > JOULE_VERSION:
            latest_rule = json.loads(JOULE)
        elif version_number > IVERSON_VERSION:
            latest_rule = json.loads(IVERSON)
        else:
            print("Unsupported console version")
            sys.exit()
    else:
        print("Could not get console version number")
        sys.exit()


def create_collection():
    collection = json.loads(COLLECTION)

    if defender_type == "host" or oob_type == "host":
        if windows:
            collection["hosts"] = [HOST_WIN_COL]
            collection["name"] = "waas-windows"
        else:
            collection["hosts"] = [HOST_LINUX_COL]
            collection["name"] = "waas-host"
    elif defender_type == "container" or oob_type == "container":
        if mock:
            collection["images"] = [CONTAINER_MOCK]
            collection["name"] = "waas-container-mock"
        else:
            collection["images"] = [CONTAINER_DVWA]
            collection["name"] = "waas-container-dvwa"
    elif defender_type == "out-of-band" or oob_type == "aws":
        collection["hosts"] = [AWS_COL]
        collection["name"] = "waas-aws"
    else:
        collection["appIDs"] = [EMB_COL]
        collection["name"] = "waas-appEmbedded"

    if customer_id is None:
        url = f"https://{console_ip}:8083/api/v1/collections"
    else:
        url = f"https://staging-consoles.cloud.twistlock.com/{customer_id}/api/v1/collections"
    response = requests.post(url, json=collection, auth=get_auth(), verify=False)
    if response.status_code == 200:
        print("Collection created successfully")
    elif response.status_code == 409:
        print("Collection is already existed")
    else:
        print("Error creating collection: " + str(response))


def create_waas_network_list():
    if customer_id is None:
        url = f"https://{console_ip}:8083/api/v1/policies/firewall/app/network-list"
    else:
        url = f"https://staging-consoles.cloud.twistlock.com/{customer_id}/api/v1/policies/firewall/app/network-list"
    body = '{"_id":"waas-network-list","subnets":["1.1.1.1"]}'
    response = requests.post(url, auth=get_auth(), data=body, verify=False)

    if response.status_code == 200:
        print("Network list created successfully")
    elif response.status_code == 409:
        print("Network list is already existed")
    else:
        print("Error creating network list: " + str(response))

    # get local ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]

    body2 = json.loads('{"_id":"","subnets":[""]}')
    body2["_id"] = f"local-ip-{defender_type}-{offset}"
    if defender_type == "app-embedded":
        body2["subnets"] = [f"{local_ip}", "31.154.166.148"]  # fargate always get this ip
    else:
        body2["subnets"] = [f"{local_ip}"]
    response = requests.post(url, auth=get_auth(), json=body2, verify=False)

    if response.status_code == 200:
        print("Network list created successfully")
    elif response.status_code == 409:
        print("Network list is already existed")
    else:
        print("Error creating network list: " + str(response))


def create_waas_custom_rules():
    if customer_id is None:
        url = f"https://{console_ip}:8083/api/v1/custom-rules"
    else:
        url = f"https://staging-consoles.cloud.twistlock.com/{customer_id}/api/v1/custom-rules"
    response = requests.get(url, auth=get_auth(), verify=False)
    res = response.json()
    global offset
    offset = res[len(res) - 1]["_id"] + 1

    request_custom_rule = json.loads('{"_id":1,"type":"waas-request","name":"request-custom-rule-for-sanity","message":"%req.http_method is denied","script":"req.http_method = \\"GET\\""}')
    request_custom_rule["_id"] = offset
    request_custom_rule["name"] = f"request-custom-rule-for-sanity{offset}"

    if customer_id is None:
        url = f"https://{console_ip}:8083/api/v1/custom-rules/{offset}"
    else:
        url = f"https://staging-consoles.cloud.twistlock.com/{customer_id}/api/v1/custom-rules/{offset}"
    response = requests.put(url, auth=get_auth(), json=request_custom_rule, verify=False)
    if response.status_code == 200:
        print("Custom rule created successfully")
    else:
        print("Error creating Custom Rule: " + str(response))

    response_custom_rule = json.loads('{"_id":1,"type":"waas-response","name":"response-custom-rule-for-sanity","message":"%resp.status_code is denied","script":"resp.status_code = 200"}')
    response_custom_rule["_id"] = offset + 1
    response_custom_rule["name"] = f"response-custom-rule-for-sanity{offset + 1}"

    if customer_id is None:
        url = f"https://{console_ip}:8083/api/v1/custom-rules/{offset + 1}"
    else:
        url = f"https://staging-consoles.cloud.twistlock.com/{customer_id}/api/v1/custom-rules/{offset + 1}"
    response = requests.put(url, auth=get_auth(), json=response_custom_rule, verify=False)
    if response.status_code == 200:
        print("Custom rule created successfully")
    else:
        print("Error creating Custom Rule: " + str(response))

    request_custom_rule_body = json.loads('{"_id":1,"type":"waas-request","name":"request-custom-rule-for-sanity-body","message":"%regexMatches in %req.http_method has this body: %req.body","script":"req.http_method contains /^P/ and lowercase(req.body) contains \\"{\\\\\\"coco\\\\\\":\\\\\\"momo\\\\\\"}\\""}')
    request_custom_rule_body["_id"] = offset + 2
    request_custom_rule_body["name"] = f"request-custom-rule-for-sanity-body{offset + 2}"

    if customer_id is None:
        url = f"https://{console_ip}:8083/api/v1/custom-rules/{offset + 2}"
    else:
        url = f"https://staging-consoles.cloud.twistlock.com/{customer_id}/api/v1/custom-rules/{offset + 2}"
    response = requests.put(url, auth=get_auth(), json=request_custom_rule_body, verify=False)
    if response.status_code == 200:
        print("Custom rule created successfully")
    else:
        print("Error creating Custom Rule: " + str(response))


def update_rule(rule, update_reason):
    global latest_rule
    latest_rule = rule

    if customer_id is None:
        url = f"https://{console_ip}:8083/api/v1/policies/firewall/app/{defender_type}"
    else:
        url = f"https://staging-consoles.cloud.twistlock.com/{customer_id}/api/v1/policies/firewall/app/{defender_type}"

    response = requests.put(url, json=latest_rule, auth=get_auth(), verify=False)
    if response.status_code == 200:
        print(f"{update_reason} - Rule updated successfully")
        sleep(5)
    else:
        print(f"{update_reason} - Error creating rule: " + str(response))


def create_rule():
    rule = latest_rule
    if defender_type == "host":
        rule["_id"] = "hostAppFirewall"
        if windows:
            rule["rules"][0]["applicationsSpec"][0]["appID"] = "app-win"
            rule["rules"][0]["applicationsSpec"][0]["apiSpec"]["endpoints"][0]["internalPort"] = WIN_INT_PORT
            rule["rules"][0]["applicationsSpec"][0]["apiSpec"]["endpoints"][0]["exposedPort"] = WIN_EXT_PORT
            rule["rules"][0]["collections"][0]["name"] = "waas-windows"
            rule["rules"][0]["name"] = "waas-windows"
            rule["rules"][0]["windows"] = True
        else:
            rule["rules"][0]["applicationsSpec"][0]["appID"] = "app-host"
            rule["rules"][0]["applicationsSpec"][0]["apiSpec"]["endpoints"][0]["internalPort"] = HOST_PORT
            rule["rules"][0]["collections"][0]["name"] = "waas-host"
            rule["rules"][0]["name"] = "waas-host"

    elif defender_type == "container":
        rule["_id"] = "containerAppFirewall"
        rule["rules"][0]["applicationsSpec"][0]["appID"] = "app-con"
        if mock:
            rule["rules"][0]["applicationsSpec"][0]["apiSpec"]["endpoints"][0]["internalPort"] = CONTAINER_PORT_MOCK
            rule["rules"][0]["collections"][0]["name"] = "waas-container-mock"
        else:
            rule["rules"][0]["applicationsSpec"][0]["apiSpec"]["endpoints"][0]["internalPort"] = CONTAINER_PORT_DVWA
            rule["rules"][0]["collections"][0]["name"] = "waas-container-dvwa"
        rule["rules"][0]["name"] = "waas-container"
        rule['rules'][0]['collections'][0]["images"] = ["*dvwa*"]

    elif defender_type == "out-of-band":
        rule["_id"] = "outOfBandAppFirewall"
        rule["rules"][0]["applicationsSpec"][0]["appID"] = "app-oob"
        if oob_type == "container":
            rule["rules"][0]["applicationsSpec"][0]["apiSpec"]["endpoints"][0]["internalPort"] = CONTAINER_PORT_MOCK
            rule["rules"][0]["collections"][0]["name"] = "waas-container-mock"
            rule["rules"][0]["name"] = "oob-container"
            rule["rules"][0]["outOfBandScope"] = "container"
        elif oob_type == "host":
            rule["rules"][0]["applicationsSpec"][0]["apiSpec"]["endpoints"][0]["internalPort"] = HOST_PORT
            rule["rules"][0]["collections"][0]["name"] = "waas-host"
            rule["rules"][0]["name"] = "oob-host"
            rule["rules"][0]["outOfBandScope"] = "host"
        else:
            rule["rules"][0]["applicationsSpec"][0]["apiSpec"]["endpoints"][0]["internalPort"] = AWS_PORT
            rule["rules"][0]["collections"][0]["name"] = "waas-aws"
            rule["rules"][0]["name"] = "oob-aws"
        rule = handle_oob(rule)

    else:
        rule["_id"] = "appEmbeddedAppFirewall"
        rule["rules"][0]["applicationsSpec"][0]["appID"] = "app-emb"
        rule["rules"][0]["applicationsSpec"][0]["apiSpec"]["endpoints"][0]["internalPort"] = EMB_INT_PORT
        rule["rules"][0]["applicationsSpec"][0]["apiSpec"]["endpoints"][0]["exposedPort"] = EMB_EXT_PORT
        rule["rules"][0]["collections"][0]["name"] = "waas-appEmbedded"
        rule["rules"][0]["name"] = "waas-appEmbedded"

    rule["rules"][0]["applicationsSpec"][0]["customRules"] = [
                                                                {"_id": offset, "effect": "disable"},
                                                                {"_id": offset + 1, "effect": "disable"},
                                                                {"_id": offset + 2, "effect": "disable"}]
    update_rule(rule, "Create WAAS rule")
    return rule


def handle_oob(rule):
    rule['rules'][0]['applicationsSpec'][0]['sqli']['effect'] = "alert"
    rule['rules'][0]['applicationsSpec'][0]['xss']['effect'] = "alert"
    rule['rules'][0]['applicationsSpec'][0]['attackTools']['effect'] = "alert"
    rule['rules'][0]['applicationsSpec'][0]['shellshock']['effect'] = "alert"
    rule['rules'][0]['applicationsSpec'][0]['malformedReq']['effect'] = "alert"
    rule['rules'][0]['applicationsSpec'][0]['cmdi']['effect'] = "alert"
    rule['rules'][0]['applicationsSpec'][0]['lfi']['effect'] = "alert"
    rule['rules'][0]['applicationsSpec'][0]['codeInjection']['effect'] = "alert"
    rule['rules'][0]['applicationsSpec'][0]['intelGathering']['infoLeakageEffect'] = "alert"
    rule['rules'][0]['applicationsSpec'][0]['maliciousUpload']['effect'] = "alert"
    rule['rules'][0]['applicationsSpec'][0]['networkControls']['advancedProtectionEffect'] = "alert"
    rule['rules'][0]['applicationsSpec'][0]['networkControls']['subnets']['fallbackEffect'] = "alert"
    rule['rules'][0]['applicationsSpec'][0]['networkControls']['countries']['fallbackEffect'] = "alert"
    rule['rules'][0]['applicationsSpec'][0]['csrfEnabled'] = False
    rule['rules'][0]['applicationsSpec'][0]['disableEventIDHeader'] = True
    rule['rules'][0]['applicationsSpec'][0]['clickjackingEnabled'] = False
    rule['rules'][0]['applicationsSpec'][0]['intelGathering']['removeFingerprintsEnabled'] = False
    return rule


def handle_log_scrubbing_rule(rules_deletion):
    if customer_id is None:
        url = f"https://{console_ip}:8083/api/v1/policies/firewall/app/log-scrubbing"
    else:
        url = f"https://staging-consoles.cloud.twistlock.com/{customer_id}/api/v1/policies/firewall/app/log-scrubbing"

    data = []
    if not rules_deletion:
        data = [{
                    "name": "LocationBase_Python",
                    "previousName": "",
                    "location": "query",
                    "key": "^name",
                    "placeholder": "[**query-secret***]",
                    "selectedType": "location"
                  },
                  {
                    "name": "LocationBase_Python_cookie",
                    "previousName": "",
                    "location": "cookie",
                    "key": "^foo",
                    "placeholder": "[**cookie-secret***]",
                    "selectedType": "location"
                  },
                  {
                    "name": "LocationBase_Python_body",
                    "previousName": "",
                    "location": "JSONPath",
                    "key": "/foo",
                    "placeholder": "[**body-secret***]",
                    "selectedType": "location"
                  },
                  {
                    "name": "LocationBase_Python_header",
                    "previousName": "",
                    "location": "header",
                    "key": "^Foo",
                    "placeholder": "[**header-secret***]",
                    "selectedType": "location"
                  },
                  {
                    "name": "PatternBase_Python",
                    "previousName": "",
                    "location": "",
                    "key": "^python",
                    "placeholder": "[TOP-SECRET]",
                    "selectedType": "pattern"
                  }]

    response = requests.put(url, json=data, auth=get_auth(), verify=False)
    if response.status_code == 200:
        if not rules_deletion:
            print("Log Scrubbing rules are created successfully - check last 4 LFI events!")
        else:
            print("Log Scrubbing rules are deleted successfully")
    else:
        print("Error handling Log Scrubbing rules: " + str(response))


def firewall_attack():
    # XSS
    requests.get(app_url + "?name=<script>")
    requests.get(app_url + "<script>")
    requests.post(app_url + "csrf", data="<script>")

    # codeInjection
    requests.get(app_url + "?name=_$$ND_FUNC$$_")
    requests.get(app_url + "_$$ND_FUNC$$_")
    requests.post(app_url + "csrf", data='_$$ND_FUNC$$_')
    requests.get(app_url + "xss", cookies={'foo': '_$$ND_FUNC$$_'})

    # SQLI
    requests.get(app_url + "?name=1 ORDER BY 1")
    try:
        requests.get(app_url + "1 ORDER BY 1")
    except Exception as e:
        print(f"Couldn't send SQLI path attack: {e}")
    requests.post(app_url + "csrf", data='1 ORDER BY 1')
    requests.post(app_url + "sqli", cookies={'foo': '1 ORDER BY 1'})
    requests.get(app_url + "xss", headers={"User-Agent": "1 ORDER BY 1"})

    # LFI
    requests.get(app_url + "?name=../../")
    requests.get(app_url + "../../")
    requests.post(app_url + "csrf", data='../../')
    requests.get(app_url + "lfi", cookies={'foo': '../../'})
    requests.get(app_url + "xss", headers={"User-Agent": "../../"})

    # attackTools
    requests.get(app_url + "csrf", headers={"User-Agent": "prowebwalker"})

    # malformed
    requests.get(app_url + "csrf", data={'coco': 'momo'})

    # CMDI
    requests.get(app_url + '?name={"coco":"$(sleep 5)"}')
    requests.get(app_url + '{"coco":"$(sleep 5)"}')
    requests.post(app_url + "csrf", data='{"coco":"$(sleep 5)"}')
    requests.get(app_url + "lfi", headers={"User-Agent": "{\"coco\":\"$(sleep 5)\"}"})
    requests.get(app_url + "xss_s", cookies={'foo': '{"coco":"$(sleep 5)"}'})

    # Shellshock
    try:
        requests.get(app_url + "lfi", headers={"User-Agent": "() { :; }; echo; echo HELLO"})
    except:
        print("Couldn't send ShellShock attack")

    # Information leakage
    if mock:
        requests.get(app_url + "info_leak")
    else:
        requests.get(app_url)


def api_protection_attack():
    rule_api_protection = latest_rule
    rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["effect"] = "alert"
    rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["fallbackEffect"] = "alert"
    rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["queryParamFallbackEffect"] = "alert"
    update_rule(rule_api_protection, "Set API Protection alert")

    # attack
    requests.get(f"http://{app_ip}/vulnerabilities/fi/ki/coco")
    requests.get(f"http://{app_ip}/vulnerabilities/fi/ki?page=k")
    requests.get(f"http://{app_ip}/vulnerabilities/fi/ki?attack=k")

    rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["effect"] = "disable"
    rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["fallbackEffect"] = "disable"
    rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["queryParamFallbackEffect"] = "disable"
    update_rule(rule_api_protection, "Disable API Protection")


def dos_protection_attack(test):
    rule_dos = latest_rule
    rule_dos["rules"][0]["applicationsSpec"][0]["dosConfig"]["enabled"] = True
    path = f"http://{app_ip}/login.php"

    if test == "burst":
        update_rule(rule_dos, "Set DOS Protection (burst)")
        for x in range(0, 10):
            try:
                requests.get(path)
            except:
                print("")
            sleep(0.3)

        rule_dos["rules"][0]["applicationsSpec"][0]["dosConfig"]["alert"]["burst"] = None
        rule_dos["rules"][0]["applicationsSpec"][0]["dosConfig"]["enabled"] = False
        update_rule(rule_dos, "Disable DOS Protection (burst)")
        return

    rule_dos["rules"][0]["applicationsSpec"][0]["dosConfig"]["alert"] = {}
    rule_dos["rules"][0]["applicationsSpec"][0]["dosConfig"]["ban"]["average"] = 1
    update_rule(rule_dos, "Set DOS Protection (average)")

    blocked = False
    while blocked is False:
        response = requests.get(path)
        if response.status_code == 403:
            blocked = True

    rule_dos["rules"][0]["applicationsSpec"][0]["dosConfig"]["enabled"] = False
    update_rule(rule_dos, "Disable DOS Protection (average)")


def ip_protection_attack():
    ip_rule = latest_rule
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["enabled"] = True
    update_rule(ip_rule, "Set IP Protection (allow)")
    requests.get(app_url + "csrf")

    # blocklist protection
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["allow"] = None
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["allowMode"] = False
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["prevent"] = [f"local-ip-{defender_type}-{offset}"]
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["blockingMode"] = "blocklisted"
    if defender_type == "out-of-band":
        ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["fallbackEffect"] = "alert"
    else:
        ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["fallbackEffect"] = "prevent"
    update_rule(ip_rule, "Set IP Protection (blocklisted)")
    requests.get(app_url + "csrf")

    # disable ip protection
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["enabled"] = False
    update_rule(ip_rule, "Disable IP Protection")


def geo_attack():
    if defender_type == "app-embedded":
        return

    geo_rule = latest_rule
    geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["enabled"] = True
    update_rule(geo_rule, "Set GEO Protection (allow)")
    requests.get(app_url + "csrf", headers={"X-Forwarded-For": "46.33.80.185"})

    geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["allow"] = None
    geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["allowMode"] = False
    if defender_type == "out-of-band":
        geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["alert"] = ["US"]
    else:
        geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["prevent"] = ["US"]
    geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["blockingMode"] = ["blocklisted"]

    update_rule(geo_rule, "Set GEO Protection (blocklisted)")
    requests.get(app_url + "csrf", headers={"X-Forwarded-For": "46.33.80.185"})

    geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["enabled"] = False
    update_rule(geo_rule, "Disable GEO Protection")


def http_header_attack():
    header_rule = latest_rule
    header_rule["rules"][0]["applicationsSpec"][0]["headerSpecs"] = [{
                                                              "name": "coco",
                                                              "values": [
                                                                "coco"
                                                              ],
                                                              "allow": False,
                                                              "effect": "alert",
                                                              "required": False
                                                            }]
    update_rule(header_rule, "Set HTTP Header protection")
    requests.get(app_url + "csrf", headers={"coco": "coco"})


def file_uplopad_attack():
    files = {'file': open('sanity_util.py', 'rb')}
    requests.post(app_url + "csrf", files=files)


def custom_rules_attack():
    custom_rule = latest_rule
    custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][0]["effect"] = "alert"
    update_rule(custom_rule, "Set Custom Rule Protection")
    requests.get(app_url + "csrf")

    custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][0]["effect"] = "disable"
    custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][1]["effect"] = "alert"
    update_rule(custom_rule, "Update Custom Rule Protection")
    requests.get(app_url + "csrf")

    custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][1]["effect"] = "disable"
    custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][2]["effect"] = "alert"
    update_rule(custom_rule, "Update Custom Rule Protection")
    requests.post(app_url + "api_observation/buyers", data='{"coco":"MOMO"}')

    custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][2]["effect"] = "disable"
    update_rule(custom_rule, "Disable Custom Rule Protection")


def log_scrubbing_attack():
    handle_log_scrubbing_rule(False)

    requests.get(app_url + "?name=../../")
    requests.post(app_url + "csrf", json={"foo": "../../"})
    requests.get(app_url + "lfi", cookies={'foo': '../../'})
    requests.get(app_url + "xss", headers={"Foo": "../../"})
    handle_log_scrubbing_rule(True)


def connectivity_and_monitoring_attack():
    if not mock or defender_type == "app-embedded":
        return

    requests.get(app_url + "get_status_code/101")
    requests.get(app_url + "get_status_code/200")
    requests.get(app_url + "get_status_code/300")
    requests.get(app_url + "get_status_code/400")
    requests.get(app_url + "get_status_code/500")

    try:
        requests.get(app_url + "get_status_code/100")
    except:
        print("creating error for connectivity and monitoring")


def inspection_size_attack():
    letters = string.ascii_lowercase
    data = ''.join(random.choice(letters) for _ in range(150000))
    requests.post(app_url + "get_status_code/200", data=data)
    requests.post(app_url + "get_status_code/200", json={"coco": f"{data}"})

    headers = {'Content-Type': 'application/xml'}
    xml = f"""<?xml version='1.0' encoding='utf-8'?> <a>{data}</a>"""
    requests.post(app_url + "get_status_code/200", data=xml, headers=headers)


def run_waas_sanity():
    # pre-setup
    get_console_version()
    create_collection()
    create_waas_custom_rules()
    create_waas_network_list()
    create_rule()

    # attacks
    dos_protection_attack("burst")
    firewall_attack()
    api_protection_attack()
    ip_protection_attack()
    geo_attack()
    http_header_attack()
    file_uplopad_attack()
    custom_rules_attack()
    log_scrubbing_attack()
    connectivity_and_monitoring_attack()
    inspection_size_attack()
    if defender_type != "out-of-band":
        dos_protection_attack("average")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='WAAS Sanity', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--console_ip', type=str, help="ip of the console", default=None, dest="console_ip")
    parser.add_argument('--app_ip', type=str, help="app ip", default=None, dest="app_ip")
    parser.add_argument('--defender_type', type=str, help="the defender type", default=None, dest="defender_type")
    parser.add_argument('--windows', type=bool, help="windows host", default=False, dest="windows")
    parser.add_argument('--customer_id', type=str, help="windows host", default=None, dest="customer_id")
    parser.add_argument('--mock', type=bool, help="if using mock service app", default=False, dest="mock")
    parser.add_argument('--oob_type', type=str, help="out of band type", default=None, dest="oob_type")

    args = parser.parse_args()
    while args.defender_type not in ["container", "host", "app-embedded", "out-of-band"]:
        print("Defender type is wrong, support only: container, host or app-embedded", "out-of-band")
        sys.exit()

    console_ip = args.console_ip
    app_ip = args.app_ip
    mock = args.mock
    if mock:
        app_url = f"http://{app_ip}/"
    else:
        app_url = f"http://{app_ip}/vulnerabilities/"
    defender_type = args.defender_type
    windows = args.windows
    customer_id = args.customer_id
    oob_type = args.oob_type

    run_waas_sanity()
