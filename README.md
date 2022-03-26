# MailToYnab
Parses transaction notifications out of email and sends them to YNAB


## Usage and setup cheat sheet

YNAB API docs are available at https://api.youneedabudget.com/

### Installs

I needed to install these to get it to run locally on OSX:

```
pip install imapclient
pip install certifi
pip install beautifulsoup4
```

### Running

On my machine, it runs with:
`PYTHONPATH=./dependencies/ynab-v1/ python3 ./src/mail_to_ynab.py`

Tests can be run from the `src` folder using:
`PYTHONPATH=./dependencies/ynab-v1/ python3 -m unittest discover -v ../tst`

