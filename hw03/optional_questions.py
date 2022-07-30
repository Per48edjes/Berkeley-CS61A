###################################
#  3. Digital, Fall 2017 Midterm  #
###################################


def collapse(n):
    """
    For non-negative N, the result of removing all digits that are equal
    to the digit on their right, so that no adjacent digits are the same.
    >>> collapse(1234)
    1234
    >>> collapse(12234441)
    12341
    >>> collapse(0)
    0
    >>> collapse(3)
    3
    >>> collapse(11200000013333)
    12013
    """
    left, last = n // 10, n % 10
    if left == 0:
        return last
    elif left % 10 == last:
        return collapse(left)
    else:
        return collapse(left) * 10 + last


#######################################################
#  5. Won't You Be My Neighbor?, Summer 2018 Midterm  #
#######################################################


def repeat_digits(n):
    """
    Given a positive integer N, returns a number with each digit repeated.
    >>> repeat_digits(1234)
    11223344
    """
    last, rest = n % 10, n // 10
    if rest == 0:
        return 11 * last
    return repeat_digits(rest) * 100 + 11 * last


#####################################
#  6. Palindromes, Fall 2019 Final  #
#####################################


def pal(n):
    """
    Return a palindrome starting with n
    >>> pal(12430)
    1243003421
    """
    m = n
    while m:
        n, m = (n * 10) + (m % 10), m // 10
    return n


def contains(a, b):
    """
    Return whether the digits of a are contained in the digits of b
    >>> contains(357, 12345678)
    True
    >>> contains(753, 12345678)
    False
    >>> contains(357, 37)
    False
    """
    if a == b:
        return True
    if a > b:
        return False
    if a % 10 == b % 10:
        return contains(a // 10, b // 10)
    else:
        return contains(a, b // 10)


def biggest_palindrome(n):
    """
    Return the largest even-length palindrome in n.
    >>> biggest_palindrome(3425534)
    4554
    >>> biggest_palindrome(126130450234125)
    21300312
    """
    return big(n, 0)


def big(n, k):
    """
    A helper function for biggest_palindrome.
    """
    if n == 0:
        return 0
    choices = [big(n // 10, k), big(n // 10, ((10 * k) + (n % 10)))]
    if contains(k, n):
        choices.append(pal(k))
    return max(choices)
