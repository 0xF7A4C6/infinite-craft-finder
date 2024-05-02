import tls_client, json, csv, os, time, threading


__storage__ = json.load(
    open("./local_storage.json", "r+", encoding="utf-8", errors="ignore")
)

__proxy__ = "http://user:pass@ip:port"
__max_thread__ = 300


class InfiniteCraft:
    def __init__(self):
        self.cookies = {
            "__cf_bm": "t_wvZOzlP.oxkObqhZnHH3QKr_KNPSHzx.TaJd5Mkdo-1714597060-1.0.1.1-Hg31uiRQpIkkDnf5Z95HIuAWB3rOT4xdO1AIEsOJfLkBPbP6otXS6y6vqOUbtlKj1uKDCzEziEEfxFOGhBhLJA",
            "cf_clearance": "pLbfZ3pXP6jX9H7DgdtZXEtZfpyGZsWYt7JO4Ldn_eA-1714597266-1.0.1.1-o6M0TuA8KKPvf7MKCtBxN6IlSVwmVHD4oJrQyNAUugh3C2agmu8bC6pMNiLnDiJA4iVVZZd8THYTm_o85euPCA",
        }

        self.headers = {
            "accept": "*/*",
            "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "if-modified-since": "Mon, 29 Apr 2024 19:09:14 GMT",
            "priority": "u=1, i",
            "referer": "https://neal.fun/infinite-craft/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        }

        self.csv_file = "./tested_crafts.csv"

    def load_tested_crafts(self):
        tested_crafts = set()

        if os.path.exists(self.csv_file):
            with open(self.csv_file, "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    first, second = row
                    tested_crafts.add((first, second))

        return tested_crafts

    def save_tested_craft(self, first, second):
        with open(self.csv_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([first, second])

    def discover(self, first: str, second: str):
        while True:
            try:
                params = {
                    "first": first,
                    "second": second,
                }

                session = tls_client.Session(
                    client_identifier="chrome112",
                    random_tls_extension_order=True,
                )

                resp = session.get(
                    "https://neal.fun/api/infinite-craft/pair",
                    params=params,
                    cookies=self.cookies,
                    headers=self.headers,
                    proxy=__proxy__,
                ).json()

                return resp
            except:
                pass

    def look(self, f_i, s_i, s_len, first_element: str, second_element: str):
        craft = self.discover(
            first=first_element["text"],
            second=second_element["text"],
        )

        self.save_tested_craft(
            first=first_element["text"],
            second=second_element["text"],
        )

        print(
            f'[{f_i}/{s_len} > {s_i}/{s_len}] [{craft["isNew"]}]: {first_element["text"]} + {second_element["text"]} = {craft["result"]}'
        )

        if not self.check_element_by_emoji(craft["result"]):
            print(f'[+] Discovered: {craft["result"]}')

            __storage__["elements"].append(
                {
                    "text": craft["result"],
                    "emoji": craft["emoji"],
                    "discovered": craft["isNew"],
                }
            )

            with open("./local_storage.json", "w", encoding="utf-8") as f:
                json.dump(__storage__, f, indent=4)

    def check_element_by_emoji(self, emoji_name):
        for element in __storage__["elements"]:
            if element["text"] == emoji_name:
                return True

        return False

    def testCraft(self):
        tested_crafts = self.load_tested_crafts()

        f_i = 0
        for first_element in __storage__["elements"]:
            f_i += 1
            s_i = 0
            for second_element in __storage__["elements"]:
                s_i += 1

                if (first_element["text"], second_element["text"]) in tested_crafts:
                    continue

                while threading.active_count() > __max_thread__:
                    time.sleep(0.5)

                threading.Thread(
                    target=self.look,
                    args=[
                        f_i,
                        s_i,
                        len(__storage__["elements"]),
                        first_element,
                        second_element,
                    ],
                ).start()

    def run(self):
        while True:
            self.testCraft()


if __name__ == "__main__":
    InfiniteCraft().run()
