# SEO Issues Fix Plan for Infratex Website

## Current SEO Issues Analysis

### Critical Issues Found

#### 1. Duplicate Category URLs (High Priority)
The site currently serves identical content on multiple URLs:
- `/products/geogrid/` and `/products/geogrids/`
- `/products/geocell/` and `/products/geocells/`
- `/products/geotextile/` and `/products/geotextiles/`
- `/products/gcl/` and `/products/gcls/`
- `/products/drainage/` and `/products/drainage-systems/`

**Impact:** Google sees these as duplicate pages, diluting SEO value and potentially causing ranking penalties.

#### 2. Duplicate Product Pages
All GCL products appear under both URL patterns:
- `/products/gcl/InfraClay3300G/`
- `/products/gcls/InfraClay3300G/`

#### 3. Missing H1 Tags
Over 100 pages lack H1 headings, including:
- Homepage
- All application pages
- All knowledge base pages
- Product category pages

#### 4. SEO-Unfriendly URLs
URLs using underscores instead of hyphens:
- `/applications/civil_construction/`
- `/applications/drainage_solutions/`
- `/applications/erosion_control/`
- etc.

#### 5. Duplicate Meta Descriptions
Multiple product pages share identical meta descriptions.

## Implementation Plan

### Phase 1: Fix Duplicate Category URLs (Immediate)

#### Step 1.1: Implement 301 Redirects
**File to modify:** `products/views.py`

Current problematic code (lines 26-37):
```python
slug_to_category = {
    'geocells': 'geocell',
    'gcls': 'gcl',
    'geotextiles': 'geotextile',
    'geogrids': 'geogrid',
    'drainage-systems': 'drainage',
}

if category_slug in slug_to_category:
    category_slug = slug_to_category[category_slug]
```

**Change to:**
```python
from django.shortcuts import redirect

def CategoryListView(request, category_slug):
    # Redirect plural/legacy URLs to canonical singular forms
    slug_redirects = {
        'geocells': 'geocell',
        'gcls': 'gcl',
        'geotextiles': 'geotextile',
        'geogrids': 'geogrid',
        'drainage-systems': 'drainage',
    }

    if category_slug in slug_redirects:
        # 301 permanent redirect to canonical URL
        return redirect('products:product_category',
                       category_slug=slug_redirects[category_slug],
                       permanent=True)

    # Continue with normal view logic for valid singular slugs...
```

#### Step 1.2: Update Internal Links
Search and replace all internal links to use singular forms:
- Update templates in `templates/`
- Update any hardcoded links in views
- Update `data/products.json` if needed

### Phase 2: Add H1 Tags (High Priority)

#### Files to modify:
1. **Homepage** - `templates/index.html`
   - Add: `<h1>Geosynthetics Solutions for Australian Infrastructure</h1>`

2. **Product Category Pages** - `templates/category_list.html`
   - Change H2 to H1 for category title

3. **Product Detail Pages** - `templates/product_detail.html`
   - Add H1 with product title

4. **Knowledge Base** - `knowledge_base/templates/`
   - Add H1 to technical guides and case studies

### Phase 3: Fix URL Structure

#### Step 3.1: Create Redirect Middleware
**New file:** `core/redirects.py`

```python
from django.shortcuts import redirect

class LegacyURLRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Define legacy URL mappings
        url_redirects = {
            '/applications/civil_construction/': '/applications/civil-construction/',
            '/applications/drainage_solutions/': '/applications/drainage-solutions/',
            '/applications/erosion_control/': '/applications/erosion-control/',
            '/applications/gcl_lining_solutions/': '/applications/gcl-lining-solutions/',
            '/applications/tunnel_drainage/': '/applications/tunnel-drainage/',
            '/applications/waterways_coastal/': '/applications/waterways-coastal/',
        }

        if path in url_redirects:
            return redirect(url_redirects[path], permanent=True)

        response = self.get_response(request)
        return response
```

#### Step 3.2: Update Application URLs
**File:** `gems/views.py` - Update render_application_detail function
**File:** `gems/urls.py` - Update URL patterns to use hyphens

### Phase 4: Add Canonical URLs

#### Step 4.1: Add to Product Views
**File:** `products/views.py`

Add canonical URL to context:
```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # Add canonical URL
    context['canonical_url'] = self.request.build_absolute_uri(
        reverse('products:product_detail', kwargs={
            'category_slug': self.object.category,
            'product_code': self.object.code
        })
    )
    return context
```

#### Step 4.2: Update Base Template
**File:** `templates/base.html`

Add in `<head>`:
```html
{% if canonical_url %}
<link rel="canonical" href="{{ canonical_url }}" />
{% endif %}
```

### Phase 5: Update Sitemap

**File:** `gems/sitemaps.py`

Ensure sitemap only includes canonical URLs:
- Remove plural category URLs
- Use hyphenated application URLs
- Exclude paginated pages beyond page 1

### Phase 6: Fix Duplicate Meta Descriptions

**File:** `products/models.py`

Add unique meta description generation:
```python
def get_meta_description(self):
    """Generate unique meta description for SEO"""
    return f"{self.title}: {self.short_description[:150]}"
```

## Testing Checklist

After implementation, verify:

- [ ] Old plural URLs redirect to singular (301 status code)
- [ ] All pages have exactly one H1 tag
- [ ] Canonical URLs are present on all pages
- [ ] Sitemap only contains canonical URLs
- [ ] No 404 errors from internal links
- [ ] Meta descriptions are unique per product
- [ ] Application URLs use hyphens, not underscores

## Monitoring

After deployment:
1. Submit updated sitemap to Google Search Console
2. Monitor for crawl errors
3. Check for 404s in server logs
4. Re-run Ubersuggest audit after 2 weeks
5. Monitor organic traffic for improvements

## Expected Results

- **Immediate:** Elimination of duplicate content issues
- **2-4 weeks:** Improved crawl efficiency
- **1-2 months:** Better rankings for category pages
- **3+ months:** Overall organic traffic increase

## Priority Order

1. **Immediate:** Fix duplicate category URLs (301 redirects)
2. **Day 1:** Add H1 tags to all pages
3. **Day 2:** Implement canonical URLs
4. **Week 1:** Fix URL structure (underscores to hyphens)
5. **Week 2:** Update sitemap and submit to Google

## Notes

- Always use 301 (permanent) redirects, not 302 (temporary)
- Keep redirect chains to a minimum (max 2 hops)
- Test thoroughly in development before deploying
- Consider implementing Django's built-in redirects app for managing redirects