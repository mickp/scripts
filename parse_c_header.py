import os
import re
import sys


# === Parse defines and enums from C header file. ===
fh = open(sys.argv[1], 'r')
while True:
    line = fh.readline()
    if not line: break
    if any([re.match(pattern, line) for pattern in [
        r'^\s*\/\*.*', # /* comments
        r'^\s*#ifndef .*', # #ifndef lines
        r'^\s*#ifdef .*',  # #ifndef lines
        r'^\s*#if .*',  # #if lines
        r'^\s*#endif.*',  # #endif lines
        r'^\s*$', # blank lines
        ]]):
        continue
    # #define flag
    if re.match(r'^\s*#define\s+\w+\s?$', line):
       continue
    # #define name value
    match = re.match(r'^\s*#define\s*(\w+)\s+(\w+)\s+(\/\*)?', line)
    if match:
        name = match.groups()[0]
        value = eval(match.groups()[1])
        globals()[name] = value
        print("%s = %s" % (name, value))
        continue
    # #define name (expr)
    match = re.match(r'^\s*#define\s*(\w+)\s+(\(.*\))', line) # #define name (expr)
    if match:
        name = match.groups()[0]
        value = eval(match.groups()[1])
        globals()[name] = value
        print("%s = %s" % (name, value))
        continue
    # #typedef enum
    match = re.match(r'^\s*typedef enum\s*(\w+)?', line)
    if match:
        tag = match.groups()[0]
        globals()[tag] = {}
        line = fh.readline()
        while not re.match(r'^.*{', line):
            line = fh.readline()
        count = 0
        while not re.match(r'^.*}', line):
            match = re.match(r'^(\s*{\s*)?\s*(\w+)(\s*=\s*(\w+))?', line)
            line = fh.readline()
            if not match:
                continue
            null, name, null, value = match.groups()
            if not value:
                # No value assigned in header file.
                value = count
                count += 1
            else:
                value = eval(value)
                # value may just be an initializer
                count = value+1
            globals()[name] = value
            globals()[tag][value] = name
            print("%s = %s" % (name, value))
        # Get the enum name.
        match = re.match(r'^.*}\s*((\w+)?;)?', line)
        name = match.groups()[-1]
        if not name:
            line = fh.readline()
            match = re.match(r'^\s*(\w+)?;?', line)
            if not match.groups()[0]:
                raise Exception('Error parsing %s: enum name not found for tag %s.'
                                  % (_HEADER, tag))
            else:
                name = match.groups()[0]
        if name != tag:
            globals()[name] = globals()[tag]
fh.close()