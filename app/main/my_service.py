from ..models import MockJson


class MockItemServices(object):
    @staticmethod
    def get_json_list():
        """get all avliable json items"""
        all_list = MockJson.query.all()
        return all_list

    @staticmethod
    def get_json(id):
        """get single item"""
        item = MockJson.query.filter_by(id=id).first()
        return item

    @staticmethod
    def isExisted(url):
        """check if a url of mock item has been saved in DB,
            if existed return id of mockJson, not existed return 0"""
        temp = MockJson.query.filter_by(url=url).first()
        if temp:
            return temp.id
        else:
            return 0

    @staticmethod
    def add_json(mock_item):
        item = MockItemServices()
