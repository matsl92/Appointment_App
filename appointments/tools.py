from datetime import time, date, datetime, timedelta

gap_step = timedelta(minutes=5) 

gap_duration = timedelta(minutes=30)

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
