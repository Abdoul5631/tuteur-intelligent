import sys, os, importlib.util
print('Python executable:', sys.executable)
print('sys.path:')
for p in sys.path:
    print(' -', p)
site_p = os.path.join(os.path.dirname(sys.executable), '..', 'Lib', 'site-packages')
print('\nGuessed site-packages:', os.path.normpath(site_p))
sp = None
# try common venv path
p1 = os.path.join(os.getcwd(), '.venv', 'Lib', 'site-packages')
if os.path.isdir(p1):
    sp = p1
else:
    # fallback to sys.path detection
    for p in sys.path:
        if p.endswith('site-packages') and os.path.isdir(p):
            sp = p
            break
if sp:
    print('\nListing setuptools/pkg_resources files in:', sp)
    for name in sorted(os.listdir(sp)):
        if 'setuptools' in name or 'pkg_resources' in name:
            print('  ', name)
else:
    print('\nNo site-packages directory found in common locations.')

print('\nimportlib.util.find_spec("setuptools") ->', importlib.util.find_spec('setuptools'))
print('importlib.util.find_spec("pkg_resources") ->', importlib.util.find_spec('pkg_resources'))
try:
    import pkg_resources
    print('\nImported pkg_resources version:', getattr(pkg_resources, '__version__', 'unknown'))
except Exception as e:
    print('\nImport pkg_resources failed:', repr(e))
