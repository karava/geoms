#!/usr/bin/env python3
"""
Quick test script to check SEO redirects on production site.
No Django required - just run this script!
"""

import requests
import sys

# Test against production
BASE_URL = "https://www.infratex.com.au"

def test_redirect(old_url, expected_redirect):
    """Test if a URL properly redirects."""
    full_url = BASE_URL + old_url

    try:
        response = requests.get(full_url, allow_redirects=False)

        if response.status_code == 301:
            location = response.headers.get('Location', '')
            # Handle both relative and absolute redirects
            if location == expected_redirect or location == BASE_URL + expected_redirect:
                return True, f"✓ {old_url} → {expected_redirect} (301)"
            else:
                return False, f"✗ {old_url} redirects to {location}, expected {expected_redirect}"
        else:
            return False, f"✗ {old_url} returns {response.status_code}, expected 301 redirect"
    except Exception as e:
        return False, f"✗ Error testing {old_url}: {e}"

def test_canonical(url):
    """Test if a canonical URL loads correctly."""
    full_url = BASE_URL + url

    try:
        response = requests.get(full_url, allow_redirects=False)

        if response.status_code == 200:
            return True, f"✓ {url} loads correctly (200)"
        else:
            return False, f"✗ {url} returns {response.status_code}, expected 200"
    except Exception as e:
        return False, f"✗ Error testing {url}: {e}"

def main():
    print(f"\n{'='*60}")
    print(f"Testing SEO Redirects on: {BASE_URL}")
    print(f"{'='*60}\n")

    all_passed = True

    # Test redirects
    print("Testing Redirects (Singular → Plural):")
    print("-" * 40)

    redirects = [
        ("/products/geocell/", "/products/geocells/"),
        ("/products/geogrid/", "/products/geogrids/"),
        ("/products/geotextile/", "/products/geotextiles/"),
        ("/products/gcl/", "/products/gcls/"),
        ("/products/drainage-systems/", "/products/drainage/"),
    ]

    for old, new in redirects:
        passed, message = test_redirect(old, new)
        print(message)
        if not passed:
            all_passed = False

    # Test canonical URLs
    print("\n\nTesting Canonical URLs (Should Load):")
    print("-" * 40)

    canonical = [
        "/products/geocells/",
        "/products/geogrids/",
        "/products/geotextiles/",
        "/products/gcls/",
        "/products/drainage/",
    ]

    for url in canonical:
        passed, message = test_canonical(url)
        print(message)
        if not passed:
            all_passed = False

    # Summary
    print(f"\n{'='*60}")
    if all_passed:
        print("✓ All tests passed! SEO fixes are working correctly.")
    else:
        print("✗ Some tests failed. Please check the implementation.")
    print(f"{'='*60}\n")

    # Additional recommendations
    print("Next Steps:")
    print("1. Check sitemap at: https://www.infratex.com.au/sitemap.xml")
    print("2. Submit to Google Search Console")
    print("3. Run full SEO audit in 24-48 hours")
    print()

if __name__ == "__main__":
    main()