#!/usr/bin/env python3
"""
Import companies from companies.json into Django Company model.
Usage: DJANGO_SETTINGS_MODULE=config.settings ./app/venv/bin/python scripts/import_companies.py
"""
import json
import sys
from pathlib import Path

# Setup Django
script_dir = Path(__file__).parent
project_root = script_dir.parent.parent.parent.parent.parent.parent  # up to 654-memento
sys.path.insert(0, str(project_root / 'app' / 'webapp'))

import django
django.setup()

from library.models import Company


def import_companies():
    """Import companies from JSON file."""
    json_path = script_dir.parent / 'data' / 'companies.json'

    with open(json_path, 'r') as f:
        data = json.load(f)

    metadata = data['metadata']
    companies = data['companies']

    print(f"Importing {len(companies)} companies for project '{metadata['project']}'")

    created_count = 0
    updated_count = 0

    for company_data in companies:
        # Use domain as unique identifier (no SIREN for US companies)
        domain = company_data.get('domain', '')

        # Prepare fields
        fields = {
            'legal_name': company_data.get('legal_name', ''),
            'commercial_name': company_data.get('commercial_name', ''),
            'domain': domain,
            'website': company_data.get('website', ''),
            'geography': company_data.get('geography', ''),
            'revenue': company_data.get('revenue', ''),
            'overview': company_data.get('overview', ''),
            'tags': company_data.get('tags', {}),
            'project': metadata['project'],
            'source': metadata['source'],
        }

        # Try to find existing by domain, or create new
        if domain:
            company, created = Company.objects.update_or_create(
                domain=domain,
                project=metadata['project'],
                defaults=fields
            )
        else:
            # No domain, create new
            company = Company.objects.create(**fields)
            created = True

        if created:
            created_count += 1
            print(f"  + Created: {company.legal_name}")
        else:
            updated_count += 1
            print(f"  ~ Updated: {company.legal_name}")

    print(f"\nDone: {created_count} created, {updated_count} updated")
    return created_count, updated_count


if __name__ == '__main__':
    import_companies()
