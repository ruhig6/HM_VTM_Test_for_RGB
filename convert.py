import os
def stage1():
    raw_path = './videos/'
    crop_path = './videos_crop/'
    raw_list = os.listdir(raw_path)
    for i in range(len(raw_list)):
        raw_yuvpath = raw_path + raw_list[i]
        yuv_name = raw_list[i].split('.')[0]
        yuv_num = yuv_name.split('_')[0]
        yuv_frame = yuv_name.split('_')[2]
        crop_path_final = crop_path + yuv_num + '_1920x1024_' + yuv_frame + '.yuv'
        print(yuv_name)
        os.system('ffmpeg -pix_fmt yuv420p -s 1920x1080 -i ' + raw_yuvpath + ' -vf crop=1920:1024:0:0 ' + crop_path_final)
    
def stage2():
    crop_path = './videos_crop/'
    crop_list = os.listdir(crop_path)
    for i in range(len(crop_list)):
        crop_yuvpath = crop_path + crop_list[i]
        yuv_name = crop_list[i].split('.')[0]
        yuv_num = yuv_name.split('_')[0]
        saveroot = './images/' + yuv_num
        savepath = './images/' + yuv_num + '/im%03d.png'
        if not os.path.exists(saveroot):
            os.makedirs(saveroot)
        os.system('ffmpeg -y -pix_fmt yuv420p -s 1920x1024 -i ' + crop_yuvpath +  ' ' + savepath)

def stage3():
    png_path = './images/'
    png_list = os.listdir(png_path)
    for i in range(len(png_list)):
        yuv_png_path = png_path + png_list[i]
        savepath = './rgb_crop444/' + png_list[i] + '_1920x1024_30.yuv'
        os.system('ffmpeg -hide_banner -framerate 30.0 -i ' + yuv_png_path + '/im%03d.png -pix_fmt yuv444p10le -vf scale=out_color_matrix=bt709 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -y ' + savepath)

if __name__ == "__main__":
    stage1()
    stage2()
    stage3()
    
