import urllib.request
import socket

# Check if port 3000 is listening
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
try:
    s.connect(('127.0.0.1', 3000))
    print("Port 3000 is OPEN!")
    s.close()
    
    # Try fetching products page
    try:
        response = urllib.request.urlopen("http://127.0.0.1:3000/products", timeout=3)
        html = response.read().decode('utf-8')
        print("Successfully fetched products page locally.")
        if "ProductModal" in html or "editData" in html or "Save Changes" in html:
            print("Modal code detected in local page!")
        else:
            print("Modal code NOT detected in local page.")
    except Exception as e:
        print(f"Error fetching page: {e}")
except Exception as e:
    print(f"Port 3000 is CLOSED: {e}")
