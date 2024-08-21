#!/bin/bash
celery -A donations worker --beat --loglevel=debug
