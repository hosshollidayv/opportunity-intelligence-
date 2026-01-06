class Opportunity:
    def __init__(self, title, description, value):
        self.title = title
        self.description = description
        self.value = value

    def to_markdown(self):
        return f"## {self.title}\n\n{self.description}\n\n**Value:** ${self.value}"
