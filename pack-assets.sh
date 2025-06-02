#!/bin/bash

for file in assets/png/*.png; do
  pngcrush -reduce -rem allb -ow $file
  optipng -clobber $file
done

zip -r -j assets.zip LICENSE-GRAPHICS assets/png/*.png >/dev/null
sha256sum assets.zip 2>&1
