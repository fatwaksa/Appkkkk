const fetch = require('node-fetch');

const BOT_TOKEN = "BOT_TOKEN_HERE";
const CHAT_ID = "-1001500719419";

module.exports = async (req, res) => {
    if(req.method !== 'POST') return res.status(405).json({status:'error', message:'Method Not Allowed'});

    try {
        const data = await req.body; // Vercel يدعم JSON تلقائيًا
        const type = data.type || "";
        const title = data.title || "";
        const story = data.story || "";
        const episode = data.episode || "";
        const image_url = data.image_url || "";
        const improvements = data.improvements || "";

        let msgText = `<b>${type.toUpperCase()}: ${title}</b>\n${story}`;
        if(type === "series" && episode) msgText += `\nالحلقة: ${episode}`;
        if(improvements) msgText += `\n💡 تحسينات: ${improvements}`;

        let telegramResp;
        if(image_url){
            telegramResp = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto`, {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body: JSON.stringify({chat_id: CHAT_ID, caption: msgText, photo: image_url, parse_mode:"HTML"})
            });
        } else {
            telegramResp = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body: JSON.stringify({chat_id: CHAT_ID, text: msgText, parse_mode:"HTML"})
            });
        }

        if(telegramResp.ok){
            res.status(200).json({status:"success", message:"تم الإرسال بنجاح!"});
        } else {
            const text = await telegramResp.text();
            res.status(500).json({status:"error", message:text});
        }

    } catch(e){
        res.status(500).json({status:"error", message:e.toString()});
    }
};
