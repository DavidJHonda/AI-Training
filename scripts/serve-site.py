#!/usr/bin/env python3
"""Serve the static site locally using the same exact rewrites as vercel.json."""
import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qs

ROOT = Path(__file__).resolve().parents[1]
REWRITES = json.loads((ROOT / 'vercel.json').read_text())['rewrites']


def rewrite_url(url):
    parts = urlsplit(url)
    query = parse_qs(parts.query, keep_blank_values=True)
    path = parts.path.rstrip('/') or '/'
    for rule in REWRITES:
        if path == rule['source'] and all(c['key'] in query for c in rule.get('has', [])):
            return urlunsplit(('', '', rule['destination'], parts.query, ''))
    return url


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        self.path = rewrite_url(self.path)
        super().do_GET()

    def do_HEAD(self):
        self.path = rewrite_url(self.path)
        super().do_HEAD()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8878)
    args = parser.parse_args()
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
