# -*- coding: utf-8 -*-

__author__ = 'ninad'


from flask_mail import Mail, Message


class Mailer(object):
    def __init__(self, app):
        self.mail = Mail()
        self.mail.init_app(app)

    def send_simple_mail(self, details):
        msg = Message(subject=details.Subject,
                      sender=details.Sender,
                      recipients=details.To,
                      html=details.Message)

        self._send(msg)

    def _send(self, msg):
        self.mail.send(msg)
