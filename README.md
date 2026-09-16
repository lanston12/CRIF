# CRIF: minimal empirical reproduction package

This repository accompanies *Communication--Computation--Control Co-Design for Cooperative AUVs via In-Network Prediction and Freshness-Adaptive MPC* (IEEE TVT submission). CRIF means **control-relevant information freshness**.

## Scope

The frozen MATLAB source and configuration files regenerate the paper's finite-horizon nonlinear REMUS100 evaluation: E2 trigger comparison, E3 LOCAL/EDGE/SKIP service choices, and E4-A short outages. The 201-job matrix includes 40 E2, 40 E3, 20 E4-A, 100 Pareto, and one matched E1 source run. The separate E4-B overlong-outage trace and its frozen configuration are included because this negative result is an essential empirical limitation. These runs are empirical; the repository does not instantiate the manuscript's terminal-set and service-envelope theorem assumptions.

## Requirements

- MATLAB R2022b, Optimization Toolbox, and Control System Toolbox.
- Python 3 with NumPy and SciPy for log metrics.
- No network access is needed after cloning; only the 21 required functions from official MSS commit `98970f71a21cfe81e7e29abdcc1bb6741789cddc` are vendored, with its MIT license. Hashes are recorded in `config/plant_provenance.md`.

## Quick reproduction

Download `CRIF_minimal_reproduction.zip` from this repository, extract it to a new directory, and run the following commands from the extracted directory. First validate the files:

```text
python verify_package.py
```

Then, in MATLAB, run a matched E2 pair using the published configuration and seed:

```matlab
startup_smoke;
run_statistical_study('experiments/evaluation/study_eval_v1.json','E2','AOI',41001,'evaluation');
run_statistical_study('experiments/evaluation/study_eval_v1.json','E2','CRIF',41001,'evaluation');
```

Read metrics from both generated MAT files:

```text
python analysis/study_metrics.py logs/mechanisms/evaluation/study_eval_v1/E2_AOI_41001.mat logs/mechanisms/evaluation/study_eval_v1/E2_CRIF_41001.mat
```

`run_statistical_study` refuses to overwrite existing runs. The full 201-job matrix can be regenerated with:

```matlab
startup_smoke;
run_study_batch('experiments/evaluation/study_jobs_v1.json',1,1);
```

The full matrix can take substantial time. For parallel workers, assign disjoint `part` indices and a common `parts` value. The included E4-B MAT file is a retained historical negative result from the separate frozen `mechanism_eval_v1` run; inspect it with `analysis/study_metrics.py` only if the metric function supports that legacy record, or load its `result` struct directly in MATLAB/Python. Do not conflate E4-A and E4-B.

## Integrity and limitations

`verify_package.py` checks the frozen statistical source/config hashes, pinned MSS file hashes, and E4-B trace checksum. Calibration logs and all 201 evaluation logs are omitted to keep the package small; regenerate the latter from the frozen job matrix. MATLAB/toolbox availability and platform-dependent optimization can affect exact floating-point trajectories. This code does not certify the nonlinear experiment or claim uniform safety.

The official MSS project is [cybergalactic/MSS](https://github.com/cybergalactic/MSS), by Thor I. Fossen and contributors. Vendored files retain its MIT license.
