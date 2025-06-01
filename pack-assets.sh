#!/bin/bash

zip -r -j assets.zip LICENSE-GRAPHICS assets/png/*.png >/dev/null
sha256sum assets.zip 2>&1
