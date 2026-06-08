import os

src = "/Users/cashify/Desktop/jf_bot_deploy/websitengga/.git"
dst = "/Users/cashify/Desktop/jf_bot_deploy/websitengga/git-backup"

try:
    if os.path.exists(src):
        os.rename(src, dst)
        print("Success! Renamed nested .git to git-backup")
    else:
        print("Source path does not exist.")
except Exception as e:
    print(f"Rename failed: {e}")
