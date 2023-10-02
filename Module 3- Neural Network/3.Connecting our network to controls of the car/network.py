import random

class NeuralNetwork:
    def __init__(self, neuron_counts):
        self.levels = []
        for i in range(len(neuron_counts) - 1):
            self.levels.append(Level(neuron_counts[i], neuron_counts[i + 1]))

    @staticmethod
    def feed_forward(given_inputs, network):
        outputs = []
        for level in network.levels:
            outputs = Level.feed_forward(given_inputs,level)
            print(outputs)
            given_inputs = outputs
        return outputs

class Level:
    def __init__(self, input_count, output_count):
        self.inputs = [0] * input_count
        self.outputs = [0] * output_count
        self.biases = [0] * output_count
        self.weights = []

        # Connect every input node with output nodes
        for _ in range(input_count):
            self.weights.append([random.uniform(-1, 1) for _ in range(output_count)])

        # Assign random values to weights and biases for now
        self.randomize()

    def randomize(self):
        for i in range(len(self.inputs)):
            for j in range(len(self.outputs)):
                self.weights[i][j] = random.uniform(-1, 1)

        for i in range(len(self.biases)):
            self.biases[i] = random.uniform(-1, 1)
        
    
    @staticmethod
    def feed_forward(given_inputs, level):
        for i in range(len(level.inputs)):
            level.inputs[i] = given_inputs[i]

        for i in range(len(level.outputs)):
            # sum_value = 0
            # for j in range(len(level.inputs)):
            #     sum_value += level.inputs[j] * level.weights[j][i]
            sum_value = sum(level.inputs[j] * level.weights[j][i] for j in range(len(level.inputs)))

            if sum_value > level.biases[i]:
                level.outputs[i] = 1
            else:
                level.outputs[i] = 0

        return level.outputs

    # def feed_forward(self, given_inputs):
    #     for i in range(len(self.inputs)):
    #         self.inputs[i] = given_inputs[i]

    #     for i in range(len(self.outputs)):
    #         sum_value = 0
    #         for j in range(len(self.inputs)):
    #             sum_value += self.inputs[j] * self.weights[j][i]

    #         if sum_value > self.biases[i]:
    #             self.outputs[i] = 1
    #         else:
    #             self.outputs[i] = 0

    #     return self.outputs

