from src.compatibility import check_compatibility, is_upgrade
from src.platform import version_tuple

def test_version_tuple():
    assert version_tuple("8.3.24") == (8, 3, 24)

def test_is_upgrade_same():
    assert is_upgrade("8.3.24", "8.3.24")

def test_is_upgrade_higher():
    assert is_upgrade("8.3.24", "8.3.25")

def test_is_upgrade_downgrade():
    assert not is_upgrade("8.3.24", "8.3.20")

def test_compat_downgrade_rejected():
    result = check_compatibility("8.3.24", "8.3.20")
    assert result["ok"] is False

def test_compat_with_breaking():
    result = check_compatibility("8.3.22", "8.3.23")
    assert not result["ok"]
    assert len(result["breaking_changes"]) > 0

def test_compat_ok():
    result = check_compatibility("8.3.24", "8.3.25")
    assert result["ok"]
