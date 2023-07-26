class ResponseManager:
    def __init__(self):
        self.filename = ""

    def getBlockedUserPage(self):
        with open("blockedIP.html", "r") as f:
            str1 = f.read()
        return str1

    def getBlockedKeywordPage(self):
        with open("blockedkeyword.html", "r") as f:
            str1 = f.read()
        return str1

    def getBlockedWebsitePage(self):
        with open("blockedwebsite.html", "r") as f:
            str1 = f.read()
        return str1
