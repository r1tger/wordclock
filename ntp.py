try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct

import utime


class NTPClient():
    # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
    NTP_DELTA = 3155673600
    DEBUG = False

    @staticmethod
    def cet_time():
        year = utime.localtime()[0]       # get current year
        HHMarch = utime.mktime((year, 3, (31 - (int(5 * year / 4 + 4)) % 7), 1, 0, 0, 0, 0, 0))  # noqa: Time of March change to CEST
        HHOctober = utime.mktime((year, 10, (31 - (int(5 * year / 4 + 1)) % 7), 1, 0, 0, 0, 0, 0))  # noqa: Time of October change to CET
        now = utime.time()
        if now < HHMarch:               # we are before last sunday of march
            cet = utime.localtime(now + 3600)  # CET:  UTC+1H
        elif now < HHOctober:           # we are before last sunday of october
            cet = utime.localtime(now + 7200)  # CEST: UTC+2H
        else:                            # we are after last sunday of october
            cet = utime.localtime(now + 3600)  # CET:  UTC+1H
        return cet

    def get_time(self, host='pool.ntp.org'):
        """ Retrieve the current time/date"""
        try:
            s = None
            NTP_QUERY = bytearray(48)
            NTP_QUERY[0] = 0x1b
            addr = socket.getaddrinfo(host, 123)[0][-1]
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1)
            s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
            s.close()
            val = struct.unpack("!I", msg[40:44])[0]
            return val - self.NTP_DELTA
        finally:
            # Close the socket
            if s:
                s.close()

    def set_time(self):
        """ There's currently no timezone support in MicroPython, so
        utime.localtime() will return UTC time (as if it was .gmtime())
        """
        t = self.get_time()
        import machine
        tm = utime.localtime(t)
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        machine.RTC().datetime(tm)
