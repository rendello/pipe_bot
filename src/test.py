#!/usr/bin/python3.8

from hypothesis import given, settings, Verbosity, assume
from hypothesis.strategies import text

from text_transform import process_text

@given(text())
@settings(max_examples=10_000_000, deadline=100, verbosity=Verbosity.verbose)
def test_process_text(s):
    assume(s not in ["|\r","| "])
    assert isinstance(process_text(s), str)

test_process_text()
