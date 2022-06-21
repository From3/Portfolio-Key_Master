#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

icons = {
    "Generator": chr(57526),
    "Manager": chr(57736),
    "Helper": chr(57627),
    "About": chr(57537),
    "Settings": chr(57621)
}

helper_text = {
    f"{icons['Generator']} Generator": [
        "Generator allows to generate new\n"
        "passwords based on selected length and\n"
        "string symbols. Also, it allows to check\n"
        "if specified passwords was ever breached\n"
        "based on \"Have I Been Pwned\" API."
    ],
    f"{icons['Manager']} Manager": [
        "Manager allows to store usernames and\n"
        "passwords under unique profile names\n"
        "to be copied and used elsewhere whenever\n"
        "needed or removed."
    ],
    f"{icons['Settings']} Settings": [
        "Settings allows to change master\n"
        "password, erase all stored profiles and\n"
        "change if application should be kept on\n"
        "top of other windows."
    ]
}
