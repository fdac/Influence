#!/bin/bash
nohup python nCommits.py > data/nCommits.data 2> data/nCommits.err &
nohup python fqCommits.py > data/fqCommits.data 2> data/fqCommits.err &
nohup python nForks.py > data/nForks.data 2> data/nForks.err &
nohup python timeContrb.py > data/timeContrb.data 2> data/timeContrb.err &
nohup python totalRepos.py > data/totalRepos.data 2> data/totalRepos.err &
