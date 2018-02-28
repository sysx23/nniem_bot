DAYS=12
MAX_LESSONS_IN_DAY=6

LESSON_STR_ATTRS = (
        "institute",
        "group",
        "subject",
        "room",
        "teacher",
        )

LESSON_NUM_ATTRS = (
        "type",
        "day",
        "number",
        )

LESSON_ATTRS = LESSON_STR_ATTRS + LESSON_NUM_ATTRS

class Lesson(object):
    def check(self):
        for attr in LESSON_ATTRS:
            if not hasattr(self,"f_"+attr) :
                return False
        for attr in LESSON_STR_ATTRS:
            if not getattr(self, "f_"+attr) :
                return False
        if self.f_day < 0 or self.f_day >= DAYS or self.f_number < 0 or self.f_number >= MAX_LESSONS_IN_DAY :
            return False
        return True
          
