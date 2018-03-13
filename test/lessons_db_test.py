from nniem_bot import lessons_db
from nniem_bot import lesson
from nniem_bot import parse_xls

def test_db(tmpdir):
    db=lessons_db.lessons_db_worker(str(tmpdir)+"/base.db")
    db.init_db()
    ll=parse_xls.parse_file('test/210.xls')
    for les in ll:
        db.append_lesson(les)
    rl=db.get_lessons(f_day=1)
    assert rl[1].f_subject == 'Алгоритмізація та програмування в економіці'


