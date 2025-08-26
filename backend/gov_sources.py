import requests
from bs4 import BeautifulSoup
from datetime import datetime


# ----------------- SEBI -----------------
def fetch_sebi_notices(query):
    url = "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=3&ssid=15&smid=0"
    results = []
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select(".table table tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                title = cols[1].get_text(strip=True)
                link = cols[1].find("a")["href"] if cols[1].find("a") else url
                date_str = cols[0].get_text(strip=True)

                if query.lower() in title.lower():
                    results.append({
                        "title": title,
                        "link": link,
                        "pubDate": date_str,
                        "source": "SEBI"
                    })
    except Exception as e:
        print("❌ Error fetching SEBI notices:", e)
    return results


# ----------------- CBI -----------------
def fetch_cbi_press_releases(query):
    url = "https://cbi.gov.in/press-releases"
    results = []
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(".views-row")

        for item in items:
            title_tag = item.find("a")
            date_tag = item.find("span", class_="date-display-single")
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            link = "https://cbi.gov.in" + title_tag["href"]
            date_str = date_tag.get_text(
                strip=True) if date_tag else datetime.today().strftime("%Y-%m-%d")

            if query.lower() in title.lower():
                results.append({
                    "title": title,
                    "link": link,
                    "pubDate": date_str,
                    "source": "CBI"
                })
    except Exception as e:
        print("❌ Error fetching CBI releases:", e)
    return results


# ----------------- RBI Enforcement -----------------
def fetch_rbi_enforcement(query):
    url = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx"
    results = []
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select("a")

        for item in items:
            title = item.get_text(strip=True)
            link = "https://www.rbi.org.in" + \
                item["href"] if item.has_attr("href") else url

            if query.lower() in title.lower():
                results.append({
                    "title": title,
                    "link": link,
                    "pubDate": datetime.today().strftime("%Y-%m-%d"),
                    "source": "RBI"
                })
    except Exception as e:
        print("❌ Error fetching RBI enforcement:", e)
    return results


# ----------------- MCA (Insolvency/Struck-off Companies) -----------------
def fetch_mca_notices(query):
    url = "https://www.mca.gov.in/bin/dms/getdocument?mds=fakeURL"
    # NOTE: MCA doesn’t expose simple HTML like SEBI/CBI.
    # Real data is behind CAPTCHAs.
    # Here we simulate via RSS-style scraping from MCA news feed pages.

    results = []
    try:
        res = requests.get(
            "https://www.mca.gov.in/content/mca/global/en/news-updates.html", timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select("a")

        for item in items:
            title = item.get_text(strip=True)
            link = "https://www.mca.gov.in" + \
                item["href"] if item.has_attr("href") else url

            if query.lower() in title.lower():
                results.append({
                    "title": title,
                    "link": link,
                    "pubDate": datetime.today().strftime("%Y-%m-%d"),
                    "source": "MCA"
                })
    except Exception as e:
        print("❌ Error fetching MCA notices:", e)
    return results


# ----------------- AGGREGATOR -----------------
def fetch_gov_sources(query):
    results = []
    results.extend(fetch_sebi_notices(query))
    results.extend(fetch_cbi_press_releases(query))
    results.extend(fetch_rbi_enforcement(query))
    results.extend(fetch_mca_notices(query))
    return results
