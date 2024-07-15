# class to run EquationGenerator class on all n in a range
# and plot results

import matplotlib.pyplot as plt
from equationGenerator import EquationGenerator
from time import time

def main():
    max_n = 6
    results = []
    file = open("batch_results.txt", "w")

    for n in range(2, max_n + 1):
        start_time = time()
        e = EquationGenerator(n)
        e.solve_all()
        e.count_soln_types()
        results.append(e.soln_found_prop)
        time_taken = time() - start_time
        print(f"Time taken: {time_taken:.2f} seconds\n")
        print(f"{n}: {e.soln_found_prop}", file=file)
    
    plt.bar(range(2, max_n+1), results)
    plt.xlabel("n")
    plt.ylabel("Proportion of equations with solutions")
    plt.title(f"Proportion of equations with solutions for n = 2 to {max_n}")
    plt.show()

if __name__ == "__main__":
    main()