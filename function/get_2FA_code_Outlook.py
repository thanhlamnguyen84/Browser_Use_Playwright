import re  #Extract 6-digit code
from exchangelib import Credentials, Account, DELEGATE

def get_2fa_code_from_outlook(email: str, password: str, subject_filter: str = "BRTSYS Customer Support"):
    """
    Connects to Outlook using exchangelib and extracts a 6-digit code from the latest email matching the subject.
    """
    credentials = Credentials(username="user-pdm38@mrbstest1.onmicrosoft.com", password="12345678@X")
    account = Account(primary_smtp_address=email, credentials=credentials, autodiscover=True, access_type=DELEGATE)

    # Search inbox for the latest matching email
    for item in account.inbox.filter(subject__contains=subject_filter).order_by('-datetime_received')[:5]:
        match = re.search(r'\b\d{6}\b', item.body)
        if match:
            return match.group(0)
    raise ValueError("No OPT code found in recent emails.")
