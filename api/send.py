# api/send.py
import json
import requests
import base64

BOT_TOKEN = "BOT_TOKEN_HERE"
CHAT_ID   = "-1001500719419"

def handler(request):
    try:
        # تحويل request.body إلى string
        body_text = None
        if hasattr(request, "body"):
            if isinstance(request.body, bytes):
                body_text = request.body.decode()
            elif isinstance(request.body, str):
                body_text = request.body
        if not body_text:
            return {"status": "error", "message": "لم يتم إرسال بيانات صالحة"}

        data = json.loads(body_text)

        type_ = data.get("type")
        title = data.get("title", "")
        story = data.get("story", "")
        episode = data.get("episode", "")
        image_base64 = data.get("image", None)

        msg_text = f"<b>{type_.upper()}: {title}</b>\n{story}"
        if type_ == "series" and episode:
            msg_text += f"\nالحلقة: {episode}"

        if image_base64:
            header, encoded = image_base64.split(",",1)
            img_bytes = base64.b64decode(encoded)
            files = {"photo": ("image.jpg", img_bytes)}
            resp = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                data={"chat_id": CHAT_ID, "caption": msg_text, "parse_mode":"HTML"},
                files=files
            )
        else:
            resp = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": msg_text, "parse_mode":"HTML"}
            )

        if resp.status_code == 200:
            return {"status":"success","message":"تم الإرسال بنجاح!"}
        else:
            return {"status":"error","message":resp.text}
    except Exception as e:
        return {"status":"error","message": str(e)}
