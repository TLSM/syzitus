from sqlalchemy import *
from flask import render_template
import mistletoe

from syzitus.helpers.base36 import *
from syzitus.helpers.security import *
from syzitus.helpers.lazy import lazy

from syzitus.__main__ import Base, cache


class Title():

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def check_eligibility(self, user):

        #legacy compatability function

        return self.evaluate(user)

    @property
    def rendered(self):
        return render_template('title.html', t=self)

    @property
    def json(self):

        return {'id': self.id,
                'text': self.text,
                'color': f'#{self.color}',
                'kind': self.kind
                }

    def evaluate(self, user):

        return bool(self.expr(user))


TITLE_DATA={
    1: {'color': 'aa8855',
        'description': 'Create your first Guild',
        'expr': "db.query(Board).filter_by(creator_id=user.id).count()",
        'kind': 1,
        'text': ', Guildmaker'},
    2: {'color': '603abb',
        'description': f'Had a good idea for {app.config["SITE_NAME"]}',
        'expr': "user.has_badge(4)",
        'kind': 1,
        'text': ', the Innovative'},
    5: {'color': '666666',
        'description': 'Responsibly report a security issue to us',
        'expr': "user.has_badge(12)",
        'kind': 3,
        'text': ' the Spymaster'},
    6: {'color': '55aa55',
        'description': f"Joined {app.config['SITE_NAME']} from another user's referral",
        'expr': "user.referred_by",
        'kind': 4,
        'text': ', the Invited'},
    9: {'color': 'dd5555',
        'description': f"Inadvertently break {app.config['SITE_NAME']}",
        'expr': "user.has_badge(11)",
        'kind': 3,
        'text': f", Breaker of {app.config['SITE_NAME']}"},
    11: {'color': '5555dd',
        'description': f"Make a contribution to the {app.config['SITE_NAME']} codebase",
        'expr': "user.has_badge(3)",
        'kind': 3,
        'text': ' the Codesmith'},
    20: {'color': '5555dd',
        'description': f'Make a contribution to {app.config["SITE_NAME"]} text or art.',
        'expr': "user.has_badge(1)",
        'kind': 3,
        'text': ' the Artisan'},
    21: {'color': 'dd5555',
        'description': 'Get at least 100 Reputation from a single post.',
        'expr': "user.submissions.filter(Submission.score_top>=100).count()",
        'kind': 1,
        'text': ' the Hot'},
    23: {'color': '5555dd',
        'description': 'Help test features in development',
        'expr': "user.has_badge(5)",
        'kind': 3,
        'text': ' the Test Dummy'},
    24: {'color': 'aa8855',
        'description': 'A Guild you created grows past 10 members.',
        'expr': "db.query(Board).filter(Board.creator_id==user.id, Board.stored_subscriber_count>=10).count()",
        'kind': 1,
        'text': ', Guildbuilder'},
    25: {'color': 'aa8855',
        'description': 'A Guild you created grows past 100 members.',
        'expr': "db.query(Board).filter(Board.creator_id==user.id, Board.stored_subscriber_count>=100).count()",
        'kind': 1,
        'text': ', Guildsmith'},
    26: {'color': 'aa8855',
        'description': 'A Guild you created grows past 1,000 members.',
        'expr': "db.query(Board).filter(Board.creator_id==user.id, Board.stored_subscriber_count>=1000).count()",
        'kind': 1,
        'text': ', Guildmaster'},
    27: {'color': 'aa8855',
        'description': 'A Guild you created grows past 10,000 members.',
        'expr': "db.query(Board).filter(Board.creator_id==user.id, Board.stored_subscriber_count>=10000).count()",
        'kind': 1,
        'text': ', Arch Guildmaster'},
    28: {'color': 'aa8855',
        'description': 'A Guild you created grows past 100,000 members.',
        'expr': "db.query(Board).filter(Board.creator_id==user.id, Board.stored_subscriber_count>=100000).count()",
        'kind': 1,
        'text': ', Guildlord'},
    29: {'color': 'aa8855',
        'description': 'A Guild you created grows past 1,000,000 members.',
        'expr': "db.query(Board).filter(Board.creator_id==user.id, Board.stored_subscriber_count>=1000000).count()",
        'kind': 1,
        'text': ', Ultimate Guildlord'},
    30: {'color': 'bb00bb',
        'description': f'Refer 1000 friends to join {app.config["SITE_NAME"]}',
        'expr': "user.referral_count>=1000",
        'kind': 1,
        'text': ', Diamond Recruiter'},
    31: {'color': 'bb00bb',
        'description': f'Refer 1 friend to join {app.config["SITE_NAME"]}.',
        'expr': "user.referral_count>=1",
        'kind': 1,
        'text': ', Bronze Recruiter'},
    32: {'color': 'bb00bb',
        'description': f'Refer 10 friends to join {app.config["SITE_NAME"]}.',
        'expr': "user.referral_count>=10",
        'kind': 1,
        'text': ', Silver Recruiter'},
    33: {'color': 'bb00bb',
        'description': f'Refer 100 friends to join {app.config["SITE_NAME"]}.',
        'expr': "user.referral_count>=100",
        'kind': 1,
        'text': ', Gold Recruiter'},
    34: {'color': '5555ff',
        'description': f'Join {app.config["SITE_NAME"]} during open Alpha.',
        'expr': "user.has_badge(15)",
        'kind': 4,
        'text': ', the Very Early Adopter'},
    35: {'color': 'aaaa22',
        'description': f'Join {app.config["SITE_NAME"]} during open Beta.',
        'expr': "user.has_badge(15) or user.has_badge(16)",
        'kind': 4,
        'text': ', the Early Adopter'},
    36: {'color': '5555dd',
        'description': 'Have at least 1 subscriber',
        'expr': "user.follower_count>=1",
        'kind': 1,
        'text': ' the Friendly'},
    37: {'color': '5555dd',
        'description': 'Have at least 10 subscribers',
        'expr': "user.follower_count>=10",
        'kind': 1,
        'text': ' the Likeable'},
    38: {'color': '5555dd',
        'description': 'Have at least 100 subscribers',
        'expr': "user.follower_count>=100",
        'kind': 1,
        'text': ' the Popular'},
    39: {'color': '5555dd',
        'description': 'Have at least 1,000 subscribers',
        'expr': "user.follower_count>=1000",
        'kind': 1,
        'text': ' the Influential'},
    40: {'color': '5555dd',
        'description': 'Have at least 10,000 subscribers',
        'expr': "user.follower_count>=10000",
        'kind': 1,
        'text': ', the Famous'}
}

TITLES={x:Title(id=x, **TITLE_DATA[x]) for x in TITLE_DATA}