# Maze Navigation with Learned Guidance

This repository contains the Jupyter notebook "extension.ipynb" that can be found [here](code/extension.ipynb), which implements and compares the following maze navigation algorithms:
- Dijkstra's Algorithm based optimistic planner
- Learned subgoal planner
- Environment similarity planner

---

## 1. Requirements

- Conda (Anaconda or Miniconda)
- The included 'environment.yml' file

GPU/CUDA is **not required**. All experiments run on CPU.

---

## 2. Setting Up the Conda Environment

Create a new environment from the Project directory:
```
conda env create -n test_env -f environment.yml
```

Activate the environment:
```
conda activate maze-env
```

---

## 3. Launch Jupyter and Open the Notebook

Open "extension.ipynb" in an IDE (VSCode) or through Jupyter Notebooks

Select maze-env as the notebook kernel

---

## 4. Run Code

Run each cell in the notebook sequentially to ensure that the code runs as expected.

Cells without function definitions in them can be omitted as all datasets and models have been saved to the data and models folders respectively. Additionally, the generation of 50000 labeled maze samples for training takes approximately 30 minutes for each maze type.

---

## 5. Expected Outputs

Running the notebook sequentially will:

1. Define functions to randomly generate mazes
2. Define functions to label mazes for training
3. Provide an example generated maze and labeled sections
4. Generate samples for a training dataset and the specified maze type
5. Create and train a model on the dataset
6. Define methods for comparing mazes
7. Compare guided maze model performance to optimistic baseline
8. Compare anti-gudide maze model performance to optimistic baseline
9. Train and compare a hybrid model to optimistic baseline
10. Generate similarity samples
11. Train compare similarity deployed guided maze model to optimistic baseline

You will see printed results and several matplotlib figures.

---
