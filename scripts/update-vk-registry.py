# updates the vulkan API registry file vk.xml to the latest available API version

import urllib.request

# requested version
tag = input("Vulkan API version (default is latest): ")
if tag == "": 
  tag = "main"
elif tag[0] != "v":
   tag = "v" + tag

# URL of the raw file in the repository
url = f"https://raw.githubusercontent.com/KhronosGroup/Vulkan-Docs/{tag}/xml/vk.xml"

# Save the file locally
output_file = "vk.xml"

try:
    urllib.request.urlretrieve(url, output_file)
    print(f"File downloaded successfully!")
except Exception as e:
    print(f"error : {e}")
    exit(1)
