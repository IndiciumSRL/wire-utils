import sys
import os
import xml.etree.ElementTree as ET
import urllib
import shutil

def getfiles(dirpath):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a

def searchelement(element,p1,p2):
        try:
                if p2 is not 'x':
                        val = "\"" + root[p1][p2].find(element).text + "\""
                else:
                        val = "\"" + root[p1].find(element).text + "\""
        except:
                val = '\"\"'
        return val


#XML File to take information from
xml_dir = os.path.join('/usr/local','freeswitch1.5.1b/log/xml_cdr/2013-04-13-00-02-01')

#CSV File to create
csv = os.path.join('/root/fixcdr','csv/Master.csv.2013-04-14-00-02-01')

c = open(csv,'w+')

xmlfiles = getfiles(xml_dir)

for xml in xmlfiles:
        flag = True
        print "Archivo: " + os.path.join(xml_dir,xml)
        aleg = xml.split('_')
        print "LEG: " + aleg[0]
        try:
                tree = ET.parse(os.path.join(xml_dir,xml))
                root = tree.getroot()
        except:
                print "Llamada FAX T38"
                flag = False

        if flag:
                if aleg[0] == "a":
                        cid_name = searchelement('caller_id_name',3,1)
                        cid_number = searchelement('caller_id_number',3,1)
                        dst_number  = searchelement('destination_number',3,1)
                        b_uuid = searchelement('bridge_uuid',1,'x')
                else:
                        cid_name = searchelement('caller_id_name',2,0)
                        cid_number = searchelement('caller_id_number',2,0)
                        dst_number  = searchelement('destination_number',2,0)
                        b_uuid = '\"\"'

                orig_signal_bond = searchelement('originate_signal_bond',1,'x')
                sip_gw_name = searchelement('sip_gateway_name',1,'x')
                duration = searchelement('duration',1,'x')
                billsec =  searchelement('billsec',1,'x')
                hangup_cause = searchelement('hangup_cause',1,'x')
                uuid = searchelement('uuid',1,'x')
                read_codec = searchelement('read_codec',1,'x')
                write_codec  = searchelement('write_codec',1,'x')
                direction = searchelement('direction',0,'x')
                kbid  = searchelement('Khomp-Board-ID',1,'x')
                kcid = searchelement('Khomp-Channel-ID',1,'x')
                ksid = searchelement('Khomp-Serial-ID',1,'x')
                orig_leg_uuid = searchelement('originating_leg_uuid',1,'x')

                try:
                        s = root[1].find('start_stamp').text
                        start_stamp = "\"" + urllib.unquote_plus(s) + "\""
                except:
                        start_stamp = '\"\"'

                try:
                        a = root[1].find('answer_stamp').text
                        answer_stamp = "\"" + urllib.unquote_plus(a) + "\""
                except:
                        answer_stamp = '\"\"'

                try:
                        e = root[1].find('end_stamp').text
                        end_stamp = "\"" + urllib.unquote_plus(e) + "\""
                except:
                        end_stamp = '\"\"'


                line = [cid_name,cid_number,dst_number,orig_signal_bond,sip_gw_name,start_stamp,answer_stamp,end_stamp,duration,billsec,hangup_cause,uuid,b_uuid,read_codec,write_codec,direction,kbid,kcid,ksid,orig_leg_uuid+'\n']
                newline = ','.join(line)
                c.write(newline)
c.close()
