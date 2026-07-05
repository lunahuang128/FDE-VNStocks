import socket
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ICT = ZoneInfo("Asia/Ho_Chi_Minh")

now_utc = datetime.now(timezone.utc)

print(f"host: {socket.gethostname()}")
print(f"utc : {now_utc:%Y-%m-%d %H:%M:%S %Z}")
print(f"ict : {now_utc.astimezone(ICT):%Y-%m-%d %H:%M:%S UTC%z}")