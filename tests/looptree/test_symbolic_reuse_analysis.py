import unittest
from pathlib import Path
from itertools import starmap

from bindings.looptree import *
from tests.util import TEST_TMP_DIR

from tests.load_config_mixin import LoadConfigMixin

from pytimeloop.looptree.reuse.summarized.symbolic import analyze_reuse


class TestSymbolicReuseAnalysis(unittest.TestCase, LoadConfigMixin):
    def test_model_with_two_level_mm(self):
        config, spec = self.load_config([
            'symbolic-mapping.yaml',
            'cascaded_mm.workload.yaml',
            'three_level.arch.yaml'
        ])

        mapping = spec['mapping']['nodes']
        workload = LooptreeWorkload.parse_cfg(config.root['problem'])
        analyzer = LooptreeWorkloadDependencyAnalyzer(workload)

        result = analyze_reuse(mapping, workload, analyzer)
        print(result)
