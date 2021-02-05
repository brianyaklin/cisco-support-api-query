# cisco-support-api-query

A utility package which can be used to query Cisco's Support API's

# Introduction

This repo provides utilities to work with Cisco's Support API's for querying
different information such as EoX records. Additional API end-points will be
added as time permits.

You will need to have your own API client key and secret with a grant type of
client_credentials.

Refer to [Cisco's API Documentation](https://developer.cisco.com/docs/support-apis/)
for complete details on how to register an application and obtain API keys.

# Example

An more complete example is provided provided in example.py, but a general workflow
of using these utilities can be seen as follows

```
from util.api_login import ApiLogin
from util.api_eox import ApiEox

# Replace with your own API key and secret
api = ApiLogin("my_client_key", "my_client_secret")

eox = ApiEox(api.auth_token)
eox.query_by_pid(['WS-C3750X-48PF-S','C3KX-PWR-1100WAC'])
print(eox.records)

# Sometime later
api.auth_still_valid()
eox.query_by_pid(['N5K-C5020P-BF','N5K-C5020-FAN', 'CISCO2851', 'NM-HDV2-1T1/E1'])
print(eox.records)
```

# Cisco Support EoX API End-Point

The [Cisco Support EoX API end-point](https://developer.cisco.com/docs/support-apis/#!eox) allows you to query Cisco's Support API for end-of-life information. Their API
has a few end-points that allow you to query by

- Dates
- Product ID's
- Serial Numbers
- Software Release Strings

The util.api_eox.py script currently permits querying by hardware Product ID's and
deduplicates the list of PID's that are provided for more efficient API queries. Up
to 20 PID's can be included in each API call and the script maximizes this effort.

Upon querying Cisco's EoX API an EOXRecord(s) is returned. The util.api_eox.py script
records this information in the self.records attribute as a list:

```
# Keys for each record are as follows
>>> eox.records[0].keys()
dict_keys(['EOLProductID', 'ProductIDDescription', 'ProductBulletinNumber', 'LinkToProductBulletinURL', 'EOXExternalAnnouncementDate', 'EndOfSaleDate', 'EndOfSWMaintenanceReleases', 'EndOfSecurityVulSupportDate', 'EndOfRoutineFailureAnalysisDate', 'EndOfServiceContractRenewal', 'LastDateOfSupport', 'EndOfSvcAttachDate', 'UpdatedTimeStamp', 'EOXMigrationDetails', 'EOXInputType', 'EOXInputValue'])

# An example record
>>> eox.records
[{'EOLProductID': 'WS-C3750X-48PF-S', 'ProductIDDescription': 'Catalyst 3750X 48 Port Full PoE IP Base', 'ProductBulletinNumber': 'EOL10623', 'LinkToProductBulletinURL': 'http://www.cisco.com/c/en/us/products/collateral/switches/catalyst-3560-x-series-switches/eos-eol-notice-c51-736139.html', 'EOXExternalAnnouncementDate': {'value': '2015-10-31', 'dateFormat': 'YYYY-MM-DD'}, 'EndOfSaleDate': {'value': '2016-10-30', 'dateFormat': 'YYYY-MM-DD'}, 'EndOfSWMaintenanceReleases': {'value': '2017-10-30', 'dateFormat': 'YYYY-MM-DD'}, 'EndOfSecurityVulSupportDate': {'value': '2019-10-30', 'dateFormat': 'YYYY-MM-DD'}, 'EndOfRoutineFailureAnalysisDate': {'value': '2017-10-30', 'dateFormat': 'YYYY-MM-DD'}, 'EndOfServiceContractRenewal': {'value': '2021-01-28', 'dateFormat': 'YYYY-MM-DD'}, 'LastDateOfSupport': {'value': '2021-10-31', 'dateFormat': 'YYYY-MM-DD'}, 'EndOfSvcAttachDate': {'value': '2017-10-30', 'dateFormat': 'YYYY-MM-DD'}, 'UpdatedTimeStamp': {'value': '2015-11-02', 'dateFormat': 'YYYY-MM-DD'}, 'EOXMigrationDetails': {'PIDActiveFlag': 'Y', 'MigrationInformation': 'Cisco Catalyst 3850 48 Port Full PoE IP Base', 'MigrationOption': 'Enter PID(s)', 'MigrationProductId': 'WS-C3850-48F-S', 'MigrationProductName': '', 'MigrationStrategy': '', 'MigrationProductInfoURL': 'http://www.cisco.com/c/en/us/products/switches/catalyst-3850-series-switches/index.html'}, 'EOXInputType': 'ShowEOXByPids', 'EOXInputValue': 'WS-C3750X-48PF-S '}]
```
