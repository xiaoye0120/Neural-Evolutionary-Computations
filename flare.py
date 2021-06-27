from genome import Genome
from population import Population
from phenomes import FeedForwardCPPN as CPPN 
from decode import decode
from visualize import draw_net

# Substrate parameters
sub_in_dims = [1, 24]
sub_sh_dims = [1, 25]
sub_o_dims = 1

# Evolutionary parameters
goal_fitness=9.0
pop_key = 0
pop_size = 150
pop_elitism = 25
num_generations = 7

def get_data(path=None):
    data = []
    label = []
    if path is None:
        path = 'source/flare/flare1.dt'
    data_lines = open(path, mode='r', encoding='utf-8', errors='ignore').readlines()
    for line_index, cur_line in enumerate(data_lines):
        if line_index <= 6:
            pass
        else:
            cur_line = list(map(lambda x: float(x), cur_line.strip().split()))
            data.append(tuple(cur_line[: 24]))
            label.append(cur_line[-1] * 2)
    print('all label:', label)
    print('all label:', set(label), min(label), max(label))
    return data, label

# Define task 定义任务
def xor(genomes):
	# xor_inputs = [(0.0,0.0, 1.),(0.0,1.0, 2.),(1.0,0.0, 3.),(1.0,1.0, 6.)]
	# expected_outputs = [0.0, 1.0, 1.0, 0.0]
	xor_inputs, expected_outputs = get_data()
	# print('xor_inputs:', xor_inputs)
	# Iterate through potential solutions
	for genome_key, genome in genomes:
		cppn = CPPN.create(genome)
		substrate = decode(cppn,sub_in_dims,sub_o_dims,sub_sh_dims)
		sum_square_error = 0.0
		for inputs, expected in zip(xor_inputs, expected_outputs):
            # inputs = inputs + (.0,)
			inputs = inputs + (1.0,)
			actual_output = substrate.activate(inputs)[0]
            # sum_square_error += ((actual_output - expected)**2.0)/25.0
			sum_square_error += ((actual_output - expected)**2.0)/len(xor_inputs)
		genome.fitness = 1.0 - sum_square_error

# Inititalize population
pop = Population(pop_key,pop_size,pop_elitism)

# Run population on the defined task for the specified number of generations
#	and collect the winner
winner_genome = pop.run(xor,goal_fitness,num_generations)

# Decode winner genome into CPPN representation
cppn = CPPN.create(winner_genome)

# Decode Substrate from CPPN
substrate = decode(cppn,sub_in_dims,sub_o_dims,sub_sh_dims)

# Visualize networks of CPPN and Substrate. Files are saved in 
# 	reports/champion_images
draw_net(cppn, filename="reports/champion_images/xor_cppn")
draw_net(substrate, filename="reports/champion_images/xor_substrate")

# Run winning genome on the task again
print("\nChampion Genome: {} with Fitness {}\n".format(winner_genome.key, 
	  											winner_genome.fitness))
xor([(winner_genome.key,winner_genome)])
