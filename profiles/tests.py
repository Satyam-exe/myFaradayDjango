import pytz

# Create your tests here.
print(str(dict(pytz.country_names)).replace(',', '), \n  (').replace(':', ',').replace('{', '(\n  (').replace('}', ')\n)'))
# .replace(',', '), (')
# .replace(':', ',')
# .replace('{', '((')
# .replace('}', '))')
hui = {
    'AD': 'Andorra',
    'fds': 'dsfdsf'
}
