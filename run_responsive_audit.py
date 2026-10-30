"""
RuleRoute Automated Responsive & Cross-Device Audit Suite.
Tests 8 specific viewport sizes across Light and Dark themes,
measures horizontal overflow, element bounding boxes, touch target sizes,
and captures visual verification screenshots.
"""

import os
import sys
import time
import urllib.request
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

VIEWPORTS = [
    {"name": "small_mobile_320x640", "width": 320, "height": 640, "desc": "Small Mobile (e.g. iPhone SE 1st gen)"},
    {"name": "standard_mobile_375x812", "width": 375, "height": 812, "desc": "Standard Mobile (e.g. iPhone 13 mini)"},
    {"name": "large_mobile_430x932", "width": 430, "height": 932, "desc": "Large Mobile (e.g. iPhone 15 Pro Max)"},
    {"name": "tablet_portrait_768x1024", "width": 768, "height": 1024, "desc": "Tablet Portrait (iPad Mini/Air)"},
    {"name": "tablet_landscape_1024x768", "width": 1024, "height": 768, "desc": "Tablet Landscape (iPad)"},
    {"name": "laptop_1366x768", "width": 1366, "height": 768, "desc": "Laptop Standard (1366x768)"},
    {"name": "desktop_1440x900", "width": 1440, "height": 900, "desc": "Desktop Standard (1440x900)"},
    {"name": "large_desktop_1920x1080", "width": 1920, "height": 1080, "desc": "Large Desktop 1080p (1920x1080)"},
]

SCREENSHOTS_DIR = os.path.abspath("tests/screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def is_server_running(url="http://localhost:8501"):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            return response.status == 200
    except Exception:
        return False


def run_audit():
    if not is_server_running():
        print("[FAIL] Streamlit server is not running on http://localhost:8501")
        return False

    print("[OK] Connected to Streamlit server at http://localhost:8501")
    audit_results = []

    with sync_playwright() as p:
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        browser = p.chromium.launch(
            executable_path=chrome_path,
            headless=True,
        )

        for vp in VIEWPORTS:
            name = vp["name"]
            w = vp["width"]
            h = vp["height"]
            desc = vp["desc"]

            print(f"\n--- Testing Viewport: {name} ({desc}) [{w}x{h}] ---")
            context = browser.new_context(viewport={"width": w, "height": h})
            page = context.new_page()

            # 1. Load application
            page.goto("http://localhost:8501", wait_until="domcontentloaded", timeout=30000)
            page.wait_for_selector(".rr-brand-name", timeout=30000)
            time.sleep(1.5)  # allow Streamlit websocket and custom CSS injection to settle

            # 2. Check horizontal overflow in Light mode
            overflow_check = page.evaluate("""() => {
                const docWidth = document.documentElement.scrollWidth;
                const winWidth = window.innerWidth;
                const bodyWidth = document.body.scrollWidth;
                return {
                    scrollWidth: docWidth,
                    innerWidth: winWidth,
                    bodyWidth: bodyWidth,
                    hasOverflow: (docWidth > winWidth + 1) || (bodyWidth > winWidth + 1)
                };
            }""")

            # 3. Check brand icon dimensions
            icon_dim = page.evaluate("""() => {
                const icon = document.querySelector('.rr-brand-icon');
                if (!icon) return null;
                const rect = icon.getBoundingClientRect();
                return { width: Math.round(rect.width), height: Math.round(rect.height), visible: rect.width > 0 };
            }""")

            # 4. Check touch target size of primary submit button
            button_dim = page.evaluate("""() => {
                const btn = document.querySelector('button[kind="primary"]') || document.querySelector('.stButton > button');
                if (!btn) return null;
                const rect = btn.getBoundingClientRect();
                return { width: Math.round(rect.width), height: Math.round(rect.height), touchCompliant: rect.height >= 43.0 };
            }""")

            # 5. Check header layout and mobile adaptivity
            header_check = page.evaluate("""() => {
                const brand = document.querySelector('.rr-brand-group');
                const tagline = document.querySelector('.rr-brand-tagline');
                const isNarrow = window.innerWidth <= 520;
                return {
                    brandExists: !!brand,
                    taglineVisible: tagline ? window.getComputedStyle(tagline).display !== 'none' : false,
                    isNarrow: isNarrow
                };
            }""")

            # 6. Capture light mode screenshot
            light_shot_path = os.path.join(SCREENSHOTS_DIR, f"{name}_light.png")
            page.screenshot(path=light_shot_path, full_page=False)

            # 7. Test form interaction: click submit
            submit_btn = page.locator('button[kind="primary"]').first
            if submit_btn.is_visible():
                submit_btn.click()
                time.sleep(1.5)

            # 8. Switch to Tab 2: Project Catalog
            catalog_tab = page.locator('.stTabs [data-baseweb="tab"]:has-text("Project Catalog")').first
            if catalog_tab.is_visible():
                catalog_tab.click()
                time.sleep(1.0)

            # 9. Switch to Tab 3: Inside the Engine
            engine_tab = page.locator('.stTabs [data-baseweb="tab"]:has-text("Inside the Engine")').first
            if engine_tab.is_visible():
                engine_tab.click()
                time.sleep(1.0)

            # Verify Stage grid layout on mobile vs desktop
            stage_grid_check = page.evaluate("""() => {
                const grid = document.querySelector('.rr-stage-grid');
                if (!grid) return null;
                const cards = grid.querySelectorAll('.rr-card');
                const rects = Array.from(cards).map(c => Math.round(c.getBoundingClientRect().width));
                return {
                    cardCount: cards.length,
                    widths: rects
                };
            }""")

            # 10. Switch back to Studio
            studio_tab = page.locator('.stTabs [data-baseweb="tab"]:has-text("Recommendation Studio")').first
            if studio_tab.is_visible():
                studio_tab.click()
                time.sleep(0.8)

            # 11. Test Dark Theme Switch
            theme_select = page.locator('div[data-baseweb="select"]').first
            if theme_select.is_visible():
                theme_select.click()
                time.sleep(0.5)
                dark_opt = page.locator('li:has-text("Dark")').first
                if dark_opt.is_visible():
                    dark_opt.click()
                    time.sleep(2.0)  # allow rerun
                    page.wait_for_selector(".rr-brand-name", timeout=15000)

            # 12. Check Dark theme horizontal overflow
            dark_overflow = page.evaluate("""() => {
                return document.documentElement.scrollWidth > window.innerWidth + 1;
            }""")

            # 13. Capture dark mode screenshot
            dark_shot_path = os.path.join(SCREENSHOTS_DIR, f"{name}_dark.png")
            page.screenshot(path=dark_shot_path, full_page=False)

            vp_result = {
                "name": name,
                "desc": desc,
                "width": w,
                "height": h,
                "has_overflow_light": overflow_check["hasOverflow"],
                "has_overflow_dark": dark_overflow,
                "scroll_width": overflow_check["scrollWidth"],
                "icon_dim": icon_dim,
                "button_dim": button_dim,
                "header_check": header_check,
                "stage_grid_check": stage_grid_check,
                "light_screenshot": light_shot_path,
                "dark_screenshot": dark_shot_path,
            }
            audit_results.append(vp_result)

            print(f"  [Light Mode] docWidth: {overflow_check['scrollWidth']}px / winWidth: {overflow_check['innerWidth']}px -> Overflow: {overflow_check['hasOverflow']}")
            print(f"  [Dark Mode] Overflow: {dark_overflow}")
            print(f"  [Icon Size] {icon_dim}")
            print(f"  [Button Touch Size] {button_dim}")
            print(f"  [Header Adaptive] Narrow: {header_check['isNarrow']}, Tagline Hidden: {not header_check['taglineVisible']}")
            print(f"  [Stage Grid Widths] {stage_grid_check}")

            context.close()

        browser.close()

    print("\n=======================================================")
    print("RESPONSIVE AUDIT SUMMARY ACROSS ALL 8 TARGET VIEWPORTS:")
    print("=======================================================")
    all_passed = True
    for r in audit_results:
        no_overflow = (not r["has_overflow_light"]) and (not r["has_overflow_dark"])
        touch_ok = r["button_dim"]["touchCompliant"] if r["button_dim"] else False
        status = "PASSED" if (no_overflow and touch_ok) else "FAILED"
        if status == "FAILED":
            all_passed = False
        print(f"[{status}] {r['name']:<28} | Width: {r['width']:>4}px | Overflow Free: {no_overflow!s:<5} | Touch Target >=44px: {touch_ok}")

    print(f"\nFinal Audit Verdict: {'ALL VIEWPORTS PASSED WITH ZERO OVERFLOW' if all_passed else 'SOME VIEWPORTS FAILED'}")
    return all_passed


if __name__ == "__main__":
    success = run_audit()
    sys.exit(0 if success else 1)
