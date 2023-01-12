# Rule ports
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
