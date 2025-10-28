# SEO Testing Guide

## Local Testing

### 1. Run the Test Script

First, install required packages:
```bash
pip install requests colorama
```

Then run the test script:
```bash
# Start Django server in one terminal
python manage.py runserver

# In another terminal, run the test
python test_seo_redirects.py
```

The script will test:
- ✅ All singular URLs redirect to plural (301)
- ✅ All plural URLs work correctly (200)
- ✅ Invalid URLs return 404
- ✅ Sitemap contains only canonical URLs

## Online Testing Tools (For Production)

### 1. Redirect Checkers

#### **Redirect Checker by SmallSEOTools**
- URL: https://smallseotools.com/redirect-checker/
- Test URLs:
  - `https://www.infratex.com.au/products/geocell/`
  - `https://www.infratex.com.au/products/geogrid/`
- Should show: 301 Permanent Redirect

#### **HTTP Status Code Checker**
- URL: https://httpstatus.io/
- Can test multiple URLs at once
- Paste all your old URLs and verify they return 301

### 2. Sitemap Validators

#### **XML Sitemap Validator**
- URL: https://www.xml-sitemaps.com/validate-xml-sitemap.html
- Enter: `https://www.infratex.com.au/sitemap.xml`
- Checks for:
  - Valid XML structure
  - Accessible URLs
  - No duplicate entries

#### **Google's Sitemap Test Tool**
- URL: Use Google Search Console
- Path: Indexing → Sitemaps → Add/Test sitemap
- Benefits: Shows exactly how Google sees your sitemap

### 3. Duplicate Content Checkers

#### **Siteliner**
- URL: https://www.siteliner.com/
- Enter: `https://www.infratex.com.au`
- Free scan up to 250 pages
- Shows:
  - Duplicate content percentage
  - Duplicate pages
  - Common content issues

#### **Screaming Frog SEO Spider** (Desktop App)
- URL: https://www.screamingfrog.co.uk/seo-spider/
- Free for up to 500 URLs
- Best for:
  - Finding all duplicate title tags
  - Identifying redirect chains
  - Checking canonical URLs

### 4. SEO Audit Tools

#### **Ubersuggest** (What you're already using)
- After implementing fixes, wait 24-48 hours
- Re-run site audit
- Compare results to previous audit

#### **Google PageSpeed Insights**
- URL: https://pagespeed.web.dev/
- Also checks for SEO issues
- Test your category pages:
  - `https://www.infratex.com.au/products/geocells/`
  - `https://www.infratex.com.au/products/geogrids/`

#### **SEO Site Checkup**
- URL: https://seositecheckup.com/
- Provides comprehensive SEO audit
- Free daily checks

### 5. Google Search Console (Most Important!)

After deploying:

1. **Submit Updated Sitemap**
   - Go to: Indexing → Sitemaps
   - Submit: `https://www.infratex.com.au/sitemap.xml`
   - Click "Request Indexing"

2. **Check Coverage Report** (After 3-5 days)
   - Go to: Indexing → Pages
   - Look for:
     - Duplicate pages (should decrease)
     - Redirect errors (should be none)
     - 404 errors (should be none from internal links)

3. **Use URL Inspection Tool**
   - Test old URLs: `https://www.infratex.com.au/products/geocell/`
   - Should show: "Page is not on Google: Redirected"
   - Test new URLs: `https://www.infratex.com.au/products/geocells/`
   - Should show: "URL is on Google"

## Testing Checklist

### Immediate Tests (Right After Deployment)

- [ ] Run local test script on production URL
- [ ] Check redirects with online redirect checker
- [ ] Validate sitemap with XML validator
- [ ] Submit updated sitemap to Google Search Console

### After 24-48 Hours

- [ ] Run Siteliner scan for duplicate content
- [ ] Check Google Search Console for crawl errors
- [ ] Re-run Ubersuggest site audit

### After 1 Week

- [ ] Check Google Search Console coverage report
- [ ] Monitor organic traffic in Google Analytics
- [ ] Review search rankings for category pages

## Quick Manual Tests

### Browser Test for Redirects
1. Open Chrome Developer Tools (F12)
2. Go to Network tab
3. Visit old URL: `https://www.infratex.com.au/products/geocell/`
4. Should see:
   - Status: 301
   - Location header: `/products/geocells/`

### Check Internal Links
1. Visit homepage
2. Hover over navigation menu
3. Check that all product category links point to plural URLs
4. Click each link to verify they work

### Test Product Pages
1. Visit a category page: `https://www.infratex.com.au/products/geocells/`
2. Click on any product
3. Verify product page loads correctly
4. Check breadcrumbs use correct category URL

## Expected Results

### Before Fix
- Ubersuggest shows duplicate URLs for each category
- Google indexes both singular and plural versions
- SEO value split between multiple URLs

### After Fix
- Only plural URLs in sitemap
- Singular URLs redirect with 301
- Google de-indexes singular URLs (takes 2-4 weeks)
- Improved rankings as duplicate penalty removed

## Monitoring Timeline

- **Day 1:** Redirects working, sitemap updated
- **Day 3-5:** Google starts crawling new structure
- **Week 1:** Old URLs marked as redirected in Search Console
- **Week 2-3:** Duplicate content warnings decrease
- **Month 1:** Rankings start to improve
- **Month 2:** Full SEO benefit realized

## Troubleshooting

### If redirects aren't working:
- Check Django DEBUG mode is False in production
- Verify middleware is loaded correctly
- Check for conflicting URL patterns

### If duplicates persist:
- Check for hardcoded URLs in templates
- Review canonical tags in HTML
- Look for external backlinks to old URLs

### If 404 errors appear:
- Check all internal links are updated
- Review product detail URL generation
- Verify category slug mappings