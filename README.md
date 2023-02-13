# HM-VTM-Test-for-RGB

## Datasets
1080p: UVG

1. Crop 1080p to 1920*1024 via ffmpeg

```
ffmpeg -pix_fmt yuv420p  -s 1920x1080 -i  BasketballDrive_1920x1080_50.yuv -vf crop=1920:1024:0:0 BasketballDrive_1920x1024_50.yuv
```

2. Convert YUV420 to PNG

```
ffmpeg -pix_fmt yuv420p -s 1920x1024 -i BasketballDrive_1920x1024_50.yuv -f image2 BasketballDrive_1920x1024_50/im%03d.png
```

3. Convert PNG to YUV44410le

```
ffmpeg -hide_banner -framerate 120.0 -i BasketballDrive_1920x1024_50/im%03d.png -pix_fmt yuv444p10le -vf scale=out_color_matrix=bt709 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -y /savepath
```

Above operatins can be realized by ```convert.py``` for videos.
