"""Open the pack locally: python3 serve.py. No install, no internet, loopback only."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import argparse, functools

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--port',type=int,default=8765); args=parser.parse_args()
    handler=functools.partial(SimpleHTTPRequestHandler,directory=str(Path(__file__).resolve().parent))
    server=ThreadingHTTPServer(('127.0.0.1',args.port),handler)
    print(f'threed® — http://localhost:{args.port}',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: print('\nStudio stopped.')
