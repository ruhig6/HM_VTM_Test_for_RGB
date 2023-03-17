# HM-VTM-Test-for-RGB

## Datasets
* 1080p: UVG

1. Crop 1080p to 1920*1024 via ffmpeg

```
ffmpeg -pix_fmt yuv420p  -s 1920x1080 -i  BasketballDrive_1920x1080_50.yuv -vf crop=1920:1024:0:0 BasketballDrive_1920x1024_50.yuv
```

2. Convert YUV420 to PNG

```
ffmpeg -pix_fmt yuv420p -s 1920x1024 -i BasketballDrive_1920x1024_50.yuv -f image2 BasketballDrive_1920x1024_50/im%03d.png
```

3. Convert PNG to YUV444 10le

```
ffmpeg -hide_banner -framerate 120.0 -i BasketballDrive_1920x1024_50/im%03d.png -pix_fmt yuv444p10le -vf scale=out_color_matrix=bt709 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -y /savepath
```

Above operatins can be realized by ```convert.py``` for videos.

## Test

* A spare CPU is needed for fair time comparison.
1. Just run for three steps: Code and recover YUV444 10le, Convert YUV444 10le to PNG, Evaluate by PSNR and MS-SSIM. Attention to modify path and cfg.

```
python run.py -d hevcB -r 1920x1024 -q 22
```

2. Use the corresponding cfg for LD or RA mode of HM/VTM. QP = 22,27,32,37.
