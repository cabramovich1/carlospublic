# Rule ports
import os

WIN_INT_PORT = 8000
WIN_EXT_PORT = 80
HOST_PORT = 8082
CONTAINER_PORT_DVWA = 80
CONTAINER_PORT_MOCK = 8081
EMB_INT_PORT = 8081
EMB_EXT_PORT = 9001
AWS_PORT = 8082

# Collection
HOST_WIN_COL = "*waas-windows*"
HOST_LINUX_COL = "*waas*"
CONTAINER_DVWA = "*dvwa*"
CONTAINER_MOCK = "*lizatwistlock/waas-mock-service*"
EMB_COL = "waas-*"
AWS_COL = "*ip-*"

PEM = """
-----BEGIN CERTIFICATE-----
MIIExDCCAqwCCQDh6wYXDUm8pzANBgkqhkiG9w0BAQsFADAkMQswCQYDVQQGEwJJ
TDEVMBMGA1UEAwwMbW9ja19jb24uY29tMB4XDTIyMDYwODEwNDcyNloXDTMyMDYw
NTEwNDcyNlowJDELMAkGA1UEBhMCSUwxFTATBgNVBAMMDG1vY2tfY29uLmNvbTCC
AiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAMN8ZLzBoZ8kmcq+AvsgGhJ5
OA4Opm1qWBkMjwbq7iFDbgO2xUfFLWxy/CQDrHchAVR/RRA3A/T4dyu3rwj3lYg5
WBzWtb63VvbjYkwHB0HTQ45f4PQjjdJqAeGkbmI/G/Ug/IiVCFDLCHEVmi3tea1a
H1f8FASbC5ck9aJruWxuHX14N6eGaMwQzRljZ8+P59dXIVwdwgRybT/8hFh9EcYE
t6sNZVBheFfjHGowVOhdEnsI4uDIb4vnJl3WRVXieqmNg2imnNzi01dBTmtuk7U9
I73Um0yNeaQ7YLfRSxvzR33GXmSLvmUgWRlmCv/UaoCwvv9mhcLSgksXPjZjvcBI
s/vmtG//YK5VRE6jpT/OVJ6bjRqO4T33JjwoWmlFtlb5KN3sxIt7172FK45u4xGu
zU4TVLK0sawDAUPD7JN99BahU+xbmEQO6Ok55i1iBBN5Bax4rbtw6F/9naXsVixs
SO5KKpuIbFvHcWEXtjw92p/FbV/24PBBK5oNCdINwSAfqlIripaStzSk+kbyO/7/
fFai43OaSpGtG4NYnDEbu0+6z/OSS2VBib2pbO7d9jIbLqhNC4c61XwqrnvnFLaS
t+wBv5d7E8VPW5+/U9ilQlG3vuoj2UAYTlqbXVWnaoBkuWi517QiYy7EsbSUU44D
lg0gT87YD0rVs0RiqWZxAgMBAAEwDQYJKoZIhvcNAQELBQADggIBAKx9NM7oecyX
R0rAL0nN99ihGvI6ENNuXRaKnhqhcTYYqgduRolqPFt7Jhw3S5eMYlDs9tc+hSZW
ddsoOVTBpD/Labhcd21NyBzFeaecubpr9jTR+QD/IbqczxjfcVL20NtQJrByvLfF
ToQo6dbu6G8BaL5dQynD+XC/Tbi/KelDDuOnZCbbYLuZRoNGiqtVrYejMMunnY2G
Sm5Wt3lfVnR6jpoAGCltDHlkHBCZDg2KWn6WIUQRXBBb230s/oCMSVYQUrxVF5e8
/Euwdw1YNquCvkvfgpOX1vC/fV3gv/77/+HlXYgJOiMlTmxJw5WaRaK0IlawXSIF
D1XSegFhXBmwMJeA+zOPkskD2U4lQYBdV/JUz9PoaW1hJusTwnnfsZImQjrMPqTX
Iyja8nhQrXHIcS5huHAlSQt+uQZXOovs+FK0z1o17QpgexB8Mp5iS6t5WLmG9Ht8
yKLjDB8e+ivnmexjbf1jYB3iPjP6+AG2gKahJbpkvFoMn6hs647VLCwbtxjwTIsE
8tBROwn0mEvsaFxvVTWSpko+LvO27vtWQVzBWoU4KOiJ2mnbZ4G4L4bXHjafor/t
6uWo+7ljb3Juy+E/n7yGTvRT+UBRCC9svtf9Sf5TPk/NY9nqxs1VusAhazWYzxkM
EZp8GQ17g6yLapzqyZne51FY8auQam5T
-----END CERTIFICATE-----
-----BEGIN PRIVATE KEY-----
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
LRfs0kfDAEH0QLF99m1UKBL6U6uocSc=
-----END PRIVATE KEY-----
"""

CERT = os.path.dirname(os.path.abspath(__file__)) + '/cert.cert'

COLLECTION = """{
  "name": "s",
  "containers": [
    "*"
  ],
  "hosts": [
    "*"
  ],
  "images": [
    "*"
  ],
  "labels": [
    "*"
  ],
  "appIDs": [
    "*"
  ],
  "functions": [
    "*"
  ],
  "namespaces": [
    "*"
  ],
  "accountIDs": [
    "*"
  ],
  "codeRepos": [
    "*"
  ],
  "clusters": [
    "*"
  ],
  "system": false,
  "color": "#857af8"
}"""

IVERSON = """
{
  "_id": "containerAppFirewall",
  "rules": [
    {
      "applicationsSpec": [
        {
          "appID": "app-F152",
          "banDurationMinutes": 5,
          "apiSpec": {
            "endpoints": [
              {
                "host": "*",
                "internalPort": 80,
                "basePath": "*",
                "exposedPort": 0
              }
            ],
            "effect": "disable",
            "fallbackEffect": "disable",
            "skipLearning": false,
            "paths": [
              {
                "path": "/vulnerabilities/fi/ki",
                "methods": [
                  {
                    "method": "GET",
                    "parameters": [
                      {
                        "name": "page",
                        "type": "number",
                        "location": "query",
                        "style": "form",
                        "explode": false
                      }
                    ]
                  }
                ]
              }
            ]
          },
          "botProtectionSpec": {
            "userDefinedBots": [

            ],
            "knownBotProtectionsSpec": {
              "searchEngineCrawlers": "disable",
              "businessAnalytics": "disable",
              "educational": "disable",
              "news": "disable",
              "financial": "disable",
              "contentFeedClients": "disable",
              "archiving": "disable",
              "careerSearch": "disable",
              "mediaSearch": "disable"
            },
            "unknownBotProtectionSpec": {
              "generic": "disable",
              "webAutomationTools": "disable",
              "webScrapers": "disable",
              "apiLibraries": "disable",
              "httpLibraries": "disable",
              "botImpersonation": "disable",
              "browserImpersonation": "disable",
              "requestAnomalies": {
                "effect": "disable",
                "threshold": 9
              }
            },
            "sessionValidation": "disable",
            "jsInjectionSpec": {
              "enabled": false,
              "timeoutEffect": "disable"
            },
            "reCAPTCHASpec": {
              "enabled": false,
              "secretKey": {

              },
              "type": "checkbox",
              "allSessions": true,
              "successExpirationHours": 24
            }
          },
          "dosConfig": {
            "enabled": false,
            "alert": {
              "burst": 1,
              "average": null
            },
            "ban": {
              "burst": null,
              "average": null
            },
            "matchConditions": [
              {
                "methods": [

                ],
                "fileTypes": [
                  ".php"
                ],
                "responseCodeRanges": [

                ],
                "responseCodeRangesTags": [

                ]
              }
            ]
          },
          "tlsConfig": {
            "minTLSVersion": "1.2",
            "metadata": {

            },
            "HSTSConfig": {
              "enabled": false,
              "maxAgeSeconds": 31536000,
              "includeSubdomains": false,
              "preload": false
            }
          },
          "networkControls": {
            "advancedProtectionEffect": "prevent",
            "subnets": {
              "enabled": false,
              "allowMode": true,
              "fallbackEffect": "prevent",
              "blockingMode": "allowed",
              "allow": [
                "waas-network-list"
              ],
              "alert": null,
              "prevent": null
            },
            "countries": {
              "enabled": false,
              "allowMode": true,
              "fallbackEffect": "prevent",
              "blockingMode": "allowed",
              "allow": [
                "IL"
              ],
              "alert": null,
              "prevent": null
            },
            "exceptionSubnets": [

            ]
          },
          "xss": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "sqli": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "cmdi": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "lfi": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "codeInjection": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "attackTools": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "shellshock": {
            "effect": "prevent"
          },
          "malformedReq": {
            "effect": "prevent"
          },
          "customBlockResponse": {

          },
          "headerSpecs": [

          ],
          "csrfEnabled": true,
          "clickjackingEnabled": true,
          "intelGathering": {
            "infoLeakageEffect": "prevent",
            "removeFingerprintsEnabled": true
          },
          "maliciousUpload": {
            "effect": "prevent",
            "allowedFileTypes": [
              "pdf"
            ],
            "allowedExtensions": [

            ]
          },
          "body": {
            "skip": false,
            "inspectionSizeBytes": 131072
          },
          "remoteHostForwarding": {
            "enabled": false,
            "target": ""
          },
          "certificate": {

          },
          "customRules": [

          ]
        }
      ],
      "readTimeoutSeconds": 5,
      "windows": false,
      "collections": [
        {
          "hosts": [
            "*"
          ],
          "images": [
            "*"
          ],
          "labels": [
            "*"
          ],
          "containers": [
            "*"
          ],
          "functions": [
            "*"
          ],
          "namespaces": [
            "*"
          ],
          "appIDs": [
            "*"
          ],
          "accountIDs": [
            "*"
          ],
          "codeRepos": [
            "*"
          ],
          "clusters": [
            "*"
          ],
          "name": "waas-con",
          "owner": "1admin2",
          "modified": "2021-08-26T07:59:09.274Z",
          "color": "#665A30",
          "system": false,
          "prisma": false
        }
      ],
      "name": "coco",
      "owner": "1admin2",
      "modified": "2021-09-19T12:14:52.511Z"
    }
  ],
  "minPort": 30000,
  "maxPort": 31000
}"""

JOULE = """
{
  "_id": "containerAppFirewall",
  "rules": [
    {
      "modified": "2021-11-24T08:07:21.810Z",
      "owner": "1admin2",
      "name": "coco",
      "previousName": "",
      "collections": [
        {
          "hosts": [
            "*"
          ],
          "images": [
            "*dvwa*"
          ],
          "labels": [
            "*"
          ],
          "containers": [
            "*"
          ],
          "functions": [
            "*"
          ],
          "namespaces": [
            "*"
          ],
          "appIDs": [
            "*"
          ],
          "accountIDs": [
            "*"
          ],
          "codeRepos": [
            "*"
          ],
          "clusters": [
            "*"
          ],
          "name": "waas-con",
          "owner": "1admin2",
          "modified": "2021-11-24T08:04:24.998Z",
          "color": "#49C811",
          "system": false,
          "prisma": false
        }
      ],
      "applicationsSpec": [
        {
          "appID": "app-F152",
          "sessionCookieSameSite": "Lax",
          "customBlockResponse": {

          },
          "banDurationMinutes": 5,
          "certificate": {

          },
          "tlsConfig": {
            "minTLSVersion": "1.2",
            "metadata": {

            },
            "HSTSConfig": {
              "enabled": false,
              "maxAgeSeconds": 31536000,
              "includeSubdomains": false,
              "preload": false
            }
          },
          "dosConfig": {
            "enabled": false,
            "alert": {
              "burst": 1
            },
            "ban": {

            },
            "matchConditions": [
              {
                "fileTypes": [
                  ".php"
                ],
                "responseCodeRangesTags": [

                ],
                "responseCodeRanges": [

                ]
              }
            ]
          },
          "apiSpec": {
            "endpoints": [
              {
                "host": "*",
                "basePath": "*",
                "exposedPort": 0,
                "internalPort": 80,
                "tls": false,
                "http2": false,
                "grpc": false
              }
            ],
            "paths": [
              {
                "path": "/vulnerabilities/fi/ki",
                "methods": [
                  {
                    "method": "GET",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form"
                      }
                    ]
                  }
                ]
              }
            ],
            "effect": "disable",
            "fallbackEffect": "disable",
            "queryParamFallbackEffect": "disable",
            "skipLearning": false
          },
          "botProtectionSpec": {
            "userDefinedBots": [

            ],
            "knownBotProtectionsSpec": {
              "searchEngineCrawlers": "disable",
              "businessAnalytics": "disable",
              "educational": "disable",
              "news": "disable",
              "financial": "disable",
              "contentFeedClients": "disable",
              "archiving": "disable",
              "careerSearch": "disable",
              "mediaSearch": "disable"
            },
            "unknownBotProtectionSpec": {
              "generic": "disable",
              "webAutomationTools": "disable",
              "webScrapers": "disable",
              "apiLibraries": "disable",
              "httpLibraries": "disable",
              "botImpersonation": "disable",
              "browserImpersonation": "disable",
              "requestAnomalies": {
                "threshold": 9,
                "effect": "disable"
              }
            },
            "sessionValidation": "disable",
            "interstitialPage": false,
            "jsInjectionSpec": {
              "enabled": false,
              "timeoutEffect": "disable"
            },
            "reCAPTCHASpec": {
              "enabled": false,
              "secretKey": {

              },
              "type": "checkbox",
              "allSessions": true,
              "successExpirationHours": 24
            }
          },
          "networkControls": {
            "advancedProtectionEffect": "prevent",
            "subnets": {
              "enabled": false,
              "allowMode": true,
              "allow": [
                "waas-network-list"
              ],
              "fallbackEffect": "prevent",
              "blockingMode": "allowed",
              "alert": null,
              "prevent": null
            },
            "countries": {
              "enabled": false,
              "allowMode": true,
              "allow": [
                "IL"
              ],
              "fallbackEffect": "prevent",
              "blockingMode": "allowed",
              "alert": null,
              "prevent": null
            }
          },
          "body": {
            "inspectionSizeBytes": 131072
          },
          "intelGathering": {
            "infoLeakageEffect": "prevent",
            "removeFingerprintsEnabled": true
          },
          "maliciousUpload": {
            "effect": "prevent",
            "allowedFileTypes": [
              "pdf"
            ],
            "allowedExtensions": [

            ]
          },
          "csrfEnabled": true,
          "clickjackingEnabled": true,
          "sqli": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "xss": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "attackTools": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "shellshock": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "malformedReq": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "cmdi": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "lfi": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "codeInjection": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "remoteHostForwarding": {

          },
          "selected": false,
          "customRules": [

          ],
          "headerSpecs": [

          ],
          "sessionCookieSecure": false
        }
      ],
      "readTimeoutSeconds": 5,
      "windows": false,
      "expandDetails": true
    }
  ],
  "minPort": 30000,
  "maxPort": 31000
}"""

KEPLER = """
{
  "_id": "containerAppFirewall",
  "rules": [
    {
      "modified": "2022-03-27T08:49:06.489Z",
      "owner": "ishater",
      "name": "coco",
      "previousName": "",
      "collections": [
        {
          "hosts": [
            "*"
          ],
          "images": [
            "*dvwa*"
          ],
          "labels": [
            "*"
          ],
          "containers": [
            "*"
          ],
          "functions": [
            "*"
          ],
          "namespaces": [
            "*"
          ],
          "appIDs": [
            "*"
          ],
          "accountIDs": [
            "*"
          ],
          "codeRepos": [
            "*"
          ],
          "clusters": [
            "*"
          ],
          "name": "waas-con",
          "owner": "ishater",
          "modified": "2022-03-27T08:48:41.287Z",
          "color": "#6B2476",
          "system": false,
          "prisma": false
        }
      ],
      "applicationsSpec": [
        {
          "appID": "app-F152",
          "sessionCookieSameSite": "Lax",
          "customBlockResponse": {

          },
          "banDurationMinutes": 5,
          "certificate": {

          },
          "tlsConfig": {
            "minTLSVersion": "1.2",
            "metadata": {

            },
            "HSTSConfig": {
              "enabled": false,
              "maxAgeSeconds": 31536000,
              "includeSubdomains": false,
              "preload": false
            }
          },
          "dosConfig": {
            "enabled": false,
            "alert": {
              "burst": 1
            },
            "ban": {

            },
            "matchConditions": [
              {
                "fileTypes": [
                  ".php"
                ],
                "responseCodeRangesTags": [

                ],
                "responseCodeRanges": [

                ]
              }
            ]
          },
          "apiSpec": {
            "endpoints": [
              {
                "host": "*",
                "basePath": "*",
                "exposedPort": 0,
                "internalPort": 80,
                "tls": false,
                "http2": false,
                "grpc": false
              }
            ],
            "paths": [
              {
                "path": "/vulnerabilities/fi/ki",
                "methods": [
                  {
                    "method": "GET",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form"
                      }
                    ]
                  }
                ]
              }
            ],
            "effect": "disable",
            "fallbackEffect": "disable",
            "queryParamFallbackEffect": "disable"
          },
          "botProtectionSpec": {
            "userDefinedBots": [

            ],
            "knownBotProtectionsSpec": {
              "searchEngineCrawlers": "disable",
              "businessAnalytics": "disable",
              "educational": "disable",
              "news": "disable",
              "financial": "disable",
              "contentFeedClients": "disable",
              "archiving": "disable",
              "careerSearch": "disable",
              "mediaSearch": "disable"
            },
            "unknownBotProtectionSpec": {
              "generic": "disable",
              "webAutomationTools": "disable",
              "webScrapers": "disable",
              "apiLibraries": "disable",
              "httpLibraries": "disable",
              "botImpersonation": "disable",
              "browserImpersonation": "disable",
              "requestAnomalies": {
                "threshold": 9,
                "effect": "disable"
              }
            },
            "sessionValidation": "disable",
            "interstitialPage": false,
            "jsInjectionSpec": {
              "enabled": false,
              "timeoutEffect": "disable"
            },
            "reCAPTCHASpec": {
              "enabled": false,
              "secretKey": {

              },
              "type": "checkbox",
              "allSessions": true,
              "successExpirationHours": 24
            }
          },
          "networkControls": {
            "advancedProtectionEffect": "prevent",
            "subnets": {
              "enabled": false,
              "allowMode": true,
              "allow": [
                "waas-network-list"
              ],
              "fallbackEffect": "prevent",
              "blockingMode": "allowed",
              "alert": null,
              "prevent": null
            },
            "countries": {
              "enabled": false,
              "allowMode": true,
              "allow": [
                "IL"
              ],
              "fallbackEffect": "prevent",
              "blockingMode": "allowed",
              "alert": null,
              "prevent": null
            }
          },
          "body": {
            "inspectionSizeBytes": 131072,
            "inspectionLimitExceededEffect": "alert"
          },
          "intelGathering": {
            "infoLeakageEffect": "prevent",
            "removeFingerprintsEnabled": true
          },
          "maliciousUpload": {
            "effect": "prevent",
            "allowedFileTypes": [
              "pdf"
            ],
            "allowedExtensions": [

            ]
          },
          "csrfEnabled": true,
          "clickjackingEnabled": true,
          "sqli": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "xss": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "attackTools": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "shellshock": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "malformedReq": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "cmdi": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "lfi": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "codeInjection": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "remoteHostForwarding": {

          },
          "selected": false,
          "responseHeaderSpecs": [

          ],
          "customRules": [

          ],
          "headerSpecs": [

          ],
          "sessionCookieSecure": false
        }
      ],
      "readTimeoutSeconds": 5,
      "windows": false,
      "skipAPILearning": false,
      "autoProtectPorts": false,
      "trafficMirroring": {

      },
      "expandDetails": true
    }
  ],
  "minPort": 30000,
  "maxPort": 31000
}"""

OOB = """
{
  "_id": "outOfBandAppFirewall",
  "rules": [
    {
      "applicationsSpec": [

      ],
      "readTimeoutSeconds": 5,
      "skipAPILearning": false,
      "unprotectedAPIDiscoveryConfig": {

      },
      "windows": false,
      "collections": [
        {
          "hosts": [
            "*"
          ],
          "images": [
            "*"
          ],
          "labels": [
            "*"
          ],
          "containers": [
            "*"
          ],
          "functions": [
            "*"
          ],
          "namespaces": [
            "*"
          ],
          "appIDs": [
            "*"
          ],
          "accountIDs": [
            "*"
          ],
          "codeRepos": [
            "*"
          ],
          "clusters": [
            "*"
          ],
          "name": "All",
          "owner": "system",
          "modified": "2022-03-27T07:13:42.144Z",
          "color": "#3FA2F7",
          "description": "System - all resources collection",
          "system": true,
          "prisma": false
        }
      ],
      "name": "coco",
      "owner": "ishater",
      "modified": "2022-03-27T08:35:03.144Z"
    }
  ],
  "minPort": 0,
  "maxPort": 0
}"""

LAGRANGE = """
{
  "_id": "containerAppFirewall",
  "rules": [
    {
      "modified": "2022-09-13T13:09:46.113Z",
      "owner": "salvoer",
      "name": "waas-container",
      "previousName": "",
      "collections": [
        {
          "hosts": [
            "*"
          ],
          "images": [
            "*lizatwistlock/waas-mock-service*"
          ],
          "labels": [
            "*"
          ],
          "containers": [
            "*"
          ],
          "functions": [
            "*"
          ],
          "namespaces": [
            "*"
          ],
          "appIDs": [
            "*"
          ],
          "accountIDs": [
            "*"
          ],
          "codeRepos": [
            "*"
          ],
          "clusters": [
            "*"
          ],
          "name": "waas-container-mock",
          "owner": "1admin2",
          "modified": "2022-09-13T12:33:16.397Z",
          "color": "#857af8",
          "system": false,
          "prisma": false
        }
      ],
      "applicationsSpec": [
        {
          "appID": "app-con",
          "sessionCookieSameSite": "Lax",
          "customBlockResponse": {

          },
          "banDurationMinutes": 5,
          "certificate": {

          },
          "tlsConfig": {
            "minTLSVersion": "1.2",
            "metadata": {

            },
            "HSTSConfig": {
              "enabled": false,
              "maxAgeSeconds": 31536000,
              "includeSubdomains": false,
              "preload": false
            }
          },
          "dosConfig": {
            "enabled": false,
            "alert": {
              "burst": 1
            },
            "ban": {

            },
            "matchConditions": [
              {
                "fileTypes": [
                  ".php"
                ],
                "responseCodeRangesTags": [

                ],
                "responseCodeRanges": [

                ]
              }
            ]
          },
          "apiSpec": {
            "endpoints": [
              {
                "host": "*",
                "basePath": "*",
                "exposedPort": 0,
                "internalPort": 8081,
                "tls": false,
                "http2": false,
                "grpc": false
              }
            ],
            "paths": [
              {
                "path": "/api_observation/merchants/small",
                "methods": [
                  {
                    "method": "GET",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form"
                      }
                    ]
                  },
                  {
                    "method": "PUT",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form"
                      }
                    ]
                  },
                  {
                    "method": "POST",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form"
                      }
                    ]
                  },{
                    "method": "DELETE",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form"
                      }
                    ]
                  },
                  {
                    "method": "OPTIONS",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form"
                      }
                    ]
                  },
                  {
                    "method": "HEAD",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form"
                      }
                    ]
                  },{
                    "method": "PATCH",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form"
                      }
                    ]
                  }

                ]
              },
              {
                "path": "/api_observation/merchants/big",
                "methods": [
                  {
                    "method": "GET",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form",
                        "min": 100,
                        "max": 200
                      }
                    ]
                  },
                  {
                    "method": "PUT",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form",
                        "min": 100,
                        "max": 200
                      }
                    ]
                  },
                  {
                    "method": "POST",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form",
                        "min": 100,
                        "max": 200
                      }
                    ]
                  },{
                    "method": "DELETE",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form",
                        "min": 100,
                        "max": 200
                      }
                    ]
                  },
                  {
                    "method": "OPTIONS",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form",
                        "min": 100,
                        "max": 200
                      }
                    ]
                  },
                  {
                    "method": "HEAD",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form",
                        "min": 100,
                        "max": 200
                      }
                    ]
                  },{
                    "method": "PATCH",
                    "parameters": [
                      {
                        "name": "page",
                        "location": "query",
                        "type": "number",
                        "style": "form",
                        "min": 100,
                        "max": 200
                      }
                    ]
                  }

                ]
              }
            ],
            "effect": "disable",
            "fallbackEffect": "disable",
            "queryParamFallbackEffect": "disable"
          },
          "botProtectionSpec": {
            "userDefinedBots": [

            ],
            "knownBotProtectionsSpec": {
              "searchEngineCrawlers": "disable",
              "businessAnalytics": "disable",
              "educational": "disable",
              "news": "disable",
              "financial": "disable",
              "contentFeedClients": "disable",
              "archiving": "disable",
              "careerSearch": "disable",
              "mediaSearch": "disable"
            },
            "unknownBotProtectionSpec": {
              "generic": "disable",
              "webAutomationTools": "disable",
              "webScrapers": "disable",
              "apiLibraries": "disable",
              "httpLibraries": "disable",
              "botImpersonation": "disable",
              "browserImpersonation": "disable",
              "requestAnomalies": {
                "threshold": 9,
                "effect": "disable"
              }
            },
            "sessionValidation": "disable",
            "interstitialPage": false,
            "jsInjectionSpec": {
              "enabled": false,
              "timeoutEffect": "disable"
            },
            "reCAPTCHASpec": {
              "enabled": false,
              "secretKey": {

              },
              "type": "checkbox",
              "allSessions": true,
              "successExpirationHours": 24
            }
          },
          "networkControls": {
            "advancedProtectionEffect": "prevent",
            "subnets": {
              "enabled": false,
              "allowMode": true,
              "allow": [
                "waas-network-list"
              ],
              "fallbackEffect": "prevent",
              "blockingMode": "allowed",
              "alert": null,
              "prevent": null
            },
            "countries": {
              "enabled": false,
              "allowMode": true,
              "allow": [
                "IL"
              ],
              "fallbackEffect": "prevent",
              "blockingMode": "allowed",
              "alert": null,
              "prevent": null
            },
            "networkControlsExceptionSubnets": {
              "subnets": null
            }
          },
          "body": {
            "inspectionSizeBytes": 131072,
            "inspectionLimitExceededEffect": "alert"
          },
          "intelGathering": {
            "infoLeakageEffect": "prevent",
            "removeFingerprintsEnabled": true
          },
          "maliciousUpload": {
            "effect": "prevent",
            "allowedFileTypes": [
              "pdf"
            ],
            "allowedExtensions": [

            ]
          },
          "csrfEnabled": true,
          "clickjackingEnabled": true,
          "sqli": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "xss": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "attackTools": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "shellshock": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "malformedReq": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "cmdi": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "lfi": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "codeInjection": {
            "effect": "prevent",
            "exceptionFields": [

            ]
          },
          "remoteHostForwarding": {

          },
          "customRules": [

          ],
          "autoApplyPatchesSpec": {
            "effect": "disable"
          },
          "responseHeaderSpecs": [

          ],
          "headerSpecs": [

          ],
          "sessionCookieSecure": false
        }
      ],
      "readTimeoutSeconds": 5,
      "windows": false,
      "skipAPILearning": false,
      "autoProtectPorts": false,
      "trafficMirroring": {

      },
      "outOfBandScope": "",
      "expandDetails": true
    }
  ],
  "minPort": 30000,
  "maxPort": 31000
}"""

MAXWELL = """
{
   "_id":"containerAppFirewall",
   "rules":[
      {
         "modified":"2023-05-01T10:38:13.252Z",
         "owner":"ashtrahman",
         "name":"waas-container",
         "previousName":"",
         "collections":[
            {
               "hosts":[
                  "*"
               ],
               "images":[
                  "twistlock/private:console_22_12_704"
               ],
               "labels":[
                  "*"
               ],
               "containers":[
                  "*"
               ],
               "functions":[
                  "*"
               ],
               "namespaces":[
                  "*"
               ],
               "appIDs":[
                  "*"
               ],
               "accountIDs":[
                  "*"
               ],
               "codeRepos":[
                  "*"
               ],
               "clusters":[
                  "*"
               ],
               "name":"waas-container-mock",
               "owner":"ashtrahman",
               "modified":"2023-05-01T10:38:04.553Z",
               "color":"#EF15C8",
               "system":false,
               "prisma":false
            }
         ],
         "applicationsSpec":[
            {
               "appID":"app-con",
               "sessionCookieSameSite":"Lax",
               "customBlockResponse":{

               },
               "banDurationMinutes":5,
               "certificate":{
                  "encrypted":""
               },
               "tlsConfig":{
                  "minTLSVersion":"1.2",
                  "metadata":{
                     "notAfter":"0001-01-01T00:00:00Z",
                     "issuerName":"",
                     "subjectName":""
                  },
                  "HSTSConfig":{
                     "enabled":false,
                     "maxAgeSeconds":31536000,
                     "includeSubdomains":false,
                     "preload":false
                  }
               },
               "dosConfig":{
                  "enabled":false,
                  "alert":{
                     "burst":1
                  },
                  "ban":{

                  },
                  "matchConditions":[
                     {
                        "fileTypes":[
                           ".php"
                        ]
                     }
                  ]
               },
               "apiSpec":{
                  "endpoints":[
                     {
                        "host":"*",
                        "basePath":"*",
                        "exposedPort":0,
                        "internalPort":8081,
                        "tls":false,
                        "http2":false,
                        "grpc":false
                     }
                  ],
                  "paths":[
                     {
                        "path":"/api_observation/merchants/small",
                        "methods":[
                           {
                              "method":"GET",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           },
                           {
                              "method":"PUT",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           },
                           {
                              "method":"POST",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           },
                           {
                              "method":"DELETE",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           },
                           {
                              "method":"OPTIONS",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           },
                           {
                              "method":"HEAD",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           },
                           {
                              "method":"PATCH",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           }
                        ]
                     },
                     {
                        "path":"/api_observation/merchants/big",
                        "methods":[
                           {
                              "method":"GET",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           },
                           {
                              "method":"PUT",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           },
                           {
                              "method":"POST",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           },
                           {
                              "method":"DELETE",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           },
                           {
                              "method":"OPTIONS",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           },
                           {
                              "method":"HEAD",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           },
                           {
                              "method":"PATCH",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           }
                        ]
                     }
                  ],
                  "effect":"disable",
                  "fallbackEffect":"disable",
                  "queryParamFallbackEffect":"disable"
               },
               "botProtectionSpec":{
                  "userDefinedBots":[

                  ],
                  "knownBotProtectionsSpec":{
                     "searchEngineCrawlers":"disable",
                     "businessAnalytics":"disable",
                     "educational":"disable",
                     "news":"disable",
                     "financial":"disable",
                     "contentFeedClients":"disable",
                     "archiving":"disable",
                     "careerSearch":"disable",
                     "mediaSearch":"disable"
                  },
                  "unknownBotProtectionSpec":{
                     "generic":"disable",
                     "webAutomationTools":"disable",
                     "webScrapers":"disable",
                     "apiLibraries":"disable",
                     "httpLibraries":"disable",
                     "botImpersonation":"disable",
                     "browserImpersonation":"disable",
                     "requestAnomalies":{
                        "threshold":9,
                        "effect":"disable"
                     }
                  },
                  "sessionValidation":"disable",
                  "interstitialPage":false,
                  "jsInjectionSpec":{
                     "enabled":false,
                     "timeoutEffect":"disable"
                  },
                  "reCAPTCHASpec":{
                     "enabled":false,
                     "siteKey":"",
                     "secretKey":{
                        "encrypted":""
                     },
                     "type":"checkbox",
                     "allSessions":true,
                     "successExpirationHours":24
                  }
               },
               "networkControls":{
                  "advancedProtectionEffect":"prevent",
                  "subnets":{
                     "enabled":false,
                     "allowMode":true,
                     "allow":[
                        "waas-network-list"
                     ],
                     "fallbackEffect":"prevent"
                  },
                  "countries":{
                     "enabled":false,
                     "allowMode":true,
                     "allow":[
                        "IL"
                     ],
                     "fallbackEffect":"prevent"
                  },
                  "networkControlsExceptionSubnets":{
                     "subnets":[

                     ]
                  }
               },
               "body":{
                  "inspectionSizeBytes":131072,
                  "inspectionLimitExceededEffect":"alert"
               },
               "intelGathering":{
                  "infoLeakageEffect":"prevent",
                  "removeFingerprintsEnabled":true
               },
               "maliciousUpload":{
                  "effect":"prevent",
                  "allowedFileTypes":[
                     "pdf"
                  ],
                  "allowedExtensions":[

                  ]
               },
               "csrfEnabled":true,
               "clickjackingEnabled":true,
               "sqli":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "xss":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "attackTools":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "shellshock":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "malformedReq":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "cmdi":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "lfi":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "codeInjection":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "remoteHostForwarding":{

               },
               "autoApplyPatchesSpec":{
                  "effect":"disable"
               }
            }
         ],
         "readTimeoutSeconds":5,
         "windows":false,
         "skipAPILearning":false,
         "autoProtectPorts":false,
         "trafficMirroring":{

         },
         "outOfBandScope":""
      }
   ],
   "minPort":30000,
   "maxPort":31000
}"""

NEWTON = """
{
   "_id":"containerAppFirewall",
   "rules":[
      {
         "modified":"2023-05-01T10:38:13.252Z",
         "owner":"ashtrahman",
         "name":"waas-container",
         "previousName":"",
         "collections":[
            {
               "hosts":[
                  "*"
               ],
               "images":[
                  "twistlock/private:console_22_12_704"
               ],
               "labels":[
                  "*"
               ],
               "containers":[
                  "*"
               ],
               "functions":[
                  "*"
               ],
               "namespaces":[
                  "*"
               ],
               "appIDs":[
                  "*"
               ],
               "accountIDs":[
                  "*"
               ],
               "codeRepos":[
                  "*"
               ],
               "clusters":[
                  "*"
               ],
               "name":"waas-container-mock",
               "owner":"ashtrahman",
               "modified":"2023-05-01T10:38:04.553Z",
               "color":"#EF15C8",
               "system":false,
               "prisma":false
            }
         ],
         "applicationsSpec":[
            {
               "appID":"app-con",
               "sessionCookieSameSite":"Lax",
               "customBlockResponse":{

               },
               "banDurationMinutes":5,
               "certificate":{
                  "encrypted":""
               },
               "tlsConfig":{
                  "minTLSVersion":"1.2",
                  "metadata":{
                     "notAfter":"0001-01-01T00:00:00Z",
                     "issuerName":"",
                     "subjectName":""
                  },
                  "HSTSConfig":{
                     "enabled":false,
                     "maxAgeSeconds":31536000,
                     "includeSubdomains":false,
                     "preload":false
                  }
               },
               "dosConfig":{
                  "enabled":false,
                  "alert":{
                     "burst":1
                  },
                  "ban":{

                  },
                  "matchConditions":[
                     {
                        "fileTypes":[
                           ".php"
                        ]
                     }
                  ]
               },
               "apiSpec":{
                  "endpoints":[
                     {
                        "host":"*",
                        "basePath":"*",
                        "exposedPort":0,
                        "internalPort":8081,
                        "tls":false,
                        "http2":false,
                        "grpc":false
                     }
                  ],
                  "paths":[
                     {
                        "path":"/api_observation/merchants/small",
                        "methods":[
                           {
                              "method":"GET",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           },
                           {
                              "method":"PUT",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           },
                           {
                              "method":"POST",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           },
                           {
                              "method":"DELETE",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           },
                           {
                              "method":"OPTIONS",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           },
                           {
                              "method":"HEAD",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           },
                           {
                              "method":"PATCH",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form"
                                 }
                              ]
                           }
                        ]
                     },
                     {
                        "path":"/api_observation/merchants/big",
                        "methods":[
                           {
                              "method":"GET",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           },
                           {
                              "method":"PUT",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           },
                           {
                              "method":"POST",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           },
                           {
                              "method":"DELETE",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           },
                           {
                              "method":"OPTIONS",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           },
                           {
                              "method":"HEAD",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           },
                           {
                              "method":"PATCH",
                              "parameters":[
                                 {
                                    "name":"page",
                                    "location":"query",
                                    "type":"number",
                                    "style":"form",
                                    "min":100,
                                    "max":200
                                 }
                              ]
                           }
                        ]
                     }
                  ],
                  "effect":"disable",
                  "fallbackEffect":"disable",
                  "queryParamFallbackEffect":"disable"
               },
               "botProtectionSpec":{
                  "userDefinedBots":[

                  ],
                  "knownBotProtectionsSpec":{
                     "searchEngineCrawlers":"disable",
                     "businessAnalytics":"disable",
                     "educational":"disable",
                     "news":"disable",
                     "financial":"disable",
                     "contentFeedClients":"disable",
                     "archiving":"disable",
                     "careerSearch":"disable",
                     "mediaSearch":"disable"
                  },
                  "unknownBotProtectionSpec":{
                     "generic":"disable",
                     "webAutomationTools":"disable",
                     "webScrapers":"disable",
                     "apiLibraries":"disable",
                     "httpLibraries":"disable",
                     "botImpersonation":"disable",
                     "browserImpersonation":"disable",
                     "requestAnomalies":{
                        "threshold":9,
                        "effect":"disable"
                     }
                  },
                  "sessionValidation":"disable",
                  "interstitialPage":false,
                  "jsInjectionSpec":{
                     "enabled":false,
                     "timeoutEffect":"disable"
                  },
                  "reCAPTCHASpec":{
                     "enabled":false,
                     "siteKey":"",
                     "secretKey":{
                        "encrypted":""
                     },
                     "type":"checkbox",
                     "allSessions":true,
                     "successExpirationHours":24
                  }
               },
               "networkControls":{
                  "advancedProtectionEffect":"prevent",
                  "subnets":{
                     "enabled":false,
                     "allowMode":true,
                     "allow":[
                        "waas-network-list"
                     ],
                     "fallbackEffect":"prevent"
                  },
                  "countries":{
                     "enabled":false,
                     "allowMode":true,
                     "allow":[
                        "IL"
                     ],
                     "fallbackEffect":"prevent"
                  },
                  "networkControlsExceptionSubnets":{
                     "subnets":[

                     ]
                  }
               },
               "body":{
                  "inspectionSizeBytes":131072,
                  "inspectionLimitExceededEffect":"alert"
               },
               "intelGathering":{
                  "infoLeakageEffect":"prevent",
                  "removeFingerprintsEnabled":true
               },
               "maliciousUpload":{
                  "effect":"prevent",
                  "allowedFileTypes":[
                     "pdf"
                  ],
                  "allowedExtensions":[

                  ]
               },
               "csrfEnabled":true,
               "clickjackingEnabled":true,
               "sqli":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "xss":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "attackTools":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "shellshock":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "malformedReq":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "cmdi":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "lfi":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "codeInjection":{
                  "effect":"prevent",
                  "exceptionFields":[

                  ]
               },
               "remoteHostForwarding":{

               },
               "autoApplyPatchesSpec":{
                  "effect":"disable"
               }
            }
         ],
         "readTimeoutSeconds":5,
         "windows":false,
         "skipAPILearning":false,
         "autoProtectPorts":false,
         "trafficMirroring":{

         },
         "outOfBandScope":""
      }
   ],
   "minPort":30000,
   "maxPort":31000
}"""

