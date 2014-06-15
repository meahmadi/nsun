from datetime import timedelta,datetime
import copy
import time
class MDateTime(object):
    def __init__(self,dtime=None,delta=None):
        basetime = dtime
        if basetime is None:
            basetime = datetime.now()
        if delta is not None:
            basetime += delta 
        self.year = basetime.year
        self.month = basetime.month
        self.day = basetime.day
        self.hour = basetime.hour
        self.minute = basetime.minute
        self.second = basetime.second
        self.msecond = basetime.microsecond / 1000
        
    @classmethod
    def create(cls,year=0,month=0,day=0,hour=0,minute=0,second=0,msecond=0):
        self = cls()
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.msecond = 0
        return self.addDelta(year, month, day, hour, minute, second, msecond)
    @classmethod
    def fromMSeconds(cls,mseconds):
        return cls.create(msecond=mseconds)
    def addDelta(myself,year=0,month=0,day=0,hour=0, minute=0,second=0, msecond=0):
        self = copy.copy(myself)
        if (msecond != 0) or (self.mseconds > 1000 or self.msecond<0):
            self.msecond += msecond
            self.second += self.msecond / 1000
            self.msecond = self.msecond % 1000
        if (self.second > 59 or self.second < 0) or (second!=0):
            self.second += second
            self.minute += self.second / 60
            self.second = self.second % 60
        if (self.minute > 59 or self.minute < 0) or (minute!=0):
            self.minute += minute
            self.hour += self.minute / 60
            self.minute = self.minute % 60
        if (self.hour > 24 or self.hour < 24) or (hour!=0):
            self.hour += hour
            self.day += self.hour / 24
            self.hour = self.hour % 24
        if (self.day > 31 or self.day < 1) or (day!=0):
            self.day += day
            self.month += self.day / 30
            self.day = self.day % 30
        if (self.month > 12 or self.month < 1) or (month!=0):
            self.month += month
            self.year += self.month / 12
            self.month = self.month % 12
        if (year!=0):
            self.year += year
        return self
    def isoformat(self):
        return "%d-%d-%d %d:%d:%d:%d"%(self.year,self.month,self.day,self.hour,self.minute,self.second,self.msecond)
    def mseconds(self):
        return (((self.year*365 + self.month * 30 + self.day)*24 + self.hour)*3600 + self.minute*60 + self.second) * 1000 + self.msecond