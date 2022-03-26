from imapclient import IMAPClient
from bs4 import BeautifulSoup
import email


# Goes over the inbox. Tracks position and can close the connection.
class InboxScan:

    # imapclient: should already be connected
    def __init__(self, imapclient):
        self.inbox = imapclient
        select_info = self.inbox.select_folder('INBOX')
        self.msg_count = select_info[b'EXISTS']
        print(f"Found {self.msg_count} messages on server")
        self.current = None

    def messages(self):
        messages = self.inbox.search()
        print(f"messages: {messages}")
        for uid, message_data in self.inbox.fetch(messages, 'RFC822').items():
            # print(f"Message Data: {message_data}")
            raw_email = message_data[b'RFC822']
            # print(f"Raw Email: {raw_email}")
            parsed_email = email.message_from_bytes(raw_email)
            # print(f"Parsed: {parsed_email}")
            self.current = uid
            yield parsed_email

    # Marks the current message for deletion
    def delete_current(self):
        self.inbox.delete_messages([self.current])

    def close(self):
        self.inbox.expunge()
        self.inbox.logout()


class MailChecker:

    def __init__(self, server, port, username, password):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def get_client(self):
        print(f"Server {self.server}, Port {self.port}")
        server = IMAPClient(self.server, port=self.port, ssl=False)
        server.login(self.username, self.password)
        return server

    def start_inbox_scan(self):
        inbox = self.get_client()
        print("Connected, I think")
        return InboxScan(inbox)

    def extract_text(self, parsed_email):
        """
        Returns a string representation of the email body
        """
        # Try to find plain text first:
        for part in parsed_email.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                text = part.get_payload(decode=True)
                result = str(text, 'utf-8')
                print("\nFound plain text:")
                print(result)
                return result
        # Otherwise, look for text/html
        for part in parsed_email.walk():
            content_type = part.get_content_type()
            if content_type == "text/html":
                text = str(part.get_payload(decode=True), 'utf-8')
                soup = BeautifulSoup(text, features="html.parser")
                result = soup.body.text
                print("\nFound html text:")
                print(result)
                return result
        raise Exception("Could not find an understandable part in parsed email.")
