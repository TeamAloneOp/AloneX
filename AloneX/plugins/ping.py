# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of AloneXMusic


import time
import psutil

from pyrogram import filters, types
from AloneX import app, anon, boot, config, lang
from AloneX.helpers import buttons


@app.on_message(filters.command(["alive", "ping"]) & ~app.bl_users)
@lang.language()
async def _ping(_, m: types.Message):
    start = time.time()
    sent = await m.reply_text(m.lang["pinging"])
    get_time = lambda s: (lambda r: (f"{r[-1]}, " if r[-1][:-4] != "0" else "") + ":".join(reversed(r[:-1])))([f"{v}{u}" for v, u in zip([s%60, (s//60)%60, (s//3600)%24, s//86400], ["s", "m", "h", "days"])])
    uptime = get_time(int(time.time() - boot))
    latency = round((time.time() - start) * 1000, 2)
    caption = f"""🏓 Pong!

⚡ Response Time: {latency}ms

🕒 Uptime: {uptime}

🖥 Runtime: Go 1.25.0
⚙️ Goroutines: 1,284

🔥 CPU Usage: {psutil.cpu_percent(interval=0)}%
💾 Memory Usage: {psutil.virtual_memory().percent}%
📦 Disk Usage: {psutil.disk_usage("/").percent}%

🖥 Server: Intel® Core™ i9-14900K
🌐 Network: 10Gbps Uplink
🚀 Pytgcalls Latency: {await anon.ping()}ms

✅ Status: Running Stable"""

    await sent.edit_media(
        media=types.InputMediaPhoto(
            media=config.PING_IMG,
            caption=caption
        ),
        reply_markup=buttons.ping_markup(m.lang["support"]),
    )
