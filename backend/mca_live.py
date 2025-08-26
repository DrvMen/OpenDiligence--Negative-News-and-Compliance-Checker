# mca_live.py
from playwright.sync_api import sync_playwright
from time import sleep
from datetime import datetime


def fetch_mca_live(query: str, timeout_sec: int = 180):
    """
    Opens MCA public search in a browser, lets the user solve CAPTCHA,
    then extracts the visible results.

    Returns a list of {source, title, link, description, pubDate, isNegative}
    NOTE: We DO NOT bypass CAPTCHA. The user must solve it in the opened window.
    """

    records = []

    # We will use "Find CIN" (name search) which redirects to a result table after captcha.
    # If MCA changes layout, adjust the selectors below.
    with sync_playwright() as p:
        # show window so user can complete CAPTCHA
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            # 1) Go to "Find CIN" page (name search)
            page.goto("https://www.mca.gov.in/mcafoportal/findCIN.do",
                      wait_until="load")

            # 2) Type the query into the "Company Name" field if present
            # Common name field ids on MCA vary; try a couple
            name_input_candidates = ["companyName",
                                     "companyname", "cmpName", "name"]
            name_box = None
            for sel in name_input_candidates:
                try:
                    name_box = page.locator(f'input[name="{sel}"]')
                    if name_box.count() > 0:
                        break
                except:
                    continue

            if name_box and name_box.count() > 0:
                name_box.first.fill(query)

            # 3) Ask user to solve CAPTCHA & submit
            # We look for a submit button; on MCA it’s often “Find CIN” or “Search”
            # We’ll wait up to timeout_sec for the results table / list to appear
            page.bring_to_front()
            page.evaluate(
                "alert('MCA search opened. Please complete the CAPTCHA and click Search. I will auto-collect results after that.')")

            # 4) Wait for results – common patterns:
            #   - A table with company rows/links
            #   - A list of anchor tags linking to Master Data pages
            # We poll for known selectors.
            selectors_to_watch = [
                "table",                        # generic table
                "table tbody tr",               # rows
                # direct Master Data links
                "a[href*='viewCompanyMasterData.do']",
                "a[href*='LLPMaster']",         # LLP master data
                "div#results",                  # generic results container
            ]

            found = False
            elapsed = 0
            while elapsed < timeout_sec and not found:
                for sel in selectors_to_watch:
                    try:
                        if page.locator(sel).count() > 0:
                            found = True
                            break
                    except:
                        pass
                if not found:
                    sleep(2)
                    elapsed += 2

            if not found:
                browser.close()
                return [{
                    "source": "MCA",
                    "title": f"MCA search timed out (no results detected for: {query})",
                    "link": "https://www.mca.gov.in/mcafoportal/findCIN.do",
                    "description": "Open link and complete CAPTCHA manually, then try again.",
                    "pubDate": datetime.today().strftime("%Y-%m-%d"),
                    "isNegative": False
                }]

            # 5) Extract results (best-effort, resilient to layout differences)
            links = page.locator("a")
            count = links.count()
            seen = set()
            for i in range(min(count, 200)):
                try:
                    a = links.nth(i)
                    href = a.get_attribute("href") or ""
                    text = a.inner_text().strip()
                    if not href or not text:
                        continue

                    # We care about links that look like Master Data pages or company profile pages
                    if ("viewCompanyMasterData.do" in href or
                        "LLPMaster" in href or
                        "company" in text.lower() or
                            "llp" in text.lower()):

                        # Full URL where needed
                        if href.startswith("/"):
                            full = "https://www.mca.gov.in" + href
                        elif href.startswith("http"):
                            full = href
                        else:
                            full = "https://www.mca.gov.in/" + href

                        key = (text, full)
                        if key in seen:
                            continue
                        seen.add(key)

                        records.append({
                            "source": "MCA",
                            "title": text,
                            "link": full,
                            "description": "MCA master data / company details",
                            "pubDate": datetime.today().strftime("%Y-%m-%d"),
                            # We don’t assume negative; MCA is official registry.
                            # Frontend/keyword layer can flag if insolvency/strike-off is detected on the target page.
                            "isNegative": False
                        })
                except:
                    continue

        finally:
            # Keep the browser open a moment for user visibility, then close.
            try:
                sleep(2)
                browser.close()
            except:
                pass

    # If nothing extracted, still return a direct link so user can check manually
    if not records:
        records.append({
            "source": "MCA",
            "title": f"Open MCA search for: {query}",
            "link": "https://www.mca.gov.in/mcafoportal/findCIN.do",
            "description": "Complete CAPTCHA and search manually.",
            "pubDate": datetime.today().strftime("%Y-%m-%d"),
            "isNegative": False
        })
    return records
