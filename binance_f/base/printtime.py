import sys


import time




class PrintDate:
    @staticmethod
    def timestamp_to_date(ts_minsecond):
        try:
            ts_minsecond = int(ts_minsecond)
            time_local = time.localtime(int(ts_minsecond / 1000))
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            print("ping " + str(ts_minsecond) + ":" + dt)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    ping_ts = 1569319465421
    PrintDate.timestamp_to_date(ping_ts)
    PrintDate.timestamp_to_date(int(ping_ts), ("ping " + str(ping_ts)))

