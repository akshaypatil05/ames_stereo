def map_project(mpp, dem_ref, left_img, left_rpc, right_img, right_rpc, front_map_proj, back_map_proj):
    import os

    mapproject_cmd_front = f"mapproject -t rpc --mpp {mpp} {dem_ref} {left_img} {left_rpc} {front_map_proj}"
    mapproject_cmd_back = f"mapproject -t rpc --mpp {mpp} {dem_ref} {right_img} {right_rpc} {back_map_proj}"
    
    print("Running:", mapproject_cmd_front)
    os.system(mapproject_cmd_front)
    
    print("Running:", mapproject_cmd_back)
    os.system(mapproject_cmd_back)

def stereo_process(front_map_proj, back_map_proj, left_rpc, right_rpc, stereo_prefix, dem_ref):
    import os

    stereo_cmd = f"parallel_stereo -t rpcmaprpc {front_map_proj} {back_map_proj} {left_rpc} {right_rpc} {stereo_prefix} {dem_ref}"
    
    print("Running:", stereo_cmd)
    os.system(stereo_cmd)


def point2dem_process(stereo_prefix):
    import os

    point2dem_cmd = f"point2dem {stereo_prefix}-PC.tif --orthoimage {stereo_prefix}-L.tif -o {stereo_prefix}/DEM_PC.tif"
    
    print("Running:", point2dem_cmd)
    os.system(point2dem_cmd)

def point2dem_utm_process(stereo_prefix,utm_zone, resolution):
    import os

    point2dem_cmd = f"point2dem {stereo_prefix}-PC.tif --orthoimage {stereo_prefix}-L.tif --utm {utm_zone} --tr {resolution} -o {stereo_prefix}/DEM_PC.tif"
    
    print("Running:", point2dem_cmd)
    os.system(point2dem_cmd)