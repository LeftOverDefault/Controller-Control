def apply_deadzone(value, deadzone=0.1):
    """Returns 0 if within deadzone, otherwise scales input"""
    if abs(value) < deadzone:
        return 0
    return value
