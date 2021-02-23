# SPDX-License-Identifier: BSD-2-Clause

import random

import pytest
from hypothesis import given, settings
from hypothesis.strategies import text
import asyncio

from text_transform import process_text
from main import macro_message_pattern, macro_last_pattern


### REGULAR TESTS #########################################################
def test_macro_last_pattern():
    empty_match_examples = [
        "Hello world",
        "Hello world$LAST",
        r"\$LAST",
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
        r"\$MESSAGE",
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


@pytest.mark.asyncio 
async def test_process_text():
    """ Fuzzes process_text. The goal is to stress-test the parsing engine. """

    tokens = ["mock ", " zalgo", "caps ", " clap", "|", ",", "\"", "\n", "{", "}", " ", "\t", "\\"]

    for i in range(50_000):
        text = ""
        for j in range(random.randint(0, (i * 5) % 80)):
            text += random.choice(tokens)
            if random.randint(0,160) == 5:
                for k in range(random.randint(0, 30)):
                    text += random.choice(" abcdefghijklmnopqrstuvwxyz")


        # Try all combinations without curly braces as well, since "unbalanced
        # curly brace" are very common and will prevent other errors from showing up.
        for t in (text, text.replace("{", "").replace("}", "")):
            #print("INPUT: ", t)
            processed = await process_text(t)
            #print("OUTPUT: ", processed)
            #print("---------------------")
            assert isinstance(processed, str)


### HYPOTHESIS TESTS ######################################################
@given(text())
@settings(max_examples=50_000, deadline=1000)
def test_process_text_hyp(s):
   assert isinstance(asyncio.run(process_text(s)), str)
