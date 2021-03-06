#!/bin/bash -e

rm -f htmlcov/*
rm -f .coverage

coverage run --source='.' ./manage.py test

PARMS=--omit='*migrations*'
echo "Coverage results:"
coverage report $PARMS

coverage xml -o htmlcov/coverage.xml $PARMS
echo "XML report generated in htmlcov/coverage.xml"

