from .evals.public_evals.browsecomp_eval import BrowseCompEval
from .evals.public_evals.drop_eval import DropEval
from .evals.public_evals.gpqa_eval import GPQAEval
from .evals.public_evals.healthbench_eval import HealthBenchEval
from .evals.public_evals.healthbench_meta_eval import HealthBenchMetaEval
from .evals.public_evals.math_eval import MathEval
from .evals.public_evals.mgsm_eval import MGSMEval
from .evals.public_evals.mmlu_eval import MMLUEval
from .evals.public_evals.humaneval_eval import HumanEval
from .sampler.chat_completion_sampler import (
    OPENAI_SYSTEM_MESSAGE_API,
    OPENAI_SYSTEM_MESSAGE_CHATGPT,
    ChatCompletionSampler,
)
from .sampler.claude_sampler import ClaudeCompletionSampler, CLAUDE_SYSTEM_MESSAGE_LMSYS
from .sampler.o_chat_completion_sampler import OChatCompletionSampler
from .sampler.responses_sampler import ResponsesSampler
from .evals.public_evals.simpleqa_eval import SimpleQAEval
from .evals.tcm_evals.tcpe_eval import TCPEEval
from .evals.tcm_evals.kg_qa_fill_blank import KGQAFillBlankEval
from .evals.tcm_evals.kg_qa_single_choice import KGQASingleChoiceEval
from .evals.tcm_evals.kg_qa_multi_choice import KGQAMultiChoiceEval
from .evals.tcm_evals.kg_qa_other import KGQAOtherEval
from .evals.tcm_evals.tcpm_qa_fill_blank import TCPMQAFillBlankEval
from .evals.tcm_evals.tcpm_qa_single_choice import TCPMQASingleChoiceEval
from .evals.tcm_evals.tcpm_qa_multi_choice import TCPMQAMultiChoiceEval
from .evals.tcm_evals.tcpm_qa_other import TCPMQAOtherEval
from .evals.tcm_evals.ner_clinic import NERClinicEval
from .evals.tcm_evals.ner_ancient import NERAncientEval
from .evals.tcm_evals.pres_diag_eval import PresDigEval
from .evals.tcm_evals.pres_diag_eval_char_f1 import PresDigEvalCharF1
from .evals.tcm_evals.diag_choice_eval import DiagChoiceEval
from .evals.tcm_evals.pres_choice_eval import PresChoiceEval
from .evals.tcm_evals.treatment_choice_eval import TreatmentChoiceEval
from . import common

ROOT_PATH = common.ROOT_PATH

def get_grading_sampler(grading_model):
    return ChatCompletionSampler(
        model=grading_model,
        max_tokens=2048,
    )

def get_equality_checker(grading_model):
    return ChatCompletionSampler(model=grading_model)
# ^^^ used for fuzzy matching, just for math


def get_evals(args):
    eval_name = args.eval
    debug_mode = args.debug
    num_examples = args.examples if args.examples is not None else (5 if debug_mode else None)

    # 初始化采样器
    grading_sampler = get_grading_sampler(args.grading_model)
    equality_checker = get_equality_checker(args.grading_model)

    # Set num_examples = None to reproduce full evals
    match eval_name:
        case "mmlu":
            return MMLUEval(num_examples=1 if debug_mode else num_examples)
        case "math":
            return MathEval(
                equality_checker=equality_checker,
                num_examples=num_examples,
                n_repeats=1 if debug_mode else args.n_repeats or 10,
            )
        case "gpqa":
            return GPQAEval(
                n_repeats=1 if debug_mode else args.n_repeats or 10,
                num_examples=num_examples,
            )
        case "mgsm":
            return MGSMEval(num_examples_per_lang=10 if debug_mode else num_examples or 250)
        case "drop":
            return DropEval(
                num_examples=10 if debug_mode else num_examples,
                train_samples_per_prompt=3,
            )
        case "humaneval":
            return HumanEval(num_examples=10 if debug_mode else num_examples)
        case "simpleqa":
            return SimpleQAEval(
                grader_model=grading_sampler,
                num_examples=10 if debug_mode else num_examples,
            )
        case "browsecomp":
            return BrowseCompEval(
                grader_model=grading_sampler,
                num_examples=10 if debug_mode else num_examples,
            )
        case "healthbench":
            return HealthBenchEval(
                grader_model=grading_sampler,
                num_examples=10 if debug_mode else num_examples,
                n_repeats=args.n_repeats or 1,
                n_threads=args.n_threads or 1,
                subset_name=None,
            )
        case "healthbench_hard":
            return HealthBenchEval(
                grader_model=grading_sampler,
                num_examples=10 if debug_mode else num_examples,
                n_repeats=args.n_repeats or 1,
                n_threads=args.n_threads or 1,
                subset_name="hard",
            )
        case "healthbench_consensus":
            return HealthBenchEval(
                grader_model=grading_sampler,
                num_examples=10 if debug_mode else num_examples,
                n_repeats=args.n_repeats or 1,
                n_threads=args.n_threads or 1,
                subset_name="consensus",
            )
        case "healthbench_meta":
            return HealthBenchMetaEval(
                grader_model=grading_sampler,
                num_examples=10 if debug_mode else num_examples,
                n_repeats=args.n_repeats or 1,
                n_threads=args.n_threads or 1,
            )
        case "tcpe":
            data_path = f"{ROOT_PATH}/eval_dataset/中医考试题.jsonl"
            return TCPEEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "kg_qa_fill_blank":
            data_path = f"{ROOT_PATH}/eval_dataset/知识图谱知识问答合集_2000_V251003.jsonl"
            return KGQAFillBlankEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "kg_qa_single_choice":
            data_path = f"{ROOT_PATH}/eval_dataset/知识图谱知识问答合集_2000_V251003.jsonl"
            return KGQASingleChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "kg_qa_multi_choice":
            data_path = f"{ROOT_PATH}/eval_dataset/知识图谱知识问答合集_2000_V251003.jsonl"
            return KGQAMultiChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "kg_qa_other":
            data_path = f"{ROOT_PATH}/eval_dataset/知识图谱知识问答合集_2000_V251003.jsonl"
            return KGQAOtherEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "tcpm_qa_fill_blank":
            data_path = f"{ROOT_PATH}/eval_dataset/中成药知识问答合集_2000_V251003.jsonl"
            return TCPMQAFillBlankEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "tcpm_qa_single_choice":
            data_path = f"{ROOT_PATH}/eval_dataset/中成药知识问答合集_2000_V251003.jsonl"
            return TCPMQASingleChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "tcpm_qa_multi_choice":
            data_path = f"{ROOT_PATH}/eval_dataset/中成药知识问答合集_2000_V251003.jsonl"
            return TCPMQAMultiChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "tcpm_qa_other":
            data_path = f"{ROOT_PATH}/eval_dataset/中成药知识问答合集_2000_V251003.jsonl"
            return TCPMQAOtherEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "ner_clinic":
            data_path = f"{ROOT_PATH}/eval_dataset/实体抽取-病历.jsonl"
            return NERClinicEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "ner_ancient":
            data_path = f"{ROOT_PATH}/eval_dataset/实体抽取-古籍.jsonl"
            return NERAncientEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "pres_diag":
            data_path = f"{ROOT_PATH}/eval_dataset/医家辨证治法处方推荐_V251001.jsonl"
            return PresDigEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "pres_diag_char_f1":
            data_path = f"{ROOT_PATH}/eval_dataset/医家辨证治法处方推荐_V251001.jsonl"
            return PresDigEvalCharF1(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "diag_choice":
            data_path = f"{ROOT_PATH}/eval_dataset/医家辨证_选择题_V251001.jsonl"
            return DiagChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "pres_choice":
            data_path = f"{ROOT_PATH}/eval_dataset/医家处方_选择题_V251001.jsonl"
            return PresChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "treatment_choice":
            data_path = f"{ROOT_PATH}/eval_dataset/医家治法_选择题_V251001.jsonl"
            return TreatmentChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        # Hard subset evaluations
        case "tcpe_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/tcpe_hard_V251015.jsonl"
            return TCPEEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "kg_qa_fill_blank_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/kg_qa_fill_blank_hard_V251015.jsonl"
            return KGQAFillBlankEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "kg_qa_single_choice_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/kg_qa_single_choice_hard_V251015.jsonl"
            return KGQASingleChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "kg_qa_multi_choice_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/kg_qa_multi_choice_hard_V251015.jsonl"
            return KGQAMultiChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "tcpm_qa_fill_blank_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/tcpm_qa_fill_blank_hard_V251015.jsonl"
            return TCPMQAFillBlankEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "tcpm_qa_single_choice_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/tcpm_qa_single_choice_hard_V251015.jsonl"
            return TCPMQASingleChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "tcpm_qa_multi_choice_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/tcpm_qa_multi_choice_hard_V251015.jsonl"
            return TCPMQAMultiChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "ner_clinic_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/ner_clinic_hard_V251015.jsonl"
            return NERClinicEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "ner_ancient_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/ner_ancient_hard_V251015.jsonl"
            return NERAncientEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "pres_diag_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/pres_diag_hard_V251015.jsonl"
            return PresDigEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "pres_diag_char_f1_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/pres_diag_hard_V251015.jsonl"
            return PresDigEvalCharF1(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "diag_choice_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/diag_choice_hard_V251015.jsonl"
            return DiagChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "pres_choice_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/pres_choice_hard_V251015.jsonl"
            return PresChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case "treatment_choice_hard":
            data_path = f"{ROOT_PATH}/eval_dataset/treatment_choice_hard_V251015.jsonl"
            return TreatmentChoiceEval(data_path=data_path, num_examples=num_examples, num_threads=args.n_threads)
        case _:
            raise Exception(f"Unrecognized eval type: {eval_name}")
