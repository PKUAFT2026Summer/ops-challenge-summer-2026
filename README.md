# OPS Challenge Summer 2026

欢迎来到 AFT 算子挑战赛（2026 夏季）！

本仓库为 **GitHub Classroom 模板仓库**，选手通过 Classroom 领取后会获得独立的私有仓库，直接 push 提交代码即可自动评分。

## Overview

* 通过 GitHub Actions + 自托管 Runner 实现自动评分（Online Judge）
* 每周切换一个 Task，每个 Task 对应不同的算子实现
* **提交方式：push 到 `main` 分支**（无需 Fork，无需 PR）
* 排名依据：通过测试后的 **最短运行时间**（`best_time`）
* 你的代码仅存在于自己的 Classroom 仓库中，其他选手无法查看

## GitHub Classroom 使用说明（组织者）

1. 将本仓库设为 **Template repository**（Settings → Template repository）
2. 在 [GitHub Classroom](https://classroom.github.com/) 创建 Assignment，选择本仓库作为模板
3. Assignment 建议选择 **Private repository**，防止选手互相看到代码
4. 确保 Organization 的自托管 Runner（标签 `grader`）对所有仓库可用
5. 将 Assignment 链接发给选手

## 选手提交流程

1. 点击 Classroom Assignment 链接，Accept 后会自动创建你的私有仓库
2. Clone 到本地，安装依赖并本地测试
3. 修改 `src/solution.py` 中的目标函数
4. Commit 并 push 到 `main` 分支
5. 在仓库的 **Actions** 页查看评分结果（Job Summary 中有详细报告）

## Setup Env

```bash
# 需要 Python 3.11

# op1. pip
pip install -r requirements.txt

# op2. poetry
poetry env use python3.11
poetry install
```

## Build ops

* 在 `src/solution.py` 中完成目标算子函数
* 注意只需要完成指定函数，函数签名以当周 Task 为准
* 提交时请只保留函数实现，不要保留测试用的 `main` 逻辑

* 测试数据可以从 [北大网盘](https://disk.pku.edu.cn/link/AAE5DFFDBA5F024C0893C0EBDA39877328) 获取，需要校园网

* 或者通过 Google Drive

  ```bash
  cd testcase

  # data_for_rolling_argmin.parquet
  gdown --fuzzy https://drive.google.com/file/d/16bBa_vO1CLfx7ffLvpicINfV6_Z5WswW/view?usp=drive_link

  # rolling_argmin_v1.npy
  gdown --fuzzy https://drive.google.com/file/d/1Ij2dXy6DLZi9-An9QiiwSzFyexYt15KM/view?usp=drive_link
  ```

* 以上数据集每周会更新

## Test

* 参考的测试脚本在 `localTest.py`

  ```bash
  python localTest.py \
    --entry_point ops_ts_argmin \
    --input_path ./testcase/data_for_rolling_argmin.parquet \
    --ref_ans_path ./testcase/rolling_argmin_v1.npy \
    --window 20
  ```

## 评分与排名

* push `src/solution.py` 到 `main` 后自动触发评分
* 也可在 Actions 页手动触发 **Grade Submission**（workflow_dispatch）
* 排行榜按 **best_time**（历史最短通过耗时）排名，可在 Issue / Discussion 查看官方公布
* 同一仓库可多次 push 重试，取最优成绩

## Timeline

1. week 1：`rolling_rank()`
2. week 2: `rolling_regbeta()`
3. week 3: `ts_argmin()`
