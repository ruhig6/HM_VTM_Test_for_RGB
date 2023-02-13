import os

num = 7
video_name = ['Beauty_1920x1080_120fps_420_8bit_YUV.yuv', 'HoneyBee_1920x1080_120fps_420_8bit_YUV.yuv', 'ReadySteadyGo_1920x1080_120fps_420_8bit_YUV.yuv',  'YachtRide_1920x1080_120fps_420_8bit_YUV.yuv', 'Bosphorus_1920x1080_120fps_420_8bit_YUV.yuv',  'Jockey_1920x1080_120fps_420_8bit_YUV.yuv', 'ShakeNDry_1920x1080_120fps_420_8bit_YUV.yuv']
short = ['Beauty', 'HoneyBee', 'ReadySteadyGo', 'YachtRide', 'Bosphorus', 'Jockey', 'ShakeNDry']
video_crop_name = ['Beauty_1920x1024_120fps_420_8bit_YUV.yuv', 'HoneyBee_1920x1024_120fps_420_8bit_YUV.yuv', 'ReadySteadyGo_1920x1024_120fps_420_8bit_YUV.yuv',  'YachtRide_1920x1024_120fps_420_8bit_YUV.yuv', 'Bosphorus_1920x1024_120fps_420_8bit_YUV.yuv',  'Jockey_1920x1024_120fps_420_8bit_YUV.yuv', 'ShakeNDry_1920x1024_120fps_420_8bit_YUV.yuv']
png_crop444_name = ['Beauty_1920x1024_120fps_444_10bit_YUV.yuv', 'HoneyBee_1920x1024_120fps_444_10bit_YUV.yuv', 'ReadySteadyGo_1920x1024_120fps_444_10bit_YUV.yuv',  'YachtRide_1920x1024_120fps_444_10bit_YUV.yuv', 'Bosphorus_1920x1024_120fps_444_10bit_YUV.yuv',  'Jockey_1920x1024_120fps_444_10bit_YUV.yuv', 'ShakeNDry_1920x1024_120fps_444_10bit_YUV.yuv']

# for i in range(num):
#     saveroot = 'images/' + short[i]
#     savepath = 'images/' + short[i] + '/im%03d.png'
#     if not os.path.exists(saveroot):
#         os.makedirs(saveroot)
#     print('ffmpeg -y -pix_fmt yuv420p -s 1920x1024 -i ' + 'videos_crop/' + video_name[i] +  ' ' + savepath)
#     os.system('ffmpeg -y -pix_fmt yuv420p -s 1920x1024 -i ' + 'videos_crop/' + video_name[i] +  ' ' + savepath)

for i in range(num):
    savepath = './rgb_crop444/' + png_crop444_name[i]
    os.system('ffmpeg -hide_banner -framerate 120.0 -i ' + './GT/' + short[i] + '/im%03d.png -pix_fmt yuv444p10le -vf scale=out_color_matrix=bt709 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -y ' + savepath)
