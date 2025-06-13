
def generate_hillshade(stereo_prefix):
    import os

    # Generate hillshade from the DEM
    hillshade_cmd = f"hillshade {stereo_prefix}/DEM_PC.tif-DEM.tif -o {stereo_prefix}/DEM_PC_hillshade.tif"
    print("Running:", hillshade_cmd)
    os.system(hillshade_cmd)
