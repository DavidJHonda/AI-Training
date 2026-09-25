import json,re,sys
m=json.load(open(sys.argv[1]))
print(' '.join('--boundary %d:%s' % (b['frame'], re.sub(r'[^A-Za-z0-9]+','_',b['label'][:24]).strip('_')) for b in m['boundaries']))
