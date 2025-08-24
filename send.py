# api/send.py
import json
import requests

def handler(request):
    try:
        body = json.loads(request.body)
        message = body.get("message", "")
        
        BOT_TOKEN = "BOT_TOKEN_HERE"
        CHAT_ID   = "-1001500719419"
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
        resp = requests.post(url, data=data)
        
        if resp.status_code == 200:
            return {"status": "success", "message": "تم الإرسال!"}
        else:
            return {"status": "error", "message": resp.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}
