import re
import time
from core.config import PHONE_REGEX

def test_phone_regex_redos():
    text = "+1 " + "123 " * 1000 + "!"
    start = time.time()
    re.findall(PHONE_REGEX, text)
    duration = time.time() - start
    assert duration < 0.1
