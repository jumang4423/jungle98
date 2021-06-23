import spidev

spi = spidev.SpiDev()
spi.open(0,0)

def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    return ((r[1] & 3) << 8) + r[2]