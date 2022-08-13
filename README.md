# ZapCreds

ZapCreds is a recon tool that harvests credentials from Zapier.

Given a Zapier user, ZapCreds will scan every Zapier account the user has access to and will retrieve private connections owned by this user and shared connections the user has access to.

----

This tool was released as part of DEFCON30. For more details, see [Low Code High Risk: Enterprise Domination via Low Code Abuse](https://github.com/mbrg/defcon30/blob/main/Low_Code_High_Risk/readme.md).

Disclaimer: these materials are presented from an attacker’s perspective with the goal of raising awareness to the risks of underestimating the security impact of No Code/Low Code. No Code/Low Code is awesome.

## Output example

|account_name|app_name            |app_icon            |connection_created                      |connection_title             |connection_owner      |
|------------|--------------------|--------------------|----------------------------------------|-----------------------------|----------------------|
|Marketing|Dropbox             |![Dropbox](https://cdn.zapier.com/storage/services/13ed79eef97afd56b212ece05251b2de.32x32.png)|2021-06-06T10:54:52Z                    |Dropbox johnw@gmail.com|John.Webb@mycompany.com  |
|Marketing|Gmail               |![Gmail](https://cdn.zapier.com/storage/services/54f0bd6f9c31b757ab20d4c7058dc7c0.32x32.png)|2021-06-06T10:00:14Z                    |Gmail Bobby.Atkinson@mycompany.com |Bobby.Atkinson@mycompany.com  |
|Marketing|Gmail               |![Gmail](https://cdn.zapier.com/storage/services/54f0bd6f9c31b757ab20d4c7058dc7c0.32x32.png)|2021-06-06T07:53:42Z                    |Gmail Lola.Burton@mycompany.com #2|Lola.Burton@mycompany.com|
|Marketing|Google Calendar     |![Google Calendar](https://cdn.zapier.com/storage/services/62c82a7958c6c29736f17d0495b6635c.32x32.png)|2022-01-25T21:08:48Z                    |Google Calendar johnw@gmail.com|John.Webb@mycompany.co  |
|Marketing|Google Drive        |![Google Drive](https://cdn.zapier.com/storage/services/bb735e567f1a1e9e3b8b7241497c2d43.32x32.png)|2022-01-26T11:10:41Z                    |Google Drive Bobby.Atkinson@mycompany.com |Bobby.Atkinson@mycompany.com  |
|SalesOps|Google Sheets       |![Google Sheets](https://cdn.zapier.com/storage/services/8913a06feb7556d01285c052e4ad59d0.32x32.png)|2022-02-20T09:20:15Z                    |Google Sheets Sariah.Cote@mycompany.com|Sariah.Cote@mycompany.com|
|SalesOps|OneNote             |![OneNote](https://cdn.zapier.com/storage/developer/e951e0105790e43b117e04b7bba34601.32x32.png)|2022-03-03T09:18:36Z                    |OneNote gibsonm@outlook.com #2|Mia.Gibson@mycompany.com  |

## Usage

### Install

```bash
git clone https://github.com/mbrg/zapcreds
# use python>=3.6
python -m pip install .
```

### Examples

Command line

```bash
zapcreds --email John.Webb@mycompany.com --password password -out found_creds.csv
```

Python

```python
import requests
from zapcreds.harvest import authenticate_session, get_credentials

session = requests.Session()
authenticate_session(session, "John.Webb@mycompany.com", "password")
creds = get_credentials(session)

print(creds.columns)
# Index(['account_name', 'account_owner', 'app_name', 'app_version', 'app_icon', 'connection_created', 'connection_title', 'connection_description', 'connection_owner'],
```

## Contributing

Pull requests and issues are always welcome.