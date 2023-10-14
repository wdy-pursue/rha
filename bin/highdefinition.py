# controlnet + img2img
# enable `Allow other script to control this extension` in settings
import requests
import io, base64
from PIL import Image,PngImagePlugin
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os
import json
from gradio_client import Client
from args import args
import random

rootpath = os.getcwd()
SourcePath = os.path.join(rootpath,"草图")
RepaintPath = os.path.join(rootpath,"结果图")
EnlargePath = os.path.join(rootpath,"高清化结果图循环上传区")
JsonPath = os.path.join(rootpath, "config",args.configjson+".json")

def getjson(JsonPath):
    with open(JsonPath, "r", encoding="utf-8") as f:
        launcher = json.load(f)
    return launcher
# config_json = getjson(JsonPath)
def get_pnginfo(localpath):
    print("正在获取图片pnginfo")
    def image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return encoded_string.decode("utf-8")  # 将bytes转换为字符串

    def getinfo(image_path,count):
        if(count is None):
            count = 15
        elif(count == ''):
            count = 15
        elif(count>15):
            count = 15
        response = requests.post(config_json['反推网址'], json={
            "data": [
            "data:image/png;base64,{}".format(image_to_base64(image_path)),
            random.choice(config_json['反推模型']),
            0.35,
            0.85,
        ]}).json()
        return ",".join(response['data'][0].split(",")[:count]) if len(response['data'][0].split(","))>count else response['data'][0]
    resdist_prompt = {}
    resdist_base64 = {}
    resdist_model = {}
    # 遍历文件夹，获取所有文件的prompt，返回字典类型
    for dirpath, dirnames, filenames in os.walk(localpath):
        for filepath in filenames:
            if filepath.endswith(".png"):
                print(filepath.split(".")[0])
                resdist_prompt[filepath.split(".")[0]] = getinfo(os.path.join(dirpath, filepath),config_json['反推prompt数量'])
                resdist_base64[filepath.split(".")[0]] = image_to_base64(os.path.join(dirpath, filepath))
                resdist_model[filepath.split(".")[0]] =  os.path.basename(dirpath)
                if not os.path.exists(os.path.join(RepaintPath,filepath.split(".")[0])):
                    os.makedirs(os.path.join(RepaintPath,filepath.split(".")[0]))
                if not os.path.exists(os.path.join(RepaintPath,filepath.split(".")[0],"重绘结果图暂存")):
                    os.makedirs(os.path.join(RepaintPath,filepath.split(".")[0],"重绘结果图暂存"))
    return resdist_prompt,resdist_base64,resdist_model
    
class controlnetRequest():
    def __init__(self, config_json,png_prompt,png_base64,batch_size,n_iter,redraw_amplitude):
        def image_to_base64(image_path):
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                return encoded_string.decode("utf-8")  # 将bytes转换为字符串
        self.headers = {
            "Authorization": config_json['秘钥']
        }
        lorastr = [0,True]
        for i in range(int(len(config_json['lora模型'])/3)):
            lorastr.append(True)
            lorastr.append("LoRA")
            lorastr.append(config_json['lora模型'][3*i+0])
            lorastr.append(config_json['lora模型'][3*i+1])
            lorastr.append(config_json['lora模型'][3*i+2])
            # 两个1都为权重值，一般只用到第一个
            # 如果有多个lora，重复后面五个
        controlnet_args = []
        for i in range(len(config_json['controlnet'])):
            input_image = png_base64
            if "图片路径" in config_json['controlnet'][i]:
                if config_json['controlnet'][i]['图片路径'] != '':
                    input_image = image_to_base64(config_json['controlnet'][i]['图片路径'])
            controlnet_dist ={
                        "enabled": True,
                        "input_image": input_image,
                        "mask": "",  # 图片遮罩，一般不用
                        "module": config_json['controlnet'][i]['模式'],  # 模式 openpose、canny等
                        "control_mode": args.control_methods,# 0 或 Balanced：平衡，对提示和控制模型没有偏好
                                          # 1 或 My prompt is more important：提示比模型更有影响力
                                          # 2 或 ControlNet is more important：控制网络模型比提示更有影响力
                        "model": config_json['controlnet'][i]['模型'],  # 模型
                        "weight": config_json['controlnet'][i]['权重'],  # 权重
                        "resize_mode": config_json['controlnet'][i]['缩放模式'],  # 如何调整输入图像以适应生成的输出分辨率。默认为 Scale to Fit (Inner Fit)。接受的值为：
                        # 0 或 Just Resize：只需将图像调整为目标宽度/高度
                        # 1 或 Scale to Fit (Inner Fit)：按比例缩放和裁剪以适应最小尺寸。保持比例。
                        # 2 或 Envelope (Outer Fit)：按比例缩放以适应最大尺寸。保持比例。
                        "lowvram": "true" == config_json['controlnet'][i]['低显存模式'].lower(),  # 低显存需要开启,如果你的显卡内存小于等于4GB，建议勾选此选项。
                        # 下面的不常用
                        "processor_res": 512,# 预处理器的分辨率。默认为 512
                        "threshold_a": 64,# 预处理器的第一个参数。仅在预处理器接受参数时生效。默认为 64
                        "threshold_b": 64,# 预处理器的第二个参数。仅在预处理器接受参数时生效。默认为 64
                        "guidance": 1,
                        "guidance_start": config_json['controlnet'][i]['引导介入时机'],
                        # 在理解此功能之前，我们应该先知道生成图片的 Sampling steps 采样步数功能，步数代表生成一张图片要刷新计算多少次，Guidance Start(T) 设置为 0 即代表开始时就介入，默认为 0，设置为 0.5 时即代表 ControlNet 从 50% 步数时开始介入计算。
                        "guidance_end": config_json['controlnet'][i]['引导终止时机'],
                        # 和引导介入时机相对应，如设置为1，则表示在100%计算完时才会退出介入也就是不退出，默认为 1，可调节范围 0-1，如设置为 0.8 时即代表从80% 步数时退出介入。
                        "guessmode": False,  # 也就是盲盒模式，不需要任何正面与负面提示词，出图效果随机
                        "rgbbgr_mode": False,  # 把颜色通道进行反转，在 NormalMap 模式可能会用到。
                        "pixel_perfect": "true" == config_json['controlnet'][i]['完美像素模式'].lower() # 启用像素完美的预处理器。默认为false
                    }
            controlnet_args.append(controlnet_dist)
        Tiled_Diffusion_payload = {
            "enabled": "true" ==  config_json['tiled_diffusion']['是否启用'].lower(),  # 是否启用
            "method": "Mixture of Diffusers",  # 方案
            "overwrite_size": True,
            "keep_input_size": True,  # 保持输入图像大小
            "image_width": config_json['宽'],
            "image_height": config_json['高'],
            "tile_width": 96,
            "tile_height": 96,
            "overlap": 48,  # 潜空间分块重叠
            "tile_batch_size": 1,  # 潜空间分块单批数量
            "upscaler_name": config_json['tiled_diffusion']['放大算法'],  # 放大算法
            "scale_factor": config_json['tiled_diffusion']['放大倍数'],  # 放大倍数
            "noise_inverse": False,  # 启用噪声反转
            "noise_inverse_steps": 30,  # 反转步数
            "noise_inverse_retouch": 1,  # 修复程度
            "noise_inverse_renoise_strength": 1,  # 重铺噪声强度
            "noise_inverse_renoise_kernel": 64,  # 重铺噪声大小
            "control_tensor_cpu": False,  # 将controlne tensor移至cpu
            "enable_bbox_control": False,
            "draw_background": False,
            "causal_layers": False,
            "bbox_control_states": []
        }
        Tiled_VAE_payload = {
            "enabled": "true" == config_json['tiled_vae'].lower(),
            "encoder_tile_size": 2800,
            "decoder_tile_size": 192,
            "vae_to_gpu": True,  # 将vae移至gpu
            "fast_decoder": True,
            "fast_encoder": True,
            "color_fix": False
        }
        Tiled_Diffusion_payload_list = list(Tiled_Diffusion_payload.values())
        Tiled_VAE_payload_list = list(Tiled_VAE_payload.values())
        self.url = config_json['网址'] + "sdapi/v1/img2img"
        self.reloadurl = config_json['网址'] + "sdapi/v1/reload-checkpoint"
        self.unloadurl = config_json['网址'] + "sdapi/v1/unload-checkpoint"
        imgdata = base64.b64decode(png_base64)
        img = Image.open(io.BytesIO(imgdata))
        self.body ={
              "init_images": [
                png_base64 # 输入图片
              ],
              "resize_mode": 2,# 如何调整输入图像以适应生成的输出分辨率。默认为 Scale to Fit (Inner Fit)。接受的值为：
                                    # 0 或 Just Resize：只需将图像调整为目标宽度/高度
                                    # 1 或 Scale to Fit (Inner Fit)：按比例缩放和裁剪以适应最小尺寸。保持比例。
                                    # 2 或 Envelope (Outer Fit)：按比例缩放以适应最大尺寸。保持比例。
              "denoising_strength": redraw_amplitude, # 重绘幅度
              "image_cfg_scale": 0,
              # "mask": "",# 图片遮罩，一般不用
              "mask_blur": 0,
              "mask_blur_x": 4,
              "mask_blur_y": 4,
              "inpainting_fill": 0,
              "inpaint_full_res": True,
              "inpaint_full_res_padding": 0,
              "inpainting_mask_invert": 0,
              "initial_noise_multiplier": 0,
              "prompt": config_json['正咒']+" " + png_prompt,                  #正向提示词
              "negative_prompt": config_json['正咒']+" ",  # 负面提示词
              "styles": [
                ""
              ],
              "seed": -1, # 随机数种子
              "subseed": -1,
              "subseed_strength": 0,
              "seed_resize_from_h": -1,
              "seed_resize_from_w": -1,
              "sampler_name": "",
              "batch_size": batch_size, # 单批数量
              "n_iter": n_iter, # 总批次数
              "steps": config_json['步数'], # 步数
              "cfg_scale": 7, # 提示词引导系数，1.忽视prompt，3.更有创意，7，在prompt和freedom中取得平衡，15，遵守prompt，30，严格按照prompt
              "width": img.size[0]*2, # 宽
              "height": img.size[1]*2, # 高
              "restore_faces": False, # 脸部修复
              "tiling": False, # 可平铺
              "do_not_save_samples": False,
              "do_not_save_grid": False,
              "eta": 0,
              "s_min_uncond": 0,
              "s_churn": 0,
              "s_tmax": 0,
              "s_tmin": 0,
              "s_noise": 1,
              "override_settings": {
                            "sd_model_checkpoint": config_json['ckpt模型'],  # ckpt模型
                            "sd_vae": config_json['vae模型']                                # vae模型
              },
              "override_settings_restore_afterwards": True,
              "script_args": lorastr, # lora
              "sampler_index": config_json['采样方法'], # 采样方法
              "include_init_images": False,
              "script_name": "",
              "send_images": True,
              "save_images": False,
              "alwayson_scripts": {
                        "controlnet":{
                        "args": controlnet_args},
                        "Tiled Diffusion": {
                        "args": Tiled_Diffusion_payload_list
                        },
                        "Tiled VAE": {
                        "args": Tiled_VAE_payload_list
            }
              }
            }
    def sendRequest(self):
        r = requests.post(self.url, json=self.body,headers=self.headers,verify=False)
        u = requests.post(self.unloadurl,headers=self.headers)
        d = requests.post(self.reloadurl,headers=self.headers)
        return r.json()

# 读取配置文件
config_json = getjson(JsonPath)
# 获取图片属性
resdist_prompt,resdist_base64,resdist_model = get_pnginfo(EnlargePath)
print(resdist_prompt)
for pngname in resdist_prompt.keys():
    xi = ""
    if "x2" == pngname.split("-")[-1].split(".")[0]:
        png = "-".join(pngname.split("-")[:-2])
        xi = "x4"
        xs = "四倍高清化结果图"
    elif "x4" == pngname.split("-")[-1].split(".")[0]:
        png = "-".join(pngname.split("-")[:-2])
        xi = "x8"
        xs = "八倍高清化结果图"
    else:
        png = "-".join(pngname.split("-")[:-1])
        xi = "x2"
        xs = "二倍高清化结果图"
    print(png + "开始高清化")
    # 初始化文件夹
    if not os.path.exists(os.path.join(RepaintPath, png,"高清化结果图暂存")):
        os.makedirs(os.path.join(RepaintPath, png,"高清化结果图暂存"))
        os.makedirs(os.path.join(RepaintPath, png, "高清化结果图暂存","二倍高清化结果图"))
        os.makedirs(os.path.join(RepaintPath, png, "高清化结果图暂存","四倍高清化结果图"))
        os.makedirs(os.path.join(RepaintPath, png, "高清化结果图暂存","八倍高清化结果图"))
    if(args.redraw_methods == 0):
        fixcount = args.fixcount
        while(fixcount > 0):
            batch_size = 5 if int(fixcount / 5) != 0 else int(fixcount % 5)
            n_iter = int(fixcount / 5) if int(fixcount / 5) != 0 else 1
            # 执行高清化
            js = controlnetRequest(config_json,
                                   resdist_prompt[pngname],
                                   resdist_base64[pngname],
                                   batch_size,
                                   n_iter,
                                   args.redrawcamplitude).sendRequest()
            if "{'error':" in str(js).lower() and "'errors':" in str(js).lower():
                print(js)
            # 遍历文件夹查看当前png最大编号
            maxid = 0
            for dirpath, dirnames, filenames in os.walk(os.path.join(RepaintPath,png,"高清化结果图暂存",xs)):
                for filepath in filenames:
                    if "-".join(filepath.split("-")[:-2]) == png:
                        if maxid<int(filepath.split("-")[-2]):
                            maxid = int(filepath.split("-")[-2])
            for i in range(batch_size*n_iter):
                image = Image.open(io.BytesIO(base64.b64decode(js["images"][i])))
                image.save(os.path.join(RepaintPath,png,"高清化结果图暂存",xs,png + "-" + str(maxid + i + 1))+"-" + xi + ".png")
            fixcount -= 5 * int(fixcount / 5) if int(fixcount / 5) != 0 else int(fixcount % 5)
    elif(args.redraw_methods == 1):
        redrawcamplitude_min = int(10 * float(args.redrawcamplitude.split("-")[0]))
        redrawcamplitude_max = int(10 * float(args.redrawcamplitude.split("-")[1]))
        for i in np.arange(redrawcamplitude_min,redrawcamplitude_max,(redrawcamplitude_max-redrawcamplitude_min)/args.fixcount):
            js = controlnetRequest(config_json,
                                   resdist_prompt[pngname],
                                   resdist_base64[pngname],
                                   1,
                                   1,
                                   round(i/10,2)).sendRequest()
            if "{'error':" in str(js).lower() and "'errors':" in str(js).lower():
                print(js)
            # 遍历文件夹查看当前png最大编号
            maxid = 0
            for dirpath, dirnames, filenames in os.walk(os.path.join(RepaintPath, png, "高清化结果图暂存", xs)):
                for filepath in filenames:
                    if "-".join(filepath.split("-")[:-2]) == png:
                        if maxid < int(filepath.split("-")[-2]):
                            maxid = int(filepath.split("-")[-2])
            image = Image.open(io.BytesIO(base64.b64decode(js["images"][0])))
            image.save(
                os.path.join(RepaintPath, png, "高清化结果图暂存", xs, png + "-" + str(maxid + 1)) + "-" + xi + ".png")
    print(png + "高清化完毕")
if os.path.exists(EnlargePath):
    for dirpath, dirnames, filenames in os.walk(EnlargePath):
        for filepath in filenames:
            os.remove(os.path.join(dirpath,filepath))