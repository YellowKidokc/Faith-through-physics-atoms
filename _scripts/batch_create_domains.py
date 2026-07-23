"""
FAITH THROUGH PHYSICS — Batch Domain Creator
Creates all initial domains from the template.
Run once. Then use new_domain.py for individual additions.

Usage: python batch_create_domains.py
"""
import os
import shutil

canonical = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template = os.path.join(canonical, '_template')

domains = [
    'master-equation', 'ten-laws', 'trinity', 'axioms',
    'physics', 'theology', 'scripture', 'christian-life',
    'education', 'psychology', 'pharmacology', 'biology',
    'economics', 'information-theory', 'consciousness',
    'music-theory', 'network-science', 'cryptography',
    'fluid-dynamics', 'control-theory', 'epidemiology',
    'ecology', 'cosmology', 'addiction-science',
    'history', 'ai-alignment',
]

created = 0
skipped = 0

for domain in domains:
    target = os.path.join(canonical, domain)
    if os.path.exists(target):
        print(f'  SKIP (exists): {domain}')
        skipped += 1
        continue
    shutil.copytree(template, target)
    print(f'  CREATED: {domain}')
    created += 1

print(f'\nDONE: {created} domains created, {skipped} skipped')
print(f'Total: {len(domains)} domains x 14 stages = {len(domains)*14} folders')
