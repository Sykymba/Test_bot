from datetime import datetime, timedelta

data = datetime.now() + timedelta(days=1)

new_data = data.strftime('%d.%m.%Y')

print(data)
print(new_data)
