"""Fix path resolution and re-execute 02_ann_model.ipynb with clean outputs."""

import json
import io
import contextlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = PROJECT_ROOT / "notebooks" / "02_ann_model.ipynb"


def fix_and_execute_notebook():
    with open(NB_PATH, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Global execution namespace
    glob = {
        "__file__": str(NB_PATH),
    }

    print("Executing cells of 02_ann_model.ipynb...")

    for idx, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue

        source = "".join(cell.get("source", []))
        if not source.strip():
            cell["outputs"] = []
            cell["execution_count"] = idx + 1
            continue

        # Adjust PROJECT definition to be robust whether run from root or notebooks
        if "PROJECT = Path.cwd().parent" in source:
            source = source.replace(
                "PROJECT = Path.cwd().parent",
                "PROJECT = Path.cwd() if (Path.cwd() / 'models').exists() else Path.cwd().parent"
            )
            cell["source"] = [line + "\n" for line in source.splitlines()]

        # If Cell 4 looks for obsolete or missing files, ensure it handles existing model files
        if "ann_preprocessor.pkl" in source:
            source = source.replace(
                '    "ann_model.pkl",\n    "ann_preprocessor.pkl",\n    "ann_label_encoder.pkl"',
                '    "ann_model.pkl",\n    "ann_model_metadata.json"'
            )
            cell["source"] = [line + "\n" for line in source.splitlines()]

        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
                exec(source, glob)
            out_text = stdout_buf.getvalue()
            err_text = stderr_buf.getvalue()

            outputs = []
            if out_text:
                outputs.append({
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [line + "\n" for line in out_text.splitlines()],
                })
            if err_text:
                outputs.append({
                    "name": "stderr",
                    "output_type": "stream",
                    "text": [line + "\n" for line in err_text.splitlines()],
                })
            cell["outputs"] = outputs
            cell["execution_count"] = idx + 1
            print(f"  Cell {idx}: Success")

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print(f"  Cell {idx} FAILED: {e}")
            print(tb)
            cell["outputs"] = [{
                "ename": type(e).__name__,
                "evalue": str(e),
                "output_type": "error",
                "traceback": tb.splitlines(),
            }]
            cell["execution_count"] = idx + 1
            raise

    with open(NB_PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)

    print("\n02_ann_model.ipynb re-executed and saved with clean outputs!")


if __name__ == "__main__":
    fix_and_execute_notebook()
