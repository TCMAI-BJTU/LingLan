import os

import argparse
from . import common
from .common import extract_sample_details, ROOT_PATH

import json
import pandas as pd
from datetime import datetime
import re
from .config_evals import get_evals
from .config_models import get_models


def main():
    parser = argparse.ArgumentParser(description="Run sampling and evaluations using different samplers and evaluations.")
    parser.add_argument("--grading-model", default="gpt-5", type=str, help="Select a grading model by name")
    parser.add_argument("--max-tokens", default=1024 * 8, type=int, help="Select a max tokens by name")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument(
        "--model",
        default="gpt-5",
        type=str,
        help="Select a model by name. Also accepts a comma-separated list of models.",
    )
    parser.add_argument(
        "--eval",
        default="tcpe,tcpm_qa_multi_choice,kg_qa_fill_blank,kg_qa_single_choice,kg_qa_multi_choice,tcpm_qa_fill_blank,tcpm_qa_single_choice,ner_ancient,pres_diag,diag_choice,pres_choice,treatment_choice,ner_clinic,pres_diag_char_f1",
        type=str,
        help="Select an eval by name. Also accepts a comma-separated list of evals.",
    )
    parser.add_argument(
        "--n-repeats",
        type=int,
        default=1,
        help="Number of repeats to run. Only supported for certain evals.",
    )
    parser.add_argument(
        "--n-threads",
        type=int,
        default=16,
        help="Number of threads to run.",
    )
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--examples", type=int, default=None, help="Number of examples to use (overrides default)")

    args = parser.parse_args()

    all_models = get_models(args)

    if args.list_models:
        print("Available models:")
        for model_name in all_models.keys():
            print(f" - {model_name}")
        return

    models_to_use = all_models
    if args.model:
        models_chosen = args.model.split(",")
        for model_name in models_chosen:
            if model_name not in all_models:
                print(f"Error: Model '{model_name}' not found.")
                return
        models_to_use = {model_name: all_models[model_name] for model_name in models_chosen}

    print(f"Running with args {args}")

    print(f"loading grading sampler with {args.grading_model}")

    if not args.eval:
        raise ValueError("No eval specified")

    evals_list = args.eval.split(",")
    evals = {}
    for eval_name in evals_list:
        try:
            # 为每个评测创建对应的args
            temp_args = type('Args', (), {
                'eval': eval_name,
                'debug': args.debug,
                'examples': args.examples,
                'grading_model': args.grading_model,
                'n_threads': args.n_threads,
                'n_repeats': args.n_repeats
            })()
            evals[eval_name] = get_evals(temp_args)
        except Exception as e:
            print(f"Error: eval '{eval_name}' not found: {e}")
            return

    print(evals)
    debug_suffix = "_DEBUG" if args.debug else ""
    print(debug_suffix)
    mergekey2resultpath = {}
    print(f"Running the following evals: {list(evals.keys())}")
    print(f"Running evals for the following models: {list(models_to_use.keys())}")

    for model_name, sampler in models_to_use.items():
        for eval_name, eval_obj in evals.items():
            # 构建文件名和路径（添加时间戳）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_stem = f"{eval_name}_{model_name}_{timestamp}"
            tmp_path = f"{ROOT_PATH}/tmp"

            # 创建按eval_name和model_name分层的目录结构
            eval_model_dir = f"{tmp_path}/{eval_name}/{model_name}"
            os.makedirs(eval_model_dir, exist_ok=True)

            print(f"开始运行评估: {eval_name} -> {model_name}")
            result = eval_obj(sampler)
            # ^^^ how to use a sampler

            # 提取每个样本的详细结果
            sample_results = extract_sample_details(result, eval_name, model_name)
            print(f"提取了 {len(sample_results)} 个样本的详细结果")

            result_filename = f"{eval_model_dir}/{file_stem}{debug_suffix}.json"
            report_filename = f"{eval_model_dir}/{file_stem}{debug_suffix}.html"
            excel_filename = f"{eval_model_dir}/{file_stem}{debug_suffix}.xlsx"

            print(f"Writing report to {report_filename}")
            with open(report_filename, "w", encoding="utf-8") as fh:
                fh.write(common.make_report(result))

            # 保存Excel文件
            if sample_results:
                detailed_samples_df = pd.DataFrame(sample_results)
                try:
                    detailed_samples_df.to_excel(excel_filename, index=False)
                except Exception as e:
                    detailed_samples_df.to_csv(excel_filename.replace(".xlsx", ".csv"), index=False, encoding="utf_8_sig")
                print(f"Writing sample details to {excel_filename}")

            assert result.metrics is not None
            metrics = result.metrics | {"score": result.score}
            # Sort metrics by key
            metrics = dict(sorted(metrics.items()))
            print(metrics)
            with open(result_filename, "w", encoding="utf-8") as f:
                f.write(json.dumps(metrics, indent=2, ensure_ascii=False))
            print(f"Writing results to {result_filename}")

            full_result_filename = f"{eval_model_dir}/{file_stem}{debug_suffix}_allresults.json"
            with open(full_result_filename, "w", encoding="utf-8") as f:
                result_dict = {
                    "score": result.score,
                    "metrics": result.metrics,
                    "htmls": result.htmls,
                    "convos": result.convos,
                    "metadata": result.metadata,
                }
                f.write(json.dumps(result_dict, indent=2, ensure_ascii=False))
                print(f"Writing all results to {full_result_filename}")

            mergekey2resultpath[f"{file_stem}"] = result_filename
    merge_metrics = []
    for eval_model_name, result_filename in mergekey2resultpath.items():
        try:
            result = json.load(open(result_filename, "r+"))
        except Exception as e:
            print(e, result_filename)
            continue
        result = result.get("f1_score", result.get("score", None))
        # 解析文件名：格式为 eval_name_model_name_YYYYMMDD_HHMMSS
        parts = eval_model_name.split("_")
        if len(parts) >= 4:
            # 最后两部分是时间戳（YYYYMMDD_HHMMSS），倒数第三部分是model_name
            # 前面所有部分组合成eval_name
            eval_name = "_".join(parts[:-3])
            model_name = parts[-3]
        else:
            # 兼容旧格式
            eval_name = eval_model_name[: eval_model_name.find("_")]
            model_name = eval_model_name[eval_model_name.find("_") + 1 :]
        merge_metrics.append({"eval_name": eval_name, "model_name": model_name, "metric": result})
    merge_metrics_df = pd.DataFrame(merge_metrics).pivot(index=["model_name"], columns="eval_name")
    print("\nAll results: ")
    print(merge_metrics_df.to_markdown())
    return merge_metrics


if __name__ == "__main__":
    main()
