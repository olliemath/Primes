"""
Python Prime Sieve

With specialization for 3 by Oliver Margetts. How's my algorithm?
"""
import sys
from math import sqrt

# Historical data for validating our results - the number of primes
# to be found under some limit, such as 168 primes under 1000
PRIME_COUNTS = {
    10: 4,
    100: 25,
    1000: 168,
    10000: 1229,
    100000: 9592,
    1000000: 78498,
    10000000: 664579,
    100000000: 5761455,
}


class PrimeSieve:

    def __init__(self, length):
        self.size = length
        self._bits = bytearray((3 * length) // 8 or 1)

    def run_sieve(self):
        """Calculate the primes up to the specified limit"""
        factor = 0
        # sqrt doesn't seem to make any difference in CPython,
        # but works much faster than "x**.5" in Pypy
        q = (3 * (sqrt(self.size) - 1)) / 8
        bitslen = len(self._bits)

        while factor < q:
            factor = self._bits.index(b"\x00", factor)

            # We miss out all things divisible by 2 and 3 in our array. This
            # means there will be two evenly spaced sequences of multiples of
            # the original prime. While these numbers below look like magic,
            # they come from some modular arithmetic:
            mod = factor // 2
            num = 2 * (factor + mod) + 5
            step = 2 * num
            start1 = factor + step

            if (bitslen - start1) % step:
                self._bits[start1::step] = b"\x01" * ((bitslen - start1) // step + 1)
            else:
                self._bits[start1::step] = b"\x01" * ((bitslen - start1) // step)
            start2 = factor + num + 2 * (1 + mod)
            if (bitslen - start2) % step:
                self._bits[start2::step] = b"\x01" * ((bitslen - start2) // step + 1)
            else:
                self._bits[start2::step] = b"\x01" * ((bitslen - start2) // step)

            factor += 1

    def nums(self):
        """Return the numbers the array bits represent"""
        return [2 * (k + k // 2) + 5 for k in range(len(self._bits))]

    def get_primes(self):
        if self.size <= 1:
            return []
        if self.size == 2:
            return [2]

        primes = [2, 3]
        for n, b in zip(self.nums(), self._bits):
            if b == 0 and n <= self.size:
                primes.append(n)
        return primes

    def count_primes(self):
        return len(self.get_primes())

    def validate_results(self):
        """Check the count of primes in the historical data (if we have it)
        to see if it matches"""
        if self.size in PRIME_COUNTS:
            return PRIME_COUNTS[self.size] == self.count_primes()

    def print_results(self, show_results, duration, passes):

        """Displays the primes found (or just the total count,
        depending on what you ask for)"""
        interpreter = sys.executable.rsplit("/", 1)[1]
        impl = "pypy" if interpreter == "pypy3" else "cpython"

        if show_results:
            print(", ".join(map(str, self.get_primes())))

        count = len(self.get_primes())
        valid = self.validate_results()
        print(
            f"Passes: {passes}, Time: {duration}, Avg: {duration / passes}, "
            f"Limit: {self.size}, Count: {count}, Valid: {valid}"
        )
        print()
        # Following 2 lines added by rbergen to conform to drag race output format
        print(f"olliemath_{impl}; {passes};{duration};1;algorithm=base,faithful=yes,bits=8")


# MAIN Entry
if __name__ == "__main__":
    from time import sleep
    from timeit import default_timer
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Python Prime Sieve")
    parser.add_argument(
        "--limit",
        "-l",
        help="Upper limit for calculating prime numbers",
        type=int,
        default=1_000_000,
    )
    parser.add_argument(
        "--time", "-t", help="Time limit", type=float, default=5
    )
    parser.add_argument(
        "--show", "-s", help="Print found prime numbers", action="store_true"
    )

    args = parser.parse_args()
    limit = args.limit
    timeout = args.time
    show_results = args.show
    sleep(1)  # This actually makes a difference dockerised

    time_start = default_timer()  # Record our starting time
    passes = 0  # We're going to count how many passes in fixed window of time

    # Run until more than 10 seconds have elapsed
    while (default_timer() - time_start < timeout):
        sieve = PrimeSieve(limit)
        sieve.run_sieve()  # # Calc the primes up to a million
        passes = passes + 1  # Count this pass

    # After the "at least 10 seconds", get the actual elapsed
    time_delta = default_timer() - time_start

    # Display outcome
    sieve.print_results(show_results, time_delta, passes)
