def add_students(students, db, Student):
    for info in students:
	s = Student.query.filter_by(email=info['email']).first()
	if not s:        
	    s = Student(email=info['email'])
        s.firstname = info['first']
        s.lastname = info['last']
	s.bcm_id = info['bcm_id']
        s.grade = info['year']
        s.department_std = info['department']
        s.studenttitle = getTitle(info)
        advisors = info['advisor']

        if advisors:
            s.advisorname1 = advisors[0]['first'] + ' ' + advisors[0]['last']
            s.advisortitle1 = getTitle(advisors[0])
            if len(advisors) == 2:
                s.advisorname2 = advisors[1]['first'] + ' ' + advisors[1]['last']
                s.advisortitle2 = getTitle(advisors[1])

        db.session.add(s)
    db.session.commit()

import re
def processName(name):
    info = {}
    # strip off PhD and MD part
    n = re.sub('Ph\.?D\.?\s*,?', '', name)
    info['isPhD'] = len(n) < len(name)
    name = n
    n = re.sub('M\.?D\.?\s*,?', '', name)
    info['isMD'] = len(n) < len(name)
    name = n.strip()
    p1 = re.compile(r'^(?P<last>[-\s\w]+),\s*(?P<first>[-\s\w]+)') # Last, First
    p2 = re.compile(r'^(?P<first>[-\s\w]+)\s+(?P<last>[-\s\w]+)') # First Last
    m1 = p1.search(name)
    m2 = p2.search(name)
    if m1:
        d=m1.groupdict()
        info['first'] = d['first']
        info['last'] = d['last']
    elif m2:
        d=m2.groupdict()
        info['first'] = d['first']
        info['last'] = d['last']
    else:
        info['first'] = 'unknown'
        info['last'] = 'unknown'
    return info


def load_students(filename):
    students = []
    import csv
    with open(filename) as f:
        f.readline()
        r = csv.reader(f)
        for x in r:
            info = processName(x[0])
            info['email'] = x[1]
	    info['bcm_id'] = x[2]
            info['year'] = x[3]
            info['department'] = x[4]
            if not x[5]:
                info['advisor'] = None
            else:
                info['advisor'] = [processName(a) for a in x[5].split('/')]
            students.append(info)
    return students

def getTitle(info):
    isMD = info['isMD']
    isPhD = info['isPhD']
    isMDPhD = isMD and isPhD
    if isMDPhD:
        return 'MD/PhD'
    elif isMD:
        return 'MD'
    elif isPhD:
        return 'PhD'

