import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk


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


class Application(tk.Frame):
    def __init__(self, master=None, humble_bundles=None):
        super().__init__(master)
        self.humble_details = humble_bundles
        self.pack()
        self.humble_menu()
        self.dt_frame = tk.Frame()
        self.dt_frame.pack()

    def humble_menu(self):
        hb_menu = tk.Menu(self.master)
        self.master.config(menu=hb_menu)
        humble_list = tk.Menu(hb_menu, tearoff=False)
        hb_menu.add_cascade(label="Bundles", menu=humble_list)
        for title in self.humble_details:
            humble_list.add_command(label=title["humble_title"],
                                    command=lambda x=title["humble_title"]: self.show_bundle(x))
        humble_list.add_command(label="Exit", command=self.quit)

    def details_frame(self, bundle_index):
        for bundle in self.humble_details:
            if bundle["humble_title"] == bundle_index:
                for tier in {i: bundle[i] for i in bundle if i != "humble_title"}:
                    group = tk.LabelFrame(self.dt_frame, text=bundle[tier]["tier_name"])
                    group.pack(fill="both", expand="yes")
                    for item in bundle[tier]["tier_items"]:
                        w = tk.Label(group, text=item)
                        w.pack()

    def erase_frame(self):
        for widget in self.dt_frame.winfo_children():
            widget.destroy()

    def show_bundle(self, bundle):
        self.erase_frame()
        self.details_frame(bundle)


home_url = "https://www.humblebundle.com"
site_data = HumbleData(home_url)
humble_bundle = site_data.bundle_details()
root = tk.Tk()
root.geometry("700x960")
root.resizable(False, False)
root.title("Humble Bundle Scrapper")
app = Application(master=root, humble_bundles=humble_bundle)
app.mainloop()
