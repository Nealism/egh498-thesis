import numpy as np


class Space(object):
    """Defines the observation and action spaces, so you can write generic
    code that applies to any Env. For example, you can choose a random
    action.

    WARNING - Custom observation & action spaces can inherit from the `Space`
    class. However, most use-cases should be covered by the existing space
    classes (e.g. `Box`, `Discrete`, etc...), and container classes (`Tuple` &
    `Dict`). Note that parametrized probability distributions (through the
    `sample()` method), and batching functions (in `gym.vector.VectorEnv`), are
    only well-defined for instances of spaces provided in gym by default.
    Moreover, some implementations of Reinforcement Learning algorithms might
    not handle custom spaces properly. Use custom spaces with care.
    """

    def __init__(self, shape=None, dtype=None, seed=None):
        import numpy as np  # takes about 300-400ms to import, so we load lazily

        self._shape = None if shape is None else tuple(shape)
        self.dtype = None if dtype is None else np.dtype(dtype)
        self._np_random = None
        if seed is not None:
            self.seed(seed)

    @property
    def np_random(self):
        """Lazily seed the rng since this is expensive and only needed if
        sampling from this space.
        """
        if self._np_random is None:
            self.seed()

        return self._np_random

    @property
    def shape(self):
        """Return the shape of the space as an immutable property"""
        return self._shape

    def sample(self):
        """Randomly sample an element of this space. Can be
        uniform or non-uniform sampling based on boundedness of space."""
        raise NotImplementedError

    def seed(self, seed=None):
        """Seed the PRNG of this space."""
        return [seed]

    def contains(self, x):
        """
        Return boolean specifying if x is a valid
        member of this space
        """
        raise NotImplementedError

    def __contains__(self, x):
        return self.contains(x)

    def __setstate__(self, state):
        # Don't mutate the original state
        state = dict(state)

        # Allow for loading of legacy states.
        # See:
        #   https://github.com/openai/gym/pull/2397 -- shape
        #   https://github.com/openai/gym/pull/1913 -- np_random
        #
        if "shape" in state:
            state["_shape"] = state["shape"]
            del state["shape"]
        if "np_random" in state:
            state["_np_random"] = state["np_random"]
            del state["np_random"]

        # Update our state
        self.__dict__.update(state)

    def to_jsonable(self, sample_n):
        """Convert a batch of samples from this space to a JSONable data type."""
        # By default, assume identity is JSONable
        return sample_n

    def from_jsonable(self, sample_n):
        """Convert a JSONable data type to a batch of samples from this space."""
        # By default, assume identity is JSONable
        return sample_n


class Box(Space):
    """
    A (possibly unbounded) box in R^n. Specifically, a Box represents the
    Cartesian product of n closed intervals. Each interval has the form of one
    of [a, b], (-oo, b], [a, oo), or (-oo, oo).

    There are two common use cases:

    * Identical bound for each dimension::
        >>> Box(low=-1.0, high=2.0, shape=(3, 4), dtype=np.float32)
        Box(3, 4)

    * Independent bound for each dimension::
        >>> Box(low=np.array([-1.0, -2.0]), high=np.array([2.0, 4.0]), dtype=np.float32)
        Box(2,)

    """

    def __init__(self, low, high, shape=None, dtype=np.float32, seed=None):
        assert dtype is not None, "dtype must be explicitly provided. "
        self.dtype = np.dtype(dtype)

        # determine shape if it isn't provided directly
        if shape is not None:
            shape = tuple(shape)
            assert (
                np.isscalar(low) or low.shape == shape
            ), "low.shape doesn't match provided shape"
            assert (
                np.isscalar(high) or high.shape == shape
            ), "high.shape doesn't match provided shape"
        elif not np.isscalar(low):
            shape = low.shape
            assert (
                np.isscalar(high) or high.shape == shape
            ), "high.shape doesn't match low.shape"
        elif not np.isscalar(high):
            shape = high.shape
            assert (
                np.isscalar(low) or low.shape == shape
            ), "low.shape doesn't match high.shape"
        else:
            raise ValueError(
                "shape must be provided or inferred from the shapes of low or high"
            )

        if np.isscalar(low):
            low = np.full(shape, low, dtype=dtype)

        if np.isscalar(high):
            high = np.full(shape, high, dtype=dtype)

        self._shape = shape
        self.low = low
        self.high = high

        def _get_precision(dtype):
            if np.issubdtype(dtype, np.floating):
                return np.finfo(dtype).precision
            else:
                return np.inf

        low_precision = _get_precision(self.low.dtype)
        high_precision = _get_precision(self.high.dtype)
        dtype_precision = _get_precision(self.dtype)

        self.low = self.low.astype(self.dtype)
        self.high = self.high.astype(self.dtype)

        # Boolean arrays which indicate the interval type for each coordinate
        self.bounded_below = -np.inf < self.low
        self.bounded_above = np.inf > self.high

        super(Box, self).__init__(self.shape, self.dtype, seed)

    def is_bounded(self, manner="both"):
        below = np.all(self.bounded_below)
        above = np.all(self.bounded_above)
        if manner == "both":
            return below and above
        elif manner == "below":
            return below
        elif manner == "above":
            return above
        else:
            raise ValueError("manner is not in {'below', 'above', 'both'}")

    def sample(self):
        """
        Generates a single random sample inside of the Box.

        In creating a sample of the box, each coordinate is sampled according to
        the form of the interval:

        * [a, b] : uniform distribution
        * [a, oo) : shifted exponential distribution
        * (-oo, b] : shifted negative exponential distribution
        * (-oo, oo) : normal distribution
        """
        high = self.high if self.dtype.kind == "f" else self.high.astype("int64") + 1
        sample = np.empty(self.shape)

        # Masking arrays which classify the coordinates according to interval
        # type
        unbounded = ~self.bounded_below & ~self.bounded_above
        upp_bounded = ~self.bounded_below & self.bounded_above
        low_bounded = self.bounded_below & ~self.bounded_above
        bounded = self.bounded_below & self.bounded_above

        # Vectorized sampling by interval type
        sample[unbounded] = self.np_random.normal(size=unbounded[unbounded].shape)

        sample[low_bounded] = (
            self.np_random.exponential(size=low_bounded[low_bounded].shape)
            + self.low[low_bounded]
        )

        sample[upp_bounded] = (
            -self.np_random.exponential(size=upp_bounded[upp_bounded].shape)
            + self.high[upp_bounded]
        )

        sample[bounded] = self.np_random.uniform(
            low=self.low[bounded], high=high[bounded], size=bounded[bounded].shape
        )
        if self.dtype.kind == "i":
            sample = np.floor(sample)

        return sample.astype(self.dtype)

    def contains(self, x):
        if not isinstance(x, np.ndarray):
            x = np.asarray(x, dtype=self.dtype)

        return (
            np.can_cast(x.dtype, self.dtype)
            and x.shape == self.shape
            and np.all(x >= self.low)
            and np.all(x <= self.high)
        )

    def to_jsonable(self, sample_n):
        return np.array(sample_n).tolist()

    def from_jsonable(self, sample_n):
        return [np.asarray(sample) for sample in sample_n]

    def __repr__(self):
        return f"Box({self.low}, {self.high}, {self.shape}, {self.dtype})"

    def __eq__(self, other):
        return (
            isinstance(other, Box)
            and (self.shape == other.shape)
            and np.allclose(self.low, other.low)
            and np.allclose(self.high, other.high)
        )

class Discrete(Space):
    r"""A discrete space in :math:`\{ 0, 1, \\dots, n-1 \}`.

    Example::

        >>> Discrete(2)

    """

    def __init__(self, n, seed=None):
        assert n >= 0
        self.n = n
        super(Discrete, self).__init__((), np.int64, seed)

    def sample(self):
        return self.np_random.randint(self.n)

    def contains(self, x):
        if isinstance(x, int):
            as_int = x
        elif isinstance(x, (np.generic, np.ndarray)) and (
            x.dtype.char in np.typecodes["AllInteger"] and x.shape == ()
        ):
            as_int = int(x)
        else:
            return False
        return as_int >= 0 and as_int < self.n

    def __repr__(self):
        return "Discrete(%d)" % self.n

    def __eq__(self, other):
        return isinstance(other, Discrete) and self.n == other.n