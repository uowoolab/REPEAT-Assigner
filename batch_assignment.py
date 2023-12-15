from multiprocessing import Pool
from pathlib import Path

from repeat_assigner import assign_repeat

n_procs = 2
src_path = Path("example_MOFs")
dst_path = Path("assigned_MOFs")
problem_path = Path("problematic_folder")


def main(cif_path):
    assign_repeat(cif_path, dst_path, problem_path)


if __name__ == "__main__":
    with Pool(processes=n_procs) as pool:
        src_glob = list(src_path.glob("*/*.cif"))
        for _ in pool.imap_unordered(main, src_glob):
            continue
