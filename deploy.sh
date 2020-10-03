#! /usr/bin/env bash

hugo && rsync -avz --delete public/ soldaini-net:/home/public/