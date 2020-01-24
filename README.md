# LSMArch
Lightweight scripts for Light Sheet Microscopy image data compression and archiving

# Dependencies:
* Operating System == Windows or Linux
* FFMPEG == 0.4.0 (The version 1.1.0 is also accessible,the original version was writen on 0.4.0)
* Python == 3.6 or 3.7
* numpy == 1.16.2
* h5py == 2.9.0
* Pillow == 6.0.0
* opencv-python == 4.0.1

# Example usage
1.Copy the scripts to the workding directory.  
2.Edit or create the `path.txt` in the same directory of the scripts.  
3.Save the path of FFMPEG executable program in the `path.txt`.  
4.Try the following mode.

## Encoding
`python lsmarch.py --encode -i <input_dir> -o <output_file_name> --crf=<crf_value>`  

The `<output_file_name>` should not contain extensions. If you want to generate `test.lav`, then just input `test`. All kinds of `<file_name>` should be written in this format.
## Decoding
`python lsmarch.py --decode -i <input_lav_file_name> -o <output_dir>`

## Checking compression information
`python lsmarch.py --check -i <lav_file_name>`


