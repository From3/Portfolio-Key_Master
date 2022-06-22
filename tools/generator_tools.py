#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import requests
from random import choice
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
import hashlib


def hash_secret(secret: str) -> str:
    return hashlib.sha1(str(secret).encode("utf-8")).hexdigest().upper()


def request_list(request_input: str) -> requests.Response:
    url = "https://api.pwnedpasswords.com/range/" + request_input
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"[Error {res.status_code}]\nCheck required")

    return res


def main_check(secret: str) -> str:
    if not secret:
        return "0"

    hashed_secret = hash_secret(secret)
    api_res = request_list(hashed_secret[:5]).text
    all_hashes = (line.split(":") for line in api_res.splitlines())

    for given_hash, times in all_hashes:
        if given_hash == hashed_secret[5:]:
            return times

    return "0"


def generate(strings, length: int) -> str:
    result = []
    values = ascii_lowercase * strings[0] + ascii_uppercase * strings[1] + digits * strings[2] + punctuation * strings[3]
    if not any(strings):
        return ""

    while len(result) < length:
        result.append(choice(values))

    return "".join(result)
