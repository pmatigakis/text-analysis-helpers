#!/bin/bash

coverage run -m unittest
coverage html -d cover
