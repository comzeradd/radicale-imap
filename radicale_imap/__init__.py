# radicale-imap IMAP authentication plugin for Radicale.
# Copyright (C) 2017 Unrud <unrud@openaliasbox.org>
# Copyright (C) 2018 Nikos Roussos <nikos@roussos.cc>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import imaplib
import ssl

from radicale.auth import BaseAuth
from radicale.config import _convert_to_bool
from radicale.log import logger


class Auth(BaseAuth):
    """Authenticate user with IMAP.

    Configuration:

    [auth]
    type = radicale_imap
    imap_host = example.com:143
    imap_secure = True
    """

    def login(self, user, password):
        # Parse configuration options
        try:
            host = self.configuration.get('auth', 'imap_host')
        except KeyError:
            host = ''

        try:
            # Radicale only does bool conversion based on config schema
            # and there seems to be no way for plugins to add items to
            # the schema. To ensure consistent boolean parsing, this
            # uses an internal function.
            secure = _convert_to_bool(self.configuration.get('auth', 'imap_secure'))
        except KeyError:
            secure = True

        try:
            if ':' in host:
                address, port = host.rsplit(':', maxsplit=1)
            else:
                address, port = host, 143
            address, port = address.strip('[] '), int(port)
        except ValueError as e:
            raise RuntimeError(
                'Failed to parse address %r: %s' % (host, e)) from e

        # Attempt connection with IMAP server
        try:
            connection = imaplib.IMAP4(host=address, port=port)
        except (OSError, imaplib.IMAP4.error) as e:
            raise RuntimeError('Failed to communicate with IMAP server %r: '
                               '%s' % (host, e)) from e

        # Upgrade connection to StartTLS
        context = ssl.create_default_context()
        if not secure:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        try:
            connection.starttls(context)
        except (imaplib.IMAP4.error, ssl.CertificateError) as e:
            raise RuntimeError('Failed to establish secure connection with %r: %s'
                               % (host, e)) from e

        # Attempt to authenticate user
        try:
            connection.login(user, password)
        except imaplib.IMAP4.error as e:
            logger.debug(
                'IMAP authentication failed: %s', e, exc_info=True)
            return ""

        connection.logout()
        return user
