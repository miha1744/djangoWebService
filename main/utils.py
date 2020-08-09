from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event, Doctor

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()


	# formats a day as a td
	# filter events by day
	def formatday(self, day, events, id):
		events_per_day = events.filter(start_time__day=day, doctor__user_id=id)
		d = ''
		kol=0
		list = []
		for event in events_per_day:
			d = ''
			kol+=1
			d = f'<a href="{event.get_daily_url}"> {kol} patients</a>'

		if day != 0:
			if d !='':
				return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
			return f"<td><span class='date'>{day}"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, events, id):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events, id)
		return f'<tr> {week} </tr>'


	# formats a month as a table
	# filter events by year and month
	def formatmonth(self,id,  withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events, id)}\n'
		return cal
