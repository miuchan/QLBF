"""Apply a "千里冰封" frozen landscape effect to an image.

This module exposes a CLI and a reusable :func:`apply_frozen_effect` function that
simulate a frosty, distant winter landscape using a series of Pillow operations.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps


@dataclass
class EffectConfig:
    """Configuration for the frozen effect."""

    contrast: float = 1.6
    cold_tint_dark: str = "#071326"
    cold_tint_light: str = "#e7f9ff"
    blur_radius: float = 1.2
    noise_intensity: float = 28.0
    noise_alpha: float = 0.22
    crystal_boost: float = 2.4
    brightness: float = 1.08
    saturation: float = 0.78


def apply_frozen_effect(image: Image.Image, config: EffectConfig | None = None) -> Image.Image:
    """Return a new image with a stylised frozen landscape effect."""

    if config is None:
        config = EffectConfig()

    base = image.convert("RGB")
    grayscale = ImageOps.grayscale(base)
    contrasted = ImageEnhance.Contrast(grayscale).enhance(config.contrast)
    tinted = ImageOps.colorize(contrasted, config.cold_tint_dark, config.cold_tint_light)

    blurred = tinted.filter(ImageFilter.GaussianBlur(radius=config.blur_radius))

    noise = Image.effect_noise(blurred.size, config.noise_intensity).convert("L")
    cold_noise = ImageOps.colorize(noise, config.cold_tint_dark, config.cold_tint_light)
    frosted = Image.blend(blurred, cold_noise, alpha=config.noise_alpha)

    edges = ImageOps.autocontrast(grayscale.filter(ImageFilter.FIND_EDGES))
    crystals = ImageOps.colorize(edges, config.cold_tint_dark, config.cold_tint_light)
    crystals = ImageEnhance.Brightness(crystals).enhance(config.crystal_boost)

    combined = ImageChops.add(frosted, crystals, scale=2.0)

    cooled = ImageEnhance.Brightness(combined).enhance(config.brightness)
    cooled = ImageEnhance.Color(cooled).enhance(config.saturation)

    return cooled


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply a 千里冰封 frozen effect to an image")
    parser.add_argument("input", type=Path, help="Path to the input image")
    parser.add_argument("output", type=Path, help="Where to save the frosted image")
    parser.add_argument(
        "--noise-intensity",
        type=float,
        default=None,
        help="Noise intensity to simulate frost particles",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = EffectConfig()
    if args.noise_intensity is not None:
        config.noise_intensity = args.noise_intensity

    with Image.open(args.input) as img:
        frosted = apply_frozen_effect(img, config)
        frosted.save(args.output)


if __name__ == "__main__":
    main()
