import poplib
import email

class MailChecker:

    def __init__(self, server, port, username, password):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.inbox = None

    def get_inbox(self):
        if (self.inbox is None):
            self.inbox = self.get_pop_client(self.server, self.port, self.username, self.password)
            print("Connected, I think")
        return self.inbox

    def get_pop_client(self, server, port, username, password):
        print(f"Server {server}, Port {port}")
        popclient = poplib.POP3(server, port)
        popclient.user(username)
        popclient.pass_(password)
        return popclient

    # Returns a list of parsed emails
    def list_inbox(self):
        msg_count, inbox_size = self.get_inbox().stat()
        print(f"Found {msg_count} messages")
        if msg_count < 1:
            return []
        msgs = []
        for i in range(1,msg_count+1):
            print(f"Fetching message {i}")
            msg = self.get_inbox().retr(i)
            raw_email = b"\n".join(msg[1])
            parsed_email = email.message_from_bytes(raw_email)
            msgs.append(parsed_email)
        return msgs

    def extract_text(self, parsed_email):
        for part in parsed_email.walk():
            type = part.get_content_type()
            # Right now, just returns the first text part, which works fine for the current email format
            if type == "text/plain":
                text = part.get_payload(decode=True)
                print("\nFound plain text:")
                print(text)
                return text

