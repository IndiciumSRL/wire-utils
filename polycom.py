#!/usr/bin/python2.6
from wirephone.model.meta import Session, Base
from wirephone.model import *
from sqlalchemy import create_engine
import sys, logging

FORMAT = '%(asctime)-15s %(lineno)s %(levelname)-8s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

log = logging.getLogger(__name__)

def init_model(engine):
        """Call me before using any of the tables or classes in the model"""
        Session.configure(bind=engine)

path = "/var/www/html/provision/"

ippbx = "10.50.51.205"

engine = create_engine("postgresql+psycopg2://postgres@127.0.0.1/wirephone")
init_model(engine)

contador = 0

while True:
        while True:
                print "Ingrese Interno"
                interno = raw_input("> ")
                try:
                        exten = Session.query(SofiaUser).filter(SofiaUser.name == unicode(interno)).one()
                except:
                        print "\nInterno no existe en la base de datos."
                        continue
                password = exten.params.get('password')
                if password is None:
                        print '\nInterno no tiene clave asignada.'
                        continue
                password = password.val
                print "Ingrese los ultimos 6 digitos de la MAC: (en minusuculas y sin \":\" El sistema autocompletara con 0004f2. Ej a ingresar: bb22cc )"
                MAC = raw_input("> ")
                MAC = '0004f2%s' % MAC
                print "\nMAC:    "+MAC
                print "Interno: ", interno
                print "La informacion es correcta? [s/n]"
                confirmacion = raw_input("> ")
                if confirmacion == "s":

                        contador+=1
                        #Crear archivos
                        #MAC.cfg
                        macfile = open (path+MAC+".cfg", "w")
                        macfile.write("<?xml version=\"1.0\" standalone=\"yes\"?>\n   <APPLICATION APP_FILE_PATH=\"sip.ld\" CONFIG_FILES=\"\" MISC_FILES=\"\" LOG_FILE_DIRECTORY=\"\" OVERRIDES_DIRECTORY=\"\" CONTACTS_DIRECTORY=\"\" LICENSE_DIRECTORY=\"\" USER_PROFILES_DIRECTORY=\"\" CALL_LISTS_DIRECTORY=\"\">\n   <APPLICATION_SPIP330 APP_FILE_PATH_SPIP330=\"2345-12200-001.sip.ld\" CONFIG_FILES_SPIP330=\"reg-basic-"+MAC+".cfg, sip-basic-"+MAC+".cfg, reg-advanced.cfg, sip-advanced.cfg, site.cfg\"/>\n   <APPLICATION_SPIP331 APP_FILE_PATH_SPIP331=\"2345-12365-001.sip.ld\" CONFIG_FILES_SPIP331=\"reg-basic-"+MAC+".cfg, sip-basic-"+MAC+".cfg, reg-advanced.cfg, sip-advanced.cfg, site.cfg\"/>\n</APPLICATION>")
                        macfile.close()

                        #REG-basic
                        regbasic = open (path+"reg-basic-"+MAC+".cfg","w")
                        regbasic.write("<?xml version=\"1.0\" standalone=\"yes\"?>\n<polycomConfig xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"polycomConfig.xsd\">\n  <call call.callsPerLineKey=\"24\">\n  </call>\n  <reg reg.1.address=\""+interno+"\" reg.1.displayName=\""+interno+"\" reg.1.auth.password=\""+password+"\" reg.1.auth.userId=\""+interno+"\" reg.1.label=\""+interno+"\" reg.1.outboundProxy.address=\""+ippbx+"\" reg.2.address=\"\" reg.2.auth.password=\"\" reg.2.auth.userId=\"\" reg.2.label=\"\" reg.2.outboundProxy.address=\"\">\n  </reg>\n</polycomConfig>")
                        regbasic.close()

                        #SIP-basic
                        sipbasic = open (path+"sip-basic-"+MAC+".cfg","w")
                        sipbasic.write("<?xml version=\"1.0\" standalone=\"yes\"?>\n<polycomConfig xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"polycomConfig.xsd\">\n  <msg>\n    <msg.mwi msg.mwi.1.callBackMode=\"registration\" msg.mwi.2.callBackMode=\"registration\">\n    </msg.mwi>\n  </msg>\n  <voIpProt>\n    <voIpProt.server voIpProt.server.1.address=\""+ippbx+"\" voIpProt.server.1.port=\"5060\" voIpProt.server.2.address=\"\" voIpProt.server.2.port=\"0\">\n    </voIpProt.server>\n    <voIpProt.SIP voIpProt.SIP.enable=\"1\">\n      <voIpProt.SIP.outboundProxy voIpProt.SIP.outboundProxy.address=\""+ippbx+"\">\n      </voIpProt.SIP.outboundProxy>\n    </voIpProt.SIP>\n  </voIpProt>\n</polycomConfig>")
                        sipbasic.close()

                        ##Fin crear archivos
                        break
                else:
                        print "Ingrese los datos nuevamente"

        print "Desea cargar otro dispositivo? [s/n]"
        otro = raw_input("> ")
        print "Archivos generados"
        print "Dispositivo numero "+str(contador)+" cargado"
        if otro == "n":
                break
        else:
                print "Nuevo dispositivo" 
