from datetime import datetime

now = datetime.now()
print(now,type(now))
print(now.strftime("%M-%H-%d-%m-%Y"),type(now.strftime("%M-%H-%d-%m-%Y")))
print(str(now),type(str(now)))

print(str(now.strftime("%M-%H-%d-%m-%Y")),type(str(now.strftime("%M-%H-%d-%m-%Y"))))