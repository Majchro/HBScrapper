import requests
from bs4 import BeautifulSoup
import re

def site_list(home_url):
    request = requests.get(home_url)
    parsed_site = BeautifulSoup(request.text, "html.parser")
    site_array = []
    for i in re.split("\n", str(parsed_site)):
        site_array.append(i.strip())
    result = [i for i in site_array if i.startswith('var productTiles')]
    packages = re.findall(r"\"product_url\"\:\s\"(.*?)\"",
                                    str(result[0]).split("[", 1)[-1][:-2])
    packages.remove("/monthly")
    return packages


def get_package(site_url):
    req = requests.get("https://www.humblebundle.com"+site_url)

    parsed_site = BeautifulSoup(req.text, "html.parser")

    site_title = parsed_site.title.string
    tiers_dict = {}

    for index, tier in enumerate(parsed_site.select(".dd-game-row")):
        tier_items = []
        for ti in tier.select(".dd-image-box-caption"):
            tier_items.append(ti.get_text().strip())
        tiers_dict["tier" + str(index)] = {
            "tier_name": tier.select(".dd-header-headline")[0].text.strip(),
            "tier_items": tier_items
        }

    print(site_title)
    for i in range(0, len(tiers_dict)):
        print(tiers_dict["tier" + str(i)]["tier_name"])
        for item in tiers_dict["tier" + str(i)]["tier_items"]:
            print("\t-" + item)


home_url = "https://www.humblebundle.com"
available_bundles = site_list(home_url)
for index, bundle in enumerate(available_bundles):
    print(str(index+1)+" - "+bundle)

chosen_bundle = int(input("Choose bundle: "))
get_package(available_bundles[chosen_bundle-1])
