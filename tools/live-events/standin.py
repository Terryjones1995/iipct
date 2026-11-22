"""A local stand-in for the server's public events feed, for testing assets/js/live-events.js. Never shipped
(tools/ is not published) and never pointed at anything real.

usage: python3 -I standin.py <site-dir> <base-dir> <port> <cert.pem> <key.pem> <scenario-file>

One HTTPS server on 127.0.0.1:<port>. The browser under test maps both host names below to it
(--host-resolver-rules) and accepts its self-signed certificate:
  https://iipct.pixelelite.ca/api/public/events    the feed, in the shape the static spec fixes; which answer it gives
                                                   is the scenario named in <scenario-file> (read on every request)
  https://terryjones1995.github.io/iipct/...       the static site from <site-dir>, at the address it is published at,
                                                   so the feed's CORS rule (that one origin) is tested for real
  https://terryjones1995.github.io/base/...        the pages of 4fcfd8d (before the reader), from <base-dir>
Scenario names: see SCENARIOS at the bottom. Event data comes from the built pages' own list (p_events.EVENTS), so
"equal" is the built events exactly; the test-only events carry "(stand-in test)" in their titles."""
import sys, os, json, ssl, time, uuid, re, html, mimetypes, socket
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from datetime import date

SITE_DIR, BASE_DIR, PORT, CERT, KEY, SCENARIO_FILE = sys.argv[1:7]
sys.path.insert(0, os.path.join(SITE_DIR, 'tools', 'generator'))
import lib, p_events  # noqa: E402

LIVE = lib.LIVE_SITE
ORIGIN = 'https://terryjones1995.github.io'
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def plain(t):
    return html.unescape(re.sub(r'<[^>]+>', '', t))

def ev_id(key):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'iipct-standin/' + key))

def feed_event(key, title, dates, status='', program='', summary='', cancelled=False):
    i = ev_id(key)
    return {'id': i, 'title': title, 'href': f'{LIVE}/events-programs/{i}', 'cancelled': cancelled, 'status': status,
            'program': program, 'summary': summary[:300], 'dates': dates}

def fdate(day, start, end, place):
    return {'day': day, 'weekday': WEEKDAYS[date.fromisoformat(day).weekday()], 'start': start, 'end': end, 'place': place}

def built():
    """The built events, as the server would list them (soonest first)."""
    out = []
    for e in p_events.EVENTS:
        dates = [fdate(d, p_events.t12(e['start']), p_events.t12(e['end']) if e['end'] else '', e['place_short']) for d in e['dates']]
        out.append(feed_event(e['key'], plain(e['title']), dates, e.get('status_short', ''), '', plain(e['text'][0])))
    return out

def answer(events, **over):
    doc = {'generatedAt': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'site': LIVE, 'events': events}
    doc.update(over)
    return doc

def by_title(events, words):
    return next(e for e in events if words in e['title'])

def sc_missing():
    ev = built()
    return answer([e for e in ev if 'Will Planning' not in e['title']])

def sc_cancelled():
    ev = built()
    by_title(ev, 'Free Massage')['cancelled'] = True
    return answer(ev)

def sc_status():
    ev = built()
    by_title(ev, 'Will Planning')['status'] = 'Registration is closed'
    return answer(ev)

NEW = feed_event('new', 'Beading Circle (stand-in test)', [fdate('2026-11-26', '6:00 pm', '8:00 pm', 'Shannonville Office'),
                                                          fdate('2026-12-03', '6:00 pm', '8:00 pm', 'Shannonville Office')],
                 '', 'Breakfast & Beads', 'A test event from the local stand-in feed: two Thursday evenings, all supplies provided.')

def sc_new():
    ev = built()
    return answer(ev[:1] + [NEW] + ev[1:])

def sc_startonly():
    ev = built()
    tomorrow = feed_event('start-only', 'Evening Talk (stand-in test)', [fdate('2026-11-23', '6:00 pm', '', 'Kingston Clinic')],
                          '', '', 'A test event whose end time was not announced: only the start time shows.')
    return answer([tomorrow] + ev)

def sc_markup():
    ev = built()
    bad = feed_event('markup', '<b>Bold?</b> <img src=x onerror="document.title=\'pwned\'"> (stand-in test)',
                     [fdate('2026-11-25', '10:00 am', '11:30 am', '<i>Somewhere</i>')], '<em>status</em>', '<script>x</script>',
                     '<a href="https://evil.example">click</a> <script>document.title="pwned"</script>')
    return answer(ev[:1] + [bad] + ev[1:])

def sc_foreign_href():
    ev = built()
    ev[2]['href'] = 'https://evil.example/events-programs/' + ev[2]['id']
    return answer(ev)

def sc_wrong_site():
    return answer(built(), site='https://evil.example')

def sc_proto():
    ev = built()
    for e in ev:
        e['__proto__'] = {'cancelled': True, 'title': 'polluted'}
        e['constructor'] = {'prototype': {'polluted': True}}
    return answer(ev)

def sc_big():
    doc = answer(built())
    doc['padding'] = 'x' * (5 * 1024 * 1024)
    return doc

SCENARIOS = {
    'empty': lambda: answer([]),
    'equal': lambda: answer(built()),
    'missing': sc_missing,
    'cancelled': sc_cancelled,
    'status': sc_status,
    'new': sc_new,
    'startonly': sc_startonly,
    'markup': sc_markup,
    'foreign-href': sc_foreign_href,
    'wrong-site': sc_wrong_site,
    'proto': sc_proto,
    'big': sc_big,              # 5 MB with a Content-Length header
    'big-chunked': sc_big,      # 5 MB streamed without a length
    'bad-json': None, 'html-type': None, 'slow': None, 'down': None,
}

class H(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def log_message(self, *a): pass

    def host(self):
        return (self.headers.get('Host') or '').split(':')[0]

    def cors(self):
        if self.headers.get('Origin') == ORIGIN:
            self.send_header('Access-Control-Allow-Origin', ORIGIN)
        self.send_header('Vary', 'Origin')

    def send(self, code, body, ctype, extra=()):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        for k, v in extra: self.send_header(k, v)
        if self.host() == 'iipct.pixelelite.ca': self.cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send(204, b'', 'text/plain', [('Access-Control-Allow-Methods', 'GET, OPTIONS')])

    def do_GET(self):
        h, path = self.host(), self.path.split('?')[0]
        if h == 'iipct.pixelelite.ca' and path == '/api/public/events':
            return self.feed()
        if h == 'terryjones1995.github.io':
            for prefix, root in (('/iipct/', SITE_DIR), ('/base/', BASE_DIR)):
                if path.startswith(prefix):
                    rel = path[len(prefix):] or 'index.html'
                    f = os.path.realpath(os.path.join(root, rel))
                    if f.startswith(os.path.realpath(root) + os.sep) and os.path.isfile(f) and '/.git' not in f:
                        ctype = mimetypes.guess_type(f)[0] or 'application/octet-stream'
                        if ctype.startswith('text/') or ctype.endswith('javascript'): ctype += '; charset=utf-8'
                        return self.send(200, open(f, 'rb').read(), ctype)
        self.send(404, b'not found', 'text/plain')

    def feed(self):
        name = open(SCENARIO_FILE).read().strip()
        if name == 'down':   # the server cannot be reached: the connection closes with no answer
            self.close_connection = True
            try: self.connection.shutdown(socket.SHUT_RDWR)
            except OSError: pass
            return
        if name == 'slow':
            time.sleep(6)
            return self.send(200, json.dumps(answer(built())).encode(), 'application/json')
        if name == 'bad-json':
            return self.send(200, b'{"generatedAt": "x", "site": ', 'application/json')
        if name == 'html-type':
            return self.send(200, json.dumps(answer(built())).encode(), 'text/html')
        body = json.dumps(SCENARIOS[name](), ensure_ascii=False).encode()
        if name == 'big-chunked':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Transfer-Encoding', 'chunked')
            self.send_header('Cache-Control', 'no-store')
            self.cors()
            self.end_headers()
            try:
                for i in range(0, len(body), 65536):
                    part = body[i:i + 65536]
                    self.wfile.write(b'%x\r\n%s\r\n' % (len(part), part))
                self.wfile.write(b'0\r\n\r\n')
            except (BrokenPipeError, ConnectionResetError, ssl.SSLError):
                pass   # the reader stopped reading at its limit
            return
        self.send(200, body, 'application/json; charset=utf-8')

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(CERT, KEY)
srv = ThreadingHTTPServer(('127.0.0.1', int(PORT)), H)
srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
print(f'stand-in ready on 127.0.0.1:{PORT}', flush=True)
srv.serve_forever()
