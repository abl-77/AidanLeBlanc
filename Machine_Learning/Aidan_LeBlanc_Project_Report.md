# Aidan LeBlanc Project Report

## 1. Survey

### 1.1 Robust Large-Scale Online Kernel Learning <a href="#ref-1">[1]</a>

This paper presents a novel approach to large-scale online learning using kernel approximation and control based methods. Previous methods exist that show control based methods are effective for online learning; however, these models are too computationally expensive to be used for large-scale applications.

The paper presents three main ideas to implement a large-scale online learning method with a control based framework.

- **RF-Based Kernel Approximation**:
  - The main idea of kernel approximation is to find a way to utilize the benefit of kernel learning without having to compute and store the full kernel matrix.
  - The paper uses random fourier features to approximate the kernels for learning.
  - These random fourier features have been shown in previous papers to accurately approximate kernels and reduce the computation time.
  - Ultimately, the kernel can be approximated with the formula:
    $$K(x_1, x_2) = E[Z(x_1)^TZ(x_2)]$$
      - Here $Z(x)$ is a random fourier transformation method discussed in the methods section of the report.
  - Thus, model predictions can be obtained from the formula:
    $$\hat{f}(x) = \theta^T Z(x)$$
      - Where $\theta$ are the parameters to be learned by the model.
  - This kernel approximation reduces the dimensionality of the input examples while maintaining some of the data structure.
 
- **Control Based Learning Framework**:
  - The central idea of optimal control theory is to solve equations of the form: $Z(n + 1) = AZ(n) + BU(n)$
      - Note the Z used here is different than the Z for RF kernel approximation
  - The way this equation is solved is by discovering a control policy for U(n) that will eventually cause the Z(n) values to converge.
  - This control policy takes the form: $U(n) = FZ(n)$
  - Thus, the problem becomes finding the optimal $F$ matrix.
  - In this paper the control problem is setup as follows: $\theta(n + 1) = \theta(n) + \Delta\theta(n)$
      - Here $\theta(n)$ is the existing parameter values after the nth example
  - The $\Delta\theta(n)$ value can then be obtained from the formula: $\Delta\theta(n) = F_nE(n)$
      - Where $F_n$ is the control matrix and $E(n)$ is the loss for each example with the current parameters.
  - The control matrix is given by a theorem in the paper, which results in the equation: $F_n = - (\gamma I + B_n^TP_nB_n)^{-1}B_n^TP_n$
      - Where $B_n$ is the gradient of the loss for the first n examples and $P_n$ can be solved iteratively.
  - From these calculations, the optimal control matrix can be calculated to correct the current model parameters.
  - This method operates similarly to gradient descent in that the parameter values are adjusted in a direction determined by the gradient; however, the use of optimal control results in faster convergence than traditional gradient descent methods.
 
- **Computational Techniques**:
  - Because the iterative computation of the $P_n$ control matrix is time consuming, for large-scale models, the authors offer a closed form solution for $P_n$.
  - The primary consideration of this computational increase is that the number of examples considered can only be one.
      - This means that the $B_n$ matrix will only be the gradient of the loss for the current example.
      - While this could reduce in some loss of accuracy, it is outweighed by the significant improvement in performance and computation time.
  - The closed form solution for $P_n$ is given: $P_n = \frac{1}{2}(1 + \sqrt{1 + 4\gamma G_n^{-1}})$
      - Here $G_n$ is the gram matrix of $B_n$ given by: $B_nB_n^T$.

These main ideas allow for the model to perform faster and more accurate robust large-scale online kernel learning. To demonstrate the results the paper compared the runtime and MSE values to other benchmark large-scale online models for a number of datasets.

<img width="617" alt="CRFR_Paper_Results" src="https://github.com/user-attachments/assets/66307bd3-3f9e-4690-800a-070e930a54f4">

The novel CRFR algorithm performed better than all of the tested models both in regards to error and time demonstrating the power of control based techniques and kernel approximation.

### 1.2 Fastfood Approximation <a  href="#ref-1">[2]</a>

**Fastfood Formula**:
This paper, consulted for the research extension portion of this project, introduces the fastfood method for accelerating kernel approximation computations. The fastfood method does this by approximating random Gaussian matrices with structured transformations.

The paper presents the following formula for approximating a kernel:

$$
V = \frac{1}{\sigma\sqrt{d}}SHG\Pi HB
$$

Where $\Pi$ is a permutation matrix, $H$ is the Hadamard matrix, and $S$, $G$, and $B$ are all random diagonal matrices. $B$ has random -1 or 1 values on its diagonal, $S$ is a random scaling matrix, and $G$ has random diagonal Gaussian entries.

The Hadamard matrix ($H$) is the matrix defined recursively as:

$$H_2 = \begin{bmatrix}
1 & 1 \\
1 & -1
\end{bmatrix}, H_2d = \begin{bmatrix}
H_d & H_d \\
H_d & -H_d
\end{bmatrix}$$

Since the Hadamard matrix has to have dimensions that are powers of 2, the input example vector can be padded with zeros to allow for the computation to work.

This matrix is capable of approximating a Gaussian Kernel faster than previous methods.

**Performance Comparison**:
This paper compares the fastfood method to the existing best method for Gaussian kernel approximation, random kitchen sinks, which are capable of approximating the kernel matrix in O(nd) time, whereas the fastfood method computes the approximation in O(nlogd) time, which is a significant improvement.

The paper also analyzes how the approximation error changes for the fastfood method.

<img width="372" alt="Fastfood_Error_Results" src="https://github.com/user-attachments/assets/4a7eea25-8b05-4bee-b5e9-8e938b44db65">

This graph shows that the fastfood method (with Hadamard matrices) has similar approximation error to random kitchen sinks. This similar error combined with the faster performance presents the fastfood method as a better alternative for Gaussian kernel approximation.

### Compare/Contrast
- Although the Fastfood approximation paper does not discuss applying the method to a control based framework, it suggests an interesting improvement over the fourier based approximation that is utilized in the control based framework.
- This potential improvement will be explored in the research portion of this report.

## 2. Methods

### Implemented Method: Control-Based Random Feature Regression (CRFR)

The CRFR algorithm is implemented fully in the CRFRExtension.py file. The algorithm described in the study can be demonstrated by using the fourier transform methods for kernel approximation.

The CRFR Algorithm implementation requires a number of methods described below:

1. **Update**:
- This method takes a labeled example and updates the parameter models accordingly
- As part of the large-scale optimization, the parameters are only updated for examples that generate a significant error (defined by a hyperparameter).
- Update amount is generated by the following method

2. **Control Input**:
- This method computes the following four values to compute the parameter updated:
- The loss matrix (B)
  - This is the gradient of the loss with respect to each parameter
- The inverse gram matrix
  - This is the inverse of the matrix $B^{T}B$
  - For this algorithm the inverse gram matrix is always a single value because the algorithm only considers the most recent example.
- The control matrix (P)
  - This matrix scales and inverts the inverse gram matrix to determine the control factor of the parameter update.
- The error matrix
  - This is difference between the model error and the target error threshold.
  - Also includes a regularization term for the model parameters.

3. **Predict**:
- This method predicts the output by multiplying the model parameters by the transformed input.
- The base model uses a random fourier feature transform to approximate the kernel.

4. **Fourier Transform**:
- This transforms the example into a lower dimensional space (2 * D, where D is a hyperparameter).
- Transformation is according to the formula:
  - $Z(x) = \sqrt{\frac{1}{D}}(sin(u_1^Tx), cos(u_1^Tx),...,sin(u_D^Tx), cos(u_D^Tx))$
  - Where u is randomly sampled from a normal distribution when the model is initialized.

5. **Initialization**:
- Beyond these methods there are also a number of helper methods to initialize and evaluate the model.
- Most of the initialization such as the model parameters is done randomly to try and avoid bias.

## 3. Research

### Extension: Incorporating Fastfood Approximation into CRFR

The CRFR algorithm has two main sections: the random feature kernel approximation, and the control based learning framework. In order to attempt to increase model runtime while maintaining accuracy, this extension explores alternative random feature kernel approximation approaches. Primarily the fastfood method discussed previously.

**CRFRFastFood**: This novel method implements the fastfood method for kernel approximation instead of random fourier features in order to further increase the speed of the CRFR algorithm and optimize performance for large-scale online learning tasks.

**Implementation**: To implement the fastfood powered method, three new methods were introduced:
- **Hadamard**: This simple method recursively calculates a hadamard matrix of dimensions $2^n$ x $2^n$
- **Fastfood Initialization**: This method initializes the V matrix discussed previously.
  - This matrix serves as the Gaussian Kernel approximation and only needs to be calculated once.
  - In order to allow for the fastfood method to reduce dimensionality, a random selection of 2D (for consistent testing) rows of the final V matrix are stored.
- **Fastfood Transform**: This method transforms a given example into a lower dimension (2D to be consistent with the random fourier features)
  - Pads the feature vector and multiplies it by the stored V matrix to reduce dimension

The rest of the implementation relies on the same control based methods as the original CRFR algorithm.

**CRFRFourier**: This algorithm is the same as the CRFR algorithm, just coded in a consistent way with CRFRFastFood for comparison purposes.

**CRFRRandom**: This method is a simple implementation where the transformation matrix is randomly initialized. The expected performance of this algorithm is very low; however, it is intended to determine how much of the benefit of the two primary algorithms is simply from reducing the dimensionality of the input data.

## 4. Results, Analysis, and Discussion

### The datasets
The datasets are the same as the rest of the project group and group analysis as we used the same datasets. Here is the description copied from our `README.md` file:

#### Electricity Load Diagrams Dataset

##### Description
The **Electricity Load Diagrams** dataset contains electricity consumption data from 370 clients, collected between 2011 and 2014. Each client is represented by a sensor (`MT_001` to `MT_370`), and readings are taken every 15 minutes.  This is taken from https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014.

##### Data Structure
- **File Path**: `../data/electricity.pkl`
- **Format**: Pickle file containing a Pandas DataFrame.
- **DataFrame Structure**:
  - **Columns**:
    - `timestamp`: `datetime` object representing the timestamp of the reading.
    - `MT_001`, `MT_002`, ..., `MT_370`: Columns representing electricity consumption values for each sensor.
  - **Index**: Default integer index after resetting.

**Sample Data**:
|    |     timestamp       |  MT_001  |  MT_002  | ... |  MT_370  |
|----|---------------------|----------|----------|-----|----------|
| 0  | 2011-01-01 00:00:00 | 85.02600 | 80.12345 | ... | 75.67890 |
| 1  | 2011-01-01 00:15:00 | 88.41798 | 82.54321 | ... | 77.89012 |
| ...| ...                 | ...      | ...      | ... | ...      |


#### Stock Market Data

##### Description
The **Stock Market Data** includes historical stock prices and volumes for the top 100 most popular symbols over the past 2 years. The data is fetched from Yahoo Finance using the `yfinance` library and includes multiple attributes for each symbol.

##### Data Structure
- **File Path**: `../data/stock.pkl`
- **Format**: Pickle file containing a Pandas DataFrame.
- **DataFrame Structure**:
  - **Columns**:
    - `timestamp`: `datetime` object representing the date of the trading day.
    - Flattened columns for each ticker and attribute, e.g., `AAPL_Open`, `AAPL_High`, `AAPL_Low`, `AAPL_Close`, `AAPL_Volume`, etc.
  - **Index**: Default integer index after resetting.

**Sample Data**:
|    |         timestamp         |  AAPL_Open  |  AAPL_High  | AAPL_Low |  AAPL_Close  |  AAPL_Volume  |  MSFT_Open  | ... |
|----|---------------------------|-------------|-------------|----------|--------------|---------------|-------------|-----|
| 0  | 2011-01-01 00:00:00-04:00 | 142.47      | 144.38      | 141.28   | 142.65       | 74602000      | 281.77      | ... |
| 1  | 2011-01-04 00:00:00-04:00 | 141.76      | 142.21      | 138.27   | 139.14       | 98322000      | 283.66      | ... |
| ...| ...                       | ...         | ...         | ...      | ...          | ...           | ...         | ... |

### Preprocessing Data
Once loaded, the datasets were used to generate sequence data for prediction using the following code:

```
def create_sequences(data, seq_length):
        sequences = []
        targets = []
        for i in range(len(data) - seq_length):
            seq = data[i:i + seq_length]
            target = data[i + seq_length]
            sequences.append(seq)
            targets.append(target)
        return np.array(sequences), np.array(targets)
```
For the purposes of this research experiment the sequence length was always specified as 10. Additionally, since the CRFR algorithm operates on a single dimension vector, the sequences were reshaped to one dimension resulting in a one dimensional vector of dimension seq_length * num_features.

### Experiment:
To train models for comparison, `abl77/CRFRMain.py` was run to train 24 models with combinations of datasets, number of training epochs, and the kernel approximation methods described in the research section. The trained models were saved in `abl77/models/` using pickle. Additionally, the time to train each model was also saved in `abl77/results/`.

#### Metrics:
To evaluate the performance and accuracy of each model two metrics were selected:
- **MAE** Is the average absolute difference between the predicted value and the ground truth given by the formula:

$$
MAE = \frac{\sum_{i = 1}^n |y_i - \hat{y}_i|}{n}
$$

- This metric measures the error over the whole dataset, so a low value indicates that the model generally predicts values accurately.
- The model does not, however, provide any information about outliers or if there are specific output features that are difficult.

- **MSE** Is the average squared difference between the predicted value and the ground truth given by the formula:

$$
MSE = \frac{\sum_{i = 1}^n (y_i -\hat{y}_i)^2}{n}
$$

- This metric also measures the error over the whole dataset, but because of the squared term, this metric is better at indicating if there are large deviations or errors.
- This indicates if a model struggles from errors due to specific output features.

Together these two matrices can give a better understanding of how a model performs and provide a basis for comparing model performance. 

#### Analysis of Model Performance:
Calculating these metrics for the 24 test models, resulted in the following graph generated using the code in `abl77/CRFREvaluate.py`:

![CRFRModelComparison](https://github.com/user-attachments/assets/7961afce-e5d5-4ff1-8fd3-afd29162b6d3)

The **Fourier method** demonstrated the most consistent and robust performance across the datasets, as indicated by the graph. It maintained approximately constant **MSE** and **MAE** values of **1.00** and **0.83**, respectively, regardless of the number of training epochs. The closeness of the MSE to the MAE suggests that the model does not produce significant outliers, as the error distribution is relatively uniform. The consistent performance across all training epochs indicates that the Fourier method converges rapidly, achieving optimal performance after just a single epoch. This rapid convergence suggests an efficient learning process, and its implications for runtime performance will be further explored in the runtime analysis.

In contrast, the **Fastfood method** exhibited the most erratic behavior, with substantial variations in both **MSE** and **MAE** values depending on the number of training epochs. For the stock dataset, the Fastfood method initially produced an **MSE** of **23.6**, indicating significant prediction errors for certain data points. These large errors may reflect the model's difficulty in generalizing to specific attributes of the stock dataset. However, after ten epochs, the Fastfood method's performance stabilized and aligned closely with the Fourier method on both datasets. Interestingly, beyond ten epochs, the performance on the stock dataset deteriorated, suggesting potential overfitting. This behavior highlights the sensitivity of the Fastfood method to the number of training epochs and the dataset characteristics.

The **Random method** delivered surprising results, with performance comparable to the Fourier method. After ten epochs, it achieved nearly identical results to the Fourier method. This outcome is unexpected given the Random method's initialization with values uniformly distributed between **-1** and **1**. The comparable performance suggests that the best parameters for these datasets may inherently be close to zero, enabling the Random method to converge effectively. While its initial performance was less consistent, the eventual alignment with the Fourier method indicates potential applicability in scenarios where computational simplicity is prioritized.

Overall, the analysis highlights the Fourier method's superior stability, the Fastfood method's sensitivity to training epochs, and the surprising efficacy of the Random method under specific conditions. These findings underscore the importance of selecting an appropriate transformation method based on dataset characteristics and performance priorities.

#### Analysis of Model Speed:
The model speed for each model was calculated by measuring the amount of time it took for each of the 24 models in `abl77/CRFRMain.py` to complete training and saving the results to `abl77/results/`. These runtime measurements resulted in the following graphs:

![StockRuntime](https://github.com/user-attachments/assets/18e35fcd-b77f-4799-9f9e-985d91386c22)
![ElectricityRuntime](https://github.com/user-attachments/assets/ac70aee2-8fe7-4df2-b673-af0f5df4b0e6)

The **Fourier method** serves as the baseline for comparison in terms of both runtime and performance. Across both datasets, it consistently demonstrates a lower runtime for smaller numbers of training epochs. This makes it particularly well-suited for applications where a smaller number of training epochs is sufficient to achieve convergence, as seen in the earlier performance analysis. However, as the number of training epochs increases (e.g., at 25 epochs), the **Fastfood method** begins to achieve better runtimes. This indicates that while the Fourier method is efficient in the short term, its advantages diminish over longer-term training. These trends highlight Fourier’s role as a strong choice for quick training tasks.

The **Fastfood method**, designed to reduce runtime compared to the Fourier method, reveals more nuanced behavior in the graphs. For a smaller number of training epochs (e.g., fewer than 15), the Fastfood method incurs a longer runtime than the Fourier method. This suggests that the overhead introduced by the structured computations in Fastfood outweighs its benefits for smaller-scale training. However, at 25 epochs, the Fastfood method overtakes Fourier in runtime efficiency. This makes Fastfood a better option for scenarios requiring extensive training, where scalability is critical. Nevertheless, for short-term tasks, the Fourier method remains the superior choice.

The **Random method** demonstrates consistently higher runtime across both datasets. This is primarily due to the design of its transformation algorithm, which involves repeated matrix multiplications for each output parameter. This computational overhead results in poor scaling efficiency compared to the Fourier and Fastfood methods. Despite this, there is potential for optimization. By initializing a larger random matrix upfront and performing a single matrix multiplication, the runtime of the Random method could likely be reduced significantly. This optimization would make it a more viable option for larger-scale datasets or extended training scenarios.

Both datasets, Stock and Electricity, exhibit similar trends in runtime across the three methods. However, the Stock dataset generally shows slightly higher runtimes, potentially due to its complexity or unique feature characteristics. This consistency in trends across datasets reinforces the generality of the observed patterns and supports the conclusions drawn regarding the methods' scalability and runtime efficiency.

Overall, the Fourier method demonstrates efficiency for short-term training tasks, the Fastfood method scales better for long-term training, and the Random method, while currently inefficient, shows promise for improvement with better optimization. These findings emphasize the importance of selecting the appropriate transformation method based on the number of training epochs and computational constraints.

#### Discussion

The proposed research extension to utilize the fastfood kernel approximation instead of random Fourier features as a way to improve runtime was not as successful as hypothesized. The implementation resulted in less consistent performance and slower runtimes for smaller training epochs.

The lack of runtime optimizations could be attributed to the error threshold value of the CRFR update method. This threshold prevents the model from updating for examples it can already accurately predict, meaning that a model which converges faster will achieve a faster runtime, even if the underlying computations take longer. As demonstrated by the experiments, the Fourier method converges more rapidly and is thus able to take advantage of the error threshold to maintain minimal runtimes during training. 

These findings suggest that while the fastfood method did not outperform the Fourier method on this dataset, it could still be advantageous in different datasets or scenarios. For instance, in large-scale online learning frameworks, the structured random projections of the fastfood method might provide significant advantages when combined with a control-based framework.

Another noteworthy result from this research extension was the unexpected performance of the random algorithm, which was initially included as a baseline. It was hypothesized to have the fastest runtime and the worst performance; however, it turned out to have the slowest runtime while delivering competitive MAE and MSE values. The competitive accuracy was likely due to the characteristics of the datasets, which seemed to favor smaller parameter weights and values. However, the ability of the random model to learn and improve with more training epochs suggests that it could be a powerful approach when applied to suitable datasets. The increased runtime, alternatively, was not as impressive. This increase in runtime was likely caused by the implementation of the transformation, which increased the number of matrix operations required. Future experiments could explore whether similar results could be achieved with reduced runtime by optimizing the transformation step.

Overall, these experiments highlight the efficacy of control-based large-scale online learning and the potential for further optimizations and discoveries. There remain significant opportunities to improve both the runtime and the accuracy of these novel algorithms, making them more effective and practical for various real-world applications.

## 5. Bibliography

1. **Papers**:

   <a id="ref-1"></a>
    1\. Chen, Huizhen, et al. "Robust Large-Scale Online Kernel Learning." Neural Computing and Applications, 2022. [URL](https://link.springer.com/article/10.1007/s00521-022-07283-5).

   2\. Le, Quoc V., et al. "Fastfood: Approximating Kernel Expansions in Loglinear Time." Proceedings of the 30th International Conference on Machine Learning, 2013. [URL](http://proceedings.mlr.press/v28/le13.pdf).

3. **AI Tools**:
   - ChatGPT for report structuring and markdown generation.
   - AI-assisted debugging and code documentation tools.

---


