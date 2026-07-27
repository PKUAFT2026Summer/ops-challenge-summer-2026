# 算子比赛提交指南

## 1. 申请 GitHub 账号并登录 Classmoji

1. 申请 [GitHub](https://github.com/) 账号。
2. 登录 [Classmoji](https://app.classmoji.io/)。
3. 选择 **Continue with GitHub**。
4. 直接选择 GitHub 的注册邮箱即可，不用管是不是 edu 邮箱。
5. 在群表格中填入你的【用户名（同 GitHub 名称）+ 注册邮箱】，例如：`Test + xxxxxxx@stu.pku.edu.cn`。
6. 等待管理员邀请你加入 `ops-challenge-summer-2026`。随后在 Classmoji 中会看到这个 Class，点击 **Active** 中比赛的卡片并 **Accept**，加入 GitHub organization 的邮件就会发送到你的 GitHub 注册邮箱。
7. 进入邮件中的 **Join** 链接完成加入。看到 Classmoji 上方的确认提示后，就说明已经正确加入。

至此，所有前期准备工作都完成了。

## 2. 提交答案

### 找到本次作业

等待管理员公布赛题后，在 **Repositories** 中找到当周任务，点击 **Open repo** 打开 GitHub 仓库。

如果你是新加入的同学，管理员可能需要手动操作后你才能看到任务；可以稍等一下，或者私戳管理员确认。

### 下载仓库

打开一个本地目录，把自己仓库里的代码 clone 到本地。第一次 clone 可能需要登录 GitHub。

```bash
# 下面是示例，注意要换成你自己的链接
git clone https://github.com/PKUAFT2026Summer/week1-Howard-03.git
```

第一次提交之前，还需要在仓库中启用自动评分：进入仓库的 **Actions** 页面，点击 **Enable Actions on this repository**。这样后续就能开启自动评分。

### 配置环境

完成 clone 后，你应该能在刚刚创建的文件夹中看到仓库里的所有文件。把[北大网盘](https://disk.pku.edu.cn/link/AAD9950DBA572E407AB0E3DB41FBF44D6A)中的数据和 `.npy` 文件下载下来，放到项目根目录下自己新建的 `testcase` 文件夹中。

也可以使用 Google Drive 下载：

```bash
mkdir -p testcase
cd testcase

# install gdown instrument
pip install gdown

# data_for_ts_argmin.parquet
gdown --fuzzy 'https://drive.google.com/file/d/1DLuX8Y9fvXk0cn7SbedDCnEIw34YcXdP/view?usp=drive_link'

# rolling_rank_dense_v1.npy
gdown --fuzzy 'https://drive.google.com/file/d/11xeeojmk4JTmrqPGxWd1es0hcHlU3Syq/view?usp=drive_link'
```

如果 `gdown` 或 `conda` 安装时报错，可以尝试把 VPN 代理改为直连，或者设置清华镜像源：

```bash
# 清除现有源缓存
conda clean -i

# 添加清华镜像源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/pro/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2/

# 设置搜索时显示通道地址
conda config --set show_channel_urls yes
```

进行配置前，先设置好虚拟环境，不要所有包都放在同一个 `base` 环境中。比赛要求的 Python 环境至少是 3.11，推荐使用 Python 3.11。

```bash
# 安装虚拟环境，提示是否安装时按 y 即可
conda create -n py311ops python=3.11

# 进入虚拟环境
conda activate py311ops

# 在项目根目录里安装依赖
pip install -r requirements.txt
```

### 提交答案

之后就可以修改代码并提交答案了。只需要修改 `src/solution.py` 这一个文件即可；提交前，先本地测试看看能不能跑通。

```bash
python localTest.py \
  --entry_point ops_ts_argmin \
  --input_path ./testcase/data_for_ts_argmin.parquet \
  --ref_ans_path ./testcase/rolling_argmin_v1.npy \
  --window 20
```

能跑通之后，就可以把答案 push 到自己的仓库里：

```bash
# 先设定 config
git config --global user.name "你的用户名"
git config --global user.email "你的 GitHub 邮箱"

git add src/solution.py
git commit -m "submit solution"
git pull --rebase origin main
git push -u origin main
```

随后可以在 **Actions** 中查看具体的运行情况。**Grader** 通过即可，**GitHub Classroom Workflow** 失败可以不用管。

## 3. 查看结果

### LeaderBoard

LeaderBoard 每 5 min 会自动刷新，在 template 仓库里可以看到每个用户的最新成绩。

### Classmoji 更新

评分通过后，在 GitHub issue 页面点击 **Close issue**，回到 Classmoji，确认作业状态变为 **Submitted**。

如果之后还要继续修改，重新打开 GitHub issue，修改代码并重新 push。确认 GitHub Actions 通过后，再次关闭 issue。
