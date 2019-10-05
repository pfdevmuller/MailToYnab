import os

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


home = os.getenv("HOME")
config_path = home +'/.mail_to_ynab'

print("Hello world!")

print(get_config(config_path))

