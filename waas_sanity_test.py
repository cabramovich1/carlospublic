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
    CONTAINER_PORT_MOCK, CONTAINER_PORT_DVWA, KEPLER, AWS_COL, AWS_PORT, LAGRANGE, PEM, CERT, MAXWELL, NEWTON

# console versions
IVERSON_VERSION = 2104439
JOULE_VERSION = 2201882
KEPLER_VERSION = 2201883
LAGRANGE_VERSION = 2210352
MAXWELL_VERSION = 2212623
NEWTON_VERSION = 3100103

console_ip = ""
app_ip = ""
app_url = ""
defender_type = ""
offset = 0
latest_rule = {}
console_version = 0
windows = False
customer_id = None
mock = False
oob_type = None
tls = False
version = ""
OOB = "out-of-band"
user = None
password = None


def get_auth():
    return (user, password)




def get_console_url(route: str):
    if customer_id is None:
        return f"https://{console_ip}:8083{route}"
    else:
        return f"https://stage-consoles-cwp.cloud.twistlock.com/{customer_id}{route}"


def get_console_version():
    global console_version
    global latest_rule
    url = get_console_url(route="/api/v1/version")
    response = requests.get(url, auth=get_auth(), verify=False)

    if response.status_code == 200:
        # version received like this '"yy.mm.xxx"' - convert it to a number yymmxxx
        version = response.text
        version = version[1:-1].rsplit(".")
        version_number = int("".join(version))

        if version_number >= NEWTON_VERSION:
            console_version = NEWTON_VERSION
            latest_rule = json.loads(NEWTON)
        elif version_number > MAXWELL_VERSION:
            console_version = MAXWELL_VERSION
            latest_rule = json.loads(MAXWELL)
        elif version_number > LAGRANGE_VERSION:
            console_version = LAGRANGE_VERSION
            latest_rule = json.loads(LAGRANGE)
        elif version_number > KEPLER_VERSION:
            console_version = KEPLER_VERSION
            latest_rule = json.loads(KEPLER)
        elif version_number > JOULE_VERSION:
            console_version = JOULE_VERSION
            latest_rule = json.loads(JOULE)
        elif version_number > IVERSON_VERSION:
            console_version = IVERSON_VERSION
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
    elif defender_type == OOB or oob_type == "aws":
        collection["hosts"] = [AWS_COL]
        collection["name"] = "waas-aws"
    else:
        collection["appIDs"] = [EMB_COL]
        collection["name"] = "waas-appEmbedded"

    url = get_console_url(route="/api/v1/collections")
    response = requests.post(url, json=collection, auth=get_auth(), verify=False)
    if response.status_code == 200:
        print("Collection created successfully")
    elif response.status_code == 409:
        print("Collection is already existed")
    else:
        print("Error creating collection: " + str(response))


def create_waas_network_list():
    url = get_console_url(route="/api/v1/policies/firewall/app/network-list")
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
    url = get_console_url(route="/api/v1/custom-rules")
    response = requests.get(url, auth=get_auth(), verify=False)
    res = response.json()
    global offset
    offset = res[len(res) - 1]["_id"] + 1

    request_custom_rule = json.loads('{"_id":1,"type":"waas-request","name":"request-custom-rule-for-sanity",'
                                     '"message":"%req.http_method is denied","script":"req.http_method = \\"GET\\""}')
    request_custom_rule["_id"] = offset
    request_custom_rule["name"] = f"request-custom-rule-for-sanity{offset}"

    url = get_console_url(route=f"/api/v1/custom-rules/{offset}")
    response = requests.put(url, auth=get_auth(), json=request_custom_rule, verify=False)
    if response.status_code == 200:
        print("Custom rule created successfully")
    else:
        print("Error creating Custom Rule: " + str(response))

    response_custom_rule = json.loads('{"_id":1,"type":"waas-response","name":"response-custom-rule-for-sanity",'
                                      '"message":"%resp.status_code is denied","script":"resp.status_code = 200"}')
    response_custom_rule["_id"] = offset + 1
    response_custom_rule["name"] = f"response-custom-rule-for-sanity{offset + 1}"

    url = get_console_url(route=f"/api/v1/custom-rules/{offset + 1}")
    response = requests.put(url, auth=get_auth(), json=response_custom_rule, verify=False)
    if response.status_code == 200:
        print("Custom rule created successfully")
    else:
        print("Error creating Custom Rule: " + str(response))

    request_custom_rule_body = json.loads('{"_id":1,"type":"waas-request","name":"request-custom-rule-for-sanity-body",'
                                          '"message":"%regexMatches in %req.http_method has this body: %req.body",'
                                          '"script":"req.http_method contains /^P/ and lowercase(req.body) contains \\"{\\\\\\"coco\\\\\\":\\\\\\"momo\\\\\\"}\\""}')
    request_custom_rule_body["_id"] = offset + 2
    request_custom_rule_body["name"] = f"request-custom-rule-for-sanity-body{offset + 2}"

    url = get_console_url(route=f"/api/v1/custom-rules/{offset + 2}")
    response = requests.put(url, auth=get_auth(), json=request_custom_rule_body, verify=False)
    if response.status_code == 200:
        print("Custom rule created successfully")
    else:
        print("Error creating Custom Rule: " + str(response))

    if console_version >= LAGRANGE_VERSION:
        request_custom_rule_body = json.loads('{"_id":1,"type":"waas-request",'
                                              '"name":"request-complex-custom-rule-for-sanity-body",'
                                              '"message":"%regexMatches in %req.http_method has this body: %req.body, and JWT %req.headers", '
                                              '"script":"req.http_method contains /^P/ and lowercase(req.body) '
                                              'contains \\"{\\\\\\"coco\\\\\\":\\\\\\"momo\\\\\\"}\\"\\nor jwtPayloadValue(req.headers[\\"Authorization\\"], \\"coco\\") contains /MOMO/"}')
        request_custom_rule_body["_id"] = offset + 3
        request_custom_rule_body["name"] = f"request-complex-custom-rule-for-sanity-body{offset + 3}"

        url = get_console_url(route=f"/api/v1/custom-rules/{offset + 3}")
        response = requests.put(url, auth=get_auth(), json=request_custom_rule_body, verify=False)
        if response.status_code == 200:
            print("Custom rule created successfully")
        else:
            print("Error creating Custom Rule: " + str(response))


def update_rule(rule, update_reason):
    global latest_rule
    latest_rule = rule

    url = get_console_url(route=f"/api/v1/policies/firewall/app/{defender_type}")
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

    elif defender_type == OOB:
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
                                                                {"_id": offset + 2, "effect": "disable"}
                                                                ]
    if console_version >= LAGRANGE_VERSION:
        rule["rules"][0]["applicationsSpec"][0]["customRules"].append({"_id": offset + 3, "effect": "disable"})

    if tls:
        if defender_type == OOB:
            rule['rules'][0]['applicationsSpec'][0]['tlsConfig']['minTLSVersion'] = ''
            requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "RSA+AESGCM"
        rule["rules"][0]["applicationsSpec"][0]["certificate"]["plain"] = PEM
        rule["rules"][0]["applicationsSpec"][0]["apiSpec"]["endpoints"][0]["tls"] = True
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


def handle_log_scrubbing_and_sensitive_data_rule(rules_deletion):
    url = get_console_url(route="/api/v1/policies/firewall/app/log-scrubbing")
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
                    "selectedType": "pattern",
                    "keyPattern": True,
                    "response": True
                  },
                  {
                    "name": "Sensitiv_Data_echo",
                    "previousName": "",
                    "location": "",
                    "key": "alex",
                    "placeholder": "[TOP-SECRET]",
                    "selectedType": "pattern",
                    "keyPattern": True,
                    "response": True,
                    "sensitiveData": True
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
    requests.get(f"{app_url}?name=<script>", verify=get_certificate())
    requests.get(f"{app_url}<script>", verify=get_certificate())
    requests.post(f"{app_url}csrf", data="<script>", verify=get_certificate())

    # codeInjection
    requests.get(f"{app_url}?name=_$$ND_FUNC$$_", verify=get_certificate())
    requests.get(f"{app_url}_$$ND_FUNC$$_", verify=get_certificate())
    requests.post(f"{app_url}csrf", data='_$$ND_FUNC$$_', verify=get_certificate())
    requests.get(f"{app_url}xss", cookies={'foo': '_$$ND_FUNC$$_'}, verify=get_certificate())

    # SQLI
    requests.get(f"{app_url}?name=1 ORDER BY 1", verify=get_certificate())
    try:
        requests.get(f"{app_url}1 ORDER BY 1", verify=get_certificate())
    except Exception as e:
        print(f"Couldn't send SQLI path attack: {e}")
    requests.post(f"{app_url}csrf", data='1 ORDER BY 1', verify=get_certificate())
    requests.post(f"{app_url}sqli", cookies={'foo': '1 ORDER BY 1'}, verify=get_certificate())
    requests.get(f"{app_url}xss", headers={"User-Agent": "1 ORDER BY 1"}, verify=get_certificate())

    # LFI
    requests.get(f"{app_url}?name=../../", verify=get_certificate())
    requests.get(f"{app_url}../../", verify=get_certificate())
    requests.post(f"{app_url}csrf", data='../../', verify=get_certificate())
    requests.get(f"{app_url}lfi", cookies={'foo': '../../'}, verify=get_certificate())
    requests.get(f"{app_url}xss", headers={"User-Agent": "../../"}, verify=get_certificate())

    # attackTools
    requests.get(f"{app_url}csrf", headers={"User-Agent": "prowebwalker"}, verify=get_certificate())

    # malformed
    requests.get(f"{app_url}csrf", data={'coco': 'momo'}, verify=get_certificate())

    # CMDI
    requests.get(app_url + '?name={"coco":"$(sleep 5)"}', verify=get_certificate())
    requests.get(app_url + '{"coco":"$(sleep 5)"}', verify=get_certificate())
    requests.post(f"{app_url}csrf", data='{"coco":"$(sleep 5)"}', verify=get_certificate())
    requests.get(f"{app_url}lfi", headers={"User-Agent": "{\"coco\":\"$(sleep 5)\"}"}, verify=get_certificate())
    requests.get(f"{app_url}xss_s", cookies={'foo': '{"coco":"$(sleep 5)"}'}, verify=get_certificate())

    # Shellshock
    try:
        requests.get(f"{app_url}lfi", headers={"User-Agent": "() { :; }; echo; echo HELLO"}, verify=get_certificate())
    except:
        print("Couldn't send ShellShock attack")

    # Information leakage
    if mock:
        requests.get(f"{app_url}info_leak", verify=get_certificate())
    else:
        requests.get(app_url, verify=get_certificate())


def api_protection_attack_unspecified_query_params():
    rule_api_protection = latest_rule
    if defender_type != OOB:
        rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["queryParamFallbackEffect"] = "prevent"
        update_rule(rule_api_protection, "Set API Protection prevent")

        # attack
        url = f"{app_url}api_observation/merchants/small?UnspecifiedParameter=haha"
        requests.get(url, verify=get_certificate())
        requests.put(url, verify=get_certificate())
        requests.post(url, verify=get_certificate())
        requests.delete(url, verify=get_certificate())
        requests.options(url, verify=get_certificate())
        requests.head(url, verify=get_certificate())
        requests.patch(url, verify=get_certificate())

    rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["queryParamFallbackEffect"] = "alert"
    update_rule(rule_api_protection, "Set API Protection alert")

    # attack
    url = f"{app_url}api_observation/merchants/small?UnspecifiedParameter=haha"
    requests.get(url, verify=get_certificate())
    requests.put(url, verify=get_certificate())
    requests.post(url, verify=get_certificate())
    requests.delete(url, verify=get_certificate())
    requests.options(url, verify=get_certificate())
    requests.head(url, verify=get_certificate())
    requests.patch(url, verify=get_certificate())

    rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["queryParamFallbackEffect"] = "disable"
    update_rule(rule_api_protection, "Disable API Protection")


def api_protection_attack_unspecified_paths_or_methods():
    rule_api_protection = latest_rule
    if defender_type != OOB:
        rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["fallbackEffect"] = "prevent"
        update_rule(rule_api_protection, "Set API Protection prevent")
        # attack
        url = f"{app_url}api_observation/merchants/huge"
        requests.get(url, verify=get_certificate())
        requests.put(url, verify=get_certificate())
        requests.post(url, verify=get_certificate())
        requests.delete(url, verify=get_certificate())
        requests.options(url, verify=get_certificate())
        requests.head(url, verify=get_certificate())
        requests.patch(url, verify=get_certificate())

    rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["fallbackEffect"] = "alert"
    update_rule(rule_api_protection, "Set API Protection alert")

    # attack
    url = f"{app_url}api_observation/merchants/huge"
    requests.get(url, verify=get_certificate())
    requests.put(url, verify=get_certificate())
    requests.post(url, verify=get_certificate())
    requests.delete(url, verify=get_certificate())
    requests.options(url, verify=get_certificate())
    requests.head(url, verify=get_certificate())
    requests.patch(url, verify=get_certificate())

    rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["fallbackEffect"] = "disable"
    update_rule(rule_api_protection, "Disable API Protection")


def api_protection_attack_all_methods():
    rule_api_protection = latest_rule
    if defender_type == OOB:
        rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["effect"] = "alert"
        rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["fallbackEffect"] = "alert"
        rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["queryParamFallbackEffect"] = "alert"
        update_rule(rule_api_protection, "Set API Protection alert for OOB")
    else:
        rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["effect"] = "prevent"
        rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["fallbackEffect"] = "prevent"
        rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["queryParamFallbackEffect"] = "prevent"
        update_rule(rule_api_protection, "Set API Protection prevent")

    # attack
    url = f"{app_url}api_observation/merchants/big"
    requests.get(f"{url}?number=150", verify=get_certificate())
    requests.get(f"{url}?number=notnumber", verify=get_certificate())
    requests.put(f"{url}?number=notanumber", verify=get_certificate())
    requests.post(f"{url}?number=notanumber", verify=get_certificate())
    requests.delete(f"{url}?number=notanumber", verify=get_certificate())
    requests.options(f"{url}?number=notanumber", verify=get_certificate())
    requests.head(f"{url}?number=notanumber", verify=get_certificate())
    requests.patch(f"{url}?number=notanumber", verify=get_certificate())
    requests.get(f"{url}?number=99", verify=get_certificate())
    requests.get(f"{url}?number=300", verify=get_certificate())


    rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["effect"] = "disable"
    rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["fallbackEffect"] = "disable"
    rule_api_protection["rules"][0]["applicationsSpec"][0]["apiSpec"]["queryParamFallbackEffect"] = "disable"
    update_rule(rule_api_protection, "Disable API Protection")


def api_discovery():
    requests.get(f"{app_url}get_status_code/200", verify=get_certificate())
    requests.get(f"{app_url}get_status_code/200", headers={"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"}, verify=get_certificate())
    requests.get(f"{app_url}get_status_code/200", headers={"User-Agent":"Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"}, verify=get_certificate())
    requests.get(f"{app_url}get_status_code/200", headers={"User-Agent":"winhttprequest"}, verify=get_certificate())
    requests.get(f"{app_url}get_status_code/200", headers={"User-Agent":"restsharp"}, verify=get_certificate())
    requests.get(f"{app_url}get_status_code/200?xss=%3Cscript%3E", verify=get_certificate())
    requests.get(f"{app_url}get_status_code/200", headers={"Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp"}, verify=get_certificate())
    requests.get(f"{app_url}get_status_code/200", headers={"X-Forwarded-For": "46.33.80.185"}, verify=get_certificate())
    requests.post(f"{app_url}api_observation/buyers", headers={"Content-Type":"application/json"}, data='{"coco":"momo"}', verify=get_certificate())
    requests.get(f"{app_url}api_observation/buyers", verify=get_certificate())
    requests.post(f"{app_url}api_protection/fictive-path/fictive-parameter", verify=get_certificate())
    requests.put(f"{app_url}api_protection/fictive-path/fictive-parameter", verify=get_certificate())
    requests.options(f"{app_url}site_map", verify=get_certificate())
    requests.patch(f"{app_url}api_observation/merchants/small", verify=get_certificate())
    requests.get(f"{app_url}get_endpoint -I", verify=get_certificate())
    requests.delete(f"{app_url}api_observation/custom_path/fictive-path", verify=get_certificate())
    requests.head(f"{app_url}api_observation/merchants/small", verify=get_certificate())
    for port in [200, 101, 300, 401, 505]:
        requests.post(f"{app_url}post_status_code", headers={"Content-Type": "application/json"},
                      json={"status_code": port}, verify=get_certificate())


def dos_protection_attack(test):
    rule_dos = latest_rule
    rule_dos["rules"][0]["applicationsSpec"][0]["dosConfig"]["enabled"] = True
    path = f"{app_url}login.php"

    if test == "burst":
        update_rule(rule_dos, "Set DOS Protection (burst)")
        for x in range(0, 10):
            try:
                requests.get(path, verify=get_certificate())
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
        response = requests.get(path, verify=get_certificate())
        if response.status_code == 403:
            blocked = True

    rule_dos["rules"][0]["applicationsSpec"][0]["dosConfig"]["enabled"] = False
    update_rule(rule_dos, "Disable DOS Protection (average)")


def ip_protection_attack():
    ip_rule = latest_rule

    # Allowed protection
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["enabled"] = True
    if defender_type != OOB:
        # Prevent
        update_rule(ip_rule, "Set IP Protection (Allow - Prevent)")
        requests.get(f"{app_url}csrf", verify=get_certificate())
    # Alert
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["fallbackEffect"] = "alert"
    update_rule(ip_rule, "Set IP Protection (Allow - Alert)")
    requests.get(f"{app_url}csrf", verify=get_certificate())

    # Blocklist protection
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["allow"] = None
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["allowMode"] = False
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["alert"] = [f"local-ip-{defender_type}-{offset}"]
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["blockingMode"] = "blocklisted"
    if defender_type != OOB:
        # Prevent
        ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["prevent"] = [
            f"local-ip-{defender_type}-{offset}"]
        ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["fallbackEffect"] = "prevent"
        update_rule(ip_rule, "Set IP Protection (Blocklisted - Prevent)")
        requests.get(f"{app_url}get_status_code/200", verify=get_certificate())
    # Alert
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["fallbackEffect"] = "alert"
    update_rule(ip_rule, "Set IP Protection (Blocklisted - Alert)")
    requests.get(f"{app_url}get_status_code/200", verify=get_certificate())

    # Disable ip protection
    ip_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["subnets"]["enabled"] = False
    update_rule(ip_rule, "Disable IP Protection")


def geo_attack():
    if defender_type == "app-embedded":
        return

    geo_rule = latest_rule

    # Allowed protection
    geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["enabled"] = True

    if defender_type != OOB:
        # Prevent
        update_rule(geo_rule, "Set GEO Protection (Allow - Prevent)")
        requests.get(f"{app_url}csrf", headers={"X-Forwarded-For": "46.33.80.185"}, verify=get_certificate())
        requests.get(f"{app_url}csrf", headers={"X-Forwarded-For": "1.159.255.255"}, verify=get_certificate())

    # Alert
    geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["fallbackEffect"] = "alert"
    update_rule(geo_rule, "Set GEO Protection (Allow - Alert)")
    requests.get(f"{app_url}csrf", headers={"X-Forwarded-For": "46.33.80.185"}, verify=get_certificate())
    requests.get(f"{app_url}csrf", headers={"X-Forwarded-For": "1.159.255.255"}, verify=get_certificate())

    # Blocklist protection
    geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["allow"] = None
    geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["allowMode"] = False
    if defender_type != OOB:
        # Prevent
        geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["prevent"] = ["US", "AU"]
        geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["blockingMode"] = ["blocklisted"]
        update_rule(geo_rule, "Set GEO Protection (blocklisted)")
        requests.get(f"{app_url}csrf", headers={"X-Forwarded-For": "46.33.80.185"}, verify=get_certificate())
        requests.get(f"{app_url}csrf", headers={"X-Forwarded-For": "1.159.255.255"}, verify=get_certificate())
        geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["prevent"] = []

    # Alert
    geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["alert"] = ["US", "AU"]
    update_rule(geo_rule, "Set GEO Protection (blocklisted)")
    requests.get(f"{app_url}csrf", headers={"X-Forwarded-For": "46.33.80.185"}, verify=get_certificate())
    requests.get(f"{app_url}csrf", headers={"X-Forwarded-For": "1.159.255.255"}, verify=get_certificate())

    geo_rule["rules"][0]["applicationsSpec"][0]["networkControls"]["countries"]["enabled"] = False
    update_rule(geo_rule, "Disable GEO Protection")


def http_header_attack():
    header_rule = latest_rule

    # Blocklisted value - Alert
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
    requests.get(f"{app_url}csrf", headers={"coco": "coco"}, verify=get_certificate())

    if defender_type != OOB:
        # Blocklisted value - Prevent
        header_rule["rules"][0]["applicationsSpec"][0]["headerSpecs"] = [{
                                                                  "name": "coco",
                                                                  "values": [
                                                                    "coco"
                                                                  ],
                                                                  "allow": False,
                                                                  "effect": "prevent",
                                                                  "required": False
                                                                }]
        update_rule(header_rule, "Set HTTP Header protection")
        requests.get(app_url + "csrf", headers={"coco": "coco"}, verify=get_certificate())

    # Missing header name - Alert
    header_rule["rules"][0]["applicationsSpec"][0]["headerSpecs"] = [{
                                                              "name": "coco",
                                                              "values": [
                                                                "coco"
                                                              ],
                                                              "allow": False,
                                                              "effect": "alert",
                                                              "required": True
                                                            }]
    update_rule(header_rule, "Set HTTP Header protection")
    requests.get(f"{app_url}csrf", headers={"notcoco": "coco"}, verify=get_certificate())

    if defender_type != OOB:
        # Missing header name - Prevent
        header_rule["rules"][0]["applicationsSpec"][0]["headerSpecs"] = [{
                                                                  "name": "coco",
                                                                  "values": [
                                                                    "coco"
                                                                  ],
                                                                  "allow": False,
                                                                  "effect": "prevent",
                                                                  "required": True
                                                                }]
        update_rule(header_rule, "Set HTTP Header protection")
        requests.get(app_url + "csrf", headers={"notcoco": "coco"}, verify=get_certificate())

        # Blocklisted Multiple value - Prevent
        header_rule["rules"][0]["applicationsSpec"][0]["headerSpecs"] = [{
                                                                  "name": "test",
                                                                  "values": [
                                                                    "coco","momo"
                                                                  ],
                                                                  "allow": False,
                                                                  "effect": "prevent",
                                                                  "required": False
                                                                }]
    update_rule(header_rule, "Set HTTP Header protection")
    requests.get(f"{app_url}csrf", headers={"test": "coco"}, verify=get_certificate())
    requests.get(f"{app_url}csrf", headers={"test": "momo"}, verify=get_certificate())


def file_uplopad_attack():
    files = {'file': open('sanity_util.py', 'rb')}
    requests.post(f"{app_url}csrf", files=files, verify=get_certificate())


def custom_rules_attack():
    custom_rule = latest_rule
    custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][0]["effect"] = "alert"
    update_rule(custom_rule, "Set Custom Rule Protection")
    requests.get(f"{app_url}csrf", verify=get_certificate())
    custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][0]["effect"] = "disable"

    custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][1]["effect"] = "alert"
    update_rule(custom_rule, "Update Custom Rule Protection")
    requests.get(f"{app_url}csrf", verify=get_certificate())
    custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][1]["effect"] = "disable"

    custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][2]["effect"] = "alert"
    update_rule(custom_rule, "Update Custom Rule Protection")
    requests.post(f"{app_url}api_observation/buyers", data='{"coco":"MOMO"}', verify=get_certificate())
    custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][2]["effect"] = "disable"

    if console_version >= LAGRANGE_VERSION:
        custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][3]["effect"] = "alert"
        update_rule(custom_rule, "Update Custom Rule Protection")
        requests.post(f"{app_url}api_observation/buyers", data='{"coco":"MOMO"}',
                      headers={"Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2NvIjoiTU9NTyJ9.pEDSD8oVe2eCgJu3rnotVBbIaCKnfRsS6-flCZdTy3Y"},
                      verify=get_certificate())

        custom_rule["rules"][0]["applicationsSpec"][0]["customRules"][3]["effect"] = "disable"
    update_rule(custom_rule, "Disable Custom Rule Protection")


def log_scrubbing_attack_and_sensitive_data():
    handle_log_scrubbing_and_sensitive_data_rule(False)

    requests.get(f"{app_url}?name=../../", verify=get_certificate())
    requests.post(f"{app_url}csrf", json={"foo": "../../"}, verify=get_certificate())
    requests.get(f"{app_url}lfi", cookies={"foo": '../../'}, verify=get_certificate())
    requests.get(f"{app_url}xss", headers={"Foo": "../../"}, verify=get_certificate())
    requests.post(f"{app_url}post_echo", headers={"Content-Type":"application/json"}, data='{"alex":"alex"}', verify=get_certificate())
    handle_log_scrubbing_and_sensitive_data_rule(True)


def connectivity_and_monitoring_attack():
    if not mock or defender_type == "app-embedded":
        return

    requests.get(f"{app_url}get_status_code/101", verify=get_certificate())
    requests.get(f"{app_url}get_status_code/200", verify=get_certificate())
    requests.get(f"{app_url}get_status_code/300", verify=get_certificate())
    requests.get(f"{app_url}get_status_code/400", verify=get_certificate())
    requests.get(f"{app_url}get_status_code/500", verify=get_certificate())

    if not tls:
        try:
            requests.get(f"{app_url}get_status_code/100", verify=get_certificate())
        except:
            print("creating error for connectivity and monitoring")


def inspection_size_attack():
    letters = string.ascii_lowercase
    data = ''.join(random.choice(letters) for _ in range(150000))
    requests.post(f"{app_url}get_status_code/200", data=data, verify=get_certificate())
    requests.post(f"{app_url}get_status_code/200", json={"coco": f"{data}"}, verify=get_certificate())

    headers = {'Content-Type': 'application/xml'}
    xml = f"""<?xml version='1.0' encoding='utf-8'?> <a>{data}</a>"""
    requests.post(f"{app_url}get_status_code/200", data=xml, headers=headers, verify=get_certificate())


def get_certificate():
    if tls:
        return CERT
    else:
        return None


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
    api_protection_attack_unspecified_query_params()
    api_protection_attack_unspecified_paths_or_methods()
    api_protection_attack_all_methods()
    ip_protection_attack()
    api_discovery()
    geo_attack()
    http_header_attack()
    file_uplopad_attack()
    custom_rules_attack()
    log_scrubbing_attack_and_sensitive_data()
    connectivity_and_monitoring_attack()
    inspection_size_attack()
    if defender_type != OOB:
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
    parser.add_argument('--tls', type=bool, help="if using tls certificate", default=False, dest="tls")
    parser.add_argument('--user', type=str, help="username for console", default=None, dest="user")
    parser.add_argument('--password', type=str, help="password for console", default=None, dest="password")

    args = parser.parse_args()
    while args.defender_type not in ["container", "host", "app-embedded", "out-of-band"]:
        print("Defender type is wrong, support only: container, host or app-embedded", "out-of-band")
        sys.exit()

    console_ip = args.console_ip
    app_ip = args.app_ip
    tls = args.tls
    mock = args.mock
    user = args.user
    password = args.password

    if user is None and password is None:
        if args.customer_id is None:
            user = '1admin2'
            password = 'Pa$$word1NotForUseOnlyInCaseYoudon$thaveanotheroption'
        else:
            user = 'ahaytovich@paloaltonetworks.com'
            password = 'jEZ255V88Nyhxcr!'
    elif user is None or password is None:
        print(f'Missing user name or password, only one parameter was supplied : user is: {user}, password is {password}')
        sys.exit()

    if mock:
        if tls:
            app_url = f"https://{app_ip}/"
        else:
            app_url = f"http://{app_ip}/"
    else:
        if tls:
            app_url = f"https://{app_ip}/vulnerabilities/"
        else:
            app_url = f"http://{app_ip}/vulnerabilities/"
    defender_type = args.defender_type
    windows = args.windows
    customer_id = args.customer_id
    oob_type = args.oob_type

    run_waas_sanity()
