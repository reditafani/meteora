# Image library (processed at build time)

Every image here is converted to AVIF + WebP + JPEG at several widths during `npm run build`.

IMPORTANT — the current files were cropped from the PDF brochure (300 dpi page scans):
they are good enough to launch, but the original high-resolution files from the
photographer should replace them (same filename = no code change needed).

Some brochure images (studio cocktail shots, the bartender close-ups on the
uniform and services pages) may be licensed stock: verify usage rights, or
replace them with Meteora's own photography.

brand/        logo extracted from the brochure → replace with the original vector logo
bars/         bar photography (Bar Collection, heroes)
cocktails/    one image per cocktail, filename = cocktail slug (src/data/cocktails.ts)
details/      close-ups (ice stamp, garnish, champagne bowl, tools)
ice/          ice formats
glassware/    glassware product shots
towers/       Signature Tower Experience
team/         staff / bartenders
venues/       venue atmosphere
hero/ weddings/ corporate/ destinations/   — ready for new real photography
