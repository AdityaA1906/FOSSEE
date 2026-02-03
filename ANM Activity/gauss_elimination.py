import numpy as np

def print_header():
    print("=" * 80)
    print("GAUSS ELIMINATION METHOD")
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

def print_augmented_matrix(A, b, title=""):
    if title:
        print(f"\n{title}")
    print("-" * 60)
    for i in range(len(A)):
        row_str = "[ "
        for j in range(len(A[i])):
            row_str += f"{A[i][j]:8.4f} "
        row_str += f"| {b[i]:8.4f} ]"
        print(row_str)
    print("-" * 60)

def gauss_elimination(A, b):
    n = len(b)
    # Create augmented matrix
    Ab = np.column_stack([A.copy(), b.copy()])
    
    print(f"\n{'=' * 80}")
    print("INITIAL AUGMENTED MATRIX [A|b]")
    print(f"{'=' * 80}")
    print_augmented_matrix(A, b)
    
    print(f"\n{'=' * 80}")
    print("FORWARD ELIMINATION")
    print(f"{'=' * 80}")
    print("Goal: Convert to upper triangular form\n")
    
    # Forward elimination
    for k in range(n):
        print(f"\n--- Step {k+1}: Eliminate column {k+1} below diagonal ---\n")
        # Display the general formulas for this step
        print("General formulas for this step (for each row i below pivot k):")
        print(f"Multiplier m_ik = a_ik / a_{k+1}{k+1} (pivot)")
        print(f"Row_i = Row_i - m_ik * Row_{k+1}")
        print("-" * 60)
        
        # Partial pivoting
        max_row = k
        for i in range(k+1, n):
            if abs(Ab[i][k]) > abs(Ab[max_row][k]):
                max_row = i
        
        if max_row != k:
            print(f"Swapping row {k+1} with row {max_row+1} for better numerical stability")
            Ab[[k, max_row]] = Ab[[max_row, k]]
            print_augmented_matrix(Ab[:, :-1], Ab[:, -1], "After row swap:")
        
        # Check for zero pivot
        if abs(Ab[k][k]) < 1e-10:
            if k == n-1: # Last element check
                pass
            else:
                print(f"ERROR: Zero pivot encountered at position ({k+1},{k+1})")
                print("The system may be singular or inconsistent.")
                return None
        
        # Eliminate below
        for i in range(k+1, n):
            if Ab[i][k] != 0:
                factor = Ab[i][k] / Ab[k][k]
                print(f"\nEliminating row {i+1}:")
                print(f"Multiplier m{i+1}{k+1} = {Ab[i][k]:.4f} / {Ab[k][k]:.4f} = {factor:.4f}")
                print(f"Operation: R{i+1} = R{i+1} - ({factor:.4f}) * R{k+1}")
                
                Ab[i] = Ab[i] - factor * Ab[k]
                
                print(f"New row {i+1}:", end=" ")
                for j in range(n+1):
                    # Clean up small values
                    if abs(Ab[i][j]) < 1e-10: Ab[i][j] = 0.0
                    print(f"{Ab[i][j]:.4f}", end=" ")
                print()
        
        print_augmented_matrix(Ab[:, :-1], Ab[:, -1], f"\nMatrix after eliminating column {k+1}:")
    
    print(f"\n{'=' * 80}")
    print("UPPER TRIANGULAR MATRIX (After Forward Elimination)")
    print(f"{'=' * 80}")
    print_augmented_matrix(Ab[:, :-1], Ab[:, -1])
    
    print(f"\n{'=' * 80}")
    print("BACK SUBSTITUTION")
    print(f"{'=' * 80}")
    print("Goal: Solve for variables from bottom to top\n")
    print("General Formula: x_i = (b_i - sum(a_ij * x_j)) / a_ii")
    print("-" * 60)
    
    # Back substitution
    x = np.zeros(n)
    
    for i in range(n-1, -1, -1):
        var_name = ['x', 'y', 'z'][i]
        
        if i == n-1:
            # Last equation
            x[i] = Ab[i][n] / Ab[i][i]
            print(f"From equation {i+1}:")
            print(f"{Ab[i][i]:.4f}*{var_name} = {Ab[i][n]:.4f}")
            print(f"{var_name} = {Ab[i][n]:.4f} / {Ab[i][i]:.4f}")
            print(f"{var_name} = {x[i]:.4f}\n")
        else:
            # Substitute known values
            sum_val = Ab[i][n]
            formula = f"{Ab[i][i]:.4f}*{var_name}"
            
            for j in range(i+1, n):
                sum_val -= Ab[i][j] * x[j]
                formula += f" + {Ab[i][j]:.4f}*{['x', 'y', 'z'][j]}"
            
            x[i] = sum_val / Ab[i][i]
            
            print(f"From equation {i+1}:")
            print(f"{formula} = {Ab[i][n]:.4f}")
            
            # Show substitution
            calc = f"{Ab[i][i]:.4f}*{var_name}"
            for j in range(i+1, n):
                calc += f" + {Ab[i][j]:.4f}*{x[j]:.4f}"
            print(f"{calc} = {Ab[i][n]:.4f}")
            
            # Show solving for variable
            rhs = Ab[i][n]
            for j in range(i+1, n):
                rhs -= Ab[i][j] * x[j]
            print(f"{Ab[i][i]:.4f}*{var_name} = {rhs:.4f}")
            print(f"{var_name} = {rhs:.4f} / {Ab[i][i]:.4f}")
            print(f"{var_name} = {x[i]:.4f}\n")
    
    print(f"{'=' * 80}")
    print("FINAL SOLUTION:")
    print(f"{'=' * 80}")
    print(f"x = {x[0]:.4f}")
    print(f"y = {x[1]:.4f}")
    print(f"z = {x[2]:.4f}")
    print(f"{'=' * 80}")
    
    return x

def verify_solution(A, b, x):
    if x is None:
        return
    
    print(f"\n{'=' * 80}")
    print("VERIFICATION")
    print(f"{'=' * 80}")
    result = np.dot(A, x)
    print("Substituting the solution back into the original equations:")
    for i in range(len(b)):
        lhs = sum(A[i][j] * x[j] for j in range(len(x)))
        print(f"Equation {i+1}: {A[i][0]:.4f}*{x[0]:.4f} + {A[i][1]:.4f}*{x[1]:.4f} + {A[i][2]:.4f}*{x[2]:.4f} = {lhs:.4f} ~= {b[i]:.4f}")
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
    
    solution = gauss_elimination(A, b)
    verify_solution(A, b, solution)
