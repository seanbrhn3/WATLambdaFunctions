import pymysql
import pymysql.cursors
import os
import uuid



class SQLClient():
    USERNAME = os.getenv("SQLUSERNAME")
    PASSWORD = os.getenv("SQLPASSWORD")
    DB_NAME = os.getenv("SQLDBNAME")
    URL = os.getenv("SQLURL")
    
    con = pymysql.connect(host=URL, user=USERNAME,
        password=PASSWORD, database=DB_NAME,cursorclass=pymysql.cursors.DictCursor)
    
    def insert(self,schema):
        try:
            cursor = self.con.cursor()
            uid = uuid.uuid4()
            title = schema.get("title",None)
            link = schema.get("link",None)
            price = schema.get("price",None)
            s3_prefix = schema.get("s3_prefix",None)
            sql_insert = f"INSERT INTO `{self.DB_NAME}`.`shoe_meta_data` (`uuid`,`name`,`link`,`price`,`s3_prefix`)VALUES('{uid}','{title}','{link}','{price}','{s3_prefix}')"
            cursor.execute(sql_insert)    
            self.con.commit()
            self.con.close()
            print(f"[+] Data Uploaded Successfully: {schema}")
        except Exception as e:
            print(f"[!] Unable to insert data: {e}")