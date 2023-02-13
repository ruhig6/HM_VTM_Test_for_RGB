import os
import numpy as np
import math
from PIL import Image
from pytorch_msssim import ms_ssim
import torchvision

# Step1 编解码
print("Step 1 start!")

raw_path = '../../data/UVG/rgb_crop444/'  #测试集
gt_path = '../../data/UVG/GT/'  #原图集
rec_path = './results/UVG/rec/RA27/' #压缩后的yuv存放路径
bin_path = './results/UVG/bin/RA27/' #编码后的码流存放路径
log_path = './results/UVG/log/RA27/' #编码后的log存放路径

if not os.path.exists(rec_path):
    os.makedirs(rec_path)
if not os.path.exists(bin_path):
    os.makedirs(bin_path)
if not os.path.exists(log_path):
    os.makedirs(log_path)
    
raw_list = os.listdir(raw_path)
for i in range(len(raw_list)):
    raw_yuvpath = raw_path + raw_list[i]
    yuv_name = raw_list[i].split('.')[0]
    yuv_frame = yuv_name.split('_')[3]
    bin_path_final = bin_path + yuv_name
    log_path_final = log_path + yuv_name
    rec_path_final = rec_path + yuv_name + '.yuv'
    print(yuv_name)
    os.system('./bin/TAppEncoderStatic -c ./cfg/UVG/uvg_ssim.cfg -c ./cfg/encoder_randomaccess_main_rext.cfg -i ' + raw_yuvpath + ' -b ' + bin_path_final + '.bin' + ' > '+ log_path_final +  '.txt')
    os.system('./bin/TAppDecoderStatic'  + ' -b ' + bin_path_final + '.bin' + ' -o ' + rec_path_final  + ' > '+ log_path_final +  '.log')
    
print("Step 1 over!")

# Step2 分帧
print("Step 2 start!")

num = 7
video_name = ['Beauty_1920x1024_120fps_444_10bit_YUV.yuv', 'HoneyBee_1920x1024_120fps_444_10bit_YUV.yuv', 'ReadySteadyGo_1920x1024_120fps_444_10bit_YUV.yuv',  'YachtRide_1920x1024_120fps_444_10bit_YUV.yuv', 'Bosphorus_1920x1024_120fps_444_10bit_YUV.yuv',  'Jockey_1920x1024_120fps_444_10bit_YUV.yuv', 'ShakeNDry_1920x1024_120fps_444_10bit_YUV.yuv']
short = ['Beauty', 'HoneyBee', 'ReadySteadyGo', 'YachtRide', 'Bosphorus', 'Jockey', 'ShakeNDry']

for k in range(num):
    saveroot = rec_path + short[k]
    savepath = rec_path + short[k] + '/im%03d.png'
    if not os.path.exists(saveroot):
        os.makedirs(saveroot)
    os.system('ffmpeg -y -pix_fmt yuv444p10le -s 1920x1024 -i ' + rec_path + video_name[k] +  ' ' + savepath)
    
print("Step 2 over!")

# Step3 评价
print("Step 3 start!")

totensor=torchvision.transforms.ToTensor()

def psnr(img1, img2):
    mse = np.mean((img1 / 1. - img2 / 1.) ** 2)
    if mse < 1.0e-10:
        return 100 * 1.0
    return 10 * math.log10(255.0 * 255.0 / mse)

all_psnr = all_ssim = 0

for m in range(num):
    path1 = rec_path +  short[m] + '/'
    path2 = gt_path + short[m] + '/'
    list_psnr = []
    list_ssim = []
    for n in range(1, 97):
        img_a = Image.open(path1 + 'im' + str(n).zfill(3) + '.png')
        img_b = Image.open(path2 + 'im' + str(n).zfill(3) + '.png')
        img_a = np.array(img_a)
        img_b = np.array(img_b)
        psnr_num = psnr(img_a, img_b)
        img_a=totensor(img_a).unsqueeze(0)
        img_b=totensor(img_b).unsqueeze(0)
        ssim_num = ms_ssim(img_a, img_b, data_range=1.0, size_average=True).numpy()
        list_ssim.append(ssim_num)
        list_psnr.append(psnr_num)
    avg_psnr = np.mean(list_psnr)
    avg_ssim = np.mean(list_ssim)
    all_psnr += avg_psnr
    all_ssim += avg_ssim
    with open(log_path + "results.txt","a") as f:
        f.write(short[m])
        f.write(' ' + str(avg_psnr))
        f.write(' ' + str(avg_ssim))
        f.write('\n')

with open(log_path + "results.txt","a") as f:
        f.write("all_videos_avg_results:")
        f.write(' ' + str(all_psnr/num))
        f.write(' ' + str(all_ssim/num))
    
print("Step 3 over!")
