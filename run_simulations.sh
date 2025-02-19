#!/bin/bash

# Define simulation parameters
EXPONENT_VALUES=(3.1 3.9 3.8)
REFERENCE_LOSS_VALUES=(5 10 5)
DATA_DIR="datafiles"
FINAL_CC="scratch/final.cc"

# Ensure the data directory exists
mkdir -p $DATA_DIR

# Loop through the three simulation runs
for i in {1..3}; do
    EXPONENT=${EXPONENT_VALUES[$((i-1))]}
    REFERENCE_LOSS=${REFERENCE_LOSS_VALUES[$((i-1))]}
    
    echo "Running simulation $i with Exponent=$EXPONENT and ReferenceLoss=$REFERENCE_LOSS"
    
    # Modify final.cc using sed
    sed -i "s/Config::SetDefault (\"ns3::LogDistancePropagationLossModel::Exponent\", DoubleValue ([0-9]\+\.[0-9]\+));/Config::SetDefault (\"ns3::LogDistancePropagationLossModel::Exponent\", DoubleValue ($EXPONENT));/" $FINAL_CC
    sed -i "s/Config::SetDefault (\"ns3::LogDistancePropagationLossModel::ReferenceLoss\", DoubleValue ([0-9]\+));/Config::SetDefault (\"ns3::LogDistancePropagationLossModel::ReferenceLoss\", DoubleValue ($REFERENCE_LOSS));/" $FINAL_CC
    
    # Run the simulation
    ./waf --run "scratch/final.cc --enableE2FileLogging=1"
    
    # Create a unique directory for this run and move generated files
    RUN_DIR="$DATA_DIR/run_$i"
    mkdir -p $RUN_DIR
    mv *.txt $RUN_DIR 2>/dev/null

done

echo "All simulations completed. Data saved in $DATA_DIR."

