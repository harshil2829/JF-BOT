import os
import subprocess
import shutil
import stat

target = "/Users/cashify/Desktop/jf_bot_deploy/websitengga/.git"

# Run chflags to unlock
try:
    print("Running chflags nouchg...")
    subprocess.run(["chflags", "-R", "nouchg", target], capture_output=True)
except Exception as e:
    print("chflags failed:", e)

# Run chmod to make everything writable
try:
    print("Modifying permissions recursively...")
    for root, dirs, files in os.walk(target):
        for d in dirs:
            os.chmod(os.path.join(root, d), stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)
        for f in files:
            os.chmod(os.path.join(root, f), stat.S_IWRITE | stat.S_IREAD)
except Exception as e:
    print("chmod failed:", e)

# Try deleting again
try:
    if os.path.exists(target):
        shutil.rmtree(target)
        print("Success! Nested .git deleted.")
    else:
        print("Path does not exist anymore.")
except Exception as e:
    print("shutil.rmtree failed:", e)
