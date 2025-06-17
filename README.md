# 📡 Stereo DSM Generation Pipelines for SPOT and Pleiades

## Overview
This repository provides a streamlined way to generate a Digital Surface Model (DSM) from SPOT 6 and Pleiades stereo imagery using NASA's Ames Stereo Pipeline.

## 🐍 Setup 
Refer to Section 2.6 for ASP installation using Conda and for general guidelines of installation https://stereopipeline.readthedocs.io/en/latest/installation.html#conda-intro

or use the .yml file for recreating the environment. 
```bash
conda env create -f asp_environment.yml
```

Ensure `stereo`, `point2dem`, and other ASP tools are available in your system PATH.

## Usage
1. Place all stereo images in `data` 📂
    - SPOT raw files should be in `data/tif`
    - Pleiades raw files should be in `data/jp2` (Plieades data has JP2 images that needs to be converted into tif)
2. Define input and output path, variables in config.json file. A sample file for both the sensors is provided (config_spot.json,config_plieades.json)
3. The data directory structure is captured in data_directory_structure.json file
4. Run the pipeline:
```bash
python run_pipeline.py config.json 
```

Outputs will be saved in `results/`.

##  💾 Data
Data can be accessed at https://drive.google.com/drive/folders/1Ez28ofTNtGOb15zQEIN2xMGfpFva3_nC?usp=sharing (access restricted to Solafune)

## Execution of the Pipeline without providing DEM
- The input to the pipeline is tif/jpg images, corrosponsing RPC files, and third-party/ exisitng DEM.
- The same pipeline can work without the DEM. We have to skip the map projection step
- When we execute the pipeline bypassing the map projection step, following warning text will appear in the terminal, this will not affect the execution (Warning: It appears that the input images are map-projected. In that case a DEM needs to be provided for stereo to give correct results).
- We can continue the execution, the pipeline will not break
- The current repo runs with default stereo processing parameters. However, one can play with additonal parameters given below

## Run stereo processing with additonal parameters
```bash
cmd = f"""
parallel_stereo -t rpc --alignment-method affineepipolar \\
    --subpixel-mode 2 \\
    --corr-seed-mode 1 \\
    --corr-kernel 25 25 \\
    --subpixel-kernel 25 25 \\
    --rm-quantile-mult 3.0 \\
    --prefilter-mode 2 \\
    --cost-mode 2 \\
    --nodata-value 0 \\
    --left-image-crop-win 0 0 0 0 \\
    {LEFT_IMG} {RIGHT_IMG} {LEFT_RPC} {RIGHT_RPC} {STEREO_PREFIX}
"""
# Execute the command
os.system(cmd)
```
| Parameter             | Recommended Value | Why?                                                                                               |
| --------------------- | ----------------- | -------------------------------------------------------------------------------------------------- |
| `-t rpc`              | rpc               | SPOT 6 uses RPC models.                                                                            |
| `--alignment-method`  | affineepipolar    | Best for RPC images to align in epipolar space without DEM.                                        |
| `--subpixel-mode`     | 2                 | Balanced precision and speed. Mode 2 uses paraboloid fitting, which is better for mining surfaces. |
| `--corr-seed-mode`    | 1                 | Fast initial correlation seeding (adequate for large, flat areas like deserts).                    |
| `--corr-kernel`       | 25 25             | Wider window for better correlation in low-texture areas like sand and rocks.                      |
| `--subpixel-kernel`   | 25 25             | Large enough to ensure subpixel refinement is effective in low-texture scenes.                     |
| `--rm-quantile-mult`  | 3.0               | Conservative outlier filtering (keeps more data but still removes major noise).                    |
| `--prefilter-mode`    | 2                 | Normalizes image intensities to improve matching in bright/sandy desert scenes.                    |
| `--cost-mode`         | 2                 | Census transform cost function, which is more robust in low-texture areas.                         |
| `--nodata-value`      | -32768            | Standard to ignore invalid pixels.                                                                 |
| `--save-crop-windows` | -                 | Saves alignment info in case you want to refine later or debug.                                    |
