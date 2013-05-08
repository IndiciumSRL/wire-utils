import os
import sys
from datetime import *
from docopt import docopt
import ESL

def main(args = None):
        """
        Debugger para logs R2 Khomp

        Usage:
        wirecli_r2_trace [--b=BOARD_ID] [--c=CHANNEL]
        wirecli_r2_trace --help

        Arguments:
        --b=BOARD_ID Permite obtener solo la salida para el canal BOARD_ID
        --c=CHANNEL Permite obtener solo la salida para el canal CHANNEL

        Options:
        --help  Show this screen.
        """

        arguments = docopt(main.__doc__)
        ch = arguments['--c']
        b = arguments['--b']
        fecha = str(datetime.today()).split(' ')
        hoy = fecha[0].replace('-','.')

        if ch is not None:
                try:
                        ch = int(arguments['--c'])
                except ValueError:
                        print 'Channel needs to be integer!'
                        sys.exit(1)
        if b is not None:
                try:
                        b = int(arguments['--b'])
                except ValueError:
                        print 'Board needs to be integer!'
                        sys.exit(1)

        c = ESL.ESLconnection('localhost', '8021', 'ClueCon')
        if not c.connected:
                print 'Could not connect to ESL. Is FreeSWITCH running?'
                sys.exit(1)

        ev = c.api('khomp', 'summary concise')
        if ev is None:
                print 'Failed checking boards'
                sys.exit(1)
        bids = []
        for board in ev.getBody().split('\n'):
                fields = board.split(';')
                try:
                        bid = int(fields[0])
                except ValueError:
                        continue
                if fields[1].startswith('EBS-E1'):
                        bids.append(bid)

        if b is not None and b not in bids:
                print 'Board %s not in system or not E1. Valid options are: %s' % (b, bids)
                sys.exit(1)



        if ch is None and b is None:
                com = "tail -f /var/log/khomp/%s/r2.log" % hoy
        elif ch is None:
                com = "tail -f /var/log/khomp/%s/r2.log | grep 'D%.2d'" % (hoy, b)
        elif b is None:
                com = "tail -f /var/log/khomp/%s/r2.log | grep 'C%.2d'" % (hoy, ch)
        else:
                com = "tail -f /var/log/khomp/%s/r2.log | grep 'D%.2d C%.2d'" % (hoy, b, ch)
        val = os.system(com)


if __name__ == '__main__':
        main(sys.argv)
