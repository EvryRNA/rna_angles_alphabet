# RNA Angles Alphabet

This repository is the work on creating an alphabet for RNA structures.

## Requirements

### Python

Python version 3.10.9 is needed, installation example with a conda environment:
```
conda create --name rna_alphabet_env python==3.10.9
```

Then activate it:
```
conda activate rna_alphabet_env
```

Finally download every necessary packages with pip (wich is automatically installed by conda):
```
pip install -r requirements.txt
```

### R

R version 4.3.0 is needed, after that the `mclust` package must be installed in R:
```
install.packages("mclust", dependencies = TRUE)
```

### C++

The C compiler `gcc` needs to be at least in 7.5.0 version

The C++ compiler `g++` needs to be at least in 9.4.0 version

To compile the C++ code that is used for the preprocessing, use: 
```shell
make compile_cpp
```
It will create the file `src/cpp_script/angle_calculation`.

## Download raw data

Download a dataset of 192 RNA in pdb format in `rna_dataset`:
```
bash load_rna_dataset.sh
```


## Pipeline

To use this program, you only need to use the pipeline.py script, it takes pdb files as input and prints the sequence that describes its structure as output.

### Basic example

```
python -m src.pipeline [--training_path TRAINING_PATH] [--testing_path TESTING_PATH] [--mol MOLECULE] [--method CLUSTERING_METHOD] [--tmp_dir TMP_DIR] [--v]
```

Here are the parameters:
- `--training_path TRAINING_PATH`: path to the directory where the pdb files will be used to train the model.
- `--testing_path TESTING_PATH`: path to a file (or directory of a unique file) that will have its sequence predicted.
- `--mol`: used to specify the type of molecule in the pdb files, it can only be "rna" or "protein".
- `--method CLUSTERING_METHOD`: type of algorithm that will be used to train th model (mean_shift for example). It can be either `dbscan`, `mean_shift`, `kmeans`, `hierarchical`, `mclust`, `outlier` or `som`.
This command will create a `tmp` directory that will contain 2 csv with all the angle values, save the model in `models/mean_shift_rna_model.pickle`, save a png with the clustering in `figures_clust/mean_shift_rna_cluster.png` and will print the final sequence in the terminal.

### Other options

- `--model MODEL` allows to directly give the path of an already existing model to skip the training step, but it need to be in `pickle` or `Rds` format.
- `--v` a boolean that plots the raw data in `models/raw_mol_data.png` if added (mol being the `--mol` option)
- `--tmp_dir TMP_DIR` allows to choose the path of the directoy used for the 2 csv files with angle values (`tmp` by default)

It is possible to only give a training path to save a model, as well as giving a model and a testing path to only predict the sequence of a unique file.


### Tests

To run the different tests locally, please use : 
```make all_tests``` 

Make sure to have `docker` and `docker-compose` installed in your computer. 


