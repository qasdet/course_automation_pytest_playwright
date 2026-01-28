from pages.example_page import ExamplePage

def test_flow(page):
    p = ExamplePage(page)
    p.goto()
    assert p.get_header() == 'Example Domain'
