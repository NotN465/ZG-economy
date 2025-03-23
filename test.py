from datetime import datetime,timedelta

last_work_time = "54-20-02-03-2025"

last_work_time = datetime.strptime(last_work_time, "%M-%H-%d-%m-%Y") + timedelta(hours=4)

print(last_work_time)