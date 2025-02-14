from sqlalchemy import *
from syzitus.__main__ import Base, cache, app

reasons = {
    1: "URL shorteners are not allowed.",
    3: "Piracy is not allowed.",
    4: "Sites hosting digitally malicious content are not allowed.",
    5: "Spam",
    6: "Doxxing is not allowed.",
    7: "Sexualizing minors is strictly prohibited.",
    8: f'User safety - This site is a {app.config["SITE_NAME"]} clone which is still displaying "{app.config["SITE_NAME"]}" as its site name.',
    9: f'You may not use {app.config["SITE_NAME"]} to engage in or plan unlawful activity.'
}


class Domain(Base):

    __tablename__ = "domains"
    id = Column(Integer, primary_key=True)
    domain = Column(String, index=True)
    is_banned=Column(Boolean, default=False, nullable=False)
    reason = Column(Integer, default=0)
    show_thumbnail = Column(Boolean, default=False)
    embed_function = Column(String(64), default=None)
    embed_template = Column(String(32), default=None)

    @property
    def reason_text(self):
        return reasons.get(self.reason)

    @property
    def permalink(self):
        return f"/admin/domain/{self.domain}"
    


class BadLink(Base):

    __tablename__ = "badlinks"
    id = Column(Integer, primary_key=True)
    reason = Column(Integer)
    link = Column(String(512))
    autoban = Column(Boolean, default=False)

    @property
    def reason_text(self):
        return reasons.get(self.reason)
