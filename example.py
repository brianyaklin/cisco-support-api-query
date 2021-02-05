"""Example usage of Cisco Support API utilities
"""

import csv
from dotenv import dotenv_values
from util.api_login import ApiLogin
from util.api_eox import ApiEox


def main():
    """Example usage of Cisco Support API utilities

    This example requires a Cisco Support API client key and secret
    stored in a .env file in the current directory. These credentials
    are used to login to the Cisco Support API to obtain an authentication
    token, which is then used with the EoX API end-point. Two example
    Cisco PID's are used to show the use of the EoX API and the results
    are saved to a CSV file.
    """

    client_key = dotenv_values('.env')['CLIENT_KEY']
    client_secret = dotenv_values('.env')['CLIENT_SECRET']

    api = ApiLogin(client_key, client_secret)
    eox = ApiEox(api.auth_token)
    pids = ['WS-C3750X-48PF-S', 'C3KX-PWR-1100WAC', ]
    eox.query_by_pid(pids)

    FNAME = 'eox_report.csv'
    with open(FNAME, mode='w') as fhand:
        fieldnames = ['EOLProductID', 'ProductIDDescription',
                      'ProductBulletinNumber', 'LinkToProductBulletinURL',
                      'EndOfSWMaintenanceReleases',
                      'EOXExternalAnnouncementDate', 'EndOfSaleDate',
                      'EndOfSecurityVulSupportDate',
                      'EndOfRoutineFailureAnalysisDate',
                      'EndOfServiceContractRenewal', 'LastDateOfSupport',
                      'EndOfSvcAttachDate', 'UpdatedTimeStamp',
                      'EOXMigrationDetails', 'EOXInputType',
                      'EOXInputValue']
        writer = csv.DictWriter(fhand, fieldnames=fieldnames)
        writer.writeheader()
        for record in eox.records:
            writer.writerow(record)

    print(f'EOX records written to file {FNAME}')


if __name__ == "__main__":
    main()
