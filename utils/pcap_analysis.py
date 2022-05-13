

from scapy.all import *
import  pandas as pd
from tld import get_tld
import matplotlib.pyplot as plt

filename = "weixin.pcapng"
pkts = rdpcap(filename)

fd = open(filename + ".txt", "w+", encoding='utf-8')
for pkt in pkts:
    #ptk.show()
    #print(type(pkt))
    #print(repr(type(pkt.payload['DNS'])))
    #print(get_tld("https://" + repr(pkt.payload['DNSQR'].qname.decode("utf-8"))[1:-2] + "/", as_object=True).fld)
    fd.write(repr(pkt.payload['DNSQR'].qname) + '\n')

s_raw = pd.Series([repr(pkt.payload['DNSQR'].qname.decode("utf-8"))[1:-2] for pkt in pkts]) 
print(s_raw)
s_raw.to_csv("weixin_raw.csv")

s = pd.Series([get_tld("https://" + repr(pkt.payload['DNSQR'].qname.decode("utf-8"))[1:-2] + "/", as_object=True).fld for pkt in pkts])
s_count = s.value_counts()
s_count = s_count[:10]
#print(s)

x = s_count.index
y = s_count.values
print(x)
print(y)

print(type(s_count))
#s_count.plot(kind='bar')
plt.xticks(rotation=45)
plt.title("douyin")
plt.bar(x, y)
for x,y in zip(x,y):
    plt.text(x, y, y, ha = 'center', va = 'bottom')

plt.show()
s_count.to_csv('weibo.csv')