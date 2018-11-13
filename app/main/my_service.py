from ..models import MockJson
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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

        sql = "select id,username,email_263 from ent_portal.t_user_info where mobile = " + '\''+ tel+ '\''

        print('----sql is : {}'.format(sql))
        r = self.ses.execute(sql)
        t = r.fetchall()
        t[0].username
        print('----t is: {}'.format(t))
        rs_dict = {'id': t[0].id, 'username': t[0].username, 'email_263': t[0].email_263}
        return rs_dict

    def query_selectStudentOrders(self, tel):

        sql = """SELECT od.id as "ord_did",od.biz_date "biedatatime",t.cert_no"t-cert_no",cn.name"codeName",odc.code_name_id"codeNameId",
        f.college_id"cliegaidbycamp", cp.college_id"collegeidbypackage",c.name"collegenamebycamp", c1.name"collegenamebypackage",
        o.serial_no"o-serial_no",od.biz_date "od-biz_date",p1.name "p1-name",p2.name "p2-name" 
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
        and t.mobile = """ + '\''+ tel+ '\''

        # print('----sql is : {}'.format(sql))
        r = self.ses.execute(sql)
        t = r.fetchall()
        all_result_list = []
        print('----sql result is: {}'.format(t))
        for i in t:
            rs_dict = {'id': i.ord_did, 'codeName': i.codeName, 'collegenamebypackage': i.collegenamebypackage}
            all_result_list.append(rs_dict)
            del rs_dict
        all_result_final={"code":"SUCCESS", "data":all_result_list, "message":""}
        return all_result_final