#!/bin/bash

# Data from https://github.com/CSSEGISandData/COVID-19

OUTFILE="${PWD}/US_Covid.txt"

DATA_DIR="/home/rct/covid_data"

if [ ! -d $DATA_DIR ]; then
  mkdir -p $DATA_DIR
  pushd $DATA_DIR
    git clone https://github.com/CSSEGISandData/COVID-19
  popd
fi

pushd ${DATA_DIR}/COVID-19
 git pull

  FILE="csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
  head -1 $FILE > $OUTFILE
  grep US $FILE >> $OUTFILE

  FILE="csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
#head -1 $FILE > $OUTFILE
  grep US $FILE >> $OUTFILE

  cat $OUTFILE
popd


