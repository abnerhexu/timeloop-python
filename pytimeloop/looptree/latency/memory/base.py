from typing import overload

from pytimeloop.looptree.reuse.isl import IslReuseAnalysisOutput
from pytimeloop.looptree.reuse.summarized import SummarizedAnalysisOutput
from pytimeloop.looptree.latency.memory import isl


ANALYSIS_TYPE_TO_ANALYZER = {
    IslReuseAnalysisOutput: isl.memory_latency,
    SummarizedAnalysisOutput: summarized.memory_latency
}


@overload
def calculate_memory_latency(reuse_analysis: IslReuseAnalysisOutput,
                             architecture,
                             mapping,
                             workload,
                             bindings):
    pass
@overload
def calculate_memory_latency(reuse_analysis: SummarizedAnalysisOutput,
                             architecture,
                             mapping,
                             workload,
                             bindings):
    pass
def calculate_memory_latency(reuse_analysis,
                             architecture,
                             mapping,
                             workload,
                             bindings):
