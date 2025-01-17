import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.get_weights(), x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        run_result = self.run(x)
        run_val = nn.as_scalar(run_result)
        if (run_val >= 0):
            return 1
        return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        isNotAccurate = True
        while (isNotAccurate):
            isNotAccurate = False
            batch_size = 1
            for features, label in dataset.iterate_once(batch_size):
                prediction = self.get_prediction(features) # scalar
                actual_val = nn.as_scalar(label)
                if (actual_val > 0 and prediction > 0):
                    # expects positive and got positive
                    update_multiplier = prediction * actual_val
                elif (actual_val > 0 and prediction < 0):
                    # expects positive and got negative
                    update_multiplier = abs(prediction) * actual_val
                elif (actual_val < 0 and prediction < 0):
                    # expects negative and got negative
                    update_multiplier = prediction * actual_val * -1
                elif (actual_val < 0 and prediction > 0):
                    # expects negative and got positive
                    update_multiplier = prediction * actual_val
                else:
                    update_multiplier = 0 # debugging purposes; should never trigger
                if (not prediction == nn.as_scalar(label)):
                    isNotAccurate = True
                    self.w.update(features, update_multiplier)


class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.

    Recommended values:

    Hidden layer sizes: between 100 and 500.
    Batch size: between 1 and 128. For Q2 and Q3, we require that total size of the dataset be evenly divisible by the batch size.
    Learning rate: between 0.0001 and 0.01.
    Number of hidden layers: between 1 and 3(It’s especially important that you start small here).

    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        # initialize layer weights and bias
        self.l1_weight = nn.Parameter(1, 200)
        self.l2_weight = nn.Parameter(200, 300)
        # self.l3_weight = nn.Parameter(500, 300)
        # self.l4_weight = nn.Parameter(300, 1)
        self.l3_weight = nn.Parameter(300, 1)
        self.l1_bias = nn.Parameter(1, 200)
        self.l2_bias = nn.Parameter(1, 300)
        self.l3_bias = nn.Parameter(1, 1)
        self.batch_size = 10
        self.learning_rate = 0.007 * -1 # multiplier is -1 * learning rate
        self.loss_function = nn.SquareLoss

        # Curious on how to get the multiplier value for train q2 when calling update, as well as how to use the nn.Relu function
        # The multiplayer is based on your learning rate, so it should be -1 * learning rate. 
        # And you can call relu just by passing in your layer’s output. We have an example in the provided code II in the spec.
        
        # self.lossFunction 
        # activation function: relu
        # y = Constant(3, 11, 10, 18) # not actual input; its the label
        # m = nn.Parameter(2, 1) # input
        # b = nn.Parameter(1, 1) # expected output
        # multiplier = 1 # learning rate
        
        # # predictions
        # xm = nn.Linear(x, m)
        # predicted_y = nn.AddBias(xm, b)
        # # minimize square loss
        # loss = nn.SquareLoss(predicted_y, y)
        # grad_wrt_m, grad_wrt_b = nn.gradients(loss, [m, b])
        # m.update(grad_wrt_m, multiplier)
        # b.update(grad_wrt_b, multiplier)
        # # loop to perform gradient updates



        # f(x)=relu(x⋅W1​+b1​)⋅W2​+b2​
        # where we have parameter matrices W1​ and W2​ 
        # and parameter vectors b1​ and b2​ to learn
        # during gradient descent. W1​ will be an i×h 
        # matrix, where i is the dimension of our input
        # vectors x, and h is the hidden layer size. 
        # b1​ will be a size h vector. 
        # need to initialize hidden layers


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        # does it return constant?
        l1_vals = nn.Linear(x, self.l1_weight)
        l1_vals = nn.AddBias(l1_vals, self.l1_bias)
        l1_vals = nn.ReLU(l1_vals)

        l2_vals = nn.Linear(l1_vals, self.l2_weight)
        l2_vals = nn.AddBias(l2_vals, self.l2_bias)
        l2_vals = nn.ReLU(l2_vals)

        l3_vals = nn.Linear(l2_vals, self.l3_weight)
        l3_vals = nn.AddBias(l3_vals, self.l3_bias)
        # l3_vals = nn.ReLU(l3_vals) # need to be able to output negative numbers

        return l3_vals
        

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        # nn.SquareLoss as the loss
        # x is input
        # need to make prediction before calling squared loss
        loss = self.loss_function(self.run(x), y)
        return loss
        



    def train(self, dataset):
        """
        Trains the model.

        Your implementation will receive full points if it gets a loss of 0.02 or better, averaged across all examples in the dataset.
        """
        "*** YOUR CODE HERE ***"
        current_loss = float('inf')
        max_loss = 0.010 
        while (current_loss > max_loss):
            batch_size = self.batch_size
            for features, label in dataset.iterate_once(batch_size):
                loss = self.get_loss(features, label) # scalar
                parameters = [self.l1_weight, self.l1_bias, self.l2_weight, self.l2_bias, self.l3_weight, self.l3_bias]
                gradients = nn.gradients(loss, parameters)
                current_loss = nn.as_scalar(loss)
                if (current_loss > max_loss): # update weights
                    for i in range(len(parameters)):
                        parameters[i].update(gradients[i], self.learning_rate)
                



class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        # initialize layer weights and bias
        self.l1_weight = nn.Parameter(784, 300)
        self.l2_weight = nn.Parameter(300, 150)
        # self.l3_weight = nn.Parameter(500, 300)
        # self.l4_weight = nn.Parameter(300, 1)
        self.l3_weight = nn.Parameter(150, 10)
        self.l1_bias = nn.Parameter(1, 300)
        self.l2_bias = nn.Parameter(1, 150)
        self.l3_bias = nn.Parameter(1, 10)
        self.batch_size = 10
        self.learning_rate = 0.005 * -1 # multiplier is -1 * learning rate
        self.loss_function = nn.SoftmaxLoss


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        l1_vals = nn.Linear(x, self.l1_weight)
        l1_vals = nn.AddBias(l1_vals, self.l1_bias)
        l1_vals = nn.ReLU(l1_vals)

        l2_vals = nn.Linear(l1_vals, self.l2_weight)
        l2_vals = nn.AddBias(l2_vals, self.l2_bias)
        l2_vals = nn.ReLU(l2_vals)

        l3_vals = nn.Linear(l2_vals, self.l3_weight)
        l3_vals = nn.AddBias(l3_vals, self.l3_bias)
        # l3_vals = nn.ReLU(l3_vals)

        return l3_vals

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        # nn.SquareLoss as the loss
        # x is input
        # need to make prediction before calling squared loss
        loss = self.loss_function(self.run(x), y)
        return loss
        

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        minimum_accuracy = 0.98
        while (dataset.get_validation_accuracy() < minimum_accuracy):
            batch_size = self.batch_size
            for features, label in dataset.iterate_once(batch_size):
                loss = self.get_loss(features, label) # scalar
                parameters = [self.l1_weight, self.l1_bias, self.l2_weight, self.l2_bias, self.l3_weight, self.l3_bias]
                gradients = nn.gradients(loss, parameters)
                current_loss = nn.as_scalar(loss)
                for i in range(len(parameters)):
                    parameters[i].update(gradients[i], self.learning_rate)
                

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        # initialize layer weights and bias
        self.batch_size = len(self.languages)
        # self.l1_weight = nn.Parameter(self.num_chars, 300)
        self.l1_weight = nn.Parameter(self.num_chars, 300)
        # self.l2_weight = nn.Parameter(300, 450)
        self.l2_weight = nn.Parameter(300, 300)
        # self.l3_weight = nn.Parameter(500, 300)
        # self.l4_weight = nn.Parameter(300, 1)
        # self.l3_weight = nn.Parameter(450, self.batch_size)
        self.l3_weight = nn.Parameter(300, self.batch_size)

        self.l1_bias = nn.Parameter(1, 300)
        self.l2_bias = nn.Parameter(1, 300)
        self.l3_bias = nn.Parameter(1, self.batch_size)
        
        self.learning_rate = 0.007 * -1 # multiplier is -1 * learning rate
        self.loss_function = nn.SoftmaxLoss

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)

        xs[1] is the list of every letter at index 1(or the 2nd letter) in each word in the batch. This is because every column of xs, is a word, not each row. So if you wanted to get the word cat, which is the 7th word in the batch, you'd do something like xs[:,7]which gets every letter in the 7th column of x. 
        Also, to address your example of xs[1][7], this wouldn't be the one hot encoding of the entire word cat. the word cat would be made up of 3 different one hot encoding, each one representing a single letter. This allows you to keep the order information.
        >> Thanks! So, xs here actually has a length of 3(which is the length of 'cat'). And xs[0] contains 1 at (7,2) representing c ,xs[1]contains 1 at (7,0) representing a and xs[2] contains 1 at (7,19) representing t. Is it right?
        Exactly! This helps with the forward() function since it lets you go through multiple words at the same time.
        """
        "*** YOUR CODE HERE ***"
        # vector_summary = xs[0] # 1x47
        # print(type(xs[0]))

        vector_summary = nn.Linear(xs[0], self.l1_weight)
        for word in xs:
            curr_word_l1 = nn.Linear(word, self.l1_weight)
            curr_word_l1 = nn.Add(curr_word_l1, vector_summary)
            curr_word_l1 = nn.AddBias(curr_word_l1, self.l1_bias)
            curr_word_l1 = nn.ReLU(curr_word_l1)

            curr_word_l2 = nn.Linear(curr_word_l1, self.l2_weight)
            curr_word_l2 = nn.AddBias(curr_word_l2, self.l2_bias)
            vector_summary = nn.ReLU(curr_word_l2)

        curr_word_l3 = nn.Linear(vector_summary, self.l3_weight)
        curr_word_l3 = nn.AddBias(curr_word_l3, self.l3_bias)
        # no ReLu at end
        return curr_word_l3

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        loss = self.loss_function(self.run(xs), y)
        return loss

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        minimum_accuracy = 0.98
        while (dataset.get_validation_accuracy() < minimum_accuracy):
            batch_size = self.batch_size
            for features, label in dataset.iterate_once(batch_size):
                loss = self.get_loss(features, label) # scalar
                parameters = [self.l1_weight, self.l1_bias, self.l2_weight, self.l2_bias, self.l3_weight, self.l3_bias]
                gradients = nn.gradients(loss, parameters)
                current_loss = nn.as_scalar(loss)
                for i in range(len(parameters)):
                    parameters[i].update(gradients[i], self.learning_rate)
              
