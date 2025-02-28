import uvicorn
import socket
import webbrowser
from fastapi import FastAPI
import base64
import ddddocr
from io import BytesIO
from PIL import Image
from fastapi.responses import HTMLResponse
from pydantic import BaseModel,Field
from typing import Union


description = """
_________________
### 项目说明：

* <strong>会HttpPost协议即可调用的原则！</strong>

* 支持部署 <strong>本地</strong> 和 <strong>服务器</strong> .

* <strong>长期更新 免费开源 欢迎赞助 </strong>

### 关于作者：

* 哔哩哔哩 <https://space.bilibili.com/37887820>

* GitHub <https://github.com/81NewArk/StupidOCR>
 
### 项目依赖：DDDDOCR+FastApi
_________________
"""

app = FastAPI(
    title='StupidOCR',
    description=description,
    version="1.0.7",
     )





class Model_Common_VerificationCode(BaseModel):
    ImageBase64: str

@app.post("/api.Common_VerificationCode", tags=["通用验证码识别"],summary='文字验证码',description='上传图片Base64编码')
async def Common_VerificationCode(item: Model_Common_VerificationCode):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    ocr = ddddocr.DdddOcr(show_ad=False)
    res = ocr.classification(base64.b64decode(item.ImageBase64))
    return {"result":res}







class Model_Arithmetic_VerificationCode(BaseModel):
    ImageBase64: str

@app.post("/api.Arithmetic_VerificationCode", tags=["通用验证码识别"],summary='算术验证码',description='上传图片Base64编码')
async def Common_VerificationCode(item: Model_Arithmetic_VerificationCode):
    ocr = ddddocr.DdddOcr(show_ad=False)
    res = ocr.classification(base64.b64decode(item.ImageBase64))
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(res)
    if "+" or '-' or 'x' or '/' or "÷" or "*" not in res:
        result= "error"
    if '+' in res:
        result = int(res.split('+')[0]) + int(res.split('+')[1][:-1])
    if '-' in res:
        result = int(res.split('-')[0]) - int(res.split('-')[1][:-1])
    if 'x' in res:
        result = int(res.split('x')[0]) * int(res.split('x')[1][:-1])
    if 'X' in res:
        result = int(res.split('X')[0]) * int(res.split('X')[1][:-1])
    if '÷' in res:
        result = int(res.split('÷')[0]) / int(res.split('÷')[1][:-1])
    if '*' in res:
        result = int(res.split('*')[0]) * int(res.split('*')[1][:-1])

    return {"result":result}







class Model_Move_Slider(BaseModel):
    MovePicture: str
    Background: str

@app.post("/api.Slider_Move",summary='缺口为滑动的单独图片，返回坐标', description='识别模式1：缺口图片为单独图片', tags=['滑块验证码识别'])
async def Common_VerificationCode(item: Model_Move_Slider):
    ocr = ddddocr.DdddOcr(show_ad=False)
    result = ocr.slide_match(base64.b64decode(item.MovePicture), base64.b64decode(item.Background),simple_target=True)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    return{"result":result}







class Model_Comparison_Slider(BaseModel):
    HaveGap_ImageBase64: str
    Full_ImageBase64: str

@app.post("/api.Slider_Comparison", summary='缺口原图和完整原图对比识别，无单独滑动的缺口图片，返回坐标', description='识别模型2：一张为有缺口原图，一张为完整原图',tags=['滑块验证码识别'])
async def Comparison_Slider(item: Model_Comparison_Slider):
    ocr = ddddocr.DdddOcr(det=False, ocr=False)
    result = ocr.slide_comparison(base64.b64decode(item.HaveGap_ImageBase64), base64.b64decode(item.Full_ImageBase64))

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    return{"result":result}







class Model_Text_Choose_Click(BaseModel):
    ChoiceClick_ImageBase64: str

@app.post("/api.Text_Choose_Click", summary='文字选点验证码识别，返回坐标', description='选点识别返回坐标', tags=['选点类验证码识别'])
async def Text_Choose_Click(item: Model_Text_Choose_Click):
    ocr1 = ddddocr.DdddOcr(show_ad=False)
    ocr2 = ddddocr.DdddOcr(det=True, show_ad=False)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    res = ocr2.detection(base64.b64decode(item.ChoiceClick_ImageBase64))
    img = Image.open(BytesIO(base64.b64decode(item.ChoiceClick_ImageBase64)))
    res = ocr2.detection(base64.b64decode(item.ChoiceClick_ImageBase64))
    result = {}
    for box in res:
        x1, y1, x2, y2 = box
        result[ocr1.classification(img.crop(box))] = [ x1+(x2-x1)//2,y1+(y2-y1)//2]  # 文字位置
    return{"result":result}









class Model_ICO_Choose_Click(BaseModel):
    ICO_ChooseClick_ImageBase64: str
    Background_ImageBase64: str

@app.post("/api.Icon_Choose_Click", summary='图标点选验证码，返回坐标', description='点选识别返回坐标', tags=['选点类验证码识别'])
async def ICO_Choose_Click(item: Model_ICO_Choose_Click):
    ocr = ddddocr.DdddOcr(show_ad=False)
    result = ocr.slide_match(base64.b64decode(item.ICO_ChooseClick_ImageBase64), base64.b64decode(item.Background_ImageBase64),simple_target=True)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return {"result":result}








class Model_Target_Detection(BaseModel):
    ImageBase6: str

@app.post("/api.Target_Detection", summary='扩展功能f，可用返回的坐标截取图片', description='检查图片内的文字 图标，返回坐标', tags=['扩展功能，目标侦察'])
async def Target_Detection(item:Model_Target_Detection):
    ocr = ddddocr.DdddOcr(det=True)
    result = ocr.detection(base64.b64decode(item.ImageBase64))
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return {"result":result}





@app.get("/support", response_class=HTMLResponse,tags=['赞助StupidOCR'],summary='打开网页：http://localhost:6688/support',include_in_schema=False)
async def support():
    return """
<html>
   <head>
    <title>赞助作者</title>
   </head>
    <body>
    <h1 align="center">给无业的作者打赏</h1>
    <h3 align="center">微信&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;支付宝</h3>
    <h1 align="center"> <img  src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZAAAAGQCAIAAAAP3aGbAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAABcRAAAXEQHKJvM/AAAoZUlEQVR42u3dfZgcVZ0v8N85Vd097y/MTEIgJAqEDEgEVPZCeJGo5NFNxETuI2pm7+oqPoSgrrgLGrzr3mcfXRNkXZXN6ObiFRNE5F4zeokXMhoI5E3AhAB5D0lGMiQzmcm8ZDIzXV11zv2jZyY93V2V6dM11X1S388zT56erq5zTp2u+aaq+vQpJqUkAAAd8EI3AABgohBYAKANBBYAaAOBBQDaQGABgDYQWACgDQQWAGgDgQUA2kBgAYA2EFgAoA0EFgBoA4EFANpAYAGANhBYAKANBBYAaAOBBQDaQGABgDYQWACgDQQWAGgDgQUA2jDzXJ8xVuhNUOR29w1/t8jjHh8eFSncGSSwZiuYO3futm3bAuifYtgbA7irSzFsppr8OwdHWACgDQQWAGgDgQUA2kBgAYA2EFgAoA0EFgBoA4EFANpAYAGAPmR+Jq9kXwTTvCVLlijUUuh33udOWLNmTaG3xmuLCt4/K1as8KuiYBqsbFKbhyMsANAGAgsAtIHAAgBtILAAQBsILADQBgILALSBwAIAbeQ7gR+ETUtLS9bn//znPxe6aV7NK3gtu3fvVihw0aJFAWyORpjMbwSj2rSZms7qWXCNjY379+8v7OYUvEsfeuih7373u8FsrPR1alO30urr67u7uye+Spj/6HBKCADaQGABgDYQWACgDQQWAGgDgQUA2kBgAYA2EFgAoA0MHE23cOFCt0XPPPOMj6V5cKuovb3dx4oOHDhwxRVXqPVSANy2yG0kmr5Onz5d6CZoAwNH/dkif7fUrSKPgaOBKeYRqr7fwz2YnQQDRycOp4QAoA0EFgBoA4EFANpAYAGANhBYAKANBBYAaAOBBQDaQGClc7vl7IYNG1jufL93bq7N1nGeQmW+347Yx1VWrlzptpN0d3fjvZsgBBYAaAOBBQDaQGABgDYQWACgDQQWAGgDgQUA2kBgAYA2EFgAoI3CzDh6/o2IC2amt3379rktCmx6NgVz587dtm1bAG1Q6O2WlpZimLLRbS0f34jz448OR1gAoA0EFgBoA4EFANpAYAGANhBYAKANBBYAaAOBBQDawJ2f061cuTLr8wcPHlRYS22VBx54IOvzjzzyiOM4BewEj7a99NJLboOtPG5YreDpp58+cuSIX1u0e/duhbXcOgEmndqUmOfBjIg+Tk25ZMkShe5VqGj27NnBVKSwypo1a4KpaPny5cFUtGDBgmB6u66uLqdVSFsybzglBABtILAAQBsILADQBgILALSBwAIAbSCwAEAbCCwA0AYGjuagvr4+6/M9PT25rqJWUXd3t78V+di2eDweTAM2bdqk0LxgOgEmXf5DuUJiw4YNwfT8qlWrivndL3hp3gNHfWxbYJ0AE4dTQgDQBgILALSBwAIAbSCwAEAbCCwA0AYCCwC0gcACAG0UYOBoS0vL4sWL3ZbK3G+hrEahIunrfYB93yIfKXTC2rVrA+s6hffO37b52+z6+nqPIcFF22yF0vJvM46wAEAbCCwA0AYCCwC0gcACAG0gsABAGwgsANAGAgsAtJHvOKzW1tZcV/GegC0wCi13s2XLlsHBwUJvUIF1dHQEVpeP710xSCQShW6CPvKcTyuw9vi7Cbnea9ebx52f/W32+XfnZwVqd372l8LbTUp3fi74lhYbnBICgDYQWACgDQQWAGgDgQUA2kBgAYA2EFgAoA0EFgBoo+ju/NzU1ORXUY899tjzzz+fddHAwIBCA9auXZv1+V27dvnYA08++eT69euzLjp+/LiPFflrx44dCmsp9LZygblWdP/993d2dvrWQe489kYF3/rWt44ePZrTltIkvBGTJfihX+vWrQumnStWrFAoUGEVfweOet/5WaEfgukEtYGjgW2pQkULFixQaJtCRf4OHPXYG/1tdkHglBAAtIHAAgBtILAAQBsILADQBgILALSBwAIAbSCwAEAfeQ6LUChZbRyWv5tQDFOm+bux/nap7/ztumC61GMcVjF3QmA8ppOcvB7AERYAaAOBBQDaQGABgDYQWACgDQQWAGgDgQUA2kBgAYA2EFgAoI88x3EF1p5i7hC1CfwC6x+3VZYtW6bQCf52XZC7VmF7218bNmzwtw3BlJb/huMICwC0gcACAG0gsABAGwgsANAGAgsAtIHAAgBtILAAQBtFd+dnHbW1tQVWV3Nzs19FHT58OJi2bd26de7cuZPaLcWvtbX10KFDWRe9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" >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    <img  src="data:image/png;base64,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" ></h1>
    <hr>
    <h2 align="left"> GitHub： <a href="https://github.com/81NewArk/StupidOCR">https://github.com/81NewArk/StupidOCR</a></h2>
    <h2 align="left"> BiLiBiLi： <a href="https://space.bilibili.com/37887820">https://space.bilibili.com/37887820</a></h2>
    <h2 align="left"> E-Mail  ： 751247667@qq.com</h2>
    </body>
</html>
         """

if __name__ == '__main__':
    print('''

   _____   _                     _       _    ____     _____   _____  
  / ____| | |                   (_)     | |  / __ \   / ____| |  __ \ 
 | (___   | |_   _   _   _ __    _    __| | | |  | | | |      | |__) |
  \___ \  | __| | | | | | '_ \  | |  / _` | | |  | | | |      |  _  / 
  ____) | | |_  | |_| | | |_) | | | | (_| | | |__| | | |____  | | \ \ 
 |_____/   \__|  \__,_| | .__/  |_|  \__,_|  \____/   \_____| |_|  \_/
                        | |                                           
                        |_|                                           

                开发文档：http://localhost:6688/docs
                赞助页面：http://127.0.0.1:6688/support

                代码编写：81NewArk
 
    ''')
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    webbrowser.open("http://"+ip+":6688/support")
    webbrowser.open("http://localhost:6688/docs")
    uvicorn.run(app, port=6688, host="0.0.0.0")
