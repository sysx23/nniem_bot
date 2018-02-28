#!/usr/bin/env python3

import xlrd
from nniem_bot import lesson

FIRST_WEEK_ROW = 7
SECOND_WEEK_ROW = 82
DAYS_IN_WEEK = 6

ROW_GROUP = 0
COLUMN_GROUP = 1
COLUMN_NUMBER = 1
COLUMN_SUBJECT = 2
COLUMN_ROOM = 6
COLUMN_TYPE = 8
COLUMN_TEACHER = 10

STR_LECTURE = "Лекцiя" # latin i!
STR_PRACTICAL = "Практичне"
STR_LABORATORY = "Лабораторна"


class UnsuccessfulParsing(Exception):
    def __init__(self, lesson=None, filename=None, row=None):
        message="Lesson does not parsed successfully"
        if filename :
            message+=" in "+filename
        if row :
            message+=" in row "+str(row)
        if lesson :
            message+="\n lesson attributes:\n"+str(vars(lesson))
        Exception.__init__(self, message )

class LessonOutOfTimetable(Exception):
    def __init__(self, day, number, filename=None):
        message="Day or number is out of timetable."
        if filename :
            message+=" in"+filename
        message+=" day: "+str(day)+"; number: "+str(number)
        Exception.__init__(self, message )

def get_lesson_row(day, number):
    if day < 0 or day >= lesson.DAYS :
        raise LessonOutOfTimetable(day,number)
    if number < 0 or number > lesson.MAX_LESSONS_IN_DAY :
        raise LessonOutOfTimetable(day,number)
    if (day == 5 or day == 11) and number > 3 : #special case for xls files
        raise LessonOutOfTimetable(day,number)
    if day < 6 :
        first_row=FIRST_WEEK_ROW
    else :
        first_row=SECOND_WEEK_ROW
        day-=DAYS_IN_WEEK
    return first_row+(day*DAYS_IN_WEEK+number)*2


def get_institute(sheet):
    group_str=sheet.row_values(ROW_GROUP)[COLUMN_GROUP]
    return group_str.split(' ', 1)[0]


def get_group(sheet):
    group_str=sheet.row_values(ROW_GROUP)[COLUMN_GROUP]
    return group_str.split(' ', 1)[1]


def get_type(sheet, row):
    """
    Returns type of lesson as int:
    0   lecture
    1   practical lesson
    2   laboratory work
    None  unknown type
    """
    type_str = sheet.row_values(row)[COLUMN_TYPE].strip()
    if type_str == STR_LECTURE :
        return 0
    elif type_str == STR_PRACTICAL :
        return 1
    elif type_str == STR_LABORATORY : #TODO: Test! By now there are no xls provided that contains laboratory works.
        return 2
    else :
        return -1


def parse_row(sheet, row):
    l=lesson.Lesson()
    l.f_institute=get_institute(sheet)
    l.f_group=get_group(sheet)
    l.f_subject=sheet.row_values(row)[COLUMN_SUBJECT]
    l.f_room=sheet.row_values(row)[COLUMN_ROOM]
    l.f_teacher=sheet.row_values(row)[COLUMN_TEACHER]
    l.f_type=get_type(sheet, row)
    return l


def parse_file(filename):
    wb = xlrd.open_workbook(filename)
    sheet =wb.sheet_by_index(0)
    lessons_list = list()
    for day in range(lesson.DAYS):
        for number in range(lesson.MAX_LESSONS_IN_DAY):
            try:
                row = get_lesson_row(day, number)
            except LessonOutOfTimetable:
                continue
            l = parse_row(sheet, row)
            if not l.f_subject:
                continue
            l.f_day=day
            l.f_number=number
            if not l.check() :
                raise UnsuccessfulParsing(filename=filename, lesson=l, row=row)
            lessons_list.append(l);
    return lessons_list

