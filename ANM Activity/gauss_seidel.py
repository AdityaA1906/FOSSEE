import numpy as np

def print_header():
    print("=" * 80)
    print("GAUSS-SEIDEL ITERATIVE METHOD")
    print("=" * 80)
    print("\nFor a system of equations:")
    print("a11*x + a12*y + a13*z = b1")
    print("a21*x + a22*y + a23*z = b2")
    print("a31*x + a32*y + a33*z = b3")
    print("=" * 80)

def get_input():
    print("\nEnter the coefficients of the system of equations:")
    print("Equation 1: a11*x + a12*y + a13*z = b1")
    a11 = float(input("Enter a11: "))
    a12 = float(input("Enter a12: "))
    a13 = float(input("Enter a13: "))
    b1 = float(input("Enter b1: "))
    
    print("\nEquation 2: a21*x + a22*y + a23*z = b2")
    a21 = float(input("Enter a21: "))
    a22 = float(input("Enter a22: "))
    a23 = float(input("Enter a23: "))
    b2 = float(input("Enter b2: "))
    
    print("\nEquation 3: a31*x + a32*y + a33*z = b3")
    a31 = float(input("Enter a31: "))
    a32 = float(input("Enter a32: "))
    a33 = float(input("Enter a33: "))
    b3 = float(input("Enter b3: "))
    
    A = np.array([[a11, a12, a13],
                  [a21, a22, a23],
                  [a31, a32, a33]], dtype=float)
    
    b = np.array([b1, b2, b3], dtype=float)
    
    return A, b

def check_diagonal_dominance(A):
    n = len(A)
    for i in range(n):
        diagonal = abs(A[i][i])
        row_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diagonal <= row_sum:
            print(f"\nWARNING: Row {i+1} is not diagonally dominant!")
            print(f"|a{i+1}{i+1}| = {diagonal} should be > {row_sum}")
            print("The method may not converge. Proceeding anyway...\n")

def gauss_seidel(A, b, tolerance=0.0001, max_iterations=100):
    n = len(b)
    x = np.zeros(n)  # Initial guess
    x_old = np.zeros(n)
    
    print(f"\nInitial guess: x = {x[0]:.4f}, y = {x[1]:.4f}, z = {x[2]:.4f}")
    print(f"Tolerance: {tolerance}")
    print(f"Maximum iterations: {max_iterations}\n")
    
    for iteration in range(1, max_iterations + 1):
        print(f"\n{'=' * 80}")
        print(f"ITERATION {iteration}")
        print(f"{'=' * 80}")
        
        # Display the formula at the start of each iteration
        print("Formulas used in this iteration:")
        print("x(k+1) = (b1 - a12*y(k) - a13*z(k)) / a11")
        print("y(k+1) = (b2 - a21*x(k+1) - a23*z(k)) / a22  [uses updated x]")
        print("z(k+1) = (b3 - a31*x(k+1) - a32*y(k+1)) / a33  [uses updated x and y]")
        print("-" * 80)
        
        print(f"Starting values: x = {x[0]:.4f}, y = {x[1]:.4f}, z = {x[2]:.4f}\n")
        
        x_old = x.copy()
        
        # Calculate new values using most recent values (Gauss-Seidel)
        for i in range(n):
            sum_val = b[i]
            
            for j in range(n):
                if i != j:
                    sum_val -= A[i][j] * x[j]
            
            x[i] = sum_val / A[i][i]
            
            # Print calculation details
            var_name = ['x', 'y', 'z'][i]
            
            # Show numerical calculation with actual values used
            calc_str = f"{var_name}({iteration}) = ({b[i]:.4f}"
            for j in range(n):
                if i != j:
                    # Note: x array strictly contains the most recent value, so we just use x[j]
                    # We print x_old[j] if j > i (future var) to explain, but programmatically x has mixture
                    # Actually for display clarity let's check index
                    val_used = x[j] 
                    calc_str += f" - {A[i][j]:.4f}*{val_used:.4f}"
            calc_str += f") / {A[i][i]:.4f}"
            print(calc_str)
            print(f"{var_name}({iteration}) = {x[i]:.4f}")
            
            if i > 0:
                 print(f"  (Note: used updated values for previous variables)")
            print()
        
        # Check convergence
        error = np.max(np.abs(x - x_old))
        print(f"Maximum error = max(|x_new - x_old|) = {error:.6f}")
        
        if error < tolerance:
            print(f"\nConverged after {iteration} iterations!")
            print(f"{'=' * 80}")
            print(f"FINAL SOLUTION:")
            print(f"{'=' * 80}")
            print(f"x = {x[0]:.4f}")
            print(f"y = {x[1]:.4f}")
            print(f"z = {x[2]:.4f}")
            print(f"{'=' * 80}")
            return x, iteration
        
    print(f"\nDid not converge within {max_iterations} iterations.")
    print(f"{'=' * 80}")
    print(f"FINAL SOLUTION (after {max_iterations} iterations):")
    print(f"{'=' * 80}")
    print(f"x = {x[0]:.4f}")
    print(f"y = {x[1]:.4f}")
    print(f"z = {x[2]:.4f}")
    print(f"{'=' * 80}")
    return x, max_iterations

def verify_solution(A, b, x):
    print(f"\n{'=' * 80}")
    print("VERIFICATION")
    print(f"{'=' * 80}")
    result = np.dot(A, x)
    print("Substituting the solution back into the original equations:")
    for i in range(len(b)):
        print(f"Equation {i+1}: {result[i]:.4f} ~= {b[i]:.4f} (Error: {abs(result[i] - b[i]):.6f})")
    print(f"{'=' * 80}")

if __name__ == "__main__":
    print_header()
    A, b = get_input()
    
    print(f"\n{'=' * 80}")
    print("SYSTEM OF EQUATIONS:")
    print(f"{'=' * 80}")
    for i in range(3):
        print(f"{A[i][0]:.4f}*x + {A[i][1]:.4f}*y + {A[i][2]:.4f}*z = {b[i]:.4f}")
    print(f"{'=' * 80}")
    
    check_diagonal_dominance(A)
    
    solution, iterations = gauss_seidel(A, b)
    verify_solution(A, b, solution)
