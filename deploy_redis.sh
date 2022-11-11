#!/bin/bash
helm del redis -n demo
helm install redis bitnami/redis -n demo --set architecture=standalone