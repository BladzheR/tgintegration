from tgintegration import BotIntegrationClient

def test_start(client: BotIntegrationClient):
    # Send /start and wait for 3 messages
    res = client.send_command_await("/start", num_expected=3)
    assert res.num_messages == 3
    assert res[0].sticker  # First message is a sticker


def test_help(client: BotIntegrationClient):
    # Send /help and wait for one message
    res = client.send_command_await("/help", num_expected=1)

    # Make some assertions about the response
    assert not res.empty, "Bot did not respond to /help command"
    assert 'reliable and unbiased bot catalog' in res.full_text.lower()
    keyboard = res.inline_keyboards[0]
    assert len(keyboard.rows[0]) == 3  # 3 buttons in first row
    assert len(keyboard.rows[1]) == 1  # 1 button in second row

    # Click the inline button that says "Contributing"
    contributing = res.inline_keyboards[0].press_button_await(pattern=r'.*Contributing')
    assert not contributing.empty, 'Pressing "Contributing" button had no effect.'
    assert "to contribute to the botlist" in contributing.full_text.lower()

    # Click the inline button that says "Help"
    help_ = res.inline_keyboards[0].press_button_await(pattern=r'.*Help')
    assert not contributing.empty, 'Pressing "Help" button had no effect.'
    assert "first steps" in help_.full_text.lower()

    # Click the inline button that says "Examples"
    examples = res.inline_keyboards[0].press_button_await(pattern=r'.*Examples')
    assert not examples.empty, 'Pressing "Examples" button had no effect.'
    assert "examples for contributing to the botlist:" in examples.full_text.lower()
