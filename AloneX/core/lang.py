# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of AloneXMusic
#ALONE-CODER

import base64
import json
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
    Language class for managing multilingual support using encrypted language files.
    """

    def __init__(self):
        self.__key = b"ALONE-CODER"
        self.lang_codes = lang_codes
        self.lang_dir = Path("AloneX/locales")
        self.languages = self.load_files()

    def _decrypt(self, data: bytes) -> str:
        try:
            decoded = base64.b64decode(data)
            decrypted = bytes(
                [decoded[i] ^ self.__key[i % len(self.__key)] for i in range(len(decoded))]
            )
            return decrypted.decode("utf-8")
        except Exception as e:
            raise ValueError(f"Failed to decrypt language file: {e}")

    def load_files(self):
        languages = {}
        lang_files = {file.stem: file for file in self.lang_dir.glob("*.alone")}
        for lang_code, lang_file in lang_files.items():
            try:
                with open(lang_file, "rb") as file:
                    encrypted_data = file.read()
                decrypted_content = self._decrypt(encrypted_data)
                languages[lang_code] = json.loads(decrypted_content)
            except Exception as e:
                logger.error(f"Error loading language file {lang_file}: {e}")
                raise e
        logger.info(f"Loaded languages: {', '.join(languages.keys())}")
        return languages

    async def get_lang(self, chat_id: int) -> dict:
        lang_code = await db.get_lang(chat_id)
        return self.languages[lang_code]

    def get_languages(self) -> dict:
        files = {f.stem for f in self.lang_dir.glob("*.alone")}
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
