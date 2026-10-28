# Ambig-SWE (2025), "Interactive Agents to Overcome Underspecificity in Software Engineering"

- **Supports:** [GAPS](../GAPS.md#related-work), *Related work* under the agent trials: interaction
  raised resolve rates by up to 74% relative to the non-interactive setting.
- **Source:** arXiv:2502.13069.
- **Retrieved:** 2026-10-28, by Claude Fable 5.1, from https://arxiv.org/abs/2502.13069 and
  https://arxiv.org/pdf/2502.13069.
- **SHA-256:** abstract page `12a826bf66a6ca87a1982f86e59c849c586e8a4609814b1626943cf771dc9c83` (43,437 bytes);
  PDF `979f59dd4519c871e99fe1ba49ad4f5531165c252e466f9148f2ab5af371e65e` (1,190,419 bytes).
- **Stored:** no (arXiv's default license does not grant redistribution).
- **Status:** verified for the abstract and the per-model interactive rates. The per-model
  non-interactive rates are in Figure 3, an image, and were not read here.

## Extraction

Abstract:

> However, when models interact for underspecified inputs, they effectively obtain vital information
> from the user leading to significant improvements in performance, up to 74% over the
> non-interactive settings, underscoring the value of effective interaction.

Introduction: "we find that interactivity can boost performance on underspecified inputs by up to 74%
over the noninteractive settings, though performance varies across models (§3)."

Relative or absolute: the paper does not say. Its interactive resolve rates are at most about 46%
(Qwen 3 Coder), with Claude Haiku 3.5 at 26.8% and Claude Sonnet 3.5 at 39.6%, so a gain of 74
points is impossible and the figure is relative. The v1.1 review's delegated check read Figure 3 as
Haiku 3.5 going from 15.4% to 26.8%, a 74% relative gain; consistent with the text, not re-read.
