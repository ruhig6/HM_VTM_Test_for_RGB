import os
import numpy as np
import math
from PIL import Image
from pytorch_msssim import ms_ssim
import torchvision

QP = 27
# Step1 编解码
print("Step 1 start!")

raw_path = '../../data/MCL/rgb_crop444/'  #测试集
gt_path = '../../data/MCL/images/'  #原图集
rec_path = './results/MCL/rec/RA' + str(QP) +'/' #压缩后的yuv存放路径
png_path = './results/MCL/png/RA' + str(QP) +'/' #分帧后的png存放路径
bin_path = './results/MCL/bin/RA' + str(QP) +'/' #编码后的码流存放路径
log_path = './results/MCL/log/RA' + str(QP) +'/' #编码后的log存放路径

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
    bin_path_final = bin_path + yuv_name
    log_path_final = log_path + yuv_name
    rec_path_final = rec_path + yuv_name + '.yuv'
    print(yuv_name)
    os.system('./bin/TAppEncoderStatic -c ./cfg/1080p/uvg_ssim.cfg -c ./cfg/encoder_randomaccess_main_rext.cfg -q ' + str(QP) + ' -i ' + raw_yuvpath + ' -b ' + bin_path_final + '.bin' + ' > '+ log_path_final +  '.txt')
    os.system('./bin/TAppDecoderStatic'  + ' -b ' + bin_path_final + '.bin' + ' -o ' + rec_path_final  + ' > '+ log_path_final +  '.log')
    
print("Step 1 over!")

# Step2 分帧
print("Step 2 start!")

rec_list = os.listdir(rec_path)
for k in range(len(rec_list)):
    rec_yuvpath = rec_path + rec_list[k]
    yuv_name = raw_list[i].split('.')[0]
    yuv_num = yuv_name.split('_')[0]
    saveroot = png_path + yuv_num
    savepath = saveroot + '/im%03d.png'
    if not os.path.exists(saveroot):
        os.makedirs(saveroot)
    os.system('ffmpeg -y -pix_fmt yuv444p10le -s 1920x1024 -i ' + rec_yuvpath +  ' ' + savepath)
    
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
png_list = os.listdir(png_path)
for m in range(len(png_list)):
    path1 = png_path +  png_list[m] + '/'
    path2 = gt_path + png_list[m] + '/'
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
        f.write(png_list[m])
        f.write(' ' + str(avg_psnr))
        f.write(' ' + str(avg_ssim))
        f.write('\n')

with open(log_path + "results.txt","a") as f:
        f.write("all_videos_avg_results:")
        f.write(' ' + str(all_psnr/len(png_list)))
        f.write(' ' + str(all_ssim/len(png_list)))
    
print("Step 3 over!")
