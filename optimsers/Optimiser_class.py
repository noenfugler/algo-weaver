
class Optimiser():
    def __init__(self):
        self.ls_survivors = []
        self.parameter1_generator = Parameter('int', 2, 100)
        self.parameter2_generator = Parameter('int', 5, 80)
        self.parameter3_generator = Parameter('int', 10, 60)

    def drop_worst(self):
        for i,v in enumerate(self.ls_survivors):
            if i == 0:
                worst_val = v.get_result()
                worst_i = i
            if v.get_result() < worst_val:
                worst_val = v.get_result()
                worst_i = i
        # print(worst_i)
        darwin = self.ls_survivors[worst_i]
        print('dropping', darwin.parameter1, darwin.parameter2, darwin.parameter3, darwin.get_result())
        self.ls_survivors.pop(worst_i)

    def list(self):
        for survivor in self.ls_survivors:
            print(survivor.parameter1, survivor.parameter2, survivor.parameter3, survivor.get_result())

    def seed(self, population):
        #generate starting population
        for p in range(0,population):
            this_strategy = Strategy(self.parameter1_generator.get_rand_value(), self.parameter2_generator.get_rand_value(), self.parameter3_generator.get_rand_value())
            self.ls_survivors.append(this_strategy)

    def run(self, iterations, population):
        #generate children
        for i in range(0,iterations):
            print()
            print('*************************************')
            print()
            for survivor in self.ls_survivors:
                self.drop_worst()
                param = int(random.random()*3)+1
                if param == 1:
                    this_child = Strategy(self.parameter1_generator.get_rand_value(), survivor.parameter2, survivor.parameter3)
                elif param == 2:
                    this_child = Strategy(survivor.parameter1, self.parameter2_generator.get_rand_value(), survivor.parameter3)
                elif param == 3:
                    this_child = Strategy(survivor.parameter1, survivor.parameter2, self.parameter3_generator.get_rand_value())
                print('adding', this_child.parameter1, this_child.parameter2, this_child.parameter3, this_child.get_result())
                print()
                self.ls_survivors.append(this_child)
