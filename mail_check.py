import os
import poplib
import email
from discovery_za_parser import DiscoveryZaParser

def get_config(path):
    config = {}
    f= open(path,'r')
    lines = f.readlines()
    for l in lines:
        tokens = l.split(':')
        if len(tokens) != 2:
            raise "Expected config lines to contain exactly two fields"
        key = tokens[0].strip()
        value = tokens[1].strip()
        config[key] = value
    return config

def get_pop_client(config):
    server = config['server']
    port = config['port']
    username = config['username']
    password = config['password']
    print(f"Server {server}, Port {port}")
    popclient = poplib.POP3(server, port)
    popclient.user(username)
    popclient.pass_(password)
    return popclient

# Returns a list of parsed emails
def list_inbox(inbox):
    msg_count, inbox_size = inbox.stat()
    print(f"Found {msg_count} messages")
    if msg_count < 1:
        return []
    msgs = []
    for i in range(1,msg_count+1):
        print(f"Fetching message {i}")
        msg = inbox.retr(i)
        raw_email = b"\n".join(msg[1])
        parsed_email = email.message_from_bytes(raw_email)
        msgs.append(parsed_email)
    return msgs

def extract_text(parsed_email):
    for part in parsed_email.walk():
        type = part.get_content_type()
        # Right now, just returns the first text part, which works fine for the current email format
        if type == "text/plain":
            text = part.get_payload(decode=True)
            print("\nFound plain text:")
            print(text)
            return text

home = os.getenv("HOME")
config_path = home +'/.mail_to_ynab'

config = get_config(config_path)
print(f"Config: {config}")

inbox = get_pop_client(config)
print("Connected, I think")
msgs = list_inbox(inbox)

parser = DiscoveryZaParser()
for msg in msgs:
    text = extract_text(msg)
    if parser.looks_like_notification(text):
        print("Looks like a notification")
        parser.get_transaction(text)
    else:
        print("Not what we are looking for")
