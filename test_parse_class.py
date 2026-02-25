#!/usr/bin/env python
"""Try parsing and executing just the class"""

# Get lines from views.py where our class is
with open('core/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Lines 326-395 (0-indexed) contain the class
class_start = 325  # 0-indexed line 326
class_end = 395
class_code = ''.join(lines[class_start:class_end])

print("Class code:")
print("=" * 60)
print(class_code[:500])
print("...")
print("=" * 60)

# Try to compile it
import ast
try:
    tree = ast.parse(class_code)
    print(f"✓ Code parses successfully, {len(tree.body)} top-level items")
    for item in tree.body:
        print(f"  - {type(item).__name__}: {getattr(item, 'name', '?')}")
except SyntaxError as e:
    print(f"✗ Syntax error: {e}")
