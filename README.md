![Cover image](images/cover.png)

`pipe|bot` is a Discord chatbot that allows you to chain multiple text commands
together with pipes. It also supports arbritrary subgrouping.

## Usage
Basic usage 

## Examples

## Installation
The standard bot can be added to your server with the following link:

I encourage any server owners to modify and self host the bot themselves, as
the bot was built to be easily extensible.

## Commands
<!-- Generated. See `utils.py` -->
<table>
<tr><th>Command</th><th>Description</th></tr>
<tr><td>caps</td><td>Uppercase</td></tr>
<tr><td>lowercase</td><td>Lowercase</td></tr>
<tr><td>swapcase</td><td>Swaps case per letter</td></tr>
<tr><td>base64</td><td>Base64 encoded</td></tr>
<tr><td>binary</td><td>Binary representation</td></tr>
<tr><td>from_base64</td><td>Text from base 64</td></tr>
<tr><td>from_hex</td><td>Text from hexidecimal</td></tr>
<tr><td>hex</td><td>Hexidecimal representation</td></tr>
<tr><td>md5</td><td>MD5 hash</td></tr>
<tr><td>sha256</td><td>SHA256 hash</td></tr>
<tr><td>blockquote</td><td>Block quote</td></tr>
<tr><td>bold</td><td>Bold</td></tr>
<tr><td>code</td><td>Inline code tag</td></tr>
<tr><td>codeblock</td><td>Code block</td></tr>
<tr><td>italic</td><td>Italics</td></tr>
<tr><td>spoiler</td><td>Spoiler tag</td></tr>
<tr><td>underline</td><td>Underline</td></tr>
<tr><td>clap</td><td>Emojis between words (default 👏)</td></tr>
<tr><td>mock</td><td>Random upper/lowercase</td></tr>
<tr><td>scramble</td><td>Scrambled characters</td></tr>
<tr><td>uwu</td><td>Cursed UwU text</td></tr>
<tr><td>zalgo</td><td>Spooky zalgo text</td></tr>
<tr><td>blackletter</td><td>Old timey blackletter</td></tr>
<tr><td>leet</td><td>Elite hacker text</td></tr>
<tr><td>redact</td><td>Letters substituted for character (default █).</td></tr>
<tr><td>serif</td><td>Unicode serif font</td></tr>
<tr><td>upsidedown</td><td>Unicode upside-down font</td></tr>
<tr><td>vaporwave</td><td>CJK full width letters</td></tr>
</table>

## Modification and development
This project is licensed under the Simplified BSD license. If modified and
publicly re-released, I ask that you change the name to avoid confusion.

A simple overview of the project files is as follows:

<table style="width:100%">

<tr>
<th>Source file</th>
<th>Function</th>
</tr>

<tr>
<td><code>main.py</code></td>
<td>The Discord bot itself. This is the file run to start the bot.</td>
</tr>

<tr>
<td><code>text_transform.py</code></td>
<td>The hand-written lexer, parser, and generator. The grand majority of the bot's
functionality is implemented here.</td>
</tr>

<tr>
<td><code>commands.py</code></td>
<td>Data related to the bots commands, including aliases, descriptions, examples,
and the names of callbacks.

The end of the file has useful data structures and regex patterns related to
the commands.</td>
</tr>

<tr>
<td><code>command_funcs.py</code></td>
<td>The callback functions for each command.</td>
</tr>

<tr>
<td><code>test.py</code></td>
<td>Hypothesis and Pytest tests, mostly focusing on the lexing / parsing /
generation stages.</td>
<tr>
</table> 


