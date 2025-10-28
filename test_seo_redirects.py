#!/usr/bin/env python3
"""
Test script to verify SEO redirect fixes are working correctly.
Run this after starting the Django development server.
NO EXTERNAL DEPENDENCIES REQUIRED - uses only Python standard library!
"""

import urllib.request
import urllib.error

# Base URL - change this for production testing
BASE_URL = "http://localhost:8000"
# Uncomment for production testing:
# BASE_URL = "https://www.infratex.com.au"

# Test cases: (old_url, expected_redirect_url, expected_status)
redirect_tests = [
    # Singular to plural redirects (should be 301)
    ("/products/geocell/", "/products/geocells/", 301),
    ("/products/geogrid/", "/products/geogrids/", 301),
    ("/products/geotextile/", "/products/geotextiles/", 301),
    ("/products/gcl/", "/products/gcls/", 301),
    ("/products/drainage-systems/", "/products/drainage/", 301),

    # Canonical URLs (should be 200)
    ("/products/geocells/", None, 200),
    ("/products/geogrids/", None, 200),
    ("/products/geotextiles/", None, 200),
    ("/products/gcls/", None, 200),
    ("/products/drainage/", None, 200),
]

def test_url(url, expected_redirect=None, expected_status=200):
    """Test a single URL for proper redirect/status."""
    import http.client
    from urllib.parse import urlparse

    parsed = urlparse(BASE_URL)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)

    # Use low-level http.client to avoid automatic redirect following
    if parsed.scheme == 'https':
        conn = http.client.HTTPSConnection(host, port)
    else:
        conn = http.client.HTTPConnection(host, port)

    try:
        # Make request without following redirects
        conn.request('GET', url)
        response = conn.getresponse()

        status_code = response.status

        # Get redirect location if present
        actual_redirect = None
        if status_code in [301, 302]:
            actual_redirect = response.getheader('Location')
            # Check if redirect matches expected
            if expected_redirect:
                if actual_redirect:
                    redirect_match = actual_redirect == expected_redirect or actual_redirect.endswith(expected_redirect)
                else:
                    redirect_match = False
            else:
                redirect_match = True
        else:
            redirect_match = True

        # Read response to clear buffer
        response.read()

        return {
            'success': status_code == expected_status and redirect_match,
            'status_code': status_code,
            'expected_status': expected_status,
            'actual_redirect': actual_redirect,
            'expected_redirect': expected_redirect
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Connection failed - is the Django server running? ({str(e)})'
        }
    finally:
        conn.close()

def run_tests():
    """Run all redirect tests."""
    print("\n" + "="*60)
    print("SEO Redirect Test Suite")
    print("="*60 + "\n")
    print(f"Testing against: {BASE_URL}\n")

    total_tests = len(redirect_tests)
    passed = 0
    failed = 0

    for url, expected_redirect, expected_status in redirect_tests:
        result = test_url(url, expected_redirect, expected_status)

        if 'error' in result:
            print(f"ERROR: {result['error']}")
            print(f"Please make sure Django server is running:")
            print(f"python manage.py runserver")
            return

        if result['success']:
            passed += 1
            status_text = "✓ PASS"
        else:
            failed += 1
            status_text = "✗ FAIL"

        print(f"{status_text}: {url}")

        if expected_status == 301:
            if result['success']:
                print(f"  → Correctly redirects to: {expected_redirect}")
            else:
                if result['status_code'] != 301:
                    print(f"  → Expected 301, got {result['status_code']}")
                else:
                    print(f"  → Expected redirect to: {expected_redirect}")
                    print(f"  → Actually redirects to: {result.get('actual_redirect', 'unknown')}")

        elif expected_status == 200:
            if result['success']:
                print(f"  → Correctly returns 200 (page exists)")
            else:
                print(f"  → Expected 200, got {result['status_code']}")

        print()

    # Summary
    print("="*60)
    if failed == 0:
        print(f"✓ All {total_tests} tests passed!")
        print("\nYour SEO redirects are working correctly!")
    else:
        print(f"Results: {passed} passed, {failed} failed")
        if BASE_URL.startswith("http://localhost"):
            print("\nNote: Make sure you've applied all the changes from products/views.py")
    print("="*60 + "\n")

def test_sitemap():
    """Test that sitemap only contains canonical URLs."""
    print("\nTesting Sitemap...")
    print("-"*40)

    sitemap_url = f"{BASE_URL}/sitemap.xml"

    try:
        response = urllib.request.urlopen(sitemap_url)
        content = response.read().decode('utf-8')

        # Check for bad URLs in sitemap
        bad_patterns = [
            '/products/geocell/',  # Should be geocells
            '/products/geogrid/',  # Should be geogrids
            '/products/geotextile/',  # Should be geotextiles
            '/products/gcl/',  # Should be gcls
            '/products/drainage-systems/',  # Should be drainage
        ]

        # Check for good URLs
        good_patterns = [
            '/products/geocells/',
            '/products/geogrids/',
            '/products/geotextiles/',
            '/products/gcls/',
            '/products/drainage/',
        ]

        issues = []
        found_good = []

        for pattern in bad_patterns:
            if pattern in content:
                issues.append(f"  ✗ Found bad URL in sitemap: {pattern}")

        for pattern in good_patterns:
            if pattern in content:
                found_good.append(f"  ✓ Found correct URL: {pattern}")
            else:
                issues.append(f"  ⚠ Missing expected URL: {pattern}")

        if issues:
            print("Issues found in sitemap:")
            for issue in issues:
                print(issue)

        if found_good:
            print("\nCorrect URLs in sitemap:")
            for good in found_good:
                print(good)

        if not issues:
            print("✓ Sitemap looks good - no duplicate URLs found!")

    except Exception as e:
        print(f"✗ Error testing sitemap: {e}")

    print()

def main():
    print("\n" + "="*60)
    print("Starting SEO Redirect Tests...")
    print(f"Testing against: {BASE_URL}")

    if BASE_URL.startswith("http://localhost"):
        print("\nMake sure Django server is running first!")
        print("Run in another terminal: python3 manage.py runserver")
        input("\nPress Enter to start tests...")

    run_tests()
    test_sitemap()

    print("Additional Manual Checks:")
    print("1. Check that product pages still load correctly")
    print("2. Verify navigation menu links go to plural URLs")
    print()

if __name__ == "__main__":
    main()