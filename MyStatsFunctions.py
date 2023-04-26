import numpy as np
import random as r
from scipy import stats

# Create function generating unique values given an array of i.e. unique users
def GenerateMyUniqueValues(desired_size, Values, constrained):
    unique = list(np.unique(Values))
    generated_values = []
    while(len(generated_values) < desired_size):
        if constrained == "constrained":
            if desired_size < max(unique):
                rand = r.randint(1, max(unique))
            else:
                print("Data is overconstrained! Reduce 'desired_size' \n")
        else:
            rand = r.randint(1, desired_size + 1)
        if rand not in generated_values:
            generated_values.append(rand)
    print(generated_values)
    return generated_values

def GenerateWeightedUniformDisitribution(desired_size, Values, weight):
    # Customise probability for mode as we know it should be more frequent
    elements_length = max(Values)
    mode = stats.mode(Values)
    mode_probability = weight
    # Remaining probability space is uniformly distributed
    uniform_probability = (1 - mode_probability)/(elements_length - 1)
    probability_array = [uniform_probability] * elements_length
    probability_array[-1] = mode_probability
    elements = range(1, elements_length + 1)
    generated_values = np.random.choice(elements, desired_size, p = probability_array)
    print(generated_values)
    return generated_values

def GenerateEnclosedUniformDistribution(desired_size, Values):
    minimum = min(Values)
    maximum = max(Values)
    elements = range(minimum, maximum + 1)
    elements_length = len(elements)
    uniform_probability = 1/elements_length
    probability_array = [uniform_probability] * elements_length
    generated_values = np.random.choice(elements, desired_size, probability_array)
    print(generated_values)
    return generated_values

def GenerateProportionateDisitribution(desired_size, Values):
    unique = list(np.unique(Values))
    elements_length = len(Values)
    probability_array = []
    for val in unique:
        count = list(Values).count(val)
        probability = count/elements_length
        probability_array.append(probability)
    generated_values = np.random.choice(unique, desired_size, probability_array)
    print(generated_values)
    return generated_values

def GenerateDiscreteDistribution(desired_size, Values, additional_array, probability_array):
    elements = list(np.unique(Values)) + additional_array
    if probability_array == None:
        length = len(elements)
        probability_array = [1/length] * length
    generated_values = np.random.choice(elements, desired_size, probability_array)
    return generated_values

def GenerateNormalDistribution(desired_size, Values):
    mean = np.average(Values)
    stddev = np.std(Values)
    distribution = np.random.normal(loc = mean, scale = stddev, size = (desired_size))
    generated_values = [int(i) for i in distribution]
    # Ensures that values are positive by shifting the distribution
    minimum = min(generated_values)
    if minimum < 0:
        generated_values = [i - (2 * minimum) for i in generated_values]
    print(generated_values)
    return generated_values

def GenerateSoldValues(desired_size, generated_qty_for_produced):
    generated_values = []
    sold_ratios = list(np.random.rand(desired_size))
    sold_ratios = [round(i, 3) for i in sold_ratios]
    for ratio, qty in zip(sold_ratios, generated_qty_for_produced):
        generated_values.append(int(ratio * qty))
    print(generated_values, sold_ratios)
    return generated_values, sold_ratios

def GenerateDummyNames(desired_size, field):
    generated_values = []
    for i in range(0, desired_size):
        name = field + "_" + str(r.randint(1, desired_size + 1))
        generated_values.append(name)
    print(generated_values)
    return generated_values
