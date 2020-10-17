class partition_number_generator:
    """A class for generating partition numbers. The results are cached for
    speed.
    For some instance X:

    - X.nth_partition_number(n)
        Returns the partition number for the number n
    """

    def __init__(self):
        """Create an object that can calculate partition numbers integers. It
        stores already calculated values for speed
        """

        # Create a generator for the indices
        self.index_generator = self.gaps_to_indices()

        # Create a list to hold these indices. We'll also want to keep track of the
        # next index. At first the next index is larger than the size of the numbers
        # list, once the numbers list becomes larger than next_index, we add it to
        # the index list and create a new next_index. This lets us keep the index
        # list as small as possible.
        self.index_list = [next(self.index_generator)]
        self.next_index = next(self.index_generator)

        # Seed the numbers list with the first partition number
        self.numbers = [1]

        self.gen = self.generate_partition_numbers()

    def generate_partition_numbers(self):
        """Generates partition numbers.
        A partition number describes how many unique ways a number can be
        represented as the sum of positive integers.

        So for example:\n
        3 can be written as {3, 2 + 1, 1 + 1 + 1}, len = 3 \n
        4 can be written as {4, 3 + 1, 2 + 2, 2 + 1 + 1, 1 + 1 + 1 + 1}, len = 5 \n
        The partition number is the length of this set

        To generate the nth number, iterate through the generator n times. So if you
        want to generate the first 10 partition numbers:
        >>> generator = generate_partition_numbers()
        >>> for i in range(10):
        >>>     print(f'{i + 1}: {next(generator)}')
        1: 1
        2: 2
        3: 3
        4: 5
        5: 7
        6: 11
        7: 15
        8: 22
        9: 30
        10: 42

        Formula comes from the Mathologer video on Youtube
        "The hardest 'What comes next?' (Euler's pentagonal formula)":
        https://youtu.be/iJ8pnCO0nTY

        Yields
        -------
        int
            The partition number of the next integer. Starts at 1.
        """

        # Create an arbitrary number of partition numbers
        while True:

            # While our index list is big enough for the current number list
            while self.next_index > len(self.numbers):

                # Calculate the answer, append it to the list of partition numbers
                # for future use, and yield it
                ans = self.calculate_single_number(self.numbers, self.index_list)
                self.numbers.append(ans)
                yield ans

            # Like I described above, add the next_index to the list of indexes
            # since we will now need it to calculate the next partition number.
            # Then create a new next_index so that we can repeat the process.
            self.index_list.append(self.next_index)
            self.next_index = next(self.index_generator)

    def nth_partition_number(self, n: int) -> int:
        """Returns the partition number of n

        Parameters
        ----------
        n : int
            The number we want the partion number of

        Returns
        -------
        int
            The partition number of n
        """

        # If we've already calculated n, return the already calculated value
        if n < len(self.numbers):
            return self.numbers[n]

        # Otherwise generate numbers until we generate n
        while n >= len(self.numbers):

            # The generator has a side effect on self.numbers adding the newly
            # calculated partition numbers to that list
            next(self.gen)

        # Return the last number in our numbers list, which should be the
        # partition number of n
        return self.numbers[-1]

    def calculate_single_number(self, numbers: list[int], indices: list[int]):
        """Given a list of the first n partition numbers and the indices of the
        numbers we will end up adding and subtracting, calculate the n+1 partition
        number.

        Parameters
        ----------
        numbers : list[int]
            The list of the first n partition numbers.

        indices : list[int]
            The list of indices of the numbers list, such that
            numbers[-indices[0]] + numbers[-indices[1]] - numbers[-indices[2]] -
            numbers[-indices[3]] + numbers[-indices[4]] + ... gives is the partition
            number of n+1. indices[-1] must be a valid index for the numbers list

        Returns
        -------
        int
            The n+1 partition number
        """

        cumulative = 0
        sign = -1

        for n, index in enumerate(indices):

            # Switch from adding to subtracting and vice versa every two terms
            if n % 2 == 0:
                sign *= -1

            # Add/subtract the number at the proper index
            cumulative += sign * numbers[-index]

        return cumulative

    def gaps_to_indices(self):
        """Turns the gaps generated by `yield_gaps` above into indices so we can
        more easily turn them into results. It simply takes the sum of all the gaps
        thus far.

        Yields
        -------
        int
            The next index of numbers to add and subtract to calculate our number of
            partitions
        """

        # Here the sum starts at 1. This is just a detail of how it's implemented.
        # Since the indices start from the end of the list and go towards the
        # beginning, having them start at 1 cleans up some of the indices. It also
        # more closely matches the numbers in the video
        cumulative = 1
        yield cumulative

        # Sum the gaps in yield_gaps() and yield the sum
        for i in self.yield_gaps():
            cumulative += i
            yield cumulative

    def yield_gaps(self):
        """A generator that yields the 1, 3, 2, 5, 3, 7, 4, ... sequence that
        describes the gaps between the indices of numbers we add and subtract to
        generate our partition number

        Yields
        -------
        int
            The next gap of between indices
        """
        i = 1
        while True:
            # yield the 1 + _ + 2 + _ + 3 + _ + 4 + ... part of the sequence
            yield i

            # yield the _ + 3 + _ + 5 + _ + 7 + _ + ... part of the sequence
            yield 2 * i + 1

            i += 1