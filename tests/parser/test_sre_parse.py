import pytest

import gixy.core.sre_parse.sre_parse as sre_parse


def test_pcre_verb_removal():
    """Test that PCRE verbs like (*ANYCRLF) are properly stripped by the parser."""
    config = "(*ANYCRLF)/(?P<target>.+?)$"

    # (*ANYCRLF) should be stripped by the parser
    expected = [
        ('literal', 47), 
        ('subpattern', (1, [('min_repeat', (1, 4294967295, [('any', None)]))])), 
        ('at', 'at_end')
    ]

    actual = sre_parse.parse(config)
    assert repr(actual) == repr(expected)


def test_incomplete_pcre_verb():
    """Test that incomplete PCRE verbs raise an appropriate error."""
    config = "(*ANYCRLF"

    with pytest.raises(sre_parse.error) as exc_info:
        sre_parse.parse(config)
    
    assert "unterminated PCRE extension" in str(exc_info.value)


def test_multiple_pcre_verbs():
    """Test handling of multiple PCRE verbs."""
    config = "(*ANYCRLF)(*UCP)test"
    
    # Both PCRE verbs should be stripped
    result = sre_parse.parse(config)
    # Should just have the literal "test"
    assert len(result) == 4  # 't', 'e', 's', 't'
    assert all(token[0] == 'literal' for token in result)


def test_pcre_verb_with_regex():
    """Test PCRE verb followed by actual regex pattern."""
    config = r"(*ANYCRLF)^https?://example\.com"
    
    # Should parse the regex after stripping PCRE verb
    result = sre_parse.parse(config)
    assert result is not None
    # First token should be at_beginning (^)
    assert result[0][0] == 'at'


def test_inline_flags_single():
    """Test inline flag with scoped group: (?i:pattern)."""
    config = "(?i:hello)"
    result = sre_parse.parse(config)
    assert len(result) == 1
    assert result[0][0] == "subpattern"
    assert result[0][1][0] is None  # Non-capturing group


def test_inline_flags_with_nested_group():
    """Test inline flag with nested capturing group: (?i:(cs|cz))."""
    config = "^(?i:(cs|cz))"
    result = sre_parse.parse(config)
    assert result is not None
    assert result[0][0] == "at"
    assert result[1][0] == "subpattern"
    assert result[1][1][0] is None  # Non-capturing


def test_inline_flags_multiple():
    """Test multiple inline flags: (?im:pattern)."""
    config = "(?im:hello)"
    result = sre_parse.parse(config)
    assert len(result) == 1
    assert result[0][0] == "subpattern"


def test_global_flags_still_work():
    """Ensure global flag syntax (?i) still works."""
    config = "(?i)hello"
    result = sre_parse.parse(config)
    assert len(result) == 5
    assert all(token[0] == "literal" for token in result)
