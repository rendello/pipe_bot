#!/usr/bin/python3.8

import pytest
from hypothesis import given, settings, Verbosity, assume
from hypothesis.strategies import text

from text_transform import process_text
from main import macro_message_pattern, macro_last_pattern

## To do: Make work with async
# @given(text())
# @settings(max_examples=10_000_000, deadline=100, verbosity=Verbosity.verbose)
# def test_process_text(s):
#    assume(s not in ["|\r","| "])
#    assert isinstance(process_text(s), str)
# test_process_text()


def test_macro_last_pattern():
    empty_match_examples = [
        "Hello world",
        "Hello world$LAST",
        "\$LAST",
        "$last",
        "$MESSAGE 000000000000000000",
    ]
    id_match_examples = [
        "$LAST 000000000000000000",
        "$LAST <@!000000000000000000>",
        "Some text $LAST  000000000000000000; text",
        "Hi, I saw you said {$LAST 000000000000000000|bold|caps}, is that correct?",
    ]

    for ex in empty_match_examples:
        assert macro_last_pattern.findall(ex) == []

    for ex in id_match_examples:
        assert all(
            substr in macro_last_pattern.findall(ex)[0][0]
            for substr in ["$LAST", "0" * 18]
        )
        assert macro_last_pattern.findall(ex)[0][1] == "0" * 18


def test_macro_message_pattern():
    empty_match_examples = [
        "Hello world",
        "Hello world$MESSAGE",
        "\$MESSAGE",
        "$message",
        "$MESSAGE",
        "$LAST 000000000000000000",
        "$MESSAGE https://discord.com/channels/111111111111111111/000000000000000000",
        "$MESSAGE https://discord.com/channels/000000000000000000",
    ]
    id_match_examples = [
        "$MESSAGE 000000000000000000",
        "$MESSAGE https://discord.com/channels/222222222222222222/111111111111111111/000000000000000000",
        "Some text $MESSAGE  000000000000000000; text",
    ]

    for ex in empty_match_examples:
        assert macro_message_pattern.findall(ex) == []

    for ex in id_match_examples:
        assert all(
            substr in macro_message_pattern.findall(ex)[0][0]
            for substr in ["$MESSAGE", "0" * 18]
        )
        assert macro_message_pattern.findall(ex)[0][1] == "0" * 18

test_macro_last_pattern()
test_macro_message_pattern()
