import datetime

def seconds_between(date1, date2):
	return abs((date2 - date1).days*86400.)


def minutes_between(date1, date2):
	return abs((date2 - date1).days*1440.)


def hours_between(date1, date2):
	return abs((date2 - date1).days*24.)


def days_between(date1, date2):
	return abs((date2 - date1).days)


def months_between(date1, date2):
	return (date2.year - date1.year)*12 + date2.month - date1.month


def years_between(date1,date2):
	return (date2.year - date1.year)+((date2.month-date1.month)/12.0)


def time_between(date1,date2):
	return date2-date1


def print_time_between(date1, date2):
	print '\n'
	print ' Time between dates:'
	print ' Date 1:', date1
	print ' Date 2:', date2
	print '----------------------------'
	print 'Seconds: {:>8}'.format(str(seconds_between(date1,date2)))
	print 'Minutes: {:>8}'.format(str(minutes_between(date1,date2)))
	print '  Hours: {:>8}'.format(str(hours_between(date1,date2)))
	print '   Days: {:>8}'.format(str(days_between(date1,date2)))
	print ' Months: {:>8}'.format(str(months_between(date1,date2)))
	print '  Years: {:>8}'.format(str(years_between(date1,date2)))
	print '  Total:', time_between(date1,date2)
	print '\n'


if __name__ == '__main__':

    import sys

    # Commandline Arguments Handling #
    if len(sys.argv) < 3:
        print "\ndate format: yyyy-mm-dd"
        sys.exit("usage: "+sys.argv[0]+" <date 1> <date2>\n")

    date1 = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d")
    date2 = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d")

    print_time_between(date1, date2)

    #print 'months:',(datetime.date(year2,month2,day2).toordinal() - datetime.date(year1,month1,day1).toordinal())/30.
