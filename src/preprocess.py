
def convert_jp2_to_tif(left_jp2, right_jp2, left_img, right_img):
    import os
    # Convert JP2 files to TIFF using OpenJPEG
    print("Converting JP2 files to TIFF...")
    os.system(f"opj_decompress -i {left_jp2} -o {left_img}")
    os.system(f"opj_decompress -i {right_jp2} -o {right_img}")
    print("Tiff Conversion completed.")

