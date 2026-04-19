# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of AloneXMusic
# ALONE-CODER

import json
import hashlib
import base64
import zlib
import sys
from functools import wraps
from pathlib import Path

from pyrogram import errors

from AloneX import db, logger

lang_codes = {
    "ar": "Arabic",
    "de": "German",
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "hi": "Hindi",
    "ja": "Japanese",
    "my": "Burmese",
    "pa": "Punjabi",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh": "Chinese",
}


class Language:
    """
    Language class for managing multilingual support using JSON language files.
    """

    def __init__(self):
        self.lang_codes = lang_codes
        self.lang_dir = Path("AloneX/locales")
        self.languages = self.load_files()

    def load_files(self):
        languages = {}
        lang_files = {file.stem: file for file in self.lang_dir.glob("*.json")}
        for lang_code, lang_file in lang_files.items():
            if lang_code == "en":
                with open(lang_file, "r", encoding="utf-8") as file:
                    data = file.read()

                # Verify SHA256 integrity
                actual_hash = hashlib.sha256(data.encode()).hexdigest()
                expected_hash = (
                    "49bf6fbd3eb313e846fa83be907edd32a2bf42e9618e9712bd5c26d815fb7d86"
                )

                if actual_hash != expected_hash:
                    logger.critical(
                        f"Integrity check failed for English localization file: {lang_file}"
                    )
                    sys.exit(1)

                try:
                    # Decode base64 and decompress with zlib
                    decoded_data = base64.b64decode(data)
                    decompressed_data = zlib.decompress(decoded_data)
                    languages[lang_code] = json.loads(
                        decompressed_data.decode("utf-8")
                    )
                except Exception as e:
                    logger.critical(
                        f"Failed to decode English localization file: {lang_file}. Error: {e}"
                    )
                    sys.exit(1)
            else:
                with open(lang_file, "r", encoding="utf-8") as file:
                    languages[lang_code] = json.load(file)
        logger.info(f"Loaded languages: {', '.join(languages.keys())}")
        return languages

    async def get_lang(self, chat_id: int) -> dict:
        lang_code = await db.get_lang(chat_id)
        return self.languages[lang_code]

    def get_languages(self) -> dict:
        files = {f.stem for f in self.lang_dir.glob("*.json")}
        return {code: self.lang_codes[code] for code in sorted(files)}

    def language(self):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                fallen = next(
                    (
                        arg
                        for arg in args
                        if hasattr(arg, "chat") or hasattr(arg, "message")
                    ),
                    None,
                )

                if not fallen.from_user:
                    return

                if hasattr(fallen, "chat"):
                    chat = fallen.chat
                elif hasattr(fallen, "message"):
                    chat = fallen.message.chat

                if chat.id in db.blacklisted:
                    logger.warning(f"Chat {chat.id} is blacklisted, leaving...")
                    return await chat.leave()

                lang_code = await db.get_lang(chat.id)
                lang_dict = self.languages[lang_code]

                setattr(fallen, "lang", lang_dict)
                try:
                    return await func(*args, **kwargs)
                except (errors.Forbidden, errors.exceptions.Forbidden):
                    logger.warning(f"Cannot write to chat {chat.id}, leaving...")
                    return await chat.leave()

            return wrapper

        return decorator
