CSCI 8000 HW 1

Special Topics in Efficient Deep Learning

Homework 1: Convolutional Neural Network

*GPUs may be needed for speeding up the neural network training process 

Description

In this homework you will practice how to write a Convolutional Neural Network (CNN) classifier
in Python with the PyTorch framework. You need to understand how a CNN works, including
backpropagation and gradient descent in order to implement this homework successfully. The goal
of this homework is:
- To implement and understand the CNN architecture.
Instruction
• The dataset used in this homework is CIFAR-10. You may need these packages: PyTorch,
NumPy, THOP (for MACs and parameters counting), OpenCV (for reading images),
Matplotlib. The commonly used classifier is Softmax.

• Requirements:

1. Contain a training function that will be called to train a model with the command
“python CNNclassify.py train”.

2. Save the model in a folder named “model” after finishing the training process.

3. Show the testing accuracy in each epoch of the training function. The test accuracy
should be greater than or equal to 75% in the end using the CIFAR-10 dataset.

1) You can add as many layers as you want for both CONV layers and FC layers.
Optimization techniques such as mini-batch, batch normalization, dropout and
regularization might be used.
2) In the first CONV layer, the filter size should be 5*5, the stride should be 1, no
padding, and the total number of filters should be 32. All other filter sizes, strides
and filter numbers are not acceptable and may result in a final grade of 0 in this
HW.
3) For other CONV layers (if any), there is no limitation for the size of filters and
strides.
Fig. 1 The screenshot of the training result.
4) You can choose as many CONV layers as you want, however, please be aware that
the computational cost of CONV layer is very high, and the training process may
take quite long.
CSCI 8000 HW 1
Fall 2024 Special Topics in Efficient Deep Learning Due 10/03/2024
5) You can also choose as many FC layers as you want to enhance the model accuracy.
There is no limitation for the size of FC layers.
6) You need to manually set the random seed for your model training process. You
need to train your network 3 times using different random seeds. In your pdf report,
you need to show the 3 random seeds used for the training and the corresponding
accuracies of the trained model. You also need to report the mean and standard
deviation of the 3 accuracies. You can use numpy.std() to calculate the standard
deviation.
7) During the training process, you need to store the training accuracy and testing
accuracy at the end of each training epoch (store in a list or something else). And
at the end of the entire training, you need to draw a single plot that contains two
curves (training accuracy and testing accuracy) that show the trend of accuracy
during training. For the plot, the X-axis should be the number of training epochs,
the Y-axis should be the accuracy. Two curves should have different colors and a
legend should be shown in the plot. You can use the Matplotlib package to draw
the plot. You only need to draw one plot to show one training process, no need to
do this for different seeds.

4. Implement a testing function that accepts the command “python CNNclassify.py test
xxx.png” to test your model by loading it from the folder “model” created in the
training step. The function should (1) read “xxx.png” and predict the output as shown
in Fig. 2, and (2) visualize the output of the first CONV layer in the trained model for
each filter (i.e., 32 visualization results), and save the visualization results as
“CONV_rslt.png” as shown in Fig. 3. The testing result would match the true image
class when the classifier achieves high accuracy. *You need to provide your own
testing image and submit the image together with your code.
Fig. 2 The screenshot of the testing result.
CSCI 8000 HW 1
Fall 2024 Special Topics in Efficient Deep Learning Due 10/03/2024
Fig. 3 The screenshot of the first CONV layer visualization (car shape).

5. Implement a testing function that accepts the command “python CNNclassify.py
resnet20”. The function should load a pretrained ResNet-20 model and test the
accuracy of this model using the entire CIFAR-10 testing dataset.

6. Use THOP package/library to count the computation cost (MACs) and number of
parameters of your neural network and ResNet-20 model, respectively. The THOP
package and its example can be found in https://pypi.org/project/thop/

7. You need to write a separate function, i.e., inference_speed_test(args), which can be
used to test the model inference speed of your own model and ResNet-20 model.
There are several points to keep in mind:
- The inference time should be measured based on a single input, not a batch. You
can use either dummy input or real image as the input.
- You should run several warmup iterations before measuring the time.
- You should run multiple inference iterations (e.g., 100 or 1000) and measure the
overall running time and calculate the average time as your final inference time.

