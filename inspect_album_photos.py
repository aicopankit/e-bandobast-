import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

photo_ids = ['54898660524', '54898649558', '54897552542', '54898418771', '54897552637', '54898650128']
for pid in photo_ids:
    url = f"https://www.flickr.com/photos/santnirankarimission/{pid}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            title = re.search(r'<title>(.*?)</title>', html)
            og_img = re.search(r'<meta property="og:image" content="([^"]+)"', html)
            print(f"Photo {pid}: {title.group(1) if title else 'N/A'}")
            if og_img:
                print(f"  Img: {og_img.group(1)}")
    except Exception as e:
        print(f"Photo {pid} failed: {e}")
