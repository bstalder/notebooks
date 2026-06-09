# Claude Code — Project Notes

## Notebook Editing

Notebooks are often too large for the `Read` tool (>256 KB). Use `jq` via Bash instead:

```bash
# Count cells
jq '.cells | length' notebook.ipynb

# Preview all cells (index + first 120 chars)
jq '[.cells[] | {cell_type, source: (.source | join(""))}]' notebook.ipynb | python3 -c "
import json, sys
cells = json.load(sys.stdin)
for i, c in enumerate(cells):
    print(f'[{i}] {c[\"cell_type\"]}: {c[\"source\"][:120].replace(chr(10),\"\\\\n\")}')
"

# Read a specific cell's source
jq '.cells[N].source | join("")' notebook.ipynb

# Get a cell's ID (needed for NotebookEdit)
jq '.cells[N].id' notebook.ipynb
```

Because `Read` hasn't been called, `NotebookEdit` will be rejected. Edit notebooks by reading and writing the raw JSON with Python via Bash:

```python
import json
with open(path) as f:
    nb = json.load(f)
nb['cells'][N]['source'] = new_source   # string, not list
nb['cells'][N]['outputs'] = []
nb['cells'][N]['execution_count'] = None
with open(path, 'w') as f:
    json.dump(nb, f, indent=1)
```

## Running Notebooks / Cells

**Jupyter is not on PATH.** Use the lsst-scipipe conda environment directly:

```
/sdf/group/rubin/sw/conda/envs/lsst-scipipe-13.0.0/bin/jupyter
/sdf/group/rubin/sw/conda/envs/lsst-scipipe-13.0.0/bin/python3
```

Current environment: `lsst-scipipe-13.0.0`

To execute a subset of cells without running the full notebook, build a mini-notebook and use `nbclient`:

```python
import asyncio, nbformat
from nbclient import NotebookClient

with open(path) as f:
    nb = nbformat.read(f, as_version=4)

target_indices = {2, 4, 81, 82}   # cells to run (0-indexed)
cells_to_run = [(i, nb.cells[i]) for i in sorted(target_indices)]

mini_nb = nbformat.v4.new_notebook()
mini_nb.metadata = nb.metadata.copy()
mini_nb.cells = [c for _, c in cells_to_run]

client = NotebookClient(
    mini_nb,
    timeout=300,
    kernel_name='python3',
    resources={'metadata': {'path': '<notebook_directory>'}},
)
asyncio.run(client.async_execute())

# Write outputs back to original notebook
for orig_idx, cell in cells_to_run:
    src = ''.join(cell.source) if isinstance(cell.source, list) else cell.source
    for mini_cell in mini_nb.cells:
        mini_src = ''.join(mini_cell.source) if isinstance(mini_cell.source, list) else mini_cell.source
        if mini_src == src:
            nb.cells[orig_idx]['outputs'] = mini_cell.get('outputs', [])
            nb.cells[orig_idx]['execution_count'] = mini_cell.get('execution_count')
            break

with open(path, 'w') as f:
    nbformat.write(nb, f)
```

Save this script to `/tmp/run_cells.py` and invoke it with:
```bash
/sdf/group/rubin/sw/conda/envs/lsst-scipipe-13.0.0/bin/python3 /tmp/run_cells.py
```

**For long-running EFD fetches** (multi-day, high-frequency topics), nbclient will time out or the kernel becomes unresponsive. Use a standalone script with `asyncio.run()` instead and write results to a parquet cache:

```python
import asyncio
from lsst_efd_client import EfdClient

async def main():
    client = EfdClient("usdf_efd")
    df = await client.select_time_series(topic, fields=fields, start=t_start, end=t_end)
    df.to_parquet(cache_path)

asyncio.run(main())
```

**High-frequency, wide topics** (e.g. `lsst.sal.MTM1M3TS.thermalData` with 96 columns at ~2 Hz) will hit transfer limits over 8-week windows. Chunk by 1-day intervals and concatenate.

## Notebook Source Format

Cell `.source` is a **list of strings** in the JSON, not a single string. Always join before manipulation:

```python
src = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
```

When writing back, a plain string is accepted by both `json.dump` and `nbformat`.

## Git

Default branch is **`main`** (renamed from `master`).

