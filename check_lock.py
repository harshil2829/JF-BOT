import os

lock_path = "/Users/cashify/Desktop/jf_bot_deploy/.git/index.lock"
if os.path.exists(lock_path):
    print(f"Found lock file: {lock_path}")
    try:
        os.remove(lock_path)
        print("Successfully removed index.lock")
    except Exception as e:
        print(f"Error removing lock: {e}")
else:
    print("No lock file found.")

# Also list files in .git to see what is there
try:
    files = os.listdir("/Users/cashify/Desktop/jf_bot_deploy/.git")
    print("Files in .git:", files)
except Exception as e:
    print(f"Error listing .git: {e}")
