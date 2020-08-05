#!/bin/bash

pip freeze | grep -v "^-e" | xargs pip uninstall -y