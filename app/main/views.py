from flask import render_template, request
from .. import db
from . import main
from flask import make_response, jsonify, Response
# from my_service import MockItemServices
from app.main.my_service import MockItemServices
import requests
from contextlib import closing
from config import objectServer
import re
from flask_admin.contrib.sqla import ModelView

@main.before_app_request
def before_all_request():
    objectServerIP = objectServer.object_server_IP  # This is server machine's IP

    url = request.url

    # using re to get path of the request, without IP
    pattern_http = r"http://[^/]+/"
    re_pattern = re.compile(pattern_http)
    origin_path = re_pattern.split(url)[1]
    print('-> origin_path: {}'.format(origin_path))

    method = request.method
    data = request.data or request.form or None
    headers = dict()
    print('-> url: {}'.format(url))
    print('-> method: {}'.format(method))
    print('-> data: {}'.format(data))
    for name, value in request.headers:
        if not value or name == 'Cache-Control':
            continue
        headers[name] = value
        print('-> name is : {} - value is : {}'.format(name, value))
    if origin_path.startswith('sdmockserver3/'):
        print('----get admin flask')

    elif MockItemServices.isExisted(origin_path):
        mock_object = MockItemServices.get_json(MockItemServices.isExisted(origin_path))


        # json_resp = jsonify(mock_object.mock_json)
        # rsp = make_response(json_resp)
        rsp = make_response(mock_object.mock_json)

        print('----> Get mock: json_resp> {}'.format(mock_object.mock_json))
        return rsp
    else:
        print("-> Cann't find mockID")
        # we can use requests.Session() to reuse TCP connection to promote performance
        # with closing(
        #         requests.request(method, url, headers=headers, data=data, stream=True)
        # ) as r:

        # r = requests.request(method, url, headers=headers, data=data, stream=True)
        r = requests.request(method, url=objectServerIP + '/' + origin_path, headers=headers, data=data, stream=True)

        print("step 1")
        response_headers = []
        for name, value in r.headers.items():
            if name.lower() in ('content-length', 'connnection', 'content-encoding'):
                continue
            response_headers.append((name, value))
        print("-> Redirect request to object mac")
        return Response(r, status=r.status_code, headers=response_headers)

# @main.route('/hi')
# def hi_():
#     return 'hi mock user~'
#
#
# @main.route('/lists', methods=['GET'])
# def get_lists():
#     json_lists = MockItem.get_json_list()
#     res = str(len(json_lists)) + ' ' + json_lists[0].name
#     return res





##for admin custom view
class CustomModelView(ModelView):
    """View function of Flask-Admin for Models page."""
    page_size = 10
    form_excluded_columns = ['create_time', 'op_time','modules']  # remove fields from the create and edit forms