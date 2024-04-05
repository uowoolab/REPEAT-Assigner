from multiprocessing import Pool
from pathlib import Path

from repeat_assigner import assign_repeat

n_procs = 4
src_path = Path("src/path")
dst_path = Path("dst/path")
problem_path = Path("problem/path")


def main(cif_path):
    assign_repeat(cif_path, dst_path, problem_path)


if __name__ == "__main__":
    with Pool(processes=n_procs) as pool:
        src_glob = list(src_path.glob("*/*.cif"))
        for _ in pool.imap_unordered(main, src_glob):
            continue
