import logging
import math
from fractions import Fraction
from typing import Literal, NamedTuple


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    level: Literal["a", "b", "rc"] | None = None
    pre_release: int | None = None
    dev: int | None = None


__version_info__: VersionInfo = VersionInfo(major=0, minor=1, micro=0)
"""Version information."""

__title__ = "somos"
"""Project title."""
__author__ = "Max Kerr (thatgaypigeon)"  # Pigeon43
"""Project author."""
__license__ = "MIT"
"""Project license."""
__copyright__ = "Copyright 2023-present Max Kerr (thatgaypigeon)"  # Pigeon43
"""Project copyright information."""
__version__ = f"{__version_info__.major}.{__version_info__.minor}.{__version_info__.micro}{f'{__version_info__.level}{__version_info__.pre_release}' if __version_info__.level is not None and __version_info__.pre_release is not None else ''}{f'.dev{__version_info__.dev}' if __version_info__.dev is not None else ''}"
"""Project version."""

logging.getLogger(__name__).addHandler(logging.NullHandler())

del logging, NamedTuple, Literal, VersionInfo

__all__ = ["Sequence"]


class Sequence:
    """Represents a somos sequence object.

    .. container:: operations

        .. describe:: x == y

            Checks if two sequences are equal.

        .. describe:: x != y

            Checks if two sequences are not equal.

        .. describe:: str(x)

            Returns the sequence list, comma separated.

        .. describe:: repr(x)

            Returns the sequence's string representation.

    A number of options can be passed to the :class:`Sequence`.

    Parameters
    ------------
    k: :class:`int`
        The integer ``k`` for which to produce the sequence ``somos-k``.
    num_terms Optional[:class:`int`] (default: :paramref:`k` ``+`` :paramref:`num_non_triv_terms`)
        The number of terms to generate.
    num_non_triv_terms: Optional[:class:`int`] (default: ``10``)
        The number of non-trivial terms to generate.
        This excludes the first :paramref:`k` terms since ``a(n) for n < k`` always returns ``1``,
        but does not include all terms for the trivial sequences ``somos-2`` and ``somos-3``.

    Attributes
    ------------
    k: :class:`int`
        The integer ``k`` for which to produce the sequence ``somos-k``.
    sequence: List[:class:`int | Fraction`]
        The list of numbers within the sequence.
    trivial: :class:`bool`
        Whether or not the sequence is trivial. ``True`` for ``k = 2`` and ``k = 3``, else ``False``.
    """

    __slots__: tuple = ("_k", "_sequence", "_trivial", "_ctx")

    def __init__(self, k: int, num_terms: int | None = None, num_non_triv_terms: int | None = None) -> None:
        if not isinstance(k, int):
            # Catch k is not int
            raise TypeError(f"Expected int, received {k.__class__.__name__} instead.")
        elif not isinstance(num_terms, int) and num_terms is not None:
            # Catch num_terms is not int
            raise TypeError(
                f"Expected int, received {num_terms.__class__.__name__} instead."
            )
        elif not isinstance(num_non_triv_terms, int) and num_non_triv_terms is not None:
            # Catch num_non_triv_terms is not int
            raise TypeError(
                f"Expected int, received {num_non_triv_terms.__class__.__name__} instead."
            )

        if k <= 1:
            # Catch values of k below 2
            raise ValueError(
                f"A k value of {k} is invalid. Please use an integer greater than 1."
            )
        elif num_terms is not None and num_terms < 1:
            # Catch values of num_terms below 1
            raise ValueError(
                f"A num_terms value of {num_terms} is invalid. Please use an integer greater than 0."
            )
        elif num_non_triv_terms is not None and num_non_triv_terms < 1:
            # Catch values of num_non_triv_terms below 1
            raise ValueError(
                f"A num_non_triv_terms value of {num_non_triv_terms} is invalid. Please use an integer greater than 0."
            )

        self._k: int = k
        self._trivial: bool = True if self.k < 3 else False
        self._sequence: list[int | Fraction] = []

        self.generate_terms(
            num_terms
            if num_terms
            else (self.k + (num_non_triv_terms if num_non_triv_terms else 10))
        )

    def _term_n(self, n: int) -> int | Fraction:
        """Returns term ``n`` of sequence ``somos-k``.

        .. warning::

            This is an internal method, not intended to be accessed by the user.

            To get term ``n`` of sequence ``somos-k``, use ``Sequence.sequence[n]``.
            Bear in mind ``Sequence.sequence`` is zero-indexed.
        """
        a: list[int | Fraction] = self.sequence
        k: int = self.k

        if n < k:
            # Catch trivial cases. (The first ``k`` terms of sequence ``somos-k`` are trivial ``1``s.)
            return 1

        _range: range = range(1, math.floor(k / 2) + 1)
        _prev_terms: list[int | Fraction] = [a[n - j] * a[n - (k - j)] for j in _range]
        a_n: int | Fraction = Fraction(sum(_prev_terms), a[n - k])
        return a_n

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Sequence) and self.k == other.k

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return ", ".join([str(n) for n in self.sequence])

    def __repr__(self) -> str:
        return f"<somos.Sequence k={self.k} sequence={self.sequence} trivial={self.trivial}>"

    @property
    def k(self) -> int:
        """The integer ``k`` for which to produce the sequence ``somos-k``."""
        return self._k

    @property
    def sequence(self) -> list[int | Fraction]:
        """The list of numbers within the sequence."""
        return self._sequence

    @property
    def trivial(self) -> bool:
        """If the sequence is trivial. ``True`` for ``k = 2`` and ``k = 3``, else ``False``."""
        return self._trivial

    def generate_terms(self, count: int) -> None:
        """Continues generating the ``sequence`` for the specified number of terms.

        Arguments
        ---------
        count: :class:`int`
            The number of terms to generate.

        Raises
        ------
        ``ValueError``: "A count value of 'count' is invalid. Please use an integer greater than 0."
            For ``count < 1``. (``count is not int`` already caught.)

        Examples
        --------
        Generate base sequence with ``3`` terms. (Total 3 terms)
        ```
        >>> seq = Sequence(5, num_terms=3)
        # 1, 1, 1
        ```

        Generate ``5`` more terms. (Total 8 terms)
        ```
        >>> seq.generate_terms(5)
        # 1, 1, 1, 1, 1, 2, 3, 5
        ```

        Generate ``10`` more terms. (Total 18 terms)
        ```
        >>> seq.generate_terms(10)
        # 1, 1, 1, 1, 1, 2, 3, 5, 11, 37, 83, 274, 1217, 6161, 22833, 165713, 1249441, 9434290
        ```"""
        if not isinstance(count, int):
            # Catch count is not int
            raise TypeError(
                f"Expected int, received {count.__class__.__name__} instead."
            )
        elif count < 1:
            # Catch values of count below 1
            raise ValueError(
                f"A count value of {count} is invalid. Please use an integer greater than 0."
            )
        elif self.k <= 3:
            # Catch trivial cases. (All terms of sequences somos-2 and somos-3 are trivial 1s.)
            self.sequence.extend([1 for i in range(count)])
            return

        for n in range(len(self.sequence), len(self.sequence) + count):
            self.sequence.append(self._term_n(n))
