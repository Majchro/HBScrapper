import requests
from bs4 import BeautifulSoup
import re


class HumbleData:
    def __init__(self, url):
        self.home_url = url

    def bundles_url_list(self):
        request = requests.get(self.home_url)
        parsed_site = BeautifulSoup(request.text, "html.parser")
        site_array = []
        for i in re.split("\n", str(parsed_site)):
            site_array.append(i.strip())
        result = [i for i in site_array if i.startswith('var productTiles')]
        packages = re.findall(r"\"product_url\"\:\s\"(.*?)\"",
                              str(result[0]).split("[", 1)[-1][:-2])
        packages.remove("/monthly")
        return packages

    def bundle_details(self):
        bundle_url_list = self.bundles_url_list()
        bundles_details = []
        for url in bundle_url_list:
            request = requests.get("https://www.humblebundle.com" + url)
            parsed_site = BeautifulSoup(request.text, "html.parser")
            tiers_dict = {"humble_title": parsed_site.title.string.split(" (", 1)[0]}
            for tier_index, tier in enumerate(parsed_site.select(".dd-game-row")):
                tier_items = []
                for ti in tier.select(".dd-image-box-caption"):
                    tier_items.append(ti.get_text().strip())
                tiers_dict["tier" + str(tier_index)] = {
                    "tier_name": tier.select(".dd-header-headline")[0].text.strip(),
                    "tier_items": tier_items
                }
            bundles_details.append(tiers_dict)
        return bundles_details
        # for i in range(0, len(tiers_dict)):
        #     print(tiers_dict["tier" + str(i)]["tier_name"])
        #     for item in tiers_dict["tier" + str(i)]["tier_items"]:
        #         print("\t-" + item)


home_url = "https://www.humblebundle.com"
site_data = HumbleData(home_url)
humble_bundle = site_data.bundle_details()
for index, bundle in enumerate(humble_bundle):
    print(str(index+1)+" - "+bundle["humble_title"])
chosen_bundle = int(input("Choose bundle: "))
print(humble_bundle[chosen_bundle-1])
