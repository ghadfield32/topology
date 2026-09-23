"""Development-only course reader. Private paths and directory listings are denied.

No authentication or multi-user sandbox is provided. Bind to loopback on a host;
containers may bind all interfaces ONLY behind a loopback port map/port-forward.
"""
from __future__ import annotations
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

PRIVATE={'my_work','progress','.git','.venv','venv','node_modules','__pycache__','.pytest_cache','.uv-cache'}


def public_path(root: Path,url: str) -> Path | None:
    root=root.resolve();text=unquote(urlsplit(url).path)
    parts=PurePosixPath(text).parts
    if '\\' in text or '\x00' in text or any(p=='..' or p in PRIVATE or p.startswith('.') for p in parts):return None
    candidate=root.joinpath(*[p for p in parts if p!='/']).resolve()
    if not candidate.is_relative_to(root):return None
    if candidate.suffix.lower() in {'.pem','.key','.p12','.pfx'}:return None
    return candidate


class ReaderHandler(SimpleHTTPRequestHandler):
    def translate_path(self,path):
        return str(public_path(Path(self.directory),path) or Path(self.directory)/'__DENIED__')

    def send_head(self):
        p=public_path(Path(self.directory),self.path)
        if p is None:
            self.send_error(403,'Private path');return None
        if p.is_dir():
            if not any((p/n).is_file() for n in ['index.html','index.htm','START_HERE.html']):
                self.send_error(403,'Directory listing disabled');return None
            if p==Path(self.directory).resolve() and self.path.split('?')[0]=='/':self.path='/START_HERE.html'
        return super().send_head()

    def list_directory(self,path):
        self.send_error(403,'Directory listing disabled');return None

    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        super().end_headers()


def serve(root: Path,port: int=8000,bind: str='127.0.0.1') -> None:
    if bind not in {'127.0.0.1','0.0.0.0','::1'}:raise ValueError('Use loopback or the explicitly chosen container bind.')
    if not 1024<=port<=65535:raise ValueError('Use a port between 1024 and 65535.')
    print(f'Course reader http://{bind}:{port}/START_HERE.html; development only. Private paths denied.',flush=True)
    with ThreadingHTTPServer((bind,port),partial(ReaderHandler,directory=str(root.resolve()))) as server:
        try:server.serve_forever()
        except KeyboardInterrupt:pass


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path.cwd())
    p.add_argument('--port',type=int,default=8000);p.add_argument('--bind',default='127.0.0.1')
    a=p.parse_args();serve(a.root,a.port,a.bind)

if __name__=='__main__':main()
