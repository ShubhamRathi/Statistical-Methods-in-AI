import json
t=open('ted_talks-10-Sep-2012.json', 'r+')
talks=json.loads(t.read())
for j in talks:
	del j['comments']
