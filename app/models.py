"""
When we create any table, we should create with
>> Create database mockXXX charset=UTF8
then >> mysql:// user:pass@localhost/db?charset=utf8, will take effect
"""

# import sys
#
# reload(sys)
# sys.setdefaultencoding('utf8')

from app import db
from sqlalchemy import func, text
from flask_sqlalchemy import SQLAlchemy


# db = SQLAlchemy()

class MockItem(db.Model):
    """
    Contain mockID, one mockID should correspond one MockJson or more
    status: 1 is valid
    """
    __talbename__ = 'mockItem'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    remark = db.Column(db.String(512))
    status = db.Column(db.Integer, default=1)
    groupID = db.Column(db.Integer)
    operator = db.Column(db.String(512), nullable=False)
    reserveParam1 = db.Column(db.String(512))
    reserveParam2 = db.Column(db.String(512))
    update_time = db.Column(db.TIMESTAMP(True), nullable=False,
                            server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    create_time = db.Column(db.TIMESTAMP(True),
                            server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class MockJson(db.Model):
    """
    Mock json data
        delay status: 0 is invalid, 1 is valid,
        status: 0 is invalid, 1 is valid
        mock_ID is the ID in MOCKITEM, NOT USING for now!!
    """
    __tablename__ = 'mockJson'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    mock_id = db.Column(db.Integer)
    url = db.Column(db.String(512), nullable=False)
    mock_json = db.Column(db.String(1024))
    status = db.Column(db.Integer, default=1)
    delay_time = db.Column(db.Integer, default=0)
    delay_status = db.Column(db.Integer, default=0)
    reserveParam1 = db.Column(db.String(512))
    reserveParam2 = db.Column(db.String(512))
    remark = db.Column(db.String(512))
    operator = db.Column(db.String(32))
    update_time = db.Column(db.TIMESTAMP(True), nullable=False,
                            server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    create_time = db.Column(db.TIMESTAMP(True),
                            server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class MockGroup(db.Model):
    """
    When we have too many testing env, we should insulate different mock interfaces to
    avoid chaos
    """
    __tablename__ = 'mock_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    operator = db.Column(db.String(32))
    op_time = db.Column(db.TIMESTAMP(True), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
