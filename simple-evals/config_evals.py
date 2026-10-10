from pathlib import Path

from .evals.tcm_evals.tcpe_eval import TCPEEval
from .evals.tcm_evals.kg_qa_fill_blank import KGQAFillBlankEval
from .evals.tcm_evals.kg_qa_single_choice import KGQASingleChoiceEval
from .evals.tcm_evals.kg_qa_multi_choice import KGQAMultiChoiceEval
from .evals.tcm_evals.tcpm_qa_fill_blank import TCPMQAFillBlankEval
from .evals.tcm_evals.tcpm_qa_single_choice import TCPMQASingleChoiceEval
from .evals.tcm_evals.tcpm_qa_multi_choice import TCPMQAMultiChoiceEval
from .evals.tcm_evals.ner_clinic import NERClinicEval
from .evals.tcm_evals.ner_ancient import NERAncientEval
from .evals.tcm_evals.pres_diag_eval import PresDigEval
from .evals.tcm_evals.pres_diag_eval_char_f1 import PresDigEvalCharF1
from .evals.tcm_evals.diag_choice_eval import DiagChoiceEval
from .evals.tcm_evals.pres_choice_eval import PresChoiceEval
from .evals.tcm_evals.treatment_choice_eval import TreatmentChoiceEval

# 从配置文件定位发布数据，不依赖启动命令的工作目录。
DATA_ROOT = Path(__file__).resolve().parents[1] / "data"
TCM_EVALS = {
    "tcm_licensing_examination": (TCPEEval, "tcm_licensing_examination/中医考试题.jsonl"),
    "fundamental_tcm_knowledge_single_choice": (
        KGQASingleChoiceEval, "fundamental_tcm_knowledge/知识图谱知识问答_单选题.jsonl"
    ),
    "fundamental_tcm_knowledge_multiple_choice": (
        KGQAMultiChoiceEval, "fundamental_tcm_knowledge/知识图谱知识问答_多选题.jsonl"
    ),
    "fundamental_tcm_knowledge_fill_blank": (
        KGQAFillBlankEval, "fundamental_tcm_knowledge/知识图谱知识问答_填空题.jsonl"
    ),
    "chinese_patent_medicine_knowledge_single_choice": (
        TCPMQASingleChoiceEval, "chinese_patent_medicine_knowledge/中成药知识问答_单选题.jsonl"
    ),
    "chinese_patent_medicine_knowledge_multiple_choice": (
        TCPMQAMultiChoiceEval, "chinese_patent_medicine_knowledge/中成药知识问答_多选题.jsonl"
    ),
    "chinese_patent_medicine_knowledge_fill_blank": (
        TCPMQAFillBlankEval, "chinese_patent_medicine_knowledge/中成药知识问答_填空题.jsonl"
    ),
    "classical_text_entity_extraction": (NERAncientEval, "information_extraction/实体抽取_古籍.jsonl"),
    "clinical_record_entity_extraction": (NERClinicEval, "information_extraction/实体抽取_病历.jsonl"),
    "syndrome_single_choice": (DiagChoiceEval, "decision_recognition/医家辨证_选择题.jsonl"),
    "treatment_method_single_choice": (TreatmentChoiceEval, "decision_recognition/医家治法_选择题.jsonl"),
    "herbal_prescription_single_choice": (PresChoiceEval, "decision_recognition/医家处方_选择题.jsonl"),
    # 三个生成任务的标签在加载时关联，保留一次生成三个结果的流程。
    "diagnostic_therapeutic_reasoning": (PresDigEval, "diagnostic_therapeutic_reasoning"),
    "diagnostic_therapeutic_reasoning_char_f1": (PresDigEvalCharF1, "diagnostic_therapeutic_reasoning"),
}
DEFAULT_TCM_EVALS = ",".join(TCM_EVALS)


def get_grading_sampler(grading_model):
    from .sampler.chat_completion_sampler import ChatCompletionSampler

    return ChatCompletionSampler(model=grading_model, max_tokens=2048)


def get_equality_checker(grading_model):
    from .sampler.chat_completion_sampler import ChatCompletionSampler

    return ChatCompletionSampler(model=grading_model)


def get_evals(args):
    eval_name = args.eval
    debug_mode = args.debug
    num_examples = args.examples if args.examples is not None else (5 if debug_mode else None)
    split = getattr(args, "split", "fullset")
    if split not in ("fullset", "hardset"):
        raise ValueError(f"Unrecognized data split: {split}")

    if eval_name in TCM_EVALS:
        evaluator_class, relative_path = TCM_EVALS[eval_name]
        evaluation = evaluator_class(
            data_path=str(DATA_ROOT / split / relative_path),
            num_examples=num_examples,
            num_threads=args.n_threads,
        )
        evaluation.dataset_split = split
        return evaluation

    # 公开通用任务按需导入；中医任务不需要额外的裁判模型。
    match eval_name:
        case "mmlu":
            from .evals.public_evals.mmlu_eval import MMLUEval
            return MMLUEval(num_examples=1 if debug_mode else num_examples)
        case "math":
            from .evals.public_evals.math_eval import MathEval
            return MathEval(
                equality_checker=get_equality_checker(args.grading_model),
                num_examples=num_examples,
                n_repeats=1 if debug_mode else args.n_repeats or 10,
            )
        case "gpqa":
            from .evals.public_evals.gpqa_eval import GPQAEval
            return GPQAEval(
                n_repeats=1 if debug_mode else args.n_repeats or 10,
                num_examples=num_examples,
            )
        case "mgsm":
            from .evals.public_evals.mgsm_eval import MGSMEval
            return MGSMEval(num_examples_per_lang=10 if debug_mode else num_examples or 250)
        case "drop":
            from .evals.public_evals.drop_eval import DropEval
            return DropEval(num_examples=10 if debug_mode else num_examples, train_samples_per_prompt=3)
        case "humaneval":
            from .evals.public_evals.humaneval_eval import HumanEval
            return HumanEval(num_examples=10 if debug_mode else num_examples)
        case "simpleqa":
            from .evals.public_evals.simpleqa_eval import SimpleQAEval
            return SimpleQAEval(
                grader_model=get_grading_sampler(args.grading_model),
                num_examples=10 if debug_mode else num_examples,
            )
        case "browsecomp":
            from .evals.public_evals.browsecomp_eval import BrowseCompEval
            return BrowseCompEval(
                grader_model=get_grading_sampler(args.grading_model),
                num_examples=10 if debug_mode else num_examples,
            )
        case "healthbench" | "healthbench_hard" | "healthbench_consensus":
            from .evals.public_evals.healthbench_eval import HealthBenchEval
            subset = {"healthbench_hard": "hard", "healthbench_consensus": "consensus"}.get(eval_name)
            return HealthBenchEval(
                grader_model=get_grading_sampler(args.grading_model),
                num_examples=10 if debug_mode else num_examples,
                n_repeats=args.n_repeats or 1,
                n_threads=args.n_threads or 1,
                subset_name=subset,
            )
        case "healthbench_meta":
            from .evals.public_evals.healthbench_meta_eval import HealthBenchMetaEval
            return HealthBenchMetaEval(
                grader_model=get_grading_sampler(args.grading_model),
                num_examples=10 if debug_mode else num_examples,
                n_repeats=args.n_repeats or 1,
                n_threads=args.n_threads or 1,
            )
        case _:
            raise ValueError(f"Unrecognized eval type: {eval_name}")
