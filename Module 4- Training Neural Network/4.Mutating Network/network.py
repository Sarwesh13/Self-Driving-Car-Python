import random
import utils

# class NeuralNetwork:
#     def __init__(self, neuron_counts):
#         self.levels = []
#         for i in range(len(neuron_counts) - 1):
#             self.levels.append(Level(neuron_counts[i], neuron_counts[i + 1]))

#     @staticmethod
#     def feed_forward(given_inputs, network):
#         outputs = []
#         for level in network.levels:
#             outputs = level.feed_forward(given_inputs)
#             given_inputs = outputs
#         return outputs

class NeuralNetwork:
    def __init__(self, neuron_counts):
        self.levels = []
        for i in range(len(neuron_counts) - 1):
            self.levels.append(Level(neuron_counts[i], neuron_counts[i+1]))

    @staticmethod
    def feed_forward(given_inputs, network):
        outputs = Level.feed_forward(given_inputs,network.levels[0])
        for i in range(1,len(network.levels)):
            outputs = Level.feed_forward(outputs,network.levels[i])
        return outputs
    
    @staticmethod
    def mutate(network,amount=1):
        for level in network.levels:
            for i in range(len(level.biases)):
                level.biases[i]=utils.lerp(level.biases[i],random.uniform(-1,1),amount)

            for i in range(len(level.weights)):
                for j in range(len(level.weights[i])):
                    level.weights[i][j]=utils.lerp(level.weights[i][j],random.uniform(-1,1),amount)
    
    def to_string(self):
        result = ""
        for i, level in enumerate(self.levels):
            result += f"Level {i}:\n"
            result += f"Inputs: {level.inputs}\n"
            result += f"Outputs: {level.outputs}\n"
            result += f"Biases: {level.biases}\n"
            result += f"Weights: {level.weights}\n\n"
        return result             

            
class Level:
    def __init__(self, input_count, output_count):
        self.inputs = [None] * input_count
        self.outputs = [None] * output_count
        self.biases = [None] * output_count
        self.weights = []

        # Connect every input node with output nodes
        for _ in range(input_count):
            self.weights.append([None for _ in range(output_count)])
        # self.weights = [[None] * output_count for _ in range(input_count)]


        # Assign random values to weights and biases for now
        self.randomize(self)

    def randomize(self,level):
        for i in range(len(level.inputs)):
            for j in range(len(level.outputs)):
                level.weights[i][j] = random.uniform(-1, 1)

        for i in range(len(level.biases)):
            level.biases[i] = random.uniform(-1, 1)

    # @staticmethod
    # def feed_forward(given_inputs,level):
    #     for i in range(len(level.inputs)):
    #         level.inputs[i] = given_inputs[i]

    #     for i in range(len(level.outputs)):
    #         sum_value = 0
    #         for j in range(len(level.inputs)):
    #             sum_value += level.inputs[j] * level.weights[j][i]

    #         if sum_value > level.biases[i]:
    #             level.outputs[i] = 1
    #         else:
    #             level.outputs[i] = 0

    #     return level.outputs

    @staticmethod
    def feed_forward(given_inputs, level):
        for i in range(len(level.inputs)):
            level.inputs[i] = given_inputs[i]

        for i in range(len(level.outputs)):
            sum_value = 0
            for j in range(len(level.inputs)):
                sum_value += level.inputs[j] * level.weights[j][i]

            if sum_value > level.biases[i]:
                level.outputs[i] = 1
            else:
                level.outputs[i] = 0

        return level.outputs
    



