import psycopg2
import sys
sys.path.append("/home/prianechka/Education/BMSTU/DB-CourseWork/DB-Coursework/src/")
from errors import *

class BaseRepo():
    def __init__(self):
        self.connection = psycopg2.connect(user="bob", password="admin", 
                                            host="localhost", port="5432", database="course")

    def execute(self, executeString):
        errorCode = OK
        result = []
        try:
            self.cur.execute(executeString)
        except Exception as e:
            print(e)
            errorCode = DATABASE_ERROR
            self.connection.rollback()
        else:
            self.connection.commit()
        
        try:
            result = self.cur.fetchall()
        except:
            pass
        
        return errorCode, result