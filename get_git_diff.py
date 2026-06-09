import subprocess

try:
    res = subprocess.run(
        ["git", "diff", "websitengga/src/app/products/ProductsClient.js"],
        cwd="/Users/cashify/Desktop/jf_bot_deploy",
        capture_output=True,
        text=True
    )
    print("Git Diff stdout:")
    print(res.stdout)
    print("Git Diff stderr:")
    print(res.stderr)
    
    status_res = subprocess.run(
        ["git", "status"],
        cwd="/Users/cashify/Desktop/jf_bot_deploy",
        capture_output=True,
        text=True
    )
    print("Git Status stdout:")
    print(status_res.stdout)
    print("Git Status stderr:")
    print(status_res.stderr)
except Exception as e:
    print(f"Error running git: {e}")
