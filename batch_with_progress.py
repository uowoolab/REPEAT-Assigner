from multiprocessing import Pool
from pathlib import Path

from tqdm import tqdm

from repeat_assigner import assign_repeat

n_procs = 2
src_path = Path("example_MOFs")
dst_path = Path("assigned_MOFs")


def main(cif_path):
    assign_repeat(cif_path, dst_path)


if __name__ == "__main__":
    with Pool(processes=n_procs) as pool:
        src_glob = list(src_path.glob("*/*.cif"))
        with tqdm(total=len(src_glob)) as progress:
            for _ in pool.imap_unordered(main, src_glob):
                progress.update()