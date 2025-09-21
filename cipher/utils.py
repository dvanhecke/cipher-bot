# Cipher-Bot
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Module: cipher.utils
Utility functions to reduce duplicate code, so its easier to edit in case of bugs/errors
"""

from typing import Dict, Tuple
import discord


def build_embed(
    title: str,
    color: int | discord.Color,
    fields: Dict[str, Tuple[str, bool]],
    description: str | None = None,
) -> discord.Embed:
    """
    Build a discord embed to show all game states to the end users

    args:
        title (str): Title of the embed
        color (int|discord.Color): hex value or dicord.Color object to be used
                                   as the accent color for the embed
        fields (Dict[str, Tuple[str, bool]]):
                                 Dictionary which represent the fields,
                                 the keys are the field name and the value is a tuple:
                                     the first element is the field value
                                     the second element is the orientation:
                                         True: horizontal (name and value next to each other)
                                         False: vertical (name above value)

        description (str|None): optional description of the embed defaults to None

    Returns:
        discord.Embed: embed ready to send to the ctx
    """

    if description is None:
        embed = discord.Embed(title=title, color=color)
    else:
        embed = discord.Embed(title=title, description=description, color=color)

    for field_name, field_values in fields.items():
        field_value, orientation = field_values
        embed.add_field(name=field_name, value=field_value, inline=orientation)

    return embed
