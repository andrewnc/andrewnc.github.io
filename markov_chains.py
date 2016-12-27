# markov_chains.py


import numpy as np

def random_markov(n):
    """Create and return a transition matrix for a random Markov chain with
    'n' states. This should be stored as an nxn NumPy array.
    """
    arr = np.random.rand(n,n)
    for i in range(n):
        arr[:,i] = arr[:,i]/sum(arr[:,i])

    return arr

def forecast(days):
    """Forecast tomorrow's weather given that today is hot."""
    transition = np.array([[0.7, 0.6], [0.3, 0.4]])
    weather = 0
    li = []


    # Sample from a binomial distribution to choose a new state.
    for i in range(days):
        weather = np.random.binomial(1,transition[1,weather])
        li.append(weather)

    return li


def four_state_forecast(days):
    """Run a simulation for the weather over the specified number of days,
    with mild as the starting state, using the four-state Markov chain.
    Return a list containing the day-by-day results, not including the
    starting day.

    Examples:
        >>> four_state_forecast(3)
        [0, 1, 3]
        >>> four_state_forecast(5)
        [2, 1, 2, 1, 1]
    """
    li = []
    weather = 1
    transition = np.array([[0.5,0.3,0.1,0.0],[0.3,0.3,0.3,0.3],[0.2,0.3,0.4,0.5],[0.0,0.1,0.2,0.2]])
    for i in range(days):
        weather = np.random.multinomial(1, transition[:,weather])
        for j in range(len(weather)):
            if weather[j] == 1:
                weather = j
                break
        li.append(weather)
    return li

def steady_state(A, tol=1e-12, N=40):
    """Compute the steady state of the transition matrix A.

    Inputs:
        A ((n,n) ndarray): A column-stochastic transition matrix.
        tol (float): The convergence tolerance.
        N (int): The maximum number of iterations to compute.

    Raises:
        ValueError: if the iteration does not converge within N steps.

    Returns:
        x ((n,) ndarray): The steady state distribution vector of A.
    """
    n,n = np.shape(A)
    x = np.random.rand(n)
    x /= sum(x)
    x_next = np.zeros(n)
    for i in xrange(N):
        x_prev = np.copy(x_next)
        x_next = np.dot(np.linalg.matrix_power(A,i), x)
        if np.allclose(x_next, x_prev,tol):
            return x_next
    raise ValueError("A does not converge")


class SentenceGenerator(object):
    """Markov chain creator for simulating bad English.

    Attributes:
        (what attributes do you need to keep track of?)

    Example:
        >>> yoda = SentenceGenerator("Yoda.txt")
        >>> print yoda.babble()
        The dark side of loss is a path as one with you.
    """

    def __init__(self, filename):
        """Read the specified file and build a transition matrix from its
        contents. You may assume that the file has one complete sentence
        written on each line.
        """
        words = set()
        my_file = open(filename)
        
        for word in my_file.read().split():
            words.add(word)
        word_count = len(words)
        self.word_count = word_count
        matrix = np.zeros((word_count+2, word_count+2))
        states = ["$tart"]
        my_file.close()

        visited = set()

        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                words = line.split()
                for i in xrange(len(words)):
                    if words[i] not in visited:
                        states.append(words[i])
                        visited.add(words[i])
                    index = states.index(words[i])
                    if i == 0:
                        matrix[index][0] += 1
                for i in xrange(len(words)):
                    index = states.index(words[i])
                    if i != len(words) -1:
                        y_index = states.index(words[i+1])
                    else:
                        y_index = word_count+1
                    matrix[y_index][index] += 1


        for column in range(0,word_count+1):
            div = sum(matrix[:,column])
            if div != 0:
                matrix[:,column] /= div
        self.transition = matrix
        states.append("$top")
        self.states = states




    def babble(self):
        """Begin at the start sate and use the strategy from
        four_state_forecast() to transition through the Markov chain.
        Keep track of the path through the chain and the corresponding words.
        When the stop state is reached, stop transitioning and terminate the
        sentence. Return the resulting sentence as a single string.
        """
        states = []
        current_state = 0
        count = 1
        babble_str = ""
        while current_state != (len(self.states)-1):
            states.append(current_state)
            next = np.random.multinomial(1, self.transition[:,current_state])
            for i in range(len(next)):
                if next[i] == 1:
                    current_state = i
            count += 1
            if count == 1000:
                break
        for state in states:
            if self.states[state] != "$tart":
                babble_str += str(self.states[state]) + " "
        return babble_str



if __name__ == "__main__":

    sg = SentenceGenerator("tswift1989.txt")
    print sg.babble()