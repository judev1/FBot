from datetime import datetime, timezone

class ftime:

    def __init__(self):
        self.set()

    def set(self):
        time = datetime.now(tz=timezone.utc)
        self.min_start, self.hour_start, self.day_start, self.month_start = [int(i) for i in time.strftime("%M %H %d %m").split()]
        self.start = self.now()

    def now(self):
        time = datetime.now(tz=timezone.utc)
        return time.strftime("%H:%M, %d/%m/%y UTC")

    def isweekend(self):
        return datetime.now().strftime("%a") in ["Sat", "Sun"]

    def uptime(self):
        time = datetime.now(tz=timezone.utc)
        min_start, hour_start, day_start, month_start = self.min_start, self.hour_start, self.day_start, self.month_start
        min_now, hour_now, day_now, month_now = [int(i) for i in time.strftime("%M %H %d %m").split()]

        if month_start > month_now:
            months = 60 - month_start + month_now
        else: months = month_now - month_start

        if day_start > day_now:
            if month_start == 2:
                days = 28 - day_start
            elif month_start in [4, 6, 9, 10]:
                days = 30 - day_start
            else:
                days = 31 - day_start
            days += day_now
            months -= 1
        else: days = day_now - day_start

        if hour_start > hour_now:
            hours = 24 - hour_start + hour_now
            days -= 1
        else: hours = hour_now - hour_start

        if min_start > min_now:
            mins = 60 - min_start + min_now
            hours -= 1
        else: mins = min_now - min_start

        days_plural, hours_plural, mins_plural = "s", "s", "s"
        if days == 1: days_plural = ""
        if hours == 1: hours_plural = ""
        if mins == 1: mins_plural = ""

        if days > 0:
            uptime = f"{days} day{days_plural}, {hours} hour{hours_plural}"
        elif hours > 0:
            uptime = f"{hours} hour{hours_plural}, {mins} minute{mins_plural}"
        else: uptime = f"{mins} minute{mins_plural}"

        return uptime