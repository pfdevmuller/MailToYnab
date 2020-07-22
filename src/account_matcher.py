class ConstantAccountMatcher(object):

    def __init__(self, constant):
        self.constant = constant

    def matches(self, text):
        return self.constant


class CardSuffixAccountMatcher(object):

    def __init__(self, suffix):
        self.suffix = suffix

    def matches(self, text):
        return self.suffix == text
