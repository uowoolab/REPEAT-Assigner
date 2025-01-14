# REPEAT-Assigner

A robust code for assigning REPEAT outputs to MOFs. Different checks are implemented to ensure the provided files refers to the same structure; if not, `AssertError` will arise with the appropriate information.

## Prerequisites

This code is tested in the following environment:
- Python 3.12.8
- pymatgen 2025.1.9

## Directory Structure

Directories storing the related MOF files should follow the below structure:

```
src/path/to/MOFs/
├── MOF1
│   ├── MOF1.cif
│   ├── POSCAR
│   └── repeat.output
├── MOF2
│   ├── MOF2.cif
│   ├── POSCAR
│   └── repeat.output
└── MOF3
    ├── MOF3.cif
    ├── POSCAR
    └── repeat.output
```

**Checkout [example_MOFs](./example_MOFs/) for example INPUTs, and [assigned_MOFs](./assigned_MOFs/) for example OUTPUTs.**

## Batch Assignment (Recommended)

1. Set up a Python environment based on the prerequisites
2. Prepare new folders for receiving assigned CIFs and problematic MOFs, e.g.:

``` bash
mkdir dst/path/to/assigned/CIFs
mkdir dst/path/to/problematic/MOFs
```

3. Modify `batch_assignment.py` to set up the appropriate paths, e.g.:

``` python
# The number of parallel jobs
n_procs = 2
# The source directory for the REPEAT outputs as shown above
src_path = Path("src/path/to/MOFs")
# The destination directory for receiving the assigned CIFs
dst_path = Path("dst/path/to/assigned/CIFs")
# The destination directory for receiving the problematic MOFs
problem_path = Path("dst/path/to/problematic/MOFs")
```

4. Simply run the `batch_assignment.py` script under an appropriate Python environment:

``` bash
python batch_assignment.py
```

5. If everything is fine, there will be no outputs in the terminal. If any necessary files are missing or problematic, the MOF name alongside an error message will be displayed, e.g.:

```
[DIMKAN] has no CIF
[QARQAF] has no POSCAR
[BIBTEP] has no REPEAT output
[ILECEH] has empty CIF
[FIHJEO] has empty POSCAR
[HALZAW] has different cell vectors in CIF and POSCAR
[IWASOR] has has different cell angles in CIF and POSCAR
[DEVNIF] has different different number of atoms in CIF and POSCAR
[IQIPIH] has has different number of atoms in POSCAR and REPEAT output
[GAXTIM] has different ordering in POSCAR and REPEAT output
```

## Options for Single Usage

**NOTE :** If you want to change any options when doing batch processing, you can modify the `main` function in the `batch_assignment.py` script.

### Saving the assigned CIF to original directory

Simply only pass the path to the CIF file:

``` bash
python repeat_assigner.py path/to/MOFs/MOF1.cif
```

The above command will result in:

```
path/to/MOFs/
├── MOF1
│   ├── MOF1.cif
│   ├── MOF1_repeat.cif
│   ├── POSCAR
│   └── repeat.output
├── ...
```

### Saving the assigned CIF to a specified location

Use the `-o` or `--outdir` option:

``` bash
python repeat_assigner.py path/to/MOFs/MOF2.cif -o path/to/new/cifs
python repeat_assigner.py path/to/MOFs/MOF2.cif --outdir path/to/new/cifs
```

The above command will result in:
```
path/to/new/cifs/
└── MOF2_repeat.cif
path/to/MOFs/
├── MOF2
│   ├── MOF2.cif
│   ├── POSCAR
│   └── repeat.output
├── ...
```

### Different names for POSCAR or REPEAT output

To specify a different filename for POSCAR, use the `-p` or `--poscar` option; for REPEAT output, use the `-r` or `--repeat` option. For example, if your MOFs files are:

```
path/to/MOFs/
├── MOF3
│   ├── MOF3.cif
│   ├── vasp.poscar
│   └── output.repeat
├── ...
```

You can use the following command:

``` bash
python repeat_assigner.py path/to/MOFs/MOF3.cif --poscar vasp.poscar --repeat output.repeat
```
