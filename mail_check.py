import os
import poplib
import email

def get_config(path):
    config = {}
    f= open(path,'r')
    lines = f.readlines()
    for l in lines:
        print(l.strip())
        tokens = l.split(':')
        if len(tokens) != 2:
            raise "Expected config lines to contain exactly two fields"
        key = tokens[0].strip()
        value = tokens[1].strip()
        config[key] = value
    return config

def list_inbox(config):
    server = config['server']
    port = config['port']
    username = config['username']
    password = config['password']
    print(f"Server {server}, Port {port}")
    popclient = poplib.POP3(server, port)
    popclient.user(username)
    popclient.pass_(password)
    print("Connected, I think")
    print(popclient.stat())

    msg = popclient.retr(2)
    raw_email = b"\n".join(msg[1])
    parsed_email = email.message_from_bytes(raw_email)
    print(parsed_email)

    # get multiple parts from message body.
    parts = parsed_email.get_payload()
    # loop for each part
    for n, part in enumerate(parts):
        # print multiple part information by invoke print_info function recursively.
        content_type = part.get_content_type() 
        print(f"Part {n}: type: {content_type}")
        print(part.get_payload(decode=True))

home = os.getenv("HOME")
config_path = home +'/.mail_to_ynab'

print("Hello world!")

config = get_config(config_path)
print("Config:")
print(config)

list_inbox(config)
