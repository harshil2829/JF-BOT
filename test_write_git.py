import os

test_path = "/Users/cashify/Desktop/jf_bot_deploy/.git/test_write.txt"
try:
    with open(test_path, "w") as f:
        f.write("test")
    print("Write success!")
    os.remove(test_path)
    print("Delete success!")
except Exception as e:
    print(f"Write failed: {e}")
