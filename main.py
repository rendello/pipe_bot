#!/usr/bin/python3.8

from parse import toAST

AST = toAST("Hello {world | zalgo} | hash md5, sha256 | mock")
print(AST)
