import pytz
import datetime

hui = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
print(hui.strftime("%A, %d %B %Y"))