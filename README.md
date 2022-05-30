# REPEAT-Assigner

## Prerequisites

This code is tested with the following packages:
- Python 3.8+
- pymatgen 2022+
- *OPTIONAL*: tqdm

## Directory Structure
Directories storing the related MOF files should follow the below structure:
```
path/to/MOFs/
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
A example would be: 
```
example_MOFs/
├── DB0-m2_o7_o24_f0_nbo
│   ├── DB0-m2_o7_o24_f0_nbo.cif
│   ├── POSCAR
│   └── repeat.output
├── DB6-cuf_3664
│   ├── DB6-cuf_3664.cif
│   ├── POSCAR
│   └── repeat.output
└── DB7-ddmof_18600
    ├── DB7-ddmof_18600.cif
    ├── POSCAR
    └── repeat.output
```
**Checkout [example_MOFs](./example_MOFs/) for example INPUTs, and [assigned_MOFs](./assigned_MOFs/) for example OUTPUTs.**


## Basic CLI Usage

### Save to original directory
```
$ python repeat_assigner.py path/to/MOFs/MOF1.cif
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

### Save to a specified location
To specify a different directory for the new cif, use the `-o` or `--outdir` option:
```
$ python repeat_assigner.py path/to/MOFs/MOF2.cif -o path/to/new/cifs
```
```
$ python repeat_assigner.py path/to/MOFs/MOF2.cif --outdir path/to/new/cifs
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
To specify a different filename for POSCAR, use the `-p` or `--poscar` option; for REPEAT output, use the `-r` or `--repeat` option.For example, if your MOFs files are:
```
path/to/MOFs/
├── MOF3
│   ├── MOF3.cif
│   ├── vasp.poscar
│   └── output.repeat
├── ...
```
You can use the following command:
```
$ python repeat_assigner.py path/to/MOFs/MOF3.cif --poscar vasp.poscar --repeat output.repeat
```

## Batch Assignment with Python
Two python scripts are provided for batch assignments: if you want have `tqdm` installed and see a progress bar, use [batch_with_progress.py](./batch_with_progress.py), else use [batch_assignment.py](./batch_assignment.py). The two scripts works the same way otherwise.

**IMPORTANT NOTE :** Please modify the `n_procs` (number of processes/threads), `src_path`, `dst_path` to the appropriate values before use.
