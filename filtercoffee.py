# Copyright (c) 2012, Christian Lyder Jacobsen. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import time
import subprocess

cmd = ['coffee', '--compile', '--print']

class CoffeeFileRemovedException(Exception): pass
class CoffeeScriptErrorException(Exception): pass

class CacheEntry(object):
    def __init__(self, js_path, coffee_path):
        self.js_path     = js_path
        self.coffee_path = coffee_path
        self.timestamp   = 0
        self.data        = None
        self.error_msg   = None
    def fetch(self):
        try:
            if self.data and self.timestamp > os.path.getmtime(self.coffee_path):
                return self.data
        except OSError:
            raise CoffeeFileRemovedException('Coffee file removed: %s' % (self.coffee_path, ))
        self.timestamp = time.time()
        p = subprocess.Popen(cmd + [self.coffee_path], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.data, self.error_msg = p.communicate()
        if p.returncode != 0:
            self.timestamp = 0
            raise CoffeeScriptErrorException(self.error_msg)
        return self.data

class FilterCoffee(object):
    def __init__(self, app, static_dir, js_ext='.js', coffee_ext='.coffee', matcher=None, xformer=None):
        def match(f):
            return f[-3:] == js_ext
        def xform(f):
            return f[:-3] + coffee_ext
        self.app        = app
        self.static_dir = static_dir
        self.match      = matcher or match
        self.xform      = xformer or xform
        self.cache      = dict()
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')[1:]
        if self.match(path):
            if path not in self.cache:
                coffee_path = self.xform(path)
                if os.path.exists(os.path.join(self.static_dir, coffee_path)):
                    jp = os.path.join(self.static_dir, path)
                    cp = os.path.join(self.static_dir, coffee_path)
                    self.cache[path] = CacheEntry(jp, cp)
                else:
                    return self.app(environ, start_response)
            try:
                data = self.cache[path].fetch()
            except CoffeeFileRemovedException:
                del self.cache[path]
                return self.app(environ, start_response)
            except CoffeeScriptErrorException, e:
                error_msg = 'CoffeeScript error:\n-------------------\n' + e.message
                output = environ.get('wsgi.error', sys.stderr)
                output.write(error_msg)
                start_response(
                        '500 Internal Server Error',
                        [('Content-Type', 'text/plain'),
                         ('Content-Length', str(len(error_msg)))])
                return [error_msg]
            start_response(
                    '200 OK', 
                    [('Content-Type', 'application/javascript'),
                     ('Cache-Control', 'no-cache'),
                     ('Content-Length', str(len(data))),
                     ('Expires', 'Thu, 31 Jan 1956 00:00:00 GMT')])
            return [data]
        return self.app(environ, start_response)

def main(path, host, port):
    import paste.fileapp
    import paste.httpserver
    import paste.reloader
    if os.environ.get('PASTE_RELOAD', None):
        paste.reloader.install()
        print 'reloader active'
    app = paste.fileapp.DirectoryApp(path)
    app = FilterCoffee(app, path)
    paste.httpserver.serve(app, host, port)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s <path> [host] [port]' % __file__
        sys.exit(1)
    path = sys.argv[1]
    if len(sys.argv) > 2:
        host = sys.argv[2]
    else:
        host = '127.0.0.1'
    if len(sys.argv) > 3:
        port = sys.argv[3]
    else:
        port = '8118'
    main(path, host, port)
