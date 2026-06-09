import os
import shutil
import stat

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

target_path = "/Users/cashify/Desktop/jf_bot_deploy/websitengga/.git"
if os.path.exists(target_path):
    print(f"Deleting {target_path}...")
    shutil.rmtree(target_path, onerror=remove_readonly)
    print("Deleted successfully.")
else:
    print("Path does not exist.")
