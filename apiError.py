class ApiError(Exception):
    title = ""
    desc = ""

    def __init__(self,title,desc):
        self.title=title
        self.desc=desc

