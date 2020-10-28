#!/usr/bin/python3.8

# A collection of utilities related to the program, but that don't need to be
# included in its source code directly.

from colorama import Fore, Back, Style
import commands


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
    text += "<table>\n<tr><th>Command</th><th>Description</th></tr>\n"

    for _, aliases in commands.primary_aliases_per_category.items():
        for alias in aliases:

            esc_alias = html_escape(alias)
            esc_description = html_escape(commands.alias_command_map[alias]['description'])

            text += f"<tr><td>{esc_alias}</td><td>{esc_description}</td></tr>\n"
    text += "</table>"
    return text

print(generate_html_command_table())
