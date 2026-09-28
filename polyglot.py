#!/usr/bin/env python3
"""Compatibility entry. Native16 supersedes the historical v14 companions."""
import sys
from datetime import datetime, timezone
import native_course

def main():
    args=sys.argv[1:]
    if args and args[0]=='verify':
        args=[x for x in args if x!='--require-rust']
    if args and args[0] in ['run','verify','compare','test','build'] and '--output' not in args:
        args += ['--output','my_work/native-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')]
    return native_course.main(args)
if __name__=='__main__':raise SystemExit(main())
