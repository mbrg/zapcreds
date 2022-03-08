import pandas as pd


def authenticate_session(session, email, password):
    """
    Authenticate session with Zapier API
    """
    # set zapsession cookie
    session.get("https://zapier.com/api/v4/identity/")

    # set csrftoken cookie
    session.get("https://zapier.com/api/v3/csrf")
    assert "csrftoken" in session.cookies, "Failed to extract csrftoken"

    # get zapier account_id
    account_resp = session.get("https://zapier.com/api/v4/account-discovery/", params={"email": email})
    assert account_resp.json().get("account", {}).get("id"), "Failed to acquire zapier account id. Zapier account does not exist."

    login_resp = session.post(
        "https://zapier.com/api/v3/login",
        headers={"x-csrftoken": session.cookies["csrftoken"], "referer": "https://zapier.com/app/login"},
        json={"account_id": account_resp.json()["account"]["id"], "email": email, "password": password},
    )
    assert 200 <= login_resp.status_code < 300, "Failed to authenticate. Wrong password?"


def __list_apps(session, account_id, is_private):
    response_object_name = "getDistinctAppsWithAuths"
    return session.post(
        url=f"https://zapier.com/api/graphql/v2",
        json={
            "operationName": "GetAppsList",
            "variables": {"accountId": account_id, "isPrivate": is_private},
            "query": f"query GetAppsList($accountId: ID!, $isPrivate: Boolean)"
            f" {{ {response_object_name}(accountId: $accountId, isPrivate: $isPrivate)"
            f" {{ edges {{ id name slug images {{ url_32x32 }} }} }}}}",
        },
    ).json()["data"][response_object_name]["edges"]


def get_credentials(session) -> pd.DataFrame:
    """
    Identify and list credentials available for use on Zapier
    """
    accounts = session.get(url="https://zapier.com/api/v3/accounts").json()["objects"]
    print(f"Found {len(accounts)} accounts")

    connections = []
    for account in accounts:
        account_id = account["id"]

        account_details = session.get(url=f"https://zapier.com/api/v4/accounts/{account_id}/").json()
        print(f"Fetched details of account with id: {account_id}")

        public_account_apps = __list_apps(session, account_id, is_private=False)
        private_account_apps = __list_apps(session, account_id, is_private=True)
        unique_apps = {app["id"]: app for app in public_account_apps + private_account_apps}
        print(
            f"Found {len(public_account_apps)} public apps, {len(private_account_apps)} private apps, {len(unique_apps)} total unique apps in account id: {account_id}"
        )

        account_connections = []
        for app in unique_apps.values():
            app_connections = session.post(
                url=f"https://zapier.com/api/graphql/v2",
                json={
                    "operationName": "GetAppConnections",
                    "variables": {"accountId": account_id, "serviceSlug": app["slug"]},
                    "query": f"query GetAppConnections($accountId: Int!, $serviceSlug: String)"
                    f" {{ authenticationsV2(accountId: $accountId, serviceSlug: $serviceSlug)"
                    f" {{ edges  {{ created description identifier owner {{ email }} selectedApi title }} }} }}",
                },
            ).json()["data"]["authenticationsV2"]["edges"]

            for connection in app_connections:
                account_connections.append(
                    {
                        "account_name": account_details["name"],
                        "account_owner": account_details["owner"]["email"],
                        "app_name": app["name"],
                        "app_version": connection["selectedApi"],
                        "app_icon": app["images"]["url_32x32"],
                        "connection_created": connection["created"],
                        "connection_title": connection["title"],
                        "connection_description": connection["description"],
                        "connection_owner": connection["owner"]["email"],
                    }
                )

        print(f"Found a total of {len(account_connections)} connections in account id: {account_id}")
        connections += account_connections

    return pd.DataFrame(connections)
