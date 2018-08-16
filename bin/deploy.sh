#!/usr/bin/env sh

gcloud config configurations activate uncannly
gcloud app deploy -q
