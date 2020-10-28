![Cover image](images/cover.png)

`pipe|bot` is a Discord chatbot that allows you to chain multiple text commands
together with pipes. It also supports arbritrary subgrouping.

## Usage
Basic usage 

## Examples
<!-- Generated. See `utils.py` -->
<table>
<tr><th>Command</th><th>Description</th><th>Example</th></tr>
<tr><td>caps</td><td>Uppercase</td><td>UPPERCASE</td></tr>
<tr><td>lowercase</td><td>Lowercase</td><td>lowercase</td></tr>
<tr><td>swapcase</td><td>Swaps case per letter</td><td>sWAPS CASE PER LETTER</td></tr>
<tr><td>base64</td><td>Base64 encoded</td><td>QmFzZTY0IGVuY29kZWQ=</td></tr>
<tr><td>binary</td><td>Binary representation</td><td>1000010 1101001 1101110 1100001 1110010 1111001 100000 1110010 1100101 1110000 1110010 1100101 1110011 1100101 1101110 1110100 1100001 1110100 1101001 1101111 1101110</td></tr>
<tr><td>from_base64</td><td>Text from base 64</td><td>N/A</td></tr>
<tr><td>from_hex</td><td>Text from hexidecimal</td><td>N/A</td></tr>
<tr><td>hex</td><td>Hexidecimal representation</td><td>48 65 78 69 64 65 63 69 6d 61 6c 20 72 65 70 72 65 73 65 6e 74 61 74 69 6f 6e</td></tr>
<tr><td>md5</td><td>MD5 hash</td><td>0205eacc79baf77a16ff08e24fbba67a</td></tr>
<tr><td>sha256</td><td>SHA256 hash</td><td>92dfe7a311aa63bf4e6171c23270b2181a011f735836cfa16a2355cc115f8a31</td></tr>
<tr><td>blockquote</td><td>Block quote</td><td>
&gt; Block quote
</td></tr>
<tr><td>bold</td><td>Bold</td><td>**Bold**</td></tr>
<tr><td>code</td><td>Inline code tag</td><td>`Inline code tag`</td></tr>
<tr><td>codeblock</td><td>Code block</td><td>```
Code block
```</td></tr>
<tr><td>italic</td><td>Italics</td><td>*Italics*</td></tr>
<tr><td>spoiler</td><td>Spoiler tag</td><td>||Spoiler tag||</td></tr>
<tr><td>underline</td><td>Underline</td><td>__Underline__</td></tr>
<tr><td>clap</td><td>Emojis between words (default 👏)</td><td>Emojis 👏 between 👏 words 👏 (default 👏 👏)</td></tr>
<tr><td>mock</td><td>Random upper/lowercase</td><td>RanDOm UppEr/LoWErCAsE</td></tr>
<tr><td>scramble</td><td>Scrambled characters</td><td>elmabSdrc taaechcsrr </td></tr>
<tr><td>uwu</td><td>Cursed UwU text</td><td>Cuwsed UwU text</td></tr>
<tr><td>zalgo</td><td>Spooky zalgo text</td><td>S̮͆p̹ͨo̩͚ȯ̓k̸ͬy̪̭ z̼̐ą͙l̐̽g̰ͭoͧ̓ t̀͠e͂ͫx͔̏t͘ͅ</td></tr>
<tr><td>blackletter</td><td>Old timey blackletter</td><td>𝔒𝔩𝔡 𝔱𝔦𝔪𝔢𝔶 𝔟𝔩𝔞𝔠𝔨𝔩𝔢𝔱𝔱𝔢𝔯</td></tr>
<tr><td>leet</td><td>Elite hacker text</td><td>31I73 H4CK3R 73X7</td></tr>
<tr><td>redact</td><td>Letters substituted for character (default █).</td><td>███████ ███████████ ███ █████████ (███████ █).</td></tr>
<tr><td>serif</td><td>Unicode serif font</td><td>𝐔𝐧𝐢𝐜𝐨𝐝𝐞 𝐬𝐞𝐫𝐢𝐟 𝐟𝐨𝐧𝐭</td></tr>
<tr><td>upsidedown</td><td>Unicode upside-down font</td><td>∩uᴉɔopǝ ndsᴉpǝ-poʍu ɟouʇ</td></tr>
<tr><td>vaporwave</td><td>CJK full width letters</td><td>ＣＪＫ ｆｕｌｌ ｗｉｄｔｈ ｌｅｔｔｅｒｓ</td></tr>
</table>

## Installation
The standard bot can be added to your server with the following link:

I encourage any server owners to modify and self host the bot themselves, as
the bot was built to be easily extensible.

## Commands
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


