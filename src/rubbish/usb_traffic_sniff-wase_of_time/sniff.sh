# script for sniffing usb traffic to parse apdu commands
# ARGS:
# 		NAME of file to create with APDU OUTPUT

# Need root previliages!
echo '	*** RUN WITH SUDO ****'
echo '*** THIS SCRIPT HAS TO BE KILLED -- USE CTRL+C ***'

# need usbmon module loaded
modprobe usbmon

# 1st locate the usb bus and device id using the output of lsusb
# save bus -> bus.out
# save deviceid -> id.out
lsusb | ./locate_bus_id.py

bus_num=$(<bus.out)
#echo $bus_folder


# start outputting the contents of usbmon
# pipe it into python script for parsing
# have the python script save the parsed outputs
#tshark -i usbmon$bus_num -w /home/nsaadouni/year_4/large_practicals/honours_project/git/src/usb_traffic_sniff/tmp/out.pcap
tshark -x -r out.pcap > out2.out
#cat /dev/usbmon$bus_num > ./tmp/$1.pcap
#| ./usb_traffic_parser.py $1

#cat /sys/kernel/debug/usb/usbmon/$bus_folder 