import unittest
from sympy import ceiling
from math import ceil
from pprint import pp

from bindings.looptree import LooptreeWorkload, LooptreeWorkloadDependencyAnalyzer

from tests.load_config_mixin import LoadConfigMixin

from pytimeloop.looptree.reuse.summarized.symbolic import analyze_reuse
from pytimeloop.looptree.reuse.summarized import compile_analysis_result


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

        tile_shapes, result = analyze_reuse(mapping, workload, analyzer)

        self.assertEqual(len(tile_shapes), 3)
        P1_tile_shape, C1_tile_shape, M1_tile_shape = tile_shapes

        REFERENCE_FILLS = {
            ('DRAM', 0, 0): (None, 18),
            ('DRAM', 1, 0): (None, 8),
            ('DRAM', 2, 0): (None, 36),
            ('GlobalBuffer', 0, 0): (None, 18.0*ceiling(4/M1_tile_shape)),
            ('GlobalBuffer', 1, 0): (None, 8)
        }

        for key, ref_value in REFERENCE_FILLS.items():
            self.assertEqual(result.fills[key],
                             ref_value,
                             f'fills for {key} do not match')


class TestCompiler(unittest.TestCase, LoadConfigMixin):
    def test_model_with_two_level_mm(self):
        config, spec = self.load_config([
            'symbolic-mapping.yaml',
            'cascaded_mm.workload.yaml',
            'three_level.arch.yaml'
        ])

        mapping = spec['mapping']['nodes']
        workload = LooptreeWorkload.parse_cfg(config.root['problem'])
        analyzer = LooptreeWorkloadDependencyAnalyzer(workload)

        tile_shapes, result = analyze_reuse(mapping, workload, analyzer)
        self.assertEqual(len(tile_shapes), 3)
        compiled_result = compile_analysis_result(result, tile_shapes)

        for M1_tile_shape_val in [1, 2, 4]:

            REFERENCE_FILLS = {
                ('DRAM', 0, 0): 18,
                ('DRAM', 1, 0): 8,
                ('DRAM', 2, 0): 36,
                ('GlobalBuffer', 0, 0): 18.0*ceil(4/M1_tile_shape_val),
                ('GlobalBuffer', 1, 0): 8
            }

            for key, ref_value in REFERENCE_FILLS.items():
                self.assertEqual(
                    compiled_result.fills[key][1](1, 1, M1_tile_shape_val),
                    ref_value,
                    f'fills for {key} do not match'
                )