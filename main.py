import requests
from bs4 import BeautifulSoup
import re


def bundles_url_list(json_parse_site_url):
    request = requests.get(json_parse_site_url)
    parsed_site = BeautifulSoup(request.text, "html.parser")
    site_array = []
    for i in re.split("\n", str(parsed_site)):
        site_array.append(i.strip())
    result = [i for i in site_array if i.startswith('var productTiles')]
    packages = re.findall(r"\"product_url\"\:\s\"(.*?)\"",
                          str(result[0]).split("[", 1)[-1][:-2])
    packages.remove("/monthly")
    return packages


def humble_title(bundle_title_site_url):
    request = requests.get("https://www.humblebundle.com" + bundle_title_site_url)
    ht = BeautifulSoup(request.text, "html.parser")
    title = ht.title.string
    return title.split(" (", 1)[0]


def get_package(get_package_site_url):
    request = requests.get("https://www.humblebundle.com"+get_package_site_url)
    parsed_site = BeautifulSoup(request.text, "html.parser")
    tiers_dict = {}
    for index, tier in enumerate(parsed_site.select(".dd-game-row")):
        tier_items = []
        for ti in tier.select(".dd-image-box-caption"):
            tier_items.append(ti.get_text().strip())
        tiers_dict["tier" + str(index)] = {
            "tier_name": tier.select(".dd-header-headline")[0].text.strip(),
            "tier_items": tier_items
        }
    humble_title(get_package_site_url)
    print(humble_title(get_package_site_url))
    for i in range(0, len(tiers_dict)):
        print(tiers_dict["tier" + str(i)]["tier_name"])
        for item in tiers_dict["tier" + str(i)]["tier_items"]:
            print("\t-" + item)


home_url = "https://www.humblebundle.com"
available_bundles = bundles_url_list(home_url)
for index, bundle in enumerate(available_bundles):
    print(str(index+1)+" - "+humble_title(bundle))
chosen_bundle = int(input("Choose bundle: "))
get_package(available_bundles[chosen_bundle-1])
