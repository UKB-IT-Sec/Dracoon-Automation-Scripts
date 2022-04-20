import pytest
from helper.normalizer import normalize_username


@pytest.mark.parametrize('input_data, expected', [
    ('test.user@example.com', 'test.user'),
    ('AuthService/test.user@example.net', 'test.user'),
    ('test', 'test')
])
def test_normalize_username(input_data, expected):
    assert normalize_username(input_data) == expected
