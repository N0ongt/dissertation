import random
import matplotlib.pyplot as plt

def generate_polynomial(secret, degree=1):
    """
    Generates a polynomial with the given secret as the constant term.
    The degree determines the highest degree of x in the polynomial.
    """
    coefficients = [secret]  # secret as the constant term
    for _ in range(degree):
        coefficients.append(random.randint(1, 100))  # random coefficients for other terms
    return coefficients

def evaluate_polynomial(coefficients, x):
    """
    Evaluates the polynomial at a given x.
    """
    result = 0
    for i, coeff in enumerate(coefficients):
        result += coeff * (x ** i)
    return result

def generate_shares(secret, n, k):
    """
    Generates n shares from a secret using Shamir's Secret Sharing with threshold k.
    """
    if k != 2:
        raise ValueError("For a linear polynomial, the threshold k must be 2.")
    
    polynomial = generate_polynomial(secret, degree=k-1)
    shares = [(i, evaluate_polynomial(polynomial, i)) for i in range(1, n + 1)]
    return shares

def lagrange_interpolation(x, points):
    """
    Performs Lagrange interpolation to find the y value at x.
    """
    total = 0
    n = len(points)
    for i in range(n):
        xi, yi = points[i]
        term = yi
        for j in range(n):
            if i != j:
                xj, _ = points[j]
                term *= (x - xj) / (xi - xj)
        total += term
    return total

def reconstruct_secret(shares):
    """
    Reconstructs the secret using the first k shares.
    """
    # For a linear polynomial, we only need 2 shares to reconstruct the secret
    points = shares[:2]
    return lagrange_interpolation(0, points)

def plot_shares(shares, secret):
    """
    Plots the shares and the reconstructed secret on a graph.
    """
    x_values = [share[0] for share in shares]
    y_values = [share[1] for share in shares]

    plt.scatter(x_values, y_values, color='blue', label='Shares')
    plt.scatter(0, secret, color='red', label='Reconstructed Secret', zorder=5)
    plt.title('Shamir Secret Sharing Shares')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    secret = 1234
    n = 5  # Total number of shares
    k = 2  # Threshold to reconstruct the secret (must be 2 for a linear polynomial)

    # Generate shares using Shamir's Secret Sharing
    shares = generate_shares(secret, n, k)

    # Print shares
    for share in shares:
        print(f"Share {share[0]}: {share[1]}")
    
    # Reconstruct the secret
    reconstructed_secret = reconstruct_secret(shares)
    print(f"Reconstructed Secret: {reconstructed_secret}")

    # Plot the shares and the reconstructed secret
    plot_shares(shares, reconstructed_secret)

if __name__ == "__main__":
    main()
