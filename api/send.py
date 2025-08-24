# api/send.py
import json
import requests
import base64
from vercel import Response

BOT_TOKEN = "BOT_TOKEN_HERE"
CHAT_ID = "-1001500719419"

def handler(request):
    try:
        # Vercel يعطي request.body كـ bytes أو str
        body_text = request.body.decode("utf-8") if isinstance(request.body, bytes) else request.body
        data = json.loads(body_text)

        type_ = data.get("type", "")
        title = data.get("title", "")
        story = data.get("story", "")
        episode = data.get("episode", "")
        image_base64 = data.get("image", None)

        msg_text = f"<b>{type_.upper()}: {title}</b>\n{story}"
        if type_ == "series" and episode:
            msg_text += f"\nالحلقة: {episode}"

        # إرسال صورة إذا موجودة
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
            return Response(json={"status":"success","message":"تم الإرسال بنجاح!"}, status=200)
        else:
            return Response(json={"status":"error","message":resp.text}, status=500)

    except Exception as e:
        return Response(json={"status":"error","message": str(e)}, status=500)
