"""
Notification System - Placeholder for Telegram alerts and other notifications.

Currently logs alerts to console. Extend with actual Telegram bot integration
by setting TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


async def send_telegram_alert(message: str) -> bool:
    """
    Send alert via Telegram bot (placeholder).

    To enable:
    1. Create a Telegram bot via @BotFather
    2. Get the bot token and your chat ID
    3. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables

    Args:
        message: Alert message to send

    Returns:
        True if sent successfully, False otherwise
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.info(f"[Telegram Placeholder] Alert: {message}")
        return False

    # Uncomment below to enable real Telegram alerts:
    # import httpx
    # url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    # payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(url, json=payload)
    #     return response.status_code == 200

    logger.info(f"[Telegram Placeholder] Would send: {message}")
    return False


async def notify_alert(alert_type: str, confidence: float, camera_id: str):
    """Send notification for a detection alert."""
    emoji_map = {"fire": "🔥", "smoke": "💨", "fall": "🚨"}
    emoji = emoji_map.get(alert_type, "⚠️")

    message = (
        f"{emoji} <b>ALERT: {alert_type.upper()} DETECTED</b>\n"
        f"Camera: {camera_id}\n"
        f"Confidence: {confidence:.0%}\n"
        f"Action required immediately!"
    )

    logger.warning(f"NOTIFICATION: {alert_type.upper()} on {camera_id} ({confidence:.0%})")
    await send_telegram_alert(message)
