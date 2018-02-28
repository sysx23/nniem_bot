from nniem_bot.parse_xls import *

def test_get_lesson_row() :
    assert get_lesson_row(0,0) == FIRST_WEEK_ROW
    assert get_lesson_row(DAYS_IN_WEEK,0) == SECOND_WEEK_ROW
    try :
        get_lesson_row(5,4)
    except LessonOutOfTimetable:
        pass
    else:
        assert False

def test_parse_file():
    ll=parse_file('test/210.xls')
    assert len(ll) == 22
