#!/bin/bash

find name_tags -type f -name "*.pdf" -print0 | xargs -0 -I{} pdf2svg "{}" "{}.svg"