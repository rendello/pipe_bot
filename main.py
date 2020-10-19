#!/usr/bin/python3.8

from text_transform import process_text

if __name__ == "__main__":
    print(process_text("Hello, {world! | zalgo | mock}, it's me {yeetus|redact}| vapor"))
    print(process_text("{hi | zalgo}hhhh hh | zalgo"))
    print(process_text("in {Soviet Russia|old}, car drives {you| zalgo | vaporwave} | clap ☭ | mock"))
    print(process_text("{Hello|zalgo}"))
    print(process_text("{Hello} jello|zalgo"))
    print(process_text("{jello|zalgo} h|mock"))
    print(process_text("{jello} h|mock|zalgo"))
    print(process_text(""))
    print(process_text("{}"))
    print(process_text("}{"))
