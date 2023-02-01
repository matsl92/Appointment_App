from datetime import time, date, datetime, timedelta

class Bubble:   # Global class
        def __init__(self, start, end):
            self.start = start
            self.end = end
        
        def __str__(self):
            return str(self.start.time())
        
        
class Label:
    def __init__(self, date):
        self.date = date.strftime('%d')
        self.day = date.strftime('%a')
        
        
class SemiGap:   # Global class
    def __init__(self, start, end, index):
        self.start = start
        self.end = end
        self.index = index
    
    def __str__(self):
        return str(self.start.time().strftime('%I:%M %p'))


def approximate_time(t):  # create_new_gaps GET
    a = t.minute
    appr_a = round(a/5)*5
    if appr_a == 60:
        return time(t.hour + 1, 0)
    else:
        return time(t.hour, appr_a)
    
def approximate_timedelta(td):
    td = td.seconds
    td = round(td/300)*300
    return timedelta(seconds=td)

def get_str_values(post):  
    values = {}
    for key, value in post.items():
        values[key] = value
    return(values)

def index_addition(index, num): # create_gaps
    elements = index.split(':')
    last = int(elements[-1])
    elements[-1] = str(last+num)
    return ':'.join(elements)

gap_step = timedelta(minutes=5) 

gap_duration = timedelta(minutes=30)