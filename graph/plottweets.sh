#!/bin/sh
echo "Plotting $1, starting from $2, with $3-second periods..."
python autosampling.py $1 "$2" $3 > "$1_timeseries"
python autoplot.py "$1_timeseries" "$2" $3

