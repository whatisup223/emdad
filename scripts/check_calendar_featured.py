# -*- coding: utf-8 -*-
import os, sys, re
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app

app = create_app('production')

with app.app_context():
    client = app.test_client()
    resp = client.get('/calendar')
    html = resp.get_data(as_text=True)
    # Count product cards in the featured section by matching the featured badge nearby
    cards = len(re.findall(r'class="product-card card', html))
    print('HTTP:', resp.status_code)
    print('Cards detected (any section):', cards)
    # Heuristic: featured section title exists?
    print('Has Featured Section:', ('Featured Products' in html) or ('المنتجات المميزة' in html))

