#!/usr/bin/env python3
#
# Copyright (C) 2016 The CyanogenMod Project
# Copyright (C) 2017-2020 The LineageOS Project
#
# Modified to update SHA1 for all proprietary blobs
#

import os
import sys
from hashlib import sha1

device = 'X01BD'
vendor = 'asus'

script_dir = os.path.dirname(os.path.abspath(__file__))
prop_file = os.path.join(script_dir, 'proprietary-files.txt')
vendor_path = os.path.normpath(
    os.path.join(script_dir, '../../../vendor', vendor, device, 'proprietary')
)

with open(prop_file, 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()


def sha1sum(path):
    h = sha1()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def cleanup():
    for index, line in enumerate(lines):
        if not line or line.startswith('#') or '|' not in line:
            continue
        lines[index] = line.split('|', 1)[0]


def resolve_blob_path(entry_without_hash):
    # Examples:
    # path
    # path;SYMLINK=...
    # src:dst
    # -path
    # -src:dst;MODULE_SUFFIX=_vendor

    file_spec = entry_without_hash.split(';', 1)[0]

    if file_spec.startswith('-'):
        file_spec = file_spec[1:]

    candidates = []
    if ':' in file_spec:
        src, dst = file_spec.split(':', 1)
        candidates.append(src)
        candidates.append(dst)
    else:
        candidates.append(file_spec)

    for rel_path in candidates:
        full_path = os.path.join(vendor_path, rel_path)
        if os.path.isfile(full_path):
            return full_path, rel_path

    return None, candidates[0]


def update():
    for index, line in enumerate(lines):
        if not line or line.startswith('#'):
            continue

        entry_without_hash = line.split('|', 1)[0]
        full_path, shown_path = resolve_blob_path(entry_without_hash)

        if full_path is None:
            print(f'[MISS] {shown_path}')
            continue

        digest = sha1sum(full_path)
        lines[index] = f'{entry_without_hash}|{digest}'
        print(f'[ OK ] {shown_path}')


if len(sys.argv) == 2 and sys.argv[1] == '-c':
    cleanup()
else:
    update()

with open(prop_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
