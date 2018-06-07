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
import datetime
from collections import OrderedDict


class JwtBodyContent(object):
    __IDENTITY_PREFIX = "identity-"
    __SUBJECT_PREFIX = "virgil-"

    def __init__(
            self,
            app_id,
            identity,
            issued_at,
            expires_at,
            data
    ):
        self._app_id = app_id
        self._identity = identity
        self._issued_at = issued_at
        self._expires_at = expires_at
        self._additional_data = data
        self._issuer = str(self.__SUBJECT_PREFIX + self._app_id)
        self.subject = str(self.__IDENTITY_PREFIX + self._identity)

    def __eq__(self, other):
        return all([
            self._issued_at == other._issued_at,
            self._expires_at == other._expires_at,
            self._additional_data == other._additional_data,
            self.issuer == other.issuer,
            self.subject == other.subject
        ])

    @classmethod
    def from_json(cls, json_loaded_dict):
        body_content = cls.__new__(cls)
        body_content._issued_at = datetime.datetime.fromtimestamp(json_loaded_dict["iat"])
        body_content._expires_at = datetime.datetime.fromtimestamp(json_loaded_dict["exp"])
        body_content._additional_data = json_loaded_dict["ada"]
        body_content._issuer = json_loaded_dict["iss"]
        body_content.subject = json_loaded_dict["sub"]
        return body_content

    @property
    def json(self):
        return OrderedDict({
            "iat": self._issued_at.timestamp(),
            "exp": self._expires_at.timestamp(),
            "ada": self._additional_data,
            "iss": self.issuer,
            "sub": self.subject
        })

    @property
    def subject_prefix(self):
        return self.__SUBJECT_PREFIX

    @property
    def identity_prefix(self):
        return self.__IDENTITY_PREFIX

    @property
    def issuer(self):
        return self._issuer

    @property
    def expires_at(self):
        return self._expires_at


