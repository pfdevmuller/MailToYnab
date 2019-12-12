import poplib
import email

# Goes over the inbox. Tracks position and can close the connection.
class InboxScan:

    # popclient: should already be connected
    def __init__(self, popclient):
        self.inbox = popclient
        self.msg_count, self.inbox_size = self.inbox.stat()
        print(f"Found {self.msg_count} messages on pop server")
        self.index = 1

    def messages(self):
        while self.index <= self.msg_count:
            print(f"\n\nFetching message {self.index}")
            msg = self.inbox.retr(self.index)
            raw_email = b"\n".join(msg[1])
            parsed_email = email.message_from_bytes(raw_email)
            yield parsed_email
            self.index += 1

    # Marks the current message for deletion
    def delete_current(self):
        print(f"Marking message {self.index} for deletion.")
        self.inbox.dele(self.index)

    def close(self):
        self.inbox.quit()

class MailChecker:

    def __init__(self, server, port, username, password):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def get_pop_client(self, server, port, username, password):
        print(f"Server {server}, Port {port}")
        popclient = poplib.POP3(server, port)
        popclient.user(username)
        popclient.pass_(password)
        return popclient

    def start_inbox_scan(self):
        inbox = self.get_pop_client(self.server, self.port, self.username, self.password)
        print("Connected, I think")
        return InboxScan(inbox)

    def extract_text(self, parsed_email):
        for part in parsed_email.walk():
            type = part.get_content_type()
            # Right now, just returns the first text part, which works fine for the current email format
            if type == "text/plain":
                text = part.get_payload(decode=True)
                print("\nFound plain text:")
                print(text)
                return text

