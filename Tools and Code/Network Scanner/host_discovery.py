from scapy.all import Ether, ARP, sr
eth = Ether()
arp = ARP()

eth.dst="ff:ff:ff:ff:ff:ff"

arp.pdst="10.30.147.1/24"

bcPckt = eth/arp

#bcPckt.show()

ans, unans = sr(bcPckt,timeout=5)

#ans . summary ( )
print("#"*30)
#unans. summary ( )

for snd, rcv in ans:
#rcv. show()
 print(rcv.psrc," : ",rcv.src)


