from flask import render_template, request
from .. import db
from . import main
from flask import make_response, jsonify, Response
#from my_service import MockItemServices
from app.main.my_service import MockItemServices
import requests
from contextlib import closing
from config import objectServer
import re
from flask_admin.contrib.sqla import ModelView
from wtforms import TextAreaField
import json
from config import logger

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
    logger.info('-> url: {}'.format(url))
    logger.info('-> method: {}'.format(method))
    logger.info('-> data: {}'.format(data))
    print('-> url: {}'.format(url))
    print('-> method: {}'.format(method))
    print('-> data: {}'.format(data))
    for name, value in request.headers:
        if not value or name == 'Cache-Control':
            continue
        headers[name] = value
        print('-> name is : {} - value is : {}'.format(name, value))
    if origin_path.startswith('sdmockserver3/'):
        pass

    elif origin_path.startswith('etl-web-service/order/selectStudentOrders'):
        body2 = request.get_data()
        dict_body = json.loads(body2)
        tel = dict_body['tel']

        mockItem = MockItemServices()
        result = mockItem.query_selectStudentOrders(tel)
        print('----sql result: {}'.format(result))

        rsp = make_response(json.dumps(result, ensure_ascii=False))
        return rsp

    elif origin_path.startswith('etl-web-service/order/queryOrderDetails'):
        body2 = request.get_data()
        dict_body = json.loads(body2)
        mockItem = MockItemServices()

        try:
            if 'serial_no_eq' in dict_body:
                serial_no = dict_body['serial_no_eq']
                logger.info('----Get serial_no : {}'.format(serial_no))
                result = mockItem.query_queryOrderDetails(serial_no)
            elif 'mobile_eq' in dict_body:
                mobile = dict_body['mobile_eq']
                logger.info('----Get mobile : {}'.format(mobile))
                result = mockItem.query_queryOrderDetails_by_mobile(mobile)
            elif 'stu_id' in dict_body:
                stu_id = dict_body['stu_id_eq']
                logger.info('----Get stu_id : {}'.format(stu_id))
                result = mockItem.query_queryOrderDetails_by_stu_id(stu_id)
            elif 'stu_id_in' in dict_body:
                stu_id_in = dict_body['stu_id_in']
                logger.info('----Get stu_id_in : {}'.format(stu_id_in))
                logger.info('----Get stu_id_in: {}'.format(stu_id_in))
                result = mockItem.query_queryOrderDetails_by_stu_id_in(stu_id_in)
            else:
                result = "----Not support parmeter, please cantact QA!"

        except Exception as ke:
            logger.error(ke)

        print('----sql result: {}'.format(result))

        rsp = make_response(json.dumps(result, ensure_ascii=False))
        return rsp


    elif MockItemServices.isExisted(origin_path):
        mock_object = MockItemServices.get_json(MockItemServices.isExisted(origin_path))

        # json_resp = jsonify(mock_object.mock_json)
        # rsp = make_response(json_resp)
        rsp = make_response(mock_object.mock_json)

        print('----> Get mock: json_resp> {}'.format(mock_object.mock_json))
        return rsp
    elif MockItemServices.isExisted('/' + origin_path):
        mock_object = MockItemServices.get_json(MockItemServices.isExisted('/' + origin_path))

        # json_resp = jsonify(mock_object.mock_json)
        # rsp = make_response(json_resp)
        rsp = make_response(mock_object.mock_json)

        print('----> Get mock: json_resp> {}'.format(mock_object.mock_json))
        return rsp
    elif MockItemServices.isExisted(origin_path + '/'):
        mock_object = MockItemServices.get_json(MockItemServices.isExisted(origin_path + '/'))

        # json_resp = jsonify(mock_object.mock_json)
        # rsp = make_response(json_resp)
        rsp = make_response(mock_object.mock_json)

        print('----> Get mock: json_resp> {}'.format(mock_object.mock_json))
        return rsp
    elif MockItemServices.isExisted('/' + origin_path + '/'):
        mock_object = MockItemServices.get_json(MockItemServices.isExisted('/' + origin_path + '/'))

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
    page_size = 20
    can_view_details = True
    # create_modal = True
    # edit_modal = True
    column_searchable_list = ['url', 'name']
    form_excluded_columns = ['delay_time', 'delay_status', 'create_time', 'update_time', 'op_time', 'mock_id',
                             'reserveParam2']  # remove fields from the create and edit forms
    column_exclude_list = ['delay_time', 'delay_status', 'create_time', 'op_time', 'mock_id',
                           'reserveParam2']

    form_overrides = {
        'mock_json': TextAreaField
    }
    form_widget_args = {
        'mock_json': {
            'style': 'height:350px'
        }
    }
