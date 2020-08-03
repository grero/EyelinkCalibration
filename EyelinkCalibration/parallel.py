from ctypes import windll
p = windll.inpout32
addr = 0xD050
p.Inp32(addr)  # default 255(all high) on my pc
p.Out32(addr, 0)  # put all low on port 2-9
p.Out32(addr+2, 0)  # set the strobe pin; first bit
p.Out32(addr+2, 1)  # set the strobe pin; first bit
