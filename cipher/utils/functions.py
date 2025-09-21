# Cipher-Bot
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Module: cipher.utils.functions
Utility functions to reduce duplicate code, so its easier to edit in case of bugs/errors
"""

from typing import Mapping
import discord


def build_embed(
    title: str,
    color: int | discord.Color,
    fields: Mapping[str, tuple[str, bool]],
    description: str | None = None,
) -> discord.Embed:
    """
    Build a discord embed to show all game states to the end users

    Args:
        title (str): Title of the embed.
        color (int | discord.Color): Accent color (hex value or discord.Color).
        fields (Mapping[str, tuple[str, bool]]):
            Mapping of field names to (field value, inline flag).
                - key   (str): field name
                - value (tuple[str, bool]):
                    * str:   field content
                    * bool:  True = inline, False = block
        description (str | None): Optional description (default: None).

    Returns:
        discord.Embed: Embed ready to send in a Discord context.
    """

    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
    )

    for field_name, (field_value, inline) in fields.items():
        embed.add_field(name=field_name, value=field_value, inline=inline)

    return embed
