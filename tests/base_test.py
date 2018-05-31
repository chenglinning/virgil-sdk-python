# Copyright (C) 2016-2018 Virgil Security Inc.
#
# Lead Maintainer: Virgil Security Inc. <support@virgilsecurity.com>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     (1) Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#     (2) Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#
#     (3) Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ''AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import json
import os
import unittest
from tests import config

from virgil_crypto import VirgilCrypto


class BaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        self.__compatibility_data_path = None
        self.__compatibility_data = None
        self.__app_private_key = None
        self.__crypto = None

    @property
    def _crypto(self):
        if self.__crypto:
            return self.__crypto
        self.__crypto = VirgilCrypto()
        return self.__crypto

    @property
    def _app_private_key(self):
        if self.__app_private_key:
            return self.__app_private_key
        with open(config.VIRGIL_APP_KEY_PATH, "rb") as key_file:
            raw_private_key = bytearray(key_file.read())

        self.__app_private_key = self._crypto.import_private_key(
            key_data=raw_private_key,
            password=config.VIRGIL_APP_KEY_PASSWORD
        )
        return self.__app_private_key

    @property
    def _compatibility_data(self):
        if self.__compatibility_data:
            return self.__compatibility_data
        with open(self._compatibility_data_path, "r") as data_file:
            raw_data = data_file.read()

        json_data = json.loads(raw_data)
        return json_data

    @property
    def _compatibility_data_path(self):
        if self.__compatibility_data_path:
            return self.__compatibility_data_path
        this_file_path = os.path.abspath(__file__)
        cwd = os.path.dirname(this_file_path)
        data_file_path = os.path.join(
            cwd,
            "data",
            "data.json"
        )
        self.__compatibility_data_path = data_file_path
        return data_file_path
