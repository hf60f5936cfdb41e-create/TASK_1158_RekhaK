"""Tests for the main CLI application."""
import json
import os
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from main import load_customers, filter_customers, save_results


def test_load_customers():
    """Test loading customers from CSV."""
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write('id,name,age,country\n')
        f.write('1,John,25,USA\n')
        f.write('2,Jane,30,Canada\n')
        temp_path = f.name

    try:
        customers = load_customers(temp_path)
        assert len(customers) == 2
        assert customers[0]['name'] == 'John'
        assert customers[1]['age'] == '30'
    finally:
        os.unlink(temp_path)


def test_filter_by_country():
    """Test filtering customers by country."""
    customers = [
        {'name': 'John', 'age': '25', 'country': 'USA'},
        {'name': 'Jane', 'age': '30', 'country': 'Canada'},
        {'name': 'Bob', 'age': '35', 'country': 'USA'},
    ]

    filtered = filter_customers(customers, country='USA')
    assert len(filtered) == 2
    assert all(c['country'] == 'USA' for c in filtered)


def test_filter_by_min_age():
    """Test filtering customers by minimum age."""
    customers = [
        {'name': 'John', 'age': '25', 'country': 'USA'},
        {'name': 'Jane', 'age': '30', 'country': 'Canada'},
        {'name': 'Bob', 'age': '18', 'country': 'USA'},
    ]

    filtered = filter_customers(customers, min_age=21)
    assert len(filtered) == 2
    assert all(int(c['age']) >= 21 for c in filtered)


def test_filter_by_country_and_min_age():
    """Test filtering customers by both country and minimum age."""
    customers = [
        {'name': 'John', 'age': '25', 'country': 'USA'},
        {'name': 'Jane', 'age': '30', 'country': 'Canada'},
        {'name': 'Bob', 'age': '18', 'country': 'USA'},
        {'name': 'Alice', 'age': '22', 'country': 'USA'},
    ]

    filtered = filter_customers(customers, country='USA', min_age=21)
    assert len(filtered) == 2
    assert all(c['country'] == 'USA' and int(c['age']) >= 21 for c in filtered)


def test_save_results():
    """Test saving results to JSON."""
    data = [
        {'name': 'John', 'age': '25', 'country': 'USA'},
        {'name': 'Jane', 'age': '30', 'country': 'Canada'},
    ]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name

    try:
        save_results(temp_path, data)

        with open(temp_path, 'r') as f:
            loaded_data = json.load(f)

        assert len(loaded_data) == 2
        assert loaded_data[0]['name'] == 'John'
    finally:
        os.unlink(temp_path)
