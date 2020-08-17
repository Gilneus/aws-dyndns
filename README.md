Dieses Skript verknüpft einen beliebigen DNS-Record für eine gewünschte AWS Hosted-Zone (*.dyndns.meineDomain.io) mit der öffentlichen IP des Clients. Sollte der DNS-Record noch nicht existieren, so wird er angelegt, andernfalls wird er einfach nur verändert.

## How to use
_Wichtig: Für die Verwendung des Skripts wird Python3 und die Python Paketverwaltung (pip) benötigt._
1. Nach dem clonen müssen zuerst die benötigten Python3-Pakete installiert werden:  ```
pip3 install requests click boto3 awscli ```
2. Es muss ein AWS-Profil auf dem Rechner angelegt werden (aws configure --profile MEINPROFIL)
3. Das DynDNS-Skript ausführen ``` python3 dyndns.py --profile MEIN-PROFIL --record MEIN-DNS-RECORD-NAME ``

## CLI
```
Usage: dyndns.py [OPTIONS]

Options:
  --profile TEXT  Name des lokalen AWS-Profils.
  --record TEXT   Name des Records, der angelegt werden soll z.B.
                  lukas.dyndns.meineDomain.io, der Teil dyndns.meineDomain.io ist dabei
                  nicht austauschbar.
  --help          Show this message and exit.
```
