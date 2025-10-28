# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Geo Gems is a Django-based B2B e-commerce website for Infratex (infratex.com.au), an Australian geosynthetics supplier. The site manages product catalogs, technical documentation, case studies, and integrates with Xero for quote management.

## Tech Stack
- **Backend:** Django 3.2.9, Python
- **Database:** SQLite (dev), PostgreSQL (prod)
- **Storage:** AWS S3 for media files
- **Integrations:** Xero API for quotes/invoices

## Common Development Commands

```bash
# Activate virtual environment (if exists)
source venv/bin/activate

# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic
```

## High-Level Architecture

### Apps Structure
- **gems/** - Main project settings and global views
- **products/** - Product catalog management
- **knowledge_base/** - Technical guides and case studies
- **apis/** - Xero integration and PDF generation
- **core/** - Middleware utilities

### Key Models
- `Product` - Core product with categories (geocell, geotextile, gcl, geogrid, drainage)
- `TechnicalGuide` / `CaseStudy` - Knowledge base content with rich text
- `Media` / `MediaRelation` - Generic file attachment system using AWS S3

### URL Patterns
- `/products/<category>/` - Category listings
- `/products/<category>/<product_code>/` - Product details
- `/knowledgebase/technical-guides/` - Tech guides (paginated)
- `/knowledgebase/case-studies/` - Case studies (paginated)
- `/apis/` - Xero quote/invoice endpoints

### Data Files
Product and application data stored in JSON:
- `data/products.json` - Product categories
- `data/applications/*.json` - Application-specific content

### Environment Variables
Key configs in `.env`:
- `DEBUG`, `DEVELOPMENT_MODE`
- `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`
- `XERO_CLIENT_ID`, `XERO_CLIENT_SECRET`
- `DATABASE_URL` (production)

## Important SEO Considerations

### Category Slug Handling
The site currently supports legacy plural URLs (e.g., `/products/geogrids/`) that redirect to singular forms (`/products/geogrid/`). This mapping is in `products/views.py:27-33`.

### Known SEO Issues
1. **Duplicate URLs:** Both plural and singular category URLs exist
2. **Missing H1 tags:** Most pages lack H1 headings
3. **Duplicate meta descriptions:** Product pages have identical descriptions

## Testing
Currently no automated tests. Manual testing required for all changes.

## Deployment
Production uses Gunicorn with PostgreSQL and serves static files from AWS S3.