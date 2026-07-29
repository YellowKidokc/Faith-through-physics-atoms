"""
FAITH THROUGH PHYSICS — New Domain Creator
Creates a single new domain folder from the template.

Usage: python new_domain.py [domain-name]
Example: python new_domain.py materials-science
"""
import os
import sys
import shutil

canonical = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template = os.path.join(canonical, '_template')

if len(sys.argv) < 2:
    print('Usage: python new_domain.py <domain-name>')
    print('Example: python new_domain.py psychology')
    sys.exit(1)

domain = sys.argv[1].lower().strip()
reserved_names = {'_template_domain', '_template', 'template_domain'}
if domain in reserved_names or domain.startswith('_'):
    print(f'ERROR: Refusing reserved/system domain name: {domain}')
    sys.exit(1)

target = os.path.join(canonical, domain)

if os.path.exists(target):
    print(f'ERROR: {target} already exists.')
    sys.exit(1)

if not os.path.exists(template):
    print(f'ERROR: Template not found at {template}')
    print('Run build_template.py first.')
    sys.exit(1)

shutil.copytree(template, target)

# Update desktop.ini icon to show empty status
# (will be updated by status_scan.py as content is added)

print(f'CREATED: {target}')
print(f'  14 stage folders with AI checklists and NLP hooks')
print(f'  Ready for atoms.')
