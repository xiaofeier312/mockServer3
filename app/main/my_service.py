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
        and t.mobile = """ + '\''+ tel+ '\''

        # print('----sql is : {}'.format(sql))
        r = self.ses.execute(sql)
        t = r.fetchall()
        all_result_list = []
        print('----sql result is: {}'.format(t))
        for i in t:
            rs_dict = {'entOrderId': i.orderdetailsID, 'firstProject': i.p1name, 'secondProject': i.p2name,\
                       'type':i.typepackname,"enterTime":i.biedatatime.strftime("%Y-%m-%d %H:%M:%S"),"statusCode":i.odstatus}
            all_result_list.append(rs_dict)

        all_result_final={"flag":"1", "data": {"name":t[0].tusername,"classType":[all_result_list]}, "error":"success."}
        return all_result_final

    def query_queryOrderDetails(self, serial_no):

        sql = """SELECT od.id as "ord_did",od.biz_date "biedatatime",t.cert_no"t-cert_no",cn.name"codeName",odc.code_name_id"codeNameId",
        f.college_id"cliegaidbycamp", cp.college_id"collegeidbypackage",c.name"collegenamebycamp", c1.name"collegenamebypackage",
        o.serial_no"o-serial_no", od.biz_date "od-biz_date",  p1.name "p1-name",p2.name "p2-name" ,   od.`serial_no` as "orderdetailsID", 
        pack.name as 'packname',od.`status_code` as 'odstatus'
        ,t.username,f.id as "familyId",t.mobile, epp.position as "eppposition",
        
        f.name,epp.name as "eppname",epp.username as "eppusername",f.id,p1.name,o.payment_date,p2.name,od.`serial_no`,t.id as "stuID",
        od.`status_code` as 'odstatus',c.name as"cname",cn.name, od.training_amount
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
        WHERE od.delete_flag=0 and o.delete_flag=0 and pack.delete_flag=0 and cp.delete_flag=0 and p1.delete_flag=0 and p2.delete_flag=0
        and od.status_code in("PAID","FREEZED") 
        and od.biz_date >"2016-10-01" 
        and ecp.person_id =epp.id
        and od.serial_no = """ + '\''+ serial_no+ '\''

        # print('----sql is : {}'.format(sql))
        r = self.ses.execute(sql)
        t = r.fetchall()
        all_result_list = []
        print('----sql result is: {}'.format(t))
        for i in t:
            rs_dict = {
                "ad": "今日头条","cert_no": "410928199104011112", "city_id": "4", "city_name": "北京", "class_adviser": "lidongbo01", "email": "123@qq.com",
                'family': i.familyname, 'family_head': i.codeName, 'collegenamebypackage': i.collegenamebypackage}
            all_result_list.append(rs_dict)
            del rs_dict
        all_result_final={"code":"SUCCESS", "data":all_result_list, "message":""}
        return all_result_final