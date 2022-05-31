from serpapi import GoogleSearch
import requests

puppet_keywords = []
doll_keywords = []

with open('keywords.txt', 'r') as f:
    doll_keywords = f.read().split('\n')
i = 0
# for keyword in puppet_keywords:
#     params = {
#     "engine": "google",
#     "ijn": "0",
#     "q": keyword,
#     "google_domain": "google.com",
#     "tbm": "isch",
#     "api_key": "1443c6f87f16435b00caf956b83c4e4e710fc9066d0b535224cf0fde67f5235e"
#     }

#     search = GoogleSearch(params)
#     results = search.get_dict()
#     for image in results['images_results']:
#         try:
#             request = requests.get(image['original'], timeout=4, stream=True)

#             with open("puppet_imgs/" + "puppet_" + str(i) + ".jpg", 'wb') as fh:
#                 # Walk through the request response in chunks of 1024 * 1024 bytes, so 1MiB
#                 for chunk in request.iter_content(1024 * 1024):
#                     # Write the chunk to the file
#                     fh.write(chunk)
#                     # Optionally we can check here if the download is taking too long
#             i += 1
#             print(i)
#         except:
#             continue

for keyword in doll_keywords:
    params = {
    "engine": "google",
    "ijn": "0",
    "q": keyword,
    "google_domain": "google.com",
    "tbm": "isch",
    "api_key": "1443c6f87f16435b00caf956b83c4e4e710fc9066d0b535224cf0fde67f5235e"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    for image in results['images_results']:
        try:
            request = requests.get(image['original'], timeout=4, stream=True)

            with open("doll_imgs/" + "doll_" + str(i) + ".jpg", 'wb') as fh:
                # Walk through the request response in chunks of 1024 * 1024 bytes, so 1MiB
                for chunk in request.iter_content(1024 * 1024):
                    # Write the chunk to the file
                    fh.write(chunk)
                    # Optionally we can check here if the download is taking too long
            i += 1
            print(i)
        except:
            continue