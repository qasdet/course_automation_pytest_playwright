class ExamplePage:
    def __init__(self, page):
        self.page = page
        self.header = page.locator('h1')

    def goto(self):
        self.page.goto('https://example.com')

    def get_header(self):
        return self.header.inner_text()
