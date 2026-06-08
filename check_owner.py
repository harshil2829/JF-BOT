import os
import stat

paths = [
    "/Users/cashify/Desktop/jf_bot_deploy",
    "/Users/cashify/Desktop/jf_bot_deploy/.git",
    "/Users/cashify/Desktop/jf_bot_deploy/websitengga",
    "/Users/cashify/Desktop/jf_bot_deploy/websitengga/.git"
]

for p in paths:
    if os.path.exists(p):
        st = os.stat(p)
        print(f"Path: {p}")
        print(f"  Owner UID: {st.st_uid}, GID: {st.st_gid}")
        print(f"  Permissions: {oct(st.st_mode)}")
    else:
        print(f"Path: {p} does not exist")
