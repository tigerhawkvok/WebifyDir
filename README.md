WebifyDir
=========

Prep a site for deployment. Code base from 2008, needs overhaul and error handling, as well as updates to components (or replacements where applicable).

When code cleanup is done, I plan to also deploy an executable via [cx-freeze](http://cx-freeze.sourceforge.net/). For now, you need Python installed to run this.

## What it does

Running this program generates a batch script (then executes it) to compress PNGs losslessly, remove CSS messes, reduce JPGs to 90% quality, and backs up all your originals.

## Binaries

All binaries by default are x64. x86 (32-bit) replacements are in the x86 directory.

## Licenses

Please note that individual components from other authors have their licenses represented in [`component-licenses`](component-licenses/). However, the licenses on the project sites should always be considered to supercede those in this repository. **If for any reason you have cause to suspect the license, or it is important for your project, please check the source page!**

### PeaZip

PeaZip can be found on [SourceForge](http://sourceforge.net/projects/peazip/).

### Pngcrush

Pngcrush can be found on [SourceForge](http://pmt.sourceforge.net/pngcrush/).

### OptiPNG

OptiPNG can be found on [SourceForge](http://optipng.sourceforge.net/).

### CSSTidy

CSSTidy can be found on [SourceForge](http://csstidy.sourceforge.net/).

### `convert.exe`

`convert.exe` is part of the [ImageMagick library](http://www.imagemagick.org/script/license.php).

### TweakPNG

TweakPNG is available on [GitHub](https://github.com/jsummers/tweakpng)
