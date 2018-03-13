import sqlite3
from nniem_bot import lesson


SQL_INIT_SCRIPT = "sql/init.sql"


class lessons_db_worker :
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def init_db(self):
        with open(SQL_INIT_SCRIPT, "r") as f:
            self.cursor.executescript(f.read())

    def get_lessons(self, f_institute=None, f_group=None, f_id=None, f_subject=None, f_type=None, f_room=None, f_day=None, f_number=None, f_teacher=None, get_all=False):
        if get_all :
            self.cursor.execute("SELECT f_institute, f_group, f_subject, f_type, f_room, f_day, f_number, f_teacher FROM lessons ORDER BY f_day, f_number")
        else :
            empty = True
            query_str = "SELECT f_institute, f_group, f_subject, f_type, f_room, f_day, f_number, f_teacher FROM lessons WHERE "
            parameters = {
                    "id":f_id,
                    "f_institute":f_institute,
                    "f_group":f_group,
                    "f_subject":f_subject,
                    "f_type":f_type,
                    "f_room":f_room,
                    "f_day":f_day,
                    "f_number":f_number,
                    "f_teacher":f_teacher,
                    }
            if f_id != None:
                query_str += "id=:id "
                empty = False
            if f_institute :
                query_str += "f_institute=:f_institute "
                empty = False
            if f_group :
                query_str += "f_group=:f_group"
                empty = False
            if f_subject :
                query_str += "f_subject=:f_subject "
                empty = False
            if f_type != None:
                query_str += "f_type=:f_type "
                empty = False
            if f_room != None:
                query_str += "f_room=:f_room "
                empty = False
            if f_day != None:
                query_str += "f_day=:f_day "
                empty = False
            if f_number != None:
                query_str += "f_number=:f_number"
                empty = False
            if f_teacher != None:
                query_str += "f_teacher=:f_teacher "
                empty = False
            if not empty :
                query_str += "ORDER BY f_day, f_number"
                self.cursor.execute(query_str, parameters)
            else :
                return list()
            lessons_list = list()Алгоритмізація та програмування в економіці
            for l_t in self.cursor.fetchall():
                lessons_list.append(tuple2lesson(l_t))
        return lessons_list

    def append_lesson(self, lesson):
        self.cursor.execute("""
        INSERT INTO lessons (f_institute, f_group, f_subject, f_type, f_room, f_day, f_number, f_teacher)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (lesson.f_institute, lesson.f_group, lesson.f_subject, lesson.f_type, lesson.f_room, lesson.f_day, lesson.f_number, lesson.f_teacher) )
        self.connection.commit()


def tuple2lesson(t):
    l=lesson.Lesson()
    l.f_institute=t[0]
    l.f_group=t[1]
    l.f_subject=t[2]
    l.f_type=t[3]
    l.f_room=t[4]
    l.f_day=t[5]
    l.f_number=t[6]
    l.f_teacher=t[7]
    return l

