import pytest
import tempfile
from pathlib import Path
from macr.system import Layer, System
from macr.library import Pb, CsI


@pytest.fixture
def sample_system():
    system = System()
    system.add_layer(Layer(Pb, 0.1, 0))
    system.add_layer(Layer(Pb, 0.1, 0))
    system.add_layer(Layer(CsI, 0.1, 1))
    system.add_layer(Layer(Pb, 0.1, 0))
    system.add_layer(Layer(CsI, 0.1, 1))
    return system


def test_system_saving_and_loading(sample_system):
    """Test system can be saved and loaded with consistency check."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test_system.pk"

        # Save system
        sample_system._saveSystem(str(filepath))
        assert filepath.exists(), "System file was not created"

        # Load system into new variable
        loaded_system = System()
        loaded_system._loadSystem(str(filepath))

        # Check consistency
        assert len(sample_system) == len(loaded_system), "System lengths don't match"
        assert sample_system.system_id == loaded_system.system_id, (
            "System IDs don't match"
        )

        for i in range(len(sample_system)):
            assert sample_system[i].thickness == loaded_system[i].thickness, (
                f"Layer {i} thickness mismatch"
            )
            assert sample_system[i].active == loaded_system[i].active, (
                f"Layer {i} active flag mismatch"
            )


def test_system_dataframe_after_loading(sample_system):
    """Test that loaded system produces identical DataFrame."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test_system.pk"

        original_df = sample_system.to_dataframe()

        sample_system._saveSystem(str(filepath))
        loaded_system = System()
        loaded_system._loadSystem(str(filepath))
        loaded_df = loaded_system.to_dataframe()

        # Compare DataFrames
        assert original_df.equals(loaded_df), "DataFrames don't match after load"
