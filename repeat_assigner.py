from collections import Counter
from datetime import date
from pathlib import Path
from re import findall
from shutil import move
import warnings

import numpy as np
from pymatgen.io.cif import CifParser
from pymatgen.io.vasp import Poscar


def move_problematic(src_dir, dst_dir):
    move(src_dir, dst_dir)


def assign_repeat(
    cif_path, dst_path=None, problem_path=None, poscar_name=None, repeat_name=None
):
    # Set defaults for arguments
    if dst_path is None:
        dst_path = cif_path.parent
    else:
        dst_path = Path(dst_path)
    if problem_path is None:
        print("Problematic folder is not set, therefore no folders will be moved.")
    if poscar_name is None:
        poscar_name = "POSCAR"
    if repeat_name is None:
        repeat_name = "repeat.output"

    # Check existance of POSCAR and REPEAT
    cif_name = cif_path.stem
    if not cif_path.is_file():
        print(f"[{cif_name}] has no CIF")
        if problem_path is not None:
            move_problematic(cif_path.parent, problem_path)
    poscar_path = cif_path.parent.joinpath(poscar_name)
    if not poscar_path.is_file():
        print(f"[{cif_name}] has no POSCAR")
        if problem_path is not None:
            move_problematic(cif_path.parent, problem_path)
        return
    repeat_path = cif_path.parent.joinpath(repeat_name)
    if not repeat_path.is_file():
        print(f"[{cif_name}] has no REPEAT output")
        if problem_path is not None:
            move_problematic(cif_path.parent, problem_path)
        return

    # Parse CIF and POSCAR using pymatgen
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            cif_struct = CifParser(cif_path).get_structures(primitive=False).pop()
        except ValueError:
            print(f"[{cif_name}] has empty CIF")
            if problem_path is not None:
                move_problematic(cif_path.parent, problem_path)
            return
        try:
            poscar_struct = Poscar.from_file(poscar_path).structure
        except ValueError:
            print(f"[{cif_name}] has empty POSCAR")
            if problem_path is not None:
                move_problematic(cif_path.parent, problem_path)
            return

    # A small function to compare floats within a certain tolerance
    def compare_float(a, b, tol=0.01):
        return abs(a - b) < (min(abs(a), abs(b)) * tol)

    # Compare cell vectors between CIF and POSCAR
    if not all(
        [
            compare_float(cif_struct.lattice.a, poscar_struct.lattice.a),
            compare_float(cif_struct.lattice.b, poscar_struct.lattice.b),
            compare_float(cif_struct.lattice.c, poscar_struct.lattice.c),
        ]
    ):
        print(f"[{cif_name}] has different cell vectors in CIF and POSCAR")
        if problem_path is not None:
            move_problematic(cif_path.parent, problem_path)
        return

    # Compare cell angles between CIF and POSCAR
    if not all(
        [
            compare_float(cif_struct.lattice.alpha, poscar_struct.lattice.alpha),
            compare_float(cif_struct.lattice.beta, poscar_struct.lattice.beta),
            compare_float(cif_struct.lattice.gamma, poscar_struct.lattice.gamma),
        ]
    ):
        print(f"[{cif_name}] has different cell angles in CIF and POSCAR")
        if problem_path is not None:
            move_problematic(cif_path.parent, problem_path)
        return

    # Compare number of atoms between CIF and POSCAR
    if len(cif_struct) != len(poscar_struct):
        print(f"[{cif_name}] has different different number of atoms in CIF and POSCAR")
        if problem_path is not None:
            move_problematic(cif_path.parent, problem_path)
        return

    # Get atomic symbols and fractional coordinates for all atoms
    symbols = [atom.specie.symbol for atom in poscar_struct]
    frac_xyz = np.around([atom.frac_coords for atom in poscar_struct], decimals=6)
    frac_xyz[frac_xyz == 0.0] = 0.0

    # Compare the numbers of each element between CIF and POSCAR
    if Counter([str(atom.specie) for atom in cif_struct]) != Counter(symbols):
        print(f"[{cif_name}] has different different number of atoms in CIF and POSCAR")
        if problem_path is not None:
            move_problematic(cif_path.parent, problem_path)
        return

    # Parse REPEAT file and compare number of atoms between POSCAR and REPEAT
    repeat_lines = findall(
        r"Charge [0-9]+ of type [0-9]+ = [0-9.-]+", repeat_path.read_text()
    )
    if len(repeat_lines) != len(poscar_struct):
        print(f"[{cif_name}] has different number of atoms in POSCAR and REPEAT output")
        if problem_path is not None:
            move_problematic(cif_path.parent, problem_path)
        return

    # While check the order of atoms, extract REPEAT charges
    repeat_charges = []
    for repeat_line, poscar_atom in zip(repeat_lines, poscar_struct):
        line_split = repeat_line.split()
        if int(line_split[4]) != poscar_atom.specie.Z:
            print(f"[{cif_name}] has different ordering in POSCAR and REPEAT output")
            if problem_path is not None:
                move_problematic(cif_path.parent, problem_path)
            return
        repeat_charges.append(line_split[-1])

    # Reassign labels for all atoms
    labels = []
    label_counter = {element: 0 for element in set(symbols)}
    for symbol in symbols:
        label_counter[symbol] += 1
        labels.append(f"{symbol}{label_counter[symbol]}")

    # Create preambles for the new CIF file
    new_cif = "# Generated by REPEAT Assigner based on pymatgen\n"
    new_cif += f"data_{cif_path.name.replace('.cif', '')}\n"
    new_cif += "_audit_creation_date              "
    new_cif += date.today().strftime("%Y-%m-%d") + "\n"
    new_cif += "_audit_creation_method            REPEAT_Assigner\n"

    # Create cell info for the new CIF file
    new_cif += f"_cell_length_a                    {cif_struct.lattice.a:.6f}\n"
    new_cif += f"_cell_length_b                    {cif_struct.lattice.b:.6f}\n"
    new_cif += f"_cell_length_c                    {cif_struct.lattice.c:.6f}\n"
    new_cif += f"_cell_angle_alpha                 {cif_struct.lattice.alpha:.6f}\n"
    new_cif += f"_cell_angle_beta                  {cif_struct.lattice.beta:.6f}\n"
    new_cif += f"_cell_angle_gamma                 {cif_struct.lattice.gamma:.6f}\n"
    new_cif += f"_cell_volume                      {cif_struct.lattice.volume:.6f}\n"

    # [ASSUMED P1] Create symmetry info for the new CIF file
    new_cif += "_symmetry_space_group_name_H-M    P1\n"
    new_cif += "_symmetry_Int_Tables_number       1\n"
    new_cif += "loop_\n"
    new_cif += "    _symmetry_equiv_pos_site_id\n"
    new_cif += "    _symmetry_equiv_pos_as_xyz\n"
    new_cif += "    1  x,y,z\n"

    # Create atom info for the new CIF file
    new_cif += "loop_\n"
    new_cif += "    _atom_site_type_symbol\n"
    new_cif += "    _atom_site_label\n"
    new_cif += "    _atom_site_fract_x\n"
    new_cif += "    _atom_site_fract_y\n"
    new_cif += "    _atom_site_fract_z\n"
    new_cif += "    _atom_type_partial_charge\n"

    # Adjust widths for the symbols and labels column
    symbol_width = len(max(symbols, key=len))
    label_width = len(max(labels, key=len))

    # Loop over all atoms and create info line for each of them
    for symbol, label, frac, charge in zip(symbols, labels, frac_xyz, repeat_charges):
        new_cif += f"    {symbol:{symbol_width}}  {label:{label_width}}  "
        new_cif += "{:.6f}  {:.6f}  {:.6f}  ".format(*frac) + f"{charge}\n"

    # Write the new CIF
    dst_path.joinpath(cif_path.name.replace(".cif", "_repeat.cif")).write_text(new_cif)


if __name__ == "__main__":
    from argparse import ArgumentParser

    ap = ArgumentParser(description="Assigning REPEAT outputs to a new CIF file.")
    ap.add_argument("cif", type=str, help="path to the CIF of interest")
    ap.add_argument(
        "-o",
        "--outdir",
        type=str,
        metavar="OUTPUT_DIR",
        help="Explicitly provide an output directory.",
    )
    ap.add_argument(
        "-p",
        "--poscar",
        type=str,
        metavar="POSCAR",
        help="Explicitly provide the name of POSCAR file.",
    )
    ap.add_argument(
        "-r",
        "--repeat",
        type=str,
        metavar="REPEAT",
        help="Explicitly provide the name of the REPEAT output file.",
    )
    args = ap.parse_args()
    assign_repeat(args.cif, args.outdir, args.poscar, args.repeat)
