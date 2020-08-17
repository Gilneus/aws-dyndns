import requests
import click
import boto3

@click.command()
@click.option('--profile', help='Name des lokalen AWS-Profils.')
@click.option('--record', help='Name des Records, der angelegt werden soll z.B. lukas.dyndns.meineDomain.io, der Teil dyndns.meineDomain.io ist dabei nicht austauschbar.')
def createDynDnsRecord(profile, record):
    session = boto3.Session(profile_name=profile)
    route53Client = session.client('route53')
    hostedZoneId = 'MEINE HOSTED ZONE ID'
    recordExists = False

    click.secho('')

    if not record.endswith('.dyndns.meineDomain.io'):
        record = record + '.dyndns.meineDomain.io'

    # Öffentliche IP ermitteln
    clientPublicIp = requests.get('https://checkip.amazonaws.com').text.strip()

    if clientPublicIp is not None:
        click.secho("Die öffentliche IP-Adresse lautet: %s" % (str(clientPublicIp)), fg='blue')

        # Check if record set exists
        recordCheckResponse = route53Client.list_resource_record_sets(
            HostedZoneId=hostedZoneId
        )

        for resource in recordCheckResponse['ResourceRecordSets']:
            if resource['Name'] == record+'.':
                recordExists = True
        
        if recordExists:
            click.secho("DNS-Eintrag %s existiert bereits, der Eintrag wird geändert." % (record), fg='blue')
        else:
            click.secho("DNS-Eintrag existiert noch nicht, der Eintrag wird angelegt.", fg='blue')

        # Eintrag ändern oder anlegen
        recordChangeResponse = route53Client.change_resource_record_sets(
            HostedZoneId=hostedZoneId,
            ChangeBatch={
                'Comment': 'add or change %s' % (record),
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': '%s.' % (record),
                            'Type': 'A',
                            'SetIdentifier': record,
                            'Region': 'eu-central-1',
                            'TTL': 60,
                            'ResourceRecords': [
                                {
                                    'Value': clientPublicIp,
                                }
                            ],
                        }
                    },
                ]
            }
        )
        if recordChangeResponse['ResponseMetadata']['HTTPStatusCode'] == 200:
            click.secho("DNS-Eintrag wurde erfolgreich angelegt, die IP-Adresse: %s ist nun über %s erreichbar." % (clientPublicIp, record), fg='green')
        else:
            click.secho("Etwas ist schief gelaufen. Fehlermeldung: \n %s" % (recordChangeResponse), fg='red')
    else:
        click.secho("Öffentliche IP-Adresse konnte nicht ermittelt werden.", fg='red')

if __name__ == '__main__':
    createDynDnsRecord()
