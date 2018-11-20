from ..models import MockJson
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal


class MockItemServices(object):
    def __init__(self):
        self.eng = create_engine('mysql+pymysql://ent_all:ent@172.16.117.226:3306/ent_portal?charset=utf8')
        self.DBSession = sessionmaker(bind=self.eng)
        self.ses = self.DBSession()

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

    def query_portal(self, tel):
        # eng=create_engine('mysql+pymysql://ent_all:ent@172.16.117.226:3306/ent_portal?charset=utf8')
        # DBSession=sessionmaker(bind=eng)
        # ses=DBSession()

        sql = "select id,username,email_263 from ent_portal.t_user_info where mobile = " + '\'' + tel + '\''

        print('----sql is : {}'.format(sql))
        r = self.ses.execute(sql)
        t = r.fetchall()
        t[0].username
        print('----t is: {}'.format(t))
        rs_dict = {'id': t[0].id, 'username': t[0].username, 'email_263': t[0].email_263}
        return rs_dict

    def query_selectStudentOrders(self, tel):

        sql = """SELECT   od.`serial_no` as "orderdetailsID",p1.name "p1name",p2.name "p2name",pack.name as "typepackname",
        od.biz_date "biedatatime",od.`status_code` as "odstatus",t.username as "tusername"
        from ent_ord_details od 
        LEFT JOIN ent_order o on o.id=od.ord_id
        LEFT JOIN t_user_info t on t.id=o.stu_id
        LEFT JOIN ent_package pack on pack.id=od.package_id
        LEFT JOIN ent_college_projs cp on cp.id=pack.college_proj_id
        LEFT JOIN ent_proj_1st p1 on p1.id=cp.proj_1st_id
        LEFT JOIN ent_proj_2nd p2 on p2.id=cp.proj_2nd_id
        LEFT JOIN ent_ord_detail_camp odc ON odc.ord_detail_id=od.id
        LEFT JOIN ent_code_name cn on cn.id =odc.code_name_id
        LEFT JOIN ent_family f ON f.family_no = odc.family_id
        LEFT JOIN ent_college c ON  c.id=f.college_id
        LEFT JOIN ent_college c1 ON c1.id=cp.college_id
        #LEFT JOIN ent_ord_exam_plan 
        WHERE od.delete_flag=0 and o.delete_flag=0 and pack.delete_flag=0 and cp.delete_flag=0 and p1.delete_flag=0 and p2.delete_flag=0
        and od.status_code in("PAID","FREEZED") 
        and od.biz_date >"2016-10-01" 
        and t.mobile = """ + '\'' + tel + '\''

        # print('----sql is : {}'.format(sql))
        r = self.ses.execute(sql)
        t = r.fetchall()
        all_result_list = []
        print('----sql result is: {}'.format(t))
        for i in t:
            rs_dict = {'entOrderId': i.orderdetailsID, 'firstProject': i.p1name, 'secondProject': i.p2name, \
                       'type': i.typepackname, "enterTime": i.biedatatime.strftime("%Y-%m-%d %H:%M:%S"),
                       "statusCode": i.odstatus}
            all_result_list.append(rs_dict)

        all_result_final = {"flag": "1", "data": {"name": t[0].tusername, "classType": [all_result_list]},
                            "error": "success."}
        return all_result_final

    def query_queryOrderDetails(self, serial_no):

        # This is not contain cp_leader, cp_dean
        sql = """SELECT od.id as "ord_did",od.biz_date "biedatatime",t.cert_no"t_cert_no",
        cn.name"codeName",odc.code_name_id"codeNameId",
        f.college_id"cliegaidbycamp", cp.college_id"collegeidbypackage",
        c.name"collegenamebycamp", c1.name"collegenamebypackage",
        o.serial_no"o-serial_no", od.biz_date "od-biz_date", od.`serial_no` as "orderdetailsID", 
        pack.name as "packname",od.status_code as "odstatus",t.username,f.id as "familyId",t.mobile, epp.position as "eppposition",    
        f.name as "familyname",epp.name as "eppname",epp.username as "eppusername",
        f.id,p1.name as "p1name",o.payment_date,p2.name as "p2name",od.serial_no,t.id as "stuID",
        od.`status_code` as "odstatus",c.name as"cname",cn.name, od.training_amount
        from ent_ord_details od 
        LEFT JOIN ent_order o on o.id=od.ord_id
        LEFT JOIN t_user_info t on t.id=o.stu_id
        LEFT JOIN ent_package pack on pack.id=od.package_id
        LEFT JOIN ent_college_projs cp on cp.id=pack.college_proj_id
        LEFT JOIN ent_proj_1st p1 on p1.id=cp.proj_1st_id
        LEFT JOIN ent_proj_2nd p2 on p2.id=cp.proj_2nd_id
        LEFT JOIN ent_ord_detail_camp odc ON odc.ord_detail_id=od.id
        LEFT JOIN ent_code_name cn on cn.id =odc.code_name_id
        LEFT JOIN ent_family f ON f.id = odc.family_id
        left join ent_code_name_person_rel ecnp on ecnp.code_name_id = cn.id     
        LEFT JOIN ent_college c ON  c.id=f.college_id   #老师的
        LEFT JOIN ent_college c1 ON c1.id=cp.college_id  #产品包
        LEFT JOIN ent_cp_person_rel ecp on ecp.family_id = f.id #and ecp.college_id = f.college_id
        Left join ent_p_cp epp on epp.id = ecnp.person_id
        #left join ent_p_co epp2 on 
        #LEFT JOIN ent_ord_exam_plan 
        WHERE od.delete_flag=0 and o.delete_flag=0 and pack.delete_flag=0 and cp.delete_flag=0 and p1.delete_flag=0 and p2.delete_flag=0 and ecp.delete_flag=0
        and od.status_code in("PAID","FREEZED") 
        and od.biz_date >"2016-10-01" 
        #and ecp.person_id =epp.id
        and od.serial_no =""" + '\'' + serial_no + '\'' + """group by  od.serial_no;"""

        sql2 = """SELECT od.id as "ord_did",epp.name, epp.username,epp.position as position
        from ent_ord_details od
        LEFT JOIN ent_order o on o.id=od.ord_id
        left join ent_ord_detail_camp odc on odc.ord_detail_id=od.id
        LEFT JOIN ent_cp_person_rel ecp on ecp.family_id = odc.family_id
        Left join ent_p_cp epp on epp.id = ecp.person_id        
        LEFT JOIN ent_college c ON  c.id=ecp.college_id   
        WHERE od.delete_flag=0 
        and od.status_code in("PAID","FREEZED") 
        and od.biz_date >"2016-10-01" 
        and epp.position in ('CP_LEADER','CP_DEAN')
        and od.serial_no = """ + '\'' + serial_no + '\'' + " group by position"

        print('----sql is : {}'.format(sql))
        r = self.ses.execute(sql)
        r2 = self.ses.execute(sql2)

        t = r.fetchall()
        if t == []:
            return ''

        t2 = r2.fetchall()

        sql2_leader = ()
        sql2_dean = ()
        # print('sql_leader: {}'.format(t2[1]))
        # print('type(t2[1]) is: {}'.format(type(t2[1])))
        if ('CP_LEADER' == t2[0].position):
            sql2_leader = t2[0]
            sql2_dean = t2[1]

        elif ('CP_LEADER' == t2[1].position):
            sql2_leader = t2[1]
            sql2_dean = t2[0]
        else:
            print("----Cannot find cp_leader!")

        all_result_list = []
        print('----sql result is: {}'.format(t))
        print('----sql2 result is: {}'.format(t2))
        for i in t:
            rs_dict = {
                "ad": "今日头条",
                "cert_no": i.t_cert_no,
                "city_id": "4",
                "city_name": "北京",
                "class_adviser": "lidongbo01",
                "email": "123@qq.com",
                "family": i.familyname,
                "family_head": sql2_leader.name,
                "family_head_em": sql2_leader.username,
                "family_id": i.familyId,
                "first_proj_name": i.p1name,
                "mobile": i.mobile,
                "pay_method_name": "天猫",
                "payment_time": i.biedatatime.strftime("%Y-%m-%d %H:%M:%S"),
                "qq_code": "123456789",
                "school_id": "1035",
                "school_name": "宁波校",
                "sec_proj_name": i.p2name,
                "serial_no": i.serial_no,
                "status_code": i.odstatus,
                "stu_id": i.stuID,
                "teach_college_head": sql2_dean.name,
                "teach_college_head_em": sql2_dean.username,
                "teach_college_id": i.cliegaidbycamp,
                "teach_college_name": i.collegenamebycamp,
                "teacher_code_name": i.codeName,
                "teacher_head": i.codeName,
                "teacher_head_em": i.eppusername,
                "third_proj_name": i.packname,
                "training_amount": str(i.training_amount.quantize(Decimal('0.00'))),
                "username": i.username,
                "weixin_id": "18334514213"
            }
            all_result_list.append(rs_dict)

        all_result_final = {"code":"SUCCESS", "data": all_result_list, "message":""}
        return all_result_final

    def query_queryOrderDetails_by_mobile(self, mobile):

        # This is not contain cp_leader, cp_dean
        sql = """SELECT od.id as "ord_did",od.biz_date "biedatatime",t.cert_no"t_cert_no",
        cn.name"codeName",odc.code_name_id"codeNameId",
        f.college_id"cliegaidbycamp", cp.college_id"collegeidbypackage",
        c.name"collegenamebycamp", c1.name"collegenamebypackage",
        o.serial_no"o-serial_no", od.biz_date "od-biz_date", od.`serial_no` as "orderdetailsID", 
        pack.name as "packname",od.status_code as "odstatus",t.username,f.id as "familyId",t.mobile, epp.position as "eppposition",    
        f.name as "familyname",epp.name as "eppname",epp.username as "eppusername",
        f.id,p1.name as "p1name",o.payment_date,p2.name as "p2name",od.serial_no,t.id as "stuID",
        od.`status_code` as "odstatus",c.name as"cname",cn.name, od.training_amount
        from ent_ord_details od 
        LEFT JOIN ent_order o on o.id=od.ord_id
        LEFT JOIN t_user_info t on t.id=o.stu_id
        LEFT JOIN ent_package pack on pack.id=od.package_id
        LEFT JOIN ent_college_projs cp on cp.id=pack.college_proj_id
        LEFT JOIN ent_proj_1st p1 on p1.id=cp.proj_1st_id
        LEFT JOIN ent_proj_2nd p2 on p2.id=cp.proj_2nd_id
        LEFT JOIN ent_ord_detail_camp odc ON odc.ord_detail_id=od.id
        LEFT JOIN ent_code_name cn on cn.id =odc.code_name_id
        LEFT JOIN ent_family f ON f.id = odc.family_id
        left join ent_code_name_person_rel ecnp on ecnp.code_name_id = cn.id     
        LEFT JOIN ent_college c ON  c.id=f.college_id   #老师的
        LEFT JOIN ent_college c1 ON c1.id=cp.college_id  #产品包
        LEFT JOIN ent_cp_person_rel ecp on ecp.family_id = f.id #and ecp.college_id = f.college_id
        Left join ent_p_cp epp on epp.id = ecnp.person_id
        #left join ent_p_co epp2 on 
        #LEFT JOIN ent_ord_exam_plan 
        WHERE od.delete_flag=0 and o.delete_flag=0 and pack.delete_flag=0 and cp.delete_flag=0 and p1.delete_flag=0 and p2.delete_flag=0 and ecp.delete_flag=0
        and od.status_code in("PAID","FREEZED") 
        and od.biz_date >"2016-10-01" 
        #and ecp.person_id =epp.id
        and t.mobile =""" + '\'' + mobile + '\'' + """group by  od.serial_no;"""

        sql2 = """SELECT od.id as "ord_did",epp.name, epp.username,epp.position as position
        from ent_ord_details od
        LEFT JOIN ent_order o on o.id=od.ord_id
        LEFT JOIN t_user_info t on t.id=o.stu_id
        left join ent_ord_detail_camp odc on odc.ord_detail_id=od.id
        LEFT JOIN ent_cp_person_rel ecp on ecp.family_id = odc.family_id
        Left join ent_p_cp epp on epp.id = ecp.person_id        
        LEFT JOIN ent_college c ON  c.id=ecp.college_id   
        WHERE od.delete_flag=0 
        and od.status_code in("PAID","FREEZED") 
        and od.biz_date >"2016-10-01" 
        and epp.position in ('CP_LEADER','CP_DEAN')
        and t.mobile =""" + '\'' + mobile + '\'' + """group by  position;"""

        print('----sql is : {}'.format(sql))
        r = self.ses.execute(sql)
        r2 = self.ses.execute(sql2)

        t = r.fetchall()
        t2 = r2.fetchall()

        sql2_leader = ()
        sql2_dean = ()
        # print('sql_leader: {}'.format(t2[1]))
        # print('type(t2[1]) is: {}'.format(type(t2[1])))
        if ('CP_LEADER' == t2[0].position):
            sql2_leader = t2[0]
            sql2_dean = t2[1]

        elif ('CP_LEADER' == t2[1].position):
            sql2_leader = t2[1]
            sql2_dean = t2[0]
        else:
            print("----Cannot find cp_leader!")

        all_result_list = []
        print('----sql result is: {}'.format(t))
        print('----sql2 result is: {}'.format(t2))
        for i in t:
            rs_dict = {
                "ad": "今日头条",
                "cert_no": i.t_cert_no,
                "city_id": "4",
                "city_name": "北京",
                "class_adviser": "lidongbo01",
                "email": "123@qq.com",
                "family": i.familyname,
                "family_head": sql2_leader.name,
                "family_head_em": sql2_leader.username,
                "family_id": i.familyId,
                "first_proj_name": i.p1name,
                "mobile": i.mobile,
                "pay_method_name": "天猫",
                "payment_time": i.biedatatime.strftime("%Y-%m-%d %H:%M:%S"),
                "qq_code": "123456789",
                "school_id": "1035",
                "school_name": "宁波校",
                "sec_proj_name": i.p2name,
                "serial_no": i.serial_no,
                "status_code": i.odstatus,
                "stu_id": i.stuID,
                "teach_college_head": sql2_dean.name,
                "teach_college_head_em": sql2_dean.username,
                "teach_college_id": i.cliegaidbycamp,
                "teach_college_name": i.collegenamebycamp,
                "teacher_code_name": i.codeName,
                "teacher_head": i.codeName,
                "teacher_head_em": i.eppusername,
                "third_proj_name": i.packname,
                "training_amount": str(i.training_amount.quantize(Decimal('0.00'))),
                "username": i.username,
                "weixin_id": "18334514213"
            }
            all_result_list.append(rs_dict)

        all_result_final = {"code":"SUCCESS", "data": all_result_list, "message":""}
        return all_result_final

    def query_queryOrderDetails_by_stu_id(self, stu_id):

        # This is not contain cp_leader, cp_dean
        sql = """SELECT od.id as "ord_did",od.biz_date "biedatatime",t.cert_no"t_cert_no",
        cn.name"codeName",odc.code_name_id"codeNameId",
        f.college_id"cliegaidbycamp", cp.college_id"collegeidbypackage",
        c.name"collegenamebycamp", c1.name"collegenamebypackage",
        o.serial_no"o-serial_no", od.biz_date "od-biz_date", od.`serial_no` as "orderdetailsID", 
        pack.name as "packname",od.status_code as "odstatus",t.username,f.id as "familyId",t.mobile, epp.position as "eppposition",    
        f.name as "familyname",epp.name as "eppname",epp.username as "eppusername",
        f.id,p1.name as "p1name",o.payment_date,p2.name as "p2name",od.serial_no,t.id as "stuID",
        od.`status_code` as "odstatus",c.name as"cname",cn.name, od.training_amount
        from ent_ord_details od 
        LEFT JOIN ent_order o on o.id=od.ord_id
        LEFT JOIN t_user_info t on t.id=o.stu_id
        LEFT JOIN ent_package pack on pack.id=od.package_id
        LEFT JOIN ent_college_projs cp on cp.id=pack.college_proj_id
        LEFT JOIN ent_proj_1st p1 on p1.id=cp.proj_1st_id
        LEFT JOIN ent_proj_2nd p2 on p2.id=cp.proj_2nd_id
        LEFT JOIN ent_ord_detail_camp odc ON odc.ord_detail_id=od.id
        LEFT JOIN ent_code_name cn on cn.id =odc.code_name_id
        LEFT JOIN ent_family f ON f.id = odc.family_id
        left join ent_code_name_person_rel ecnp on ecnp.code_name_id = cn.id     
        LEFT JOIN ent_college c ON  c.id=f.college_id   #老师的
        LEFT JOIN ent_college c1 ON c1.id=cp.college_id  #产品包
        LEFT JOIN ent_cp_person_rel ecp on ecp.family_id = f.id #and ecp.college_id = f.college_id
        Left join ent_p_cp epp on epp.id = ecnp.person_id
        #left join ent_p_co epp2 on 
        #LEFT JOIN ent_ord_exam_plan 
        WHERE od.delete_flag=0 and o.delete_flag=0 and pack.delete_flag=0 and cp.delete_flag=0 and p1.delete_flag=0 and p2.delete_flag=0 and ecp.delete_flag=0
        and od.status_code in("PAID","FREEZED") 
        and od.biz_date >"2016-10-01" 
        #and ecp.person_id =epp.id
        and t.id =""" + '\'' + stu_id + '\'' + """group by  od.serial_no;"""

        sql2 = """SELECT od.id as "ord_did",epp.name, epp.username,epp.position as position
        from ent_ord_details od
        LEFT JOIN ent_order o on o.id=od.ord_id
        LEFT JOIN t_user_info t on t.id=o.stu_id
        left join ent_ord_detail_camp odc on odc.ord_detail_id=od.id
        LEFT JOIN ent_cp_person_rel ecp on ecp.family_id = odc.family_id
        Left join ent_p_cp epp on epp.id = ecp.person_id        
        LEFT JOIN ent_college c ON  c.id=ecp.college_id   
        WHERE od.delete_flag=0 
        and od.status_code in("PAID","FREEZED") 
        and od.biz_date >"2016-10-01" 
        and epp.position in ('CP_LEADER','CP_DEAN')
        and t.id =""" + '\'' + stu_id + '\'' + """group by  position;"""

        print('----sql is : {}'.format(sql))
        r = self.ses.execute(sql)
        r2 = self.ses.execute(sql2)

        t = r.fetchall()
        t2 = r2.fetchall()

        sql2_leader = ()
        sql2_dean = ()
        # print('sql_leader: {}'.format(t2[1]))
        # print('type(t2[1]) is: {}'.format(type(t2[1])))
        if ('CP_LEADER' == t2[0].position):
            sql2_leader = t2[0]
            sql2_dean = t2[1]

        elif ('CP_LEADER' == t2[1].position):
            sql2_leader = t2[1]
            sql2_dean = t2[0]
        else:
            print("----Cannot find cp_leader!")

        all_result_list = []
        print('----sql result is: {}'.format(t))
        print('----sql2 result is: {}'.format(t2))
        for i in t:
            rs_dict = {
                "ad": "今日头条",
                "cert_no": i.t_cert_no,
                "city_id": "4",
                "city_name": "北京",
                "class_adviser": "lidongbo01",
                "email": "123@qq.com",
                "family": i.familyname,
                "family_head": sql2_leader.name,
                "family_head_em": sql2_leader.username,
                "family_id": i.familyId,
                "first_proj_name": i.p1name,
                "mobile": i.mobile,
                "pay_method_name": "天猫",
                "payment_time": i.biedatatime.strftime("%Y-%m-%d %H:%M:%S"),
                "qq_code": "123456789",
                "school_id": "1035",
                "school_name": "宁波校",
                "sec_proj_name": i.p2name,
                "serial_no": i.serial_no,
                "status_code": i.odstatus,
                "stu_id": i.stuID,
                "teach_college_head": sql2_dean.name,
                "teach_college_head_em": sql2_dean.username,
                "teach_college_id": i.cliegaidbycamp,
                "teach_college_name": i.collegenamebycamp,
                "teacher_code_name": i.codeName,
                "teacher_head": i.codeName,
                "teacher_head_em": i.eppusername,
                "third_proj_name": i.packname,
                "training_amount": str(i.training_amount.quantize(Decimal('0.00'))),
                "username": i.username,
                "weixin_id": "18334514213"
            }
            all_result_list.append(rs_dict)

        all_result_final = {"code":"SUCCESS", "data": all_result_list, "message":""}
        return all_result_final


    def query_queryOrderDetails_by_stu_id_in(self, stu_id_in):

        # This is not contain cp_leader, cp_dean
        sql = """SELECT od.id as "ord_did",od.biz_date "biedatatime",t.cert_no"t_cert_no",
        cn.name"codeName",odc.code_name_id"codeNameId",
        f.college_id"cliegaidbycamp", cp.college_id"collegeidbypackage",
        c.name"collegenamebycamp", c1.name"collegenamebypackage",
        o.serial_no"o-serial_no", od.biz_date "od-biz_date", od.`serial_no` as "orderdetailsID", 
        pack.name as "packname",od.status_code as "odstatus",t.username,f.id as "familyId",t.mobile, epp.position as "eppposition",    
        f.name as "familyname",epp.name as "eppname",epp.username as "eppusername",
        f.id,p1.name as "p1name",o.payment_date,p2.name as "p2name",od.serial_no,t.id as "stuID",
        od.`status_code` as "odstatus",c.name as"cname",cn.name, od.training_amount
        from ent_ord_details od 
        LEFT JOIN ent_order o on o.id=od.ord_id
        LEFT JOIN t_user_info t on t.id=o.stu_id
        LEFT JOIN ent_package pack on pack.id=od.package_id
        LEFT JOIN ent_college_projs cp on cp.id=pack.college_proj_id
        LEFT JOIN ent_proj_1st p1 on p1.id=cp.proj_1st_id
        LEFT JOIN ent_proj_2nd p2 on p2.id=cp.proj_2nd_id
        LEFT JOIN ent_ord_detail_camp odc ON odc.ord_detail_id=od.id
        LEFT JOIN ent_code_name cn on cn.id =odc.code_name_id
        LEFT JOIN ent_family f ON f.id = odc.family_id
        left join ent_code_name_person_rel ecnp on ecnp.code_name_id = cn.id     
        LEFT JOIN ent_college c ON  c.id=f.college_id   #老师的
        LEFT JOIN ent_college c1 ON c1.id=cp.college_id  #产品包
        LEFT JOIN ent_cp_person_rel ecp on ecp.family_id = f.id #and ecp.college_id = f.college_id
        Left join ent_p_cp epp on epp.id = ecnp.person_id
        #left join ent_p_co epp2 on 
        #LEFT JOIN ent_ord_exam_plan 
        WHERE od.delete_flag=0 and o.delete_flag=0 and pack.delete_flag=0 and cp.delete_flag=0 and p1.delete_flag=0 and p2.delete_flag=0 and ecp.delete_flag=0
        and od.status_code in("PAID","FREEZED") 
        and od.biz_date >"2016-10-01" 
        #and ecp.person_id =epp.id
        and t.id in """ + '(' + stu_id_in + ')' + """group by  od.serial_no;"""

        sql2 = """SELECT od.id as "ord_did",epp.name, epp.username,epp.position as position
        from ent_ord_details od
        LEFT JOIN ent_order o on o.id=od.ord_id
        LEFT JOIN t_user_info t on t.id=o.stu_id
        left join ent_ord_detail_camp odc on odc.ord_detail_id=od.id
        LEFT JOIN ent_cp_person_rel ecp on ecp.family_id = odc.family_id
        Left join ent_p_cp epp on epp.id = ecp.person_id        
        LEFT JOIN ent_college c ON  c.id=ecp.college_id   
        WHERE od.delete_flag=0 
        and od.status_code in("PAID","FREEZED") 
        and od.biz_date >"2016-10-01" 
        and epp.position in ('CP_LEADER','CP_DEAN')
        and t.id in """ + '(' + stu_id_in + ')' + """group by  position;"""

        print('----sql is : {}'.format(sql))
        r = self.ses.execute(sql)
        r2 = self.ses.execute(sql2)

        t = r.fetchall()
        t2 = r2.fetchall()

        sql2_leader = ()
        sql2_dean = ()
        # print('sql_leader: {}'.format(t2[1]))
        # print('type(t2[1]) is: {}'.format(type(t2[1])))
        if ('CP_LEADER' == t2[0].position):
            sql2_leader = t2[0]
            sql2_dean = t2[1]

        elif ('CP_LEADER' == t2[1].position):
            sql2_leader = t2[1]
            sql2_dean = t2[0]
        else:
            print("----Cannot find cp_leader!")

        all_result_list = []
        print('----sql result is: {}'.format(t))
        print('----sql2 result is: {}'.format(t2))
        for i in t:
            rs_dict = {
                "ad": "今日头条",
                "cert_no": i.t_cert_no,
                "city_id": "4",
                "city_name": "北京",
                "class_adviser": "lidongbo01",
                "email": "123@qq.com",
                "family": i.familyname,
                "family_head": sql2_leader.name,
                "family_head_em": sql2_leader.username,
                "family_id": i.familyId,
                "first_proj_name": i.p1name,
                "mobile": i.mobile,
                "pay_method_name": "天猫",
                "payment_time": i.biedatatime.strftime("%Y-%m-%d %H:%M:%S"),
                "qq_code": "123456789",
                "school_id": "1035",
                "school_name": "宁波校",
                "sec_proj_name": i.p2name,
                "serial_no": i.serial_no,
                "status_code": i.odstatus,
                "stu_id": i.stuID,
                "teach_college_head": sql2_dean.name,
                "teach_college_head_em": sql2_dean.username,
                "teach_college_id": i.cliegaidbycamp,
                "teach_college_name": i.collegenamebycamp,
                "teacher_code_name": i.codeName,
                "teacher_head": i.codeName,
                "teacher_head_em": i.eppusername,
                "third_proj_name": i.packname,
                "training_amount": str(i.training_amount.quantize(Decimal('0.00'))),
                "username": i.username,
                "weixin_id": "18334514213"
            }
            all_result_list.append(rs_dict)

        all_result_final = {"code":"SUCCESS", "data": all_result_list, "message":""}
        return all_result_final
