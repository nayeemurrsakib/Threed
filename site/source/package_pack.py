"""Create the download archive and inventory without including temporary Python caches."""
import csv, hashlib, json, pathlib, zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
    catalog=json.loads((ROOT/'catalog.json').read_text())
    with (ROOT/'CATALOG.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['id','name','category','model','transparent_png','triangles','vertices','mesh_parts','bytes','material_slots'])
        for a in catalog['assets']:writer.writerow([a['id'],a['name'],a['category'],a['model'],f'renders/{a["id"]}.png',a['triangles'],a['vertices'],a['parts'],a['bytes'],' | '.join(a['materialSlots'])])
    paths=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ('SHA256SUMS.txt','.DS_Store') and not p.name.endswith('.zip') and 'studies' not in p.relative_to(ROOT).parts)
    (ROOT/'SHA256SUMS.txt').write_text('\n'.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT)}' for p in paths)+'\n')
    paths.append(ROOT/'SHA256SUMS.txt');dest=ROOT.parent/'downloads/threed-vol01.zip';dest.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
        for p in paths:z.write(p,pathlib.Path('threed-pack')/p.relative_to(ROOT))
    with zipfile.ZipFile(dest) as z:assert z.testzip() is None
    print(json.dumps({'archive':str(dest),'files':len(paths),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
