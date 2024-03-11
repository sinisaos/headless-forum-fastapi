#!/bin/bash

export PICCOLO_CONF="tests.piccolo_conf_test"
python -m pytest --cov=api --cov-report=html --cov-fail-under=90 -s $@