def verify_text(actual: str, expected: str):
    """
    Verifies that expected text exists in the actual text.

    Args:
        actual (str): Full string to search within.
        expected (str): Substring to look for.

    Raises:
        AssertionError: If expected text is not found.
    """
    if not isinstance(actual, str) or not isinstance(expected, str):
        raise TypeError("Both arguments must be strings.")

    if expected not in actual:
        raise AssertionError(
            f"❌ Verification failed:\nExpected: '{expected}'\nActual:   '{actual}'"
        )

    print(f"✅ Verification passed: '{expected}' found in actual result.")
