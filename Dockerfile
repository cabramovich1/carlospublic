FROM python:alpine
ENV  APP_USER="1admin2"
ENV  APP_PASSWORD="M8%9SrK#qb2kguVG"
COPY server.py server.py
EXPOSE 8080
ENTRYPOINT /server.py -a True -u ${APP_USER} -p ${APP_PASSWORD} -P 8080


# Twistlock Container Defender - app embedded
ADD twistlock_defender_app_embedded.tar.gz /tmp
ENV DEFENDER_TYPE="appEmbedded"
ENV DEFENDER_APP_ID="shir-app-embedded-ec2"
ENV FILESYSTEM_MONITORING="true"
ENV WS_ADDRESS="wss://3.249.208.216:8084"
ENV DATA_FOLDER="/tmp"
ENV INSTALL_BUNDLE="eyJzZWNyZXRzIjp7ImRlZmVuZGVyLWNhLnBlbSI6Ii0tLS0tQkVHSU4gQ0VSVElGSUNBVEUtLS0tLVxuTUlJREhUQ0NBZ1dnQXdJQkFnSVJBT0pvT2NFQlpBQU0yT3dkYlpiR2lNNHdEUVlKS29aSWh2Y05BUUVMQlFBd1xuS0RFU01CQUdBMVVFQ2hNSlZIZHBjM1JzYjJOck1SSXdFQVlEVlFRREV3bFVkMmx6ZEd4dlkyc3dIaGNOTWpJd1xuT0RBNU1UTXdPREF3V2hjTk1qVXdPREE0TVRNd09EQXdXakFvTVJJd0VBWURWUVFLRXdsVWQybHpkR3h2WTJzeFxuRWpBUUJnTlZCQU1UQ1ZSM2FYTjBiRzlqYXpDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ1xuZ2dFQkFMNXl4RzE4eGVKbEY2R05VNmpZNk1XZ0NaRERlYjZkUnIwc1V1TDZ3VVhrdHNPVEp0R1ViZGlkaWRBTlxuUEdNTDcxditrWFZtcDkwZElLUTdBMWsxQzhmbEE3N0VUU2dpYkw5OWp3YjdMN25DMi9IcTlpL21QU0U0TzhmZ1xuUUpuUis1MTBzWDZNKy92WlZIYjBqc25jL3BKYnBnKytRZzBiT0VJTnFiOUF4dkNOSHdUYkd2STBLb3VTa25PcFxucW5lVXdKMUphZWpyMFBUVFF1WjJmTGltQkVhWXYzM0s3dHE4akFwZE1tQmVrMHhib3dKUmIxc01DRzRQU1hSc1xuSzFEV3h5TWhVdXRvNXlCdDhVSGdENmUzdzU0S2VVWmRESGEyM0oyV2pYdUlUNG51OTIyelpDdjVrR3ZmaDVjWFxubVJGWUdtZWdtZzVLeld2aFF6QnhnTmdGRkpNQ0F3RUFBYU5DTUVBd0RnWURWUjBQQVFIL0JBUURBZ0tzTUE4R1xuQTFVZEV3RUIvd1FGTUFNQkFmOHdIUVlEVlIwT0JCWUVGTVdEL0xwa0g0T2lvRXBGRFBkdVJySUEvVjdWTUEwR1xuQ1NxR1NJYjNEUUVCQ3dVQUE0SUJBUUMwaHhZQW04K2phYWxRQ2hCR0RGNGZNYkppMGxURmdNN2tOVUpXSTc1dVxuVU1ybTdqcFU1cVdiUVlEb0txSlg0dVhMaDdZWTJ3MEdzNEF5eHQ4VG5BTVFzMGhodi8xMWR1aTN2ek9GMVB5Q1xuVWQzZUZ4MDIycGlUNEFTQ0FjNE5BY3RsUXFvdk1Oano2andvUHQ2VWFRUmJXQlFYM1AxOWUwOTMzN1dSN2xLMFxuNDZaYzczUmNKZXl0MEQ1dm9GcFFTWjJvaEVwUUFHV0MxVzFZMEJLUlV6OVBZa1BmQnExN2E1dnZRSEUzUFRoK1xuUlVXbnUwN3dYdDJLN2VOQXo4ZkI2ZWljK1hIakJVR0tIUksxMm82Z3lrcG1Sak5BdGNhS092NEtIT2h5UXlDVVxuVG14OEhkZHBRL2Z3U095elgvSkRZL3JzczRmVDQ2eUl1VE5Id3RLQmdMZ2Zcbi0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS1cbiIsImRlZmVuZGVyLWNsaWVudC1jZXJ0LnBlbSI6Ii0tLS0tQkVHSU4gQ0VSVElGSUNBVEUtLS0tLVxuTUlJRFBEQ0NBaVNnQXdJQkFnSVJBTkhqYTRvcDIrM1kzRFRGSWIxamt1QXdEUVlKS29aSWh2Y05BUUVMQlFBd1xuS0RFU01CQUdBMVVFQ2hNSlZIZHBjM1JzYjJOck1SSXdFQVlEVlFRREV3bFVkMmx6ZEd4dlkyc3dIaGNOTWpJd1xuT0RBNU1UTXdPREF3V2hjTk1qVXdPREE0TVRNd09EQXdXakFvTVJJd0VBWURWUVFLRXdsVWQybHpkR3h2WTJzeFxuRWpBUUJnTlZCQU1UQ1d4dlkyRnNhRzl6ZERDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ1xuZ2dFQkFNZDkySmtrNSs1V3BubGpCck9LUlhiamxwZk1kbnVnZHNRVk1iV1ZKTTBPMXBkOHRwbGgvNWJTLzcvUVxuTjFzYVJwdGdvT0xDcmxBKzV5Y1hKVElabUlpLzdNaGRKRUM5aXFRd1lsM01QZ2JvT053M1BaSXp2WGtWVU1JelxuZnFFWXlacTBTOFdMVU5nNzAyQWlJVDFuL0dpdkVSZVJmdEUveTdmK3Y4Nk45RU9FV3NrSzN6RjlvdWdTUWJzdVxuamhETFRrdnZMcEZqL3VyYjY4VUtiT1VWNkhYVVpDOXpZVmN1VHN4MklKMThWMm5kaWs2enZyWGRmVkk3Vk03SlxuZDFTOTFwSDkzRE9kVno5aG00RTZwQTVVYmEwUDR2NW9BYSs4NXp5eEJqUXVweCtrSE5YQTZ1S1k3VDh4SDdoUlxuWmxWK2g3SE9oK3pWMlJSVk4reEl0eWZRQlg4Q0F3RUFBYU5oTUY4d0RnWURWUjBQQVFIL0JBUURBZ2VBTUJNR1xuQTFVZEpRUU1NQW9HQ0NzR0FRVUZCd01DTUF3R0ExVWRFd0VCL3dRQ01BQXdId1lEVlIwakJCZ3dGb0FVeFlQOFxudW1RZmc2S2dTa1VNOTI1R3NnRDlYdFV3Q1FZRktnUUJBZ2NFQURBTkJna3Foa2lHOXcwQkFRc0ZBQU9DQVFFQVxuZTQvcVlwb3kzcGhYbTMxNEswMmd1SkgzUUZuYVl4Z2x3UHV2bi9GNFJBSWdDbVBLNUpIRTV0VkgrdWh6OS9TR1xuZ2dCNzliUDNsZ0czQWh4SmNoY1Q4dHAxVnNMa2IxWklZMUZ3cFJmdG9SYUVTdDN3Um9HYkFaN29NNmVVbXQvc1xuVTV1cmNFUXpScVNDaEVRbEM4eEdteEx1bUROYlBqelVPMm9EMmhjajEvTk00SkNrSTN2WTUyVGpQL0RvZitXQlxuVVFuZmpJSVh5NnpuZTBWcFlUclgvMERNNUJlWitUanlDV05adzBBSE03WG96M1Jqd2hVei9mdW1sYklycmVNRlxuM0hBR29NY1RxZU9URzFiMlhpQVkyQmF0bVl4U0hPMWlwNDRnSnJ3ZVVFUS9lVWJiUllSTTk4eGZvMDNMVCsvWVxuclVRZ3ErOUpUQ042VnZxMGkwWUZjUT09XG4tLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tXG4iLCJkZWZlbmRlci1jbGllbnQta2V5LnBlbSI6Ii0tLS0tQkVHSU4gUlNBIFBSSVZBVEUgS0VZLS0tLS1cblByb2MtVHlwZTogNCxFTkNSWVBURURcbkRFSy1JbmZvOiBBRVMtMjU2LUNCQywyMTc4MGE3MGM1NjFlNjE3ODVhOTliOGNkYTA5MDhmMlxuXG5ZTkY2OUZscXpiNHlDNmhwYWdrRTUxb1ZFWTVIS3FUYy8zYU5BZ3ZOR1E5TmlnbmJTLzBydUJ1bGRoaTlLbExjXG5kV0xoeXgydkVuUEZLV3ptRmcrTitGZHcyNXhnMlV5MnlMR2tFUTlGQnAxYTVBWEphMlBvV0t5TlpsNnBuOStqXG5jaU9DZE50d0RnV29zV0wzWURyKzBHM2RPd1dpTFlNUkR6c0thYU9LL1hYNmt0bFdxbUZCNUtaMlpqenFoMVc1XG5EQ0kxQlhETEJ4WlRMV2ZWNGtCU2JGRS9UdnlUcG05NjZIVkx1aWRtSkNMMHVLeDhhVzdzd2lFbzBuc25HT0ZzXG56SnVHbGJOWW9vUUZLTkNQWDhObDJhWGRMdG9KSFh5bStoTkpjSG4vbStYa0VpY05vNlpJaUZWVGFXU1Bja0xBXG5iMG41OVQ5MWFGNmRweHcxTWRxWHI0aVZLOU0xTWJTa0xRdEdLbjNPZDFwdzJ6MUtKbUJKRlVtdnVDMmQwOFhTXG5obEY3VUJoeW1DTmsvRHU3Uy9ncGthNFdBajRjQ09CYVRSZHZaSlEyN2VaZ1cxdW1VdHlWNjE0aXpWR0oyMUl0XG5uZXlpN0VManVJK0VNSDlxOGtsYmFuK292dU1qN2w4Rm1tSGsvd0pQYWRiMWU1cHFOZzFrY3BCS3h1SU5JbnJ3XG5GNHpjc3FLei9Hcjl5eXQ3MFhMYUVlMFZlZlFhRVNYd3lEMlgybkJYZ0haUTNTRWVrWlZMOGJEQTJabW5WNGVLXG5HVDJVVkhPeGtnczRuNXlqQS9vS1FVclY0WWZYR0ZoYzllVHpKVndoWnYrN1VyQ0UyRjRPSzlMNGJ0QTJCMzA2XG5GSEROV2kzY0dDanR5NldtMGt6cWo3VmRnZmtma1liTXptYzFTOXRYcmpYb2hXTnZDQ0tkYW9UNEZBY1lFNnJPXG5LU0dvZVUyN1YzbHA4TG83NVFsMGE3NE81SVlDZEtrdThhRXFpdzRaeGorckJvdjVXYjNFTTFuMDloNDVETTdQXG5wbnpzemw3Y3REczNGU0FIekVNWkhQQ1NHNUd2VVRnM0JhTVZGMmxITjIvRmlQT2FnV29iUUREVXZZbHdLcFc0XG5hNE9sT0pRZ3BJZUFJQ0JOT0hicDV3RUE5Q3pyZTVNZ0R3QWx6cEc2aE52bE1mN3RPZ2tSYzA5WHBRZjFxQXJ5XG41VzVkTzU2aVNRZFpkYjY3SVFGTU9sdEpaTnRhaGNKQmlaZkgvcFRRanZmemFpOWN2TDlGYWo2cDVLVS9saFZQXG5PTGZmQWFIQ0VXTjVqeGdNcUZBdHVnSzdKTjJUbHhFdTQxdTU5K2kyY2FlQ2RPNWtLWWlMVm4yeGZHSHpGUnhKXG5qN3NHRG1ZN0gvRGN3MnlIZHQyK0Z4dnllRkhmeEdDQTZoRG03QUFNTVZZczhtTnhSODVGV2ZyY21zZGZwUnRaXG5MdUZmemtSdkJ4YTllaWcwZWx2a3dZRnkwVmIyRExzQkxrQWVyQiszb1JqWmNmOFZKU1d5ajF0ajlPZHV6aDI5XG5pTkt4VUxxeU9hZGJNbGpzZXBZVHEydHRtRXZtZHBoenBPaG1uaU5uQUdBclhwTDVObnA3ZWplVGd4VFVIWVFWXG53R2w0MldXU1RDQXpHVmdEcmtMM21KNmg3MnFnSklIa3Z5U1lyZUkyOHNrWnIwT3kzRTVDbkp6ZjhYWlZOM0N4XG43MkM4K3JVdGxNTTFUeFNFeUpiZ2Y4ZW9jQ2wvVG9EbGVkcFV6STNvZ3piU0xPRWhaZXpQSFZvNDdsZGFiQlpBXG56SE9DYzZHS3hMa1V1RGJ0WTEzWStwTENDYjNhOTZJR0M4UGhtWm5qWkNrL3oyb2Y4dWl6d3BkQnJZak9TeDB6XG5aK0djU1JvRmZKWlppLzBPb0UyN2cwRTNoWlBtTWJJekNNT1ZQSlJBZHJieThZNEJnWXM4dnBNUDF5WHpUYnJxXG5Xa1lzOUdMSVlVb1V5eTlMaFQ3TGJMUEMxTitBMWs5OGFIWitiWE05UmJCMUhLVWFqQ2hXWURHcGxmWk1ZK0FoXG4rMXBWTzkyZ3psUE00NFBPMFRVUWhGZzlLb1FEb1FlTmJnbTdaa1ZucDlLelBkRjh4T3h2NkZuV0VlUm5QQ1hTXG4tLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLVxuIiwic2VydmljZS1wYXJhbWV0ZXIiOiJoZkR4RnJ1SHZPNTBqam9pR3E5NTFqaUh2Z3FmQ00rUFhZcHZnRmlwaVFiOTduMVRtWko2a2cyaFRkakM4d2Y0dmtwSXdsa2hraExpTE0relQ4eTNIdz09In0sImdsb2JhbFByb3h5T3B0Ijp7Imh0dHBQcm94eSI6IiIsIm5vUHJveHkiOiIiLCJjYSI6IiIsInVzZXIiOiIiLCJwYXNzd29yZCI6eyJlbmNyeXB0ZWQiOiIifX0sIm1pY3Jvc2VnQ29tcGF0aWJsZSI6ZmFsc2UsImltYWdlU2NhbklEIjoiM2NlYWIwMWEtOTA2Ni04MGVlLTY1NDktNzE5ZmRjOGZjMjgzIn0="
ENTRYPOINT exec /tmp/defender app-embedded /bin/sh -c '/server.py -a True -u ${APP_USER} -p ${APP_PASSWORD} -P 8080'