# RNA Angles Alphabet

This repository is the work on creating an alphabet for RNA structures.

## Requirements

### Python

Python version 3.10.9 is needed, installation example with a conda environment:
`conda create --name rna_alphabet_env python==3.10.9`

Then activate it:
`conda activate rna_alphabet_env`

Finally download every necessary packages with pip (wich is automatically installed by conda):
`pip install -r requirements.txt`

### R

R version 4.3.0 is needed, after that the `mclust` package must be installed in R:
`install.packages("mclust", dependencies = TRUE)`

### C++

The C compiler `gcc` needs to be at least in 7.5.0 version

The C++ compiler `g++` needs to be at least in 9.4.0 version


## Download raw data

Download a dataset of 192 RNA in pdb format in `rna_dataset`:
`bash load_rna_dataset.sh`


## Pipeline

To use this program, you only need to use the pipeline.py script, it takes pdb files as input and print the sequence that describe its structure as output.

### Basic example

`python -m src.pipeline --training_path rna_dataset --testing_path file.pdb --mol rna --method mean_shift`

Here are the parameters:
- The "training_path" is the path to the directory where the pdb files will be used to train the model.
- The "testing_path" is the path where the file that the script will give its structure is (it can also be a directory).
- "mol" is used to specify the type of molecule in the pdb files, it can only be "rna" or "protein".
- The "method" is the type of algorithm that will be used to train th model, here the mean shift method.

This command will create a "tmp" directory that will contain 2 csv with all the angle values, save the model in "models/mean_shift_rna_model.pickle", save a png with the clustering in "figures_clust/mean_shift_rna_cluster.png" and will print the final sequence in the terminal.











### Tests

To run the different tests locally, please use : 
```make all_tests``` 


Make sure to have `docker` and `docker-compose` installed in your computer. 


