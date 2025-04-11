import jwt
import time
import re
from exchangelib import DELEGATE, Account, Configuration, Credentials, OAuth2LegacyCredentials
# from robot.libraries.BuiltIn import BuiltIn
import html
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

def get_auth_token(username,password):
    currtime = int(time.time())

    secret_key = "wwCHvIR6XCxeY1yDeNp6HPUtoi9YexvP"
    params = {
        "username": username,
        "password": password,
        "iat": currtime,
        "exp": currtime + 10
    }
    auth = jwt.encode(params, secret_key, algorithm='HS256')
    auth = auth.decode("utf-8")
    print(auth)
    return "Bearer " + auth


def get_2fa_code_from_outlook(user, password, mail_server_url):
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    tenant_id = os.getenv('TENANT_ID')

    credentials = OAuth2LegacyCredentials(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id,
    username=user, password=password)
    config = Configuration(server=mail_server_url, credentials=credentials, auth_type='OAuth 2.0')
    account = Account(user, credentials=credentials, autodiscover=False, config=config,access_type=DELEGATE)

    print("Setup is OK")
    try:
        p = re.compile(r'\d{6}')
        return p.findall(account.inbox.all().order_by('-datetime_received')[0].body)[0]
    except:
        return "NONE"


def get_code(user, password, mail_server_url):
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    tenant_id = os.getenv('TENANT_ID')

    credentials = OAuth2LegacyCredentials(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id,
    username=user, password=password)
    config = Configuration(server=mail_server_url, credentials=credentials, auth_type='OAuth 2.0')
    account = Account(user, credentials=credentials, autodiscover=False, config=config,access_type=DELEGATE)

    print("Setup is OK")
    p = re.compile(r'\w+')
    return p.findall(account.inbox.all().order_by('-datetime_received')[0].body)[84]


def get_takeout_file(user, password, mail_server_url):
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    tenant_id = os.getenv('TENANT_ID')

    credentials = OAuth2LegacyCredentials(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id,
    username=user, password=password)
    config = Configuration(server=mail_server_url, credentials=credentials, auth_type='OAuth 2.0')
    account = Account(user, credentials=credentials, autodiscover=False, config=config,access_type=DELEGATE)

    print("Setup is OK")
    p = re.compile(r'\w+')
    return p.findall(account.inbox.all().order_by('-datetime_received')[0].body)[74]

def get_content_email(user, password, mail_server_url):
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    tenant_id = os.getenv('TENANT_ID')

    credentials = OAuth2LegacyCredentials(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id,
    username=user, password=password)
    config = Configuration(server=mail_server_url, credentials=credentials, auth_type='OAuth 2.0')
    account = Account(user, credentials=credentials, autodiscover=False, config=config,access_type=DELEGATE)
    print("Setup is OK")
    p = re.compile(r'\w+|\W+')
    print(p)
    if "html" in p.findall(account.inbox.all().order_by('-datetime_received')[0].body):
        text = ""
        for i in p.findall(account.inbox.all().order_by('-datetime_received')[0].body):
            text = text + i
        result_text = html.unescape(re.sub('<[^>]*>', '', text))
        return re.findall(r'\w+|\W+', result_text)
    else:
        return p.findall(account.inbox.all().order_by('-datetime_received')[0].body)


def get_subject_email(user, password, mail_server_url):
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    tenant_id = os.getenv('TENANT_ID')

    credentials = OAuth2LegacyCredentials(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id,
    username=user, password=password)
    config = Configuration(server=mail_server_url, credentials=credentials, auth_type='OAuth 2.0')
    account = Account(user, credentials=credentials, autodiscover=False, config=config,access_type=DELEGATE)

    try:
        p = re.compile(r'\w+|\W+')
        return p.findall(account.inbox.all().order_by('-datetime_received')[0].subject)
    except:
        return ["No email"]


def delete_all_emails(user, password, mail_server_url):
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    tenant_id = os.getenv('TENANT_ID')

    credentials = OAuth2LegacyCredentials(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id,
    username=user, password=password)
    config = Configuration(server=mail_server_url, credentials=credentials, auth_type='OAuth 2.0')
    account = Account(user, credentials=credentials, autodiscover=False, config=config,access_type=DELEGATE)
    account.inbox.empty()

def verify_receive_inform_email(user, password, mail_server_url, timeout, subject, *content):
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    tenant_id = os.getenv('TENANT_ID')

    credentials = OAuth2LegacyCredentials(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id,
    username=user, password=password)
    config = Configuration(server=mail_server_url, credentials=credentials, auth_type='OAuth 2.0')
    account = Account(user, credentials=credentials, autodiscover=False, config=config,access_type=DELEGATE)

    start = time.time()
    time.sleep(5)
    for i in range(timeout):
        item_list = account.inbox.all().order_by('-datetime_received')
        if not len(list(item_list)) and (time.time() - start > timeout):
            time.sleep(1)
            continue

        if time.time() - start > timeout:
            break
        if item_list.count() >= 1:
            item = item_list[0]
            if item.subject == subject:
                break
        time.sleep(1)

    if item_list.count() == 0:
        raise AssertionError("No email received")
    BuiltIn().log("Email \nsubject: {} \nbody: {}".format(item.subject,item.body))
    BuiltIn().should_be_equal(item.subject, subject)
    content_pattern = '*' + '*'.join(content) + '*'
    BuiltIn().should_match(item.body, content_pattern)

def convert_datetime_to_timezone(datetime_str, from_tz, to_tz, result_format="%d/%m/%Y %I:%M %p"):
    input_time = datetime.strptime(datetime_str, result_format)
    from_timezone = pytz.timezone(from_tz)
    localized_time = from_timezone.localize(input_time)

    to_timezone = pytz.timezone(to_tz)
    converted_time = localized_time.astimezone(to_timezone)

    return converted_time.strftime(result_format)

def get_latest_path(response):
    data = response['data']
    latest_entry = sorted(data, key=lambda x: x['create_time'], reverse=True)[0]

    return latest_entry['path']
