# test_engine.py - Unit tests for game engine

from engine import Player

def test_stat_changes():
    print("Test 1: Stat changes...")
    p = Player("TestPlayer")
    p.apply_effects({"Health": 10, "Happiness": -5})
    
    assert p.stats["Health"] == 60, f"Health should be 60, got {p.stats['Health']}"
    assert p.stats["Happiness"] == 45, f"Happiness should be 45, got {p.stats['Happiness']}"
    print("✅ Stat changes test passed")

def test_stat_clamping():
    print("Test 2: Stat boundaries (0-100)...")
    p = Player("TestPlayer")
    p.apply_effects({"Health": 200, "Happiness": -200})
    
    assert p.stats["Health"] == 100, f"Health max should be 100, got {p.stats['Health']}"
    assert p.stats["Happiness"] == 0, f"Happiness min should be 0, got {p.stats['Happiness']}"
    print("✅ Stat boundaries test passed")

def test_ending():
    print("Test 3: Ending system...")
    from engine import get_ending
    p = Player("TestPlayer")
    p.stats = {"Health": 90, "Happiness": 30, "Intelligence": 30, "Wealth": 30, "Social": 30}
    
    ending = get_ending(p)
    assert "yoga" in ending.lower() or "health" in ending.lower(), "Highest stat should be Health"
    print("✅ Ending test passed")

if __name__ == "__main__":
    print("=" * 40)
    print("Running Engine Tests...")
    print("=" * 40)
    
    test_stat_changes()
    test_stat_clamping()
    test_ending()
    
    print("=" * 40)
    print("🎉 All tests passed!")