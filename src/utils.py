#!/usr/bin/python3.8

# A collection of utilities related to the program, but that don't need to be
# included in its source code directly.

import asyncio

from colorama import Fore, Back, Style
import commands
import text_transform


def t_print(tokens, show_key=False) -> None:
    """ Prints arbritrary tokens with unique colors. """

    foreground = (Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.CYAN,
        Fore.MAGENTA, Fore.WHITE)
    style = Style.BRIGHT, Style.NORMAL, Style.DIM

    color_map = {}

    for i, (token_type, _) in enumerate(TOKENS):
        # (Jumps through foreground colors, then loops back and uses second
        # style, et cetera. Enable show_key for visualization.)
        color_map[token_type] = (
            foreground[i % len(foreground)]
            + style[int(i / len(foreground)) % len(style)]
        )
        if show_key:
            print(color_map[token_type] + token_type + Style.RESET_ALL)

    for token in tokens:
        if token.type_ == "WHITESPACE":
            color = Back.GREEN
        else:
            color = color_map[token.type_]
        print(color + token.value + Style.RESET_ALL, end="")
    print()


def generate_html_command_table():
    """ Generate the command table for the README. """

    def html_escape(text):
        html_escapes = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;",
        }
        for char, esc_char in html_escapes.items():
            text = text.replace(char, esc_char)
        return text

    text = "<!-- Generated. See `utils.py` -->\n"
    text += "<table>\n<tr><th>Command</th><th>Description</th><th>Example</th></tr>\n"

    for _, aliases in commands.primary_aliases_per_category.items():
        for alias in aliases:
            description = commands.alias_command_map[alias]['description']

            esc_alias = html_escape(alias)
            esc_description = html_escape(description)

            try:
                esc_example = html_escape(asyncio.run(text_transform.process_text(f"{description}|{alias}")))
            except:
                esc_example = "N/A"

            text += f"<tr><td>{esc_alias}</td><td>{esc_description}</td><td>{esc_example}</td></tr>\n"
    text += "</table>"
    return text

print(generate_html_command_table())
