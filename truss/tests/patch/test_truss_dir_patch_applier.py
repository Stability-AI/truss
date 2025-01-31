import logging
from pathlib import Path

from truss.patch.truss_dir_patch_applier import TrussDirPatchApplier
from truss.templates.control.control.helpers.types import (
    Action,
    ModelCodePatch,
    Patch,
    PatchType,
    PythonRequirementPatch,
    SystemPackagePatch,
)
from truss.truss_config import TrussConfig

TEST_LOGGER = logging.getLogger("test_logger")


def test_model_code_patch(custom_model_truss_dir: Path):
    applier = TrussDirPatchApplier(custom_model_truss_dir, TEST_LOGGER)
    applier(
        [
            Patch(
                type=PatchType.MODEL_CODE,
                body=ModelCodePatch(
                    action=Action.UPDATE, path="model.py", content="test_content"
                ),
            )
        ]
    )
    assert (custom_model_truss_dir / "model" / "model.py").read_text() == "test_content"


def test_python_requirement_patch(custom_model_truss_dir: Path):
    req = "git+https://github.com/huggingface/transformers.git"
    applier = TrussDirPatchApplier(custom_model_truss_dir, TEST_LOGGER)
    applier(
        [
            Patch(
                type=PatchType.PYTHON_REQUIREMENT,
                body=PythonRequirementPatch(
                    action=Action.ADD,
                    requirement=req,
                ),
            )
        ]
    )
    assert TrussConfig.from_yaml(
        custom_model_truss_dir / "config.yaml"
    ).requirements == [req]


def test_system_requirement_patch(custom_model_truss_dir: Path):
    applier = TrussDirPatchApplier(custom_model_truss_dir, TEST_LOGGER)
    applier(
        [
            Patch(
                type=PatchType.SYSTEM_PACKAGE,
                body=SystemPackagePatch(
                    action=Action.ADD,
                    package="curl",
                ),
            )
        ]
    )
    assert TrussConfig.from_yaml(
        custom_model_truss_dir / "config.yaml"
    ).system_packages == ["curl"]
