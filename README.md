# LSMArch
Lightweight scripts for Light Sheet Microscopy image data compression and archiving. The compression result will be saved in an LAV file.

# Dependencies:
* Operating System == Windows or Linux
* FFMPEG == 4.2.1
* Python == 3.6 or 3.7
* numpy == 1.16.2
* h5py == 2.9.0
* Pillow == 6.0.0
* opencv-python == 4.0.1

# Example usage
1.Copy the scripts to the workding directory.  
2.Use `divide.py` to divide your image into lower 10-bit part and higher 6-bit part.  
3.Edit or create the `path.txt` in the same directory of the scripts.  
4.Save the path of FFMPEG executable program in the `path.txt`.  
5.Try the following modes.

## Dividing
`python divide.py -i <input_dir> -o <output_dir>`  

For example,
`python divide.py -i wholepics -o testin`  
Then the original images in the `wholepics` will be divided into lower and higher part and saved in `testin` and generates `resize.txt`.

### Explanation for the value in `resize.txt`
* 0 means the original height and width enable compression
* 1 means one row needs to be deleted
* 2 means one column needs to be deleted
* 3 means one column and one row need to be deleted

## How to write `path.txt`
For Windows, it can be `F:/ffmpeg-static/ffmpeg-20190923-3104100-win64-static/bin/ffmpeg.exe` or `F:\\ffmpeg-static\\ffmpeg-20190923-3104100-win64-static\\bin\\ffmpeg.exe`

For Linux, it can be `/home/xxx/ffmpeg-4.2.2-amd64-static/ffmpeg`


## Encoding
`python lsmarch.py --encode -i <input_dir> -o <output_file_name> --crf=<crf_value>`  

For example,  
`python lsmarch.py --encode -i testin -o test --crf=15`  
Then the images that were firstly divided into lower 10-bit part and higher 6-bit part in the `testin` folder will be compressed into `test.lav`.

The `<output_file_name>` should not contain extensions. If you want to generate `test.lav`, then just input `test`. All kinds of `<file_name>` should be written in this format.
## Decoding
`python lsmarch.py --decode -i <input_lav_file_name> -o <output_dir>`  

For example,  
`python lsmarch.py --decode -i test -o crf15out`  
Then the images in `test.lav` will be extracted into directory `crf15out`

## Checking compression information
`python lsmarch.py --check -i <lav_file_name>`  

For example,  
`python lsmarch.py --check -i test`
Then you can check the information in `test.lav`.

