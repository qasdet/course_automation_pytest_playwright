def test_example(page):
    page.goto('https://example.com')
    assert page.locator('h1').inner_text() == 'Example Domain'
