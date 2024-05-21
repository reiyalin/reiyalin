from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage, StickerSendMessage,ImageSendMessage,VideoSendMessage,AudioSendMessage, LocationSendMessage, TemplateSendMessage, CarouselTemplate


line_bot_api = LineBotApi('rspO/Sep7Rv+PMKRrmJhv3G7SyzKiPKrwungfkPyfMYKgVbA9p6OweWH/yJcBJkvsDALay/9kzLQjUGp6vvJxEa7HUEYqHS4+wh5ZvHAO/R796lZeTbD7gCakhgIM6c9gnw2o+NkW9dMz6l2vR40pQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5262424c2dfe1e5b84b054531bbdcf6c')


@csrf_exempt
def callback(request: HttpRequest) -> HttpResponse:
    
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']

        # get request body as text
        body = request.body.decode('utf-8')

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()

        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@handler.add(MessageEvent, message=TextMessage)
def message_text(event: MessageEvent):
    message=event.message.text
    if message=="您好":
        line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage("測試中")
		)
    elif message=="貼圖":
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=2))
    
    elif message == '早安':
        message_multi=[
         TextSendMessage(text='今天又是美好的一天'),
         StickerSendMessage(package_id=8522, sticker_id=16581267),
		]
        line_bot_api.reply_message(event.reply_token,message_multi)
		
    elif message == '定位':
        line_bot_api.reply_message(
			event.reply_token, LocationSendMessage(title='聯成電腦', address='忠孝', latitude=25.041877560752006, longitude=121.55144734602491)) # 更改為自己要傳的位置經緯度
#25.041877560752006, 121.55144734602491