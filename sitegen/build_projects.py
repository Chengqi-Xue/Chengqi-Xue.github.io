# -*- coding: utf-8 -*-
from common import *
from projects_meta import PROJECTS
from diagrams import DIAGRAMS

R = "../"
IMG = R + "assets/img/"
VID = R + "assets/video/"
CV = R + "assets/cv/"


def diagram_fig(key, cap_en, cap_zh):
    return f'<figure class="fig fig-wide plain">{DIAGRAMS[key]()}<figcaption>{t(cap_en, cap_zh)}</figcaption></figure>'


def contributions(items):
    return '<div class="contrib">' + ''.join(f'<div><b>{t(te, tz)}</b>{t(be, bz)}</div>' for te, tz, be, bz in items) + '</div>'


def prev_next(slug):
    i = [p_['slug'] for p_ in PROJECTS].index(slug)
    prv = PROJECTS[i - 1] if i > 0 else PROJECTS[-1]
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    return (f'<div class="next"><a href="{prv["slug"]}.html"><div class="k">{t("Previous project", "上一个项目")}</div><div class="n">{t(*prv["title"])}</div></a>'
            f'<a href="{nxt["slug"]}.html"><div class="k">{t("Next project", "下一个项目")}</div><div class="n">{t(*nxt["title"])}</div></a></div>')


def page(slug, title_en, title_zh, desc_en, hero_html, hero_media, sections_html):
    out = head(f"{title_en} — Chengqi Xue", f"{title_zh} — 薛程琪", desc_en, root=R, page_class="dark-top")
    out += header(root=R, active="research")
    out += hero_html
    if hero_media:
        out += f'<div class="phero-media"><div class="wrap">{hero_media}</div></div>'
    out += sections_html
    out += section("more", "More research", "更多研究", prev_next(slug), cls="alt")
    out += footer(root=R)
    open(f'../projects/{slug}.html', 'w', encoding='utf-8').write(out)
    print("ok", slug)


# =====================================================================
# 1. VTLA
# =====================================================================
def vtla():
    pr = PROJECTS[0]
    hero = project_hero(pr['kind'], *pr['title'], *pr['q'], [
        ("Role", "角色", "Sole author of the dissertation; built the full stack from force dataset to robot demo", "毕业论文独立作者；从力数据集到真机演示的全栈搭建"),
        ("Period", "时间", "September 2025 – August 2026", "2025 年 9 月 – 2026 年 8 月"),
        ("Supervisor", "导师", "Prof. Shan Luo, King’s College London", "罗山教授，伦敦国王学院"),
        ("Hardware", "硬件", "Franka Emika arm, GelSight Mini, ATI Nano17, custom 3D-printed end-effector, wrist camera", "Franka Emika 机械臂、GelSight Mini、ATI Nano17、自制 3D 打印末端执行器、手腕相机"),
        ("Models", "模型", "Qwen2.5-VL-7B-Instruct + QLoRA, ResNet-18 load estimator, π0.5 VLA backbone", "Qwen2.5-VL-7B-Instruct + QLoRA、ResNet-18 力估计器、π0.5 VLA 骨干"),
    ])
    hero_media = video(VID + "vtla-demo.mp4", VID + "vtla-demo.jpg",
                       "The full demonstration: the arm presses four similar-looking garments in turn, the model ranks them by touch, and the chosen garment is grasped and placed in the basket. (3 min 28 s)",
                       "完整演示：机械臂依次按压四件外观相近的衣物，模型凭触觉排序，再夹起选中的衣物放入篮筐。（3 分 28 秒）", wide=True)

    s = ''
    # Why
    s += section("why", "Why touch, and why this task", "为什么是触觉，为什么是这个任务", prose(
        ("Fabric is one of the most common materials a robot will ever handle and one of the hardest to perceive. Garment sorting for recycling, laundry automation and assistive dressing all require judgements—which of these two is softer, thicker, more elastic, rougher?—that colour images often cannot support: two fabrics that photograph almost identically can differ strongly in weave, pile and compliance. Touch is exactly the modality that exposes those properties.",
         "织物是机器人最常接触、也最难感知的材料之一。衣物回收分拣、洗衣自动化、辅助穿衣都需要回答“这两件哪件更软、更厚、更有弹性、更粗糙”——而这些判断单靠彩色图像往往无法完成：两块拍起来几乎一样的布，在织法、绒面和顺应性上可能差别很大。触觉正是能暴露这些属性的模态。"),
        ("The idea of pairing a GelSight sensor with a multimodal large language model comes from MLLM-Fabric, which showed that a vision–language model can compare two fabrics along softness, thickness, elasticity and texture. I took that idea as the starting point and built a complete system around it on a Franka arm: my own tactile force dataset, my own training and evaluation pipeline for the language model, a custom end-effector, and a deployment chain that runs with no force sensor in the loop.",
         "把 GelSight 传感器与多模态大语言模型结合的思路参考了 MLLM-Fabric 这篇论文：它证明了视觉-语言模型可以在柔软度、厚度、弹性和纹理四个维度上比较两块织物。我以此为起点，在 Franka 机械臂上围绕它搭建了一整套系统：自采的触觉力数据集、自建的语言模型训练与评测流水线、自制末端执行器，以及一条回路中不需要力传感器的部署链路。"),
        ("Three goals drove the work: teach a 7B vision–language model to judge fabric properties from tactile images; measure that ability honestly, on fabrics the model has never touched; and get the whole loop—press, estimate force, reason, rank, grasp, place—running on the real robot.",
         "三个目标贯穿整个工作：让一个 7B 的视觉-语言模型学会从触觉图像判断织物属性；在模型从未摸过的织物上诚实地衡量这种能力；并让“按压-估力-推理-排序-抓取-放置”的完整闭环在真机上跑起来。")))

    # System
    body = diagram_fig("vtla", "System architecture. Two strictly separated data pipelines—the self-collected force data (A) and the fabric-comparison data (B)—meet for the first time inside the robot, where the force estimator supplies the force values the language model expects.",
                       "系统架构。两条严格隔离的数据流水线——自采的力数据（A）与织物比较数据（B）——第一次汇合是在机器人上：力估计器提供语言模型所需要的力数值。")
    body += two_col(
        figure(IMG + "vtla-setup-overview.jpg", "The platform: four deliberately similar-looking garments on hangers, the Franka arm with the custom end-effector, and the collection basket. Visual similarity is a design choice—the comparison has to be carried by touch, not colour.",
               "实验平台：四件刻意挑选的外观相近的衣物挂在衣架上，Franka 机械臂装着自制末端执行器，前方是收集篮。外观相似是有意为之——比较必须靠触觉完成，而不是靠颜色。"),
        figure(IMG + "vtla-setup-press.jpg", "A press in progress: the GelSight face pinches a single fabric layer against the backing paddle, so every press happens against a defined, repeatable substrate.",
               "按压进行中：GelSight 感知面与背板夹住单层织物，使每次按压都在确定、可重复的衬底上进行。"))
    body += h(3, "The end-effector I designed", "我设计的末端执行器")
    body += two_col(
        prose(("The stock parallel-jaw fingers cannot press or grasp a hanging garment. I designed and 3D-printed two asymmetric fingers that extend the Franka Hand and integrate all three jobs of the demonstration—locating, pressing and grasping—in one tool, so no tool change happens anywhere in the sequence.",
               "原装平行夹爪既按不了也抓不了悬挂的衣物。我设计并 3D 打印了两根不对称手指，延长 Franka Hand，把演示中定位、按压、抓取三件事集成在同一个工具上，整个流程无需换工具。"),
              ("Three decisions carry the load. Slender, tapered fingers can pass through a hanging garment and isolate a single layer without dragging its neighbours. Ribbed compliant tips are the sacrificial first contact if a finger strikes the hanger or rail—protecting the GelSight’s elastomer and optics, which are the most fragile and expensive parts. And a broad backing paddle opposite the sensor turns a freely yielding garment into a defined press, matching the flat-substrate presses of the training data.",
               "三个设计决定起了关键作用：细长渐缩的手指可以穿过悬挂的衣物、只隔离出单层而不带动相邻衣物；带肋的柔性指尖是手指撞到衣架或横杆时的牺牲件，保护 GelSight 最脆弱也最昂贵的弹性体与光学部件；传感器对面的宽背板把会随意变形的衣物变成一次确定的按压，与训练数据中平面衬底的按压条件一致。")),
        figure(IMG + "vtla-gripper.jpg", "The custom end-effector: the right finger carries the GelSight Mini mid-finger with its sensing face inward, recessed behind a compliant tip; the left finger is a backing paddle. The wrist camera sits on the same mount.",
               "自制末端执行器：右指中段内嵌 GelSight Mini，感知面朝内并缩在柔性指尖后方；左指是背板。手腕相机安装在同一支架上。"))
    s += section("system", "The system on the robot", "机器人上的系统", body, cls="alt")

    # Force estimator
    body = prose(("The language model reads each tactile frame together with the contact force at which it was taken, so the robot needs a force value for every press. A robot pressing hanging garments has no force sensor in the loop—so I made the tactile image itself report the force. I collected a dedicated dataset: 200 fabrics pressed by a GelSight Mini on the Franka arm with an ATI Nano17 beneath the fabric as ground truth—401 sessions, 12,178 presses, 99,797 usable frames after quality filtering.",
                  "语言模型读取每帧触觉图像时需要同时知道拍摄时的接触力，因此每次按压都要有一个力数值；而机器人按压悬挂衣物时回路里并没有力传感器——于是我让触觉图像自己“报出”力。为此我采集了专门的数据集：在 Franka 上用 GelSight Mini 按压 200 种织物，织物下方放置 ATI Nano17 作为真值——共 401 个采集会话、12,178 次按压，质量过滤后 99,797 帧可用。"),
                 ("Three calibrations underpin its use. Cross-correlating force with image change over 120 presses measured a 40 ms camera–force delay; applying the correction moved the peak frame in 38% of presses. Three independent checks established that force labels are trustworthy up to 22 N. And the photometric reconstruction passed its criteria only marginally, so single-frame magnitudes are never used as absolute labels.",
                  "三项标定支撑了它的使用：在 120 次按压上做力与图像变化的互相关，测得相机–力的时延为 40 ms，校正后 38% 的按压峰值帧发生了变化；三项独立检查确定力标签在 22 N 以内可信；光度重建仅勉强通过判据，因此单帧重建幅值从不作为绝对标签使用。"))
    body += stats([("12,178", "calibrated presses over 200 fabrics", "次标定按压，覆盖 200 种织物"),
                   ("0.33 N", "MAE on 30 fabrics never seen in training", "30 种训练中未见织物上的 MAE"),
                   ("96.3%", "of 14,728 held-out frames within 1 N", "的 14,728 帧留出帧误差 < 1 N"),
                   ("−22%", "error from choosing checkpoints by force MAE instead of the auxiliary head", "按力 MAE 而非辅助头选择检查点带来的误差下降")])
    body += two_col(
        figure(IMG + "vtla-fig_load_scatter.png", "Deployment-path force estimation on all 14,728 held-out frames: estimate against the Nano17 reference (MAE 0.325 N, RMSE 0.442 N, bias −0.049 N).",
               "部署推理路径上对全部 14,728 帧留出帧的力估计：估计值 vs Nano17 真值（MAE 0.325 N，RMSE 0.442 N，偏差 −0.049 N）。"),
        figure(IMG + "vtla-force-prediction.jpg", "Per-frame estimates on example press sequences from the deployment session—the pre-contact frame is asserted as 0 N because the regressor cannot represent a regime it never saw.",
               "部署会话中若干按压序列的逐帧估计——接触前的帧被直接写为 0 N，因为回归器无法输出它从未见过的区间。"))
    body += two_col(
        figure(IMG + "vtla-fig_force_hist.png", "Force support of the self-collected data after the 22 N cut. Evidence density collapses above 20 N, which is why the deployment ladder tops out at 19.9 N.",
               "22 N 截断后自采数据的力分布。20 N 以上证据密度骤降，因此部署时的力阶梯最高取 19.9 N。"),
        figure(IMG + "vtla-fig_v2_projection.png", "Commissioning the estimator against the Nano17 itself at five plateaus (5–15 N): slope ≈ 0.99, intercept ≈ +0.08 N, every plateau within its pre-registered acceptance region.",
               "用 Nano17 对估计器做验收：5–15 N 五个平台，斜率 ≈ 0.99、截距 ≈ +0.08 N，所有平台都落在预先登记的接受区间内。"))
    body += callout("87% of the estimator’s improvement (0.433 → 0.326 N) came from selecting checkpoints by force error—the quantity that is actually deployed—rather than from a bigger model or more data. The input representation (raw RGB, background difference or photometric reconstruction) made no statistical difference across three seeds.",
                    "估计器 87% 的提升（0.433 → 0.326 N）来自“按力误差——也就是真正要部署的量——来选检查点”，而不是更大的模型或更多数据。输入表示（原始 RGB、背景差分或光度重建）在三个随机种子下没有统计学差异。")
    s += section("force", "Replacing the force sensor with a tactile image", "用一张触觉图像取代力传感器", body)

    # VLM reproduction
    body = prose(("Training data come from the public MLLM-Fabric image set—200 fabrics, each photographed and pressed by a GelSight at four increasing forces, with ordinal labels (low / medium / high) for softness, thickness, elasticity and texture. I wrote the whole pipeline on top of it: a single prompt generator that turns a fabric pair into a question, an image compositor, the training loop, and the evaluation harness. Every comparison in the project—3,937 training pairs, 400 test pairs, and 34,883 pairs I constructed myself—goes through that one generator.",
                  "训练数据来自公开的 MLLM-Fabric 图像集——200 种织物，每种都有 RGB 照片和 GelSight 在四个递增力值下的按压图像，并在柔软度、厚度、弹性、纹理四个属性上标注了低/中/高三个等级。我在此之上写了完整的流水线：把一对织物变成一个问题的提示生成器、拼图模块、训练循环和评测框架。项目里所有比较——3,937 组训练对、400 组测试对，以及我自己构造的 34,883 组——都经由这同一个生成器。"),
                 ("Qwen2.5-VL-7B-Instruct was fine-tuned with QLoRA (4-bit base, rank-32 adapters, 80.7 M trainable parameters) on a single H100. Each input is a composite image—two rows, one per fabric: an RGB view followed by four GelSight frames at increasing force—plus the force values in text. I measured that beyond the processor’s pixel budget a larger stored image adds no model-visible resolution, which let me cut the upload from 11.76 GB to 1.77 GB with pixel-level equivalence.",
                  "Qwen2.5-VL-7B-Instruct 在单张 H100 上用 QLoRA 微调（4-bit 基座、秩 32 适配器、80.7 M 可训练参数）。每个输入是一张拼接图：两行各代表一块织物，先是 RGB 视图，然后是四帧力逐渐增大的 GelSight 图像，再加上文本中的力数值。我验证了超过处理器像素预算后更大的图片不会增加模型可见的分辨率，于是把上传量从 11.76 GB 压到 1.77 GB 而保持像素级等价。"))
    body += figure(IMG + "vtla-composite-input.jpg", "An actual composite input from the robot demonstration (fabrics F1 and F2). Each row is one fabric: an RGB view, then GelSight frames selected at the force ladder 0 / 13.5 / 16.8 / 19.9 N.",
                   "真机演示中的一张真实输入（织物 F1 与 F2）。每行一块织物：RGB 视图，然后是按 0 / 13.5 / 16.8 / 19.9 N 力阶梯选出的 GelSight 帧。", wide=True)
    body += h(3, "Two readouts, and a precision trap", "两种读出方式，以及一个精度陷阱")
    body += prose(("A generative model has to be turned into a discrete answer somehow. I built two instruments. A free-text parser, calibrated against all 3,937 training rationales with a measured noise floor of 1.94 percentage points—the first, uncalibrated version carried a 6.36-point bias, which is why I calibrate the parser before trusting any number it produces. And a forced-choice readout that compares candidate log-likelihoods, which needs no parser but is numerically fragile: in bfloat16 the representable values near a log-likelihood of 16–32 are 0.125 apart, while genuine differences are often 0.01–0.2. An early bf16 run collapsed most items into exact ties and produced a plausible-looking but fake accuracy of 0.75. All scoring is now in fp32; none of the 7,600 scored items tied.",
                   "生成式模型的输出总得变成一个离散答案。我做了两套工具：一个用全部 3,937 条训练解释标定过的自由文本解析器，测得噪声底 1.94 个百分点——未标定的第一版有 6.36 个百分点的系统偏差，所以解析器必须先标定再使用；另一个是比较候选答案对数似然的强制二选一读出，它不需要解析器，但在数值上很脆弱：bfloat16 在对数似然 16–32 附近的可表示间隔是 0.125，而真实差异常常只有 0.01–0.2。早期一次 bf16 运行把大部分样本压成了精确平局，得到一个看似合理实则虚假的 0.75 准确率。现在所有打分都用 fp32，7,600 个样本中没有一个平局。"),)
    body += two_col(
        figure(IMG + "vtla-fig_margin.png", "Forced-choice margins for four representative cells: zero-shot margins sit near zero, fine-tuned margins an order of magnitude higher. Zero exact ties in 7,600 items.",
               "四个代表性单元的强制选择置信差：零样本模型接近零，微调后高出一个数量级。7,600 个样本零平局。"),
        figure(IMG + "vtla-fig_runtime.png", "Measured cloud-runtime model from a two-point method: 50.6 s fixed cost plus 23.6 s per sample on an H100—the number that sized the robot run.",
               "两点法测得的云端运行时模型：H100 上固定开销 50.6 s，每样本 23.6 s——真机运行的时间预算就来自这里。"))
    s += section("vlm", "Teaching a vision–language model to compare fabrics by touch", "让视觉-语言模型学会用触觉比较织物", body, cls="alt")

    # Protocol
    body = prose(("A high score on fabrics the model has already touched proves little: if the training pairs reveal every fabric’s level, a look-up table answers the test without reading a single pixel. So I designed the evaluation around that risk. For every (training set, test set) pair I compute how far pure look-up could get—the ceiling—and report each accuracy next to it. And I built a second test on fabrics the model never saw: a 160/40 fabric-disjoint split in which no training pair involves a test fabric, verified by a learned domain probe that cannot tell the two sides apart.",
                  "在模型已经摸过的织物上拿高分并不能说明什么：如果训练对已经暴露了每块织物的等级，一张查找表一个像素都不用看就能答题。所以我把评测设计围绕这个风险展开：对每一组（训练集, 测试集）都计算纯查表能达到的上限，并把每个准确率与上限并列报告；同时构造了一个模型从未见过的织物测试——160/40 的织物不相交划分，没有任何训练对涉及测试织物，并用学习型域探针验证两侧无法区分。"),
                 ("Results: on the seen-fabric test the fine-tuned model scores 0.985, up from 0.49 for the untuned base model. On the unseen-fabric test the same configuration scores 0.865 against a 0.50 ceiling—tactile comparison that transfers to new material. A size-matched control that saw the test fabrics at the same training volume returns to 0.985, so having touched a fabric before is worth +0.12, concentrated almost entirely in Elasticity (+0.37); Thickness and Texture generalise almost perfectly.",
                  "结果：在已见织物测试上，微调模型从未微调基座的 0.49 提升到 0.985；在未见织物测试上，同样的配置在 0.50 的上限下得到 0.865——这是能迁移到新材料上的触觉比较能力。一个在相同训练量下见过测试织物的规模匹配对照回到 0.985，说明“摸过这块布”值 +0.12，而且几乎全部集中在弹性这一属性上（+0.37）；厚度与纹理几乎完美泛化。"))
    body += two_col(
        figure(IMG + "vtla-fig_t1_gap.png", "Forced-choice accuracy with per-cell look-up ceilings (red). Left: the seen-fabric test, where every fine-tuned run sits just below a ceiling of 1.00. Right: the unseen-fabric test, where the model reaches 0.865 against a 0.50 ceiling.",
               "带逐单元查表上限（红色）的强制选择准确率。左：已见织物测试集，所有微调模型都紧贴 1.00 的上限；右：未见织物测试集，模型在 0.50 的上限下达到 0.865。"),
        figure(IMG + "vtla-fig_unseen.png", "The seen-fabric contribution by property (n = 100 each): Elasticity +0.37, Softness +0.10, Texture +0.01, Thickness 0.00.",
               "按属性拆分“见过织物”的贡献（每项 n = 100）：弹性 +0.37，柔软度 +0.10，纹理 +0.01，厚度 0.00。"))
    body += h(3, "A harder task at zero annotation cost", "零标注成本的更难任务")
    body += prose(("The standard pairs only compare fabrics two grades apart. Real sorting is harder—the difference is often one grade—and the ordinal labels already determine every such comparison: enumerating ordered pairs one grade apart gave me 63,300 adjacent-level pairs with no new labelling. A model trained on two-grade pairs alone reaches 0.839 on this finer task (ceiling 0.50); adding 4,000 of the enumerated pairs to training raises it to 0.975. Ablations then bound what the model actually relies on: swapping the left/right indices changes only 4 of 400 predictions, and rewriting the force text to the robot’s own force ladder changes none, so the deployment force range does not disturb the model.",
                   "标准的比较对只涉及相差两级的织物。真实分拣更难——差别往往只有一级——而等级标注本身已经决定了所有这类比较：枚举相差一级的有序对，我得到了 63,300 组相邻等级对，不需要任何新标注。只用两级对训练的模型在这个更细的任务上达到 0.839（上限 0.50）；把 4,000 组枚举对加入训练后提升到 0.975。消融实验进一步界定了模型真正依赖什么：交换左右索引只改变 400 个预测中的 4 个；把力文本改写成机器人自己的力阶梯一个都不变——说明部署时的力范围不会干扰模型。"),)
    body += two_col(
        figure(IMG + "vtla-fig_adjacent.png", "Adjacent-level results with per-cell ceilings. Adding enumerated pairs improves the task substantially but also moves the cell ceiling; the two numbers are always read together.",
               "相邻等级任务的结果与逐单元上限。加入枚举对显著提升了任务表现，同时也抬高了上限；两个数字必须一起看。"),
        figure(IMG + "vtla-fig_probe.png", "Force-text probes: margins barely move across identity, deployment-ladder and ladder-plus-zero variants, and the largest perturbation sits below the smallest identity margin.",
               "力文本扰动探针：在原样、部署阶梯、阶梯加零三个变体之间置信差几乎不动，最大扰动量低于最小原始置信差。"))
    s += section("protocol", "Testing on fabrics the model has never touched", "在模型从未摸过的织物上检验", body)

    # Robot demo
    body = prose(("The deployment chain runs locally except for VLM scoring, which runs on a cloud H100 with the same evaluator and adapter as the benchmark, verified by hash. A press trajectory is taught once under zero stiffness by guiding the arm by hand, validated against four recorded-trajectory checks, then replayed with a hard stop that halts the arm within one 20 ms control cycle. Every captured GelSight frame receives a force estimate; a slot selector picks one pre-contact frame and three loading frames nearest the ladder targets, subject to six gates.",
                  "部署链除了 VLM 打分之外全部在本地运行，打分在云端 H100 上进行，使用与基准测试完全相同、经哈希校验的评测器与适配器。按压轨迹在零刚度下手把手示教一次，通过四项轨迹记录检查后回放，并配有能在一个 20 ms 控制周期内停住机械臂的硬停保护。每一帧 GelSight 图像都得到一个力估计；槽位选择器按六道门选出一帧接触前帧和三帧最接近阶梯目标的加载帧。"),
                 ("Four garments give six unordered pairs per property, each evaluated in both presentation orders; a pair counts only if both orders choose the same physical garment. The run completed 48 prompts in 1,005 s, exactly as the two-point timing model predicted. 18 of 24 comparisons were order-consistent; the six contradictions were left unresolved rather than papered over. For the query “suitable for summer clothing” the recommendation layer selected garment F4—lowest thickness, weighted against softness and texture—and attached a warning that elasticity evidence is weak—the property that scored lowest on the unseen-fabric test.",
                  "四件衣物在每种属性上构成六个无序对，每对按两种呈现顺序各评一次；只有两种顺序都选中同一件实物时才算数。整轮运行 48 条提示用了 1,005 s，与两点法时间模型的预测完全吻合。24 次比较中 18 次顺序一致，6 次矛盾被如实保留而不是掩盖。对于“适合夏天穿”的查询，推荐层选中了 F4——厚度最低，并以柔软度和纹理加权——同时附上“弹性证据较弱”的提示——弹性正是未见织物测试中得分最低的属性。"))
    body += figure(IMG + "vtla-sequence.jpg", "The executed sequence. (a) Home. (b)–(e) The arm presses each garment in turn, pinching fabric between the GelSight face and the backing paddle. (f) After ranking, the tapered fingers pass through the chosen garment and close on a single layer. (g) It is carried to the basket. (h) The arm moves to the next garment.",
                   "执行序列。(a) 初始位姿；(b)–(e) 机械臂依次按压每件衣物，把织物夹在 GelSight 与背板之间；(f) 排序后，渐缩手指穿过选中的衣物并夹住单层；(g) 运送到篮筐；(h) 转向下一件衣物。", wide=True)
    body += h(3, "Action policy: π0.5 and teleoperated demonstrations", "动作策略：π0.5 与遥操作示教")
    body += two_col(
        prose(("For the manipulation stage I used π0.5 as the vision-language-action backbone. I collected teleoperated demonstrations of the press-grasp-place cycle with a Quest controller mapped to the Franka end-effector, so that a language-conditioned policy could learn the approach, press and single-layer grasp from human motion rather than hand-coded waypoints. The force-estimation and tactile-reasoning modules plug in unchanged, because the policy only needs the “which garment” decision as a goal.",
               "操作阶段我以 π0.5 作为视觉-语言-动作骨干。我用映射到 Franka 末端的 Quest 手柄采集了“按压-抓取-放置”循环的遥操作示教，让语言条件化的策略从人的动作中学习接近、按压与单层抓取，而不是依赖手写路径点。力估计与触觉推理模块无需改动即可接入，因为策略只需要“选哪件衣物”这一目标。"),
              ("With the project clock running, the recorded demonstration ran the press trajectory in taught-and-replayed mode with hard stops, which gave the safest and most traceable evidence for the dissertation; the π0.5 branch continued in parallel and became the main policy work of the Tactile UMI project, where I fine-tuned π0.5 on calibrated hand-held demonstrations and ran it on a Franka FR3.",
               "考虑到项目周期，论文中记录的演示以示教-回放加硬停的方式执行按压轨迹，这是最安全、最可追溯的证据；π0.5 分支则并行推进，并成为 Tactile UMI 项目中我的主要策略工作——在标定过的手持示教上微调 π0.5，并在 Franka FR3 上实机运行。")),
        video(VID + "vtla-teleop.mp4", VID + "vtla-teleop.jpg", "Collecting teleoperated demonstrations for the π0.5 action policy with a Quest controller mapped to the Franka end-effector.",
              "用映射到 Franka 末端的 Quest 手柄为 π0.5 动作策略采集遥操作示教。"))
    body += stats([("48", "prompts scored in one robot run, 1,005 s", "条提示在一轮真机运行中打分，用时 1,005 s"),
                   ("18 / 24", "pairwise comparisons consistent in both orders", "次成对比较在正反两序下一致"),
                   ("0", "force sensors in the deployment loop", "个力传感器在部署回路中"),
                   ("1", "end-effector for pressing, grasping and placing", "个末端执行器完成按压、抓取与放置")])
    s += section("demo", "The robot demonstration", "真机演示", body, cls="alt")

    # Contributions & links
    body = contributions([
        ("Hardware", "硬件", "Designed and printed the end-effector; built the force-collection rig with the ATI Nano17; ran 401 collection sessions.", "设计并打印末端执行器；搭建带 ATI Nano17 的力采集装置；完成 401 个采集会话。"),
        ("Data and calibration", "数据与标定", "Sync-delay measurement, trust range, photometric checks, fabric-disjoint split with a domain probe.", "同步时延测量、可信范围、光度检查，以及带域探针的织物不相交划分。"),
        ("Models", "模型", "ResNet-18 load estimator; QLoRA fine-tuning of Qwen2.5-VL-7B across eight training configurations; π0.5 teleop pipeline.", "ResNet-18 力估计器；Qwen2.5-VL-7B 的八种训练配置 QLoRA 微调；π0.5 遥操作流水线。"),
        ("Evaluation", "评测", "Prompt and image pipeline, calibrated parser, fp32 forced choice, unseen-fabric split with per-cell ceilings, perturbation probes.", "提示与拼图流水线、标定解析器、fp32 强制选择、带逐单元上限的未见织物划分、扰动探针。"),
        ("Deployment", "部署", "Teach-and-replay with hard stops, gated slot selection, hash-linked provenance from press to recommendation.", "带硬停的示教回放、门控槽位选择、从按压到推荐的哈希链路溯源。"),
    ])
    body += links([(CV + "VTLA_Report_Chengqi_Xue.pdf", "Read the dissertation (PDF)", "阅读毕业论文（PDF）")])
    body += callout("Scope: all VLM runs use a single seed, and the four-garment demonstration is an integration test of the full loop rather than an accuracy measurement, since the garments have no independent property labels.",
                    "说明：所有 VLM 实验使用单一随机种子；四件衣物的演示是对完整闭环的集成测试，而非准确率测量，因为这些衣物没有独立的属性标签。")
    s += section("contrib", "My contribution", "我做的部分", body)

    page("vtla", pr['title'][0], pr['title'][1],
         "Vision–tactile–language–action learning on a Franka arm: GelSight touch, a tactile force estimator, a QLoRA-tuned Qwen2.5-VL that compares fabrics by touch, and a real-robot fabric-sorting demonstration.",
         hero, hero_media, s)


# =====================================================================
# 2. Tactile UMI
# =====================================================================
def umi():
    pr = PROJECTS[1]
    hero = project_hero(pr['kind'], *pr['title'], *pr['q'], [
        ("Role", "角色", "Co-built the hand-held system, calibration and audit tooling; owned the π0.5 policy branch", "共同搭建手持系统、标定与审计工具；负责 π0.5 策略分支"),
        ("With", "合作", "Suhang Xia (Diffusion Policy branch); UniForce guidance from Zhuo Chen; Prof. Shan Luo’s lab, KCL", "夏苏杭（Diffusion Policy 分支）；UniForce 由陈卓指导；KCL 罗山教授实验室"),
        ("Period", "时间", "2026", "2026 年"),
        ("Hardware", "硬件", "UMI-style hand-held gripper, wrist fisheye camera, custom GelSight + GelSight Mini, Meta Quest, Franka FR3 with Robotiq gripper", "UMI 式手持夹爪、手腕鱼眼相机、自制 GelSight + GelSight Mini、Meta Quest、带 Robotiq 夹爪的 Franka FR3"),
        ("Software", "软件", "openpi / π0.5, LeRobot format, Zarr + H5 pipelines, ArUco calibration, Rerun audit viewer", "openpi / π0.5、LeRobot 格式、Zarr + H5 流水线、ArUco 标定、Rerun 审计查看器"),
    ])
    hero_media = two_col(
        video(VID + "umi-pi05-demo.mp4", VID + "umi-pi05-demo.jpg",
              "π0.5 fine-tuned on the Tactile UMI demonstrations, running autonomously on the Franka FR3 at 5× speed. The on-screen counter tallies successful rollouts as they happen.",
              "在 Tactile UMI 示教上微调的 π0.5，在 Franka FR3 上自主运行（5 倍速）。屏幕上的计数器实时统计成功回放次数。", cls="square"),
        '<div class="hero-side">' + h(3, "What the video shows", "视频里发生了什么") + prose(
            ("The FR3 carries the same Robotiq gripper and GelSight fingertips as the hand-held UMI, so the policy sees the world the way the demonstrations did. Each rollout starts from a reset pose; the policy receives the wrist image and robot state, predicts a chunk of camera-relative actions, and the arm moves the object toward the target.",
             "FR3 装着与手持 UMI 相同的 Robotiq 夹爪和 GelSight 指尖，所以策略看到的世界与示教时一致。每次回放从复位位姿开始；策略接收手腕图像与机器人状态，预测一段相机坐标系下的动作块，机械臂把物体移向目标。"),
            ("No teleoperation, no scripted waypoints: every motion comes from π0.5 fine-tuned on 222 hand-held demonstrations.",
             "没有遥操作，也没有预设路径点：所有动作都来自在 222 条手持示教上微调的 π0.5。")) + '</div>', cls="c12")
    s = ''
    s += section("why", "The idea", "项目思路", prose(
        ("Universal Manipulation Interface (UMI) showed that a hand-held gripper with a wrist camera lets people collect robot demonstrations anywhere, far faster than teleoperation. But a wrist camera cannot tell how hard the fingers are squeezing, whether an object has started to slip, or what a cloth feels like. We added touch: two GelSight fingertips record a tactile video stream next to the RGB stream, Quest tracking supplies the 6-DoF pose, and an ArUco marker gives the gripper width.",
         "Universal Manipulation Interface（UMI）证明了带手腕相机的手持夹爪可以让人在任何地方采集机器人示教，比遥操作快得多。但手腕相机看不出手指捏得多紧、物体是否开始打滑、一块布摸起来是什么感觉。于是我们加上了触觉：两个 GelSight 指尖在 RGB 流旁边同步记录触觉视频，Quest 追踪提供六自由度位姿，ArUco 标记给出夹爪开度。"),
        ("The hard part is not the sensors but trusting them together. Four streams with four clocks and four coordinate frames have to become one robot-ready timeline, and every transformation has to be measured before it is used. We treated calibration and data quality as part of the learning system, not as hidden setup—every episode is inspectable from acquisition through alignment, curation and deployment.",
         "难点不在传感器本身，而在于让它们一起可信。四路数据流、四个时钟、四个坐标系必须合成一条机器人可用的时间线，每一个变换在使用前都要先测出来。我们把标定和数据质量当作学习系统的一部分，而不是看不见的前置工作——每条示教从采集、对齐、筛选到部署都可以被检视。"),
        ("Then the corpus split into two policy branches. My lab mate trained a tactile-conditioned Diffusion Policy; I converted the same demonstrations to LeRobot format and fine-tuned π0.5, a vision-language-action model, and deployed it on the FR3. This page covers the π0.5 branch.",
         "随后数据被用于两条策略分支：实验室同学训练了触觉条件化的 Diffusion Policy；我把同一批示教转换成 LeRobot 格式，微调视觉-语言-动作模型 π0.5，并部署到 FR3 上。这一页介绍 π0.5 这一分支。")))

    body = figure(IMG + "umi-workflow.jpg", "End-to-end workflow: system setup and calibration → collection and curation → representation and policy learning. Each stage produces a traceable artifact; geometry, timing and data quality are closed before training.",
                  "端到端工作流：系统搭建与标定 → 采集与筛选 → 表示与策略学习。每个阶段都产出可追溯的产物；几何、时序与数据质量在训练前全部闭环。", wide=True, cls="plain")
    body += diagram_fig("umi", "Where the branches split. Both policies learn from the same calibrated corpus; my branch converts it to LeRobot format and fine-tunes π0.5, the lab mate’s branch feeds frozen UniForce contact tokens into a Diffusion Policy.",
                        "分支在哪里分开。两种策略都从同一套标定过的数据学习；我的分支把数据转换为 LeRobot 格式并微调 π0.5，同学的分支把冻结的 UniForce 接触 token 送入 Diffusion Policy。")
    body += gallery([
        (IMG + "umi-lab-setup.jpg", "The bench: Franka FR3 with the Robotiq gripper and GelSight fingertips, the hand-held UMI gripper, Quest controllers, and the ArUco board used for calibration.", "实验台：带 Robotiq 夹爪与 GelSight 指尖的 Franka FR3、手持 UMI 夹爪、Quest 手柄，以及用于标定的 ArUco 标定板。"),
        (IMG + "umi-calibration-board.jpg", "Hand–eye calibration in progress: the wrist camera sees the checkerboard while the robot’s flange pose is logged, giving the camera-to-flange transform.", "手眼标定进行中：手腕相机观察棋盘格的同时记录法兰位姿，求解相机到法兰的变换。"),
        (IMG + "umi-collection-gui.jpg", "The collection interface: live RGB, both tactile views, Quest pose, gripper width and stream health in one window, so an operator sees a broken stream before an episode is recorded.", "采集界面：实时 RGB、两路触觉视图、Quest 位姿、夹爪开度与各流状态集中在一个窗口，操作者在录制前就能发现异常。"),
    ])
    s += section("system", "One system, four sensor streams, one timeline", "一个系统、四路传感、一条时间线", body, cls="alt")

    body = prose(("Every transformation is measured before it is trusted, and the measurements are kept as a ledger so they can be repeated whenever a camera or mounting changes.",
                  "每一个变换在被信任之前都要先测量，并把测量结果记录成账本，这样一旦相机或安装发生变化就可以重做。"),)
    body += stats([("40", "Quest–camera pose pairs in the hand–eye solution, none rejected", "组 Quest–相机位姿对用于手眼求解，无一剔除"),
                   ("1.67 / 3.09 / 1.91 mm", "fixed-board translation spread, axis-wise", "固定标定板平移离散度（逐轴）"),
                   ("−56.7 ms / +25 ms", "measured stream offsets: Quest to RGB, right tactile to RGB", "测得的流间偏移：Quest→RGB，右触觉→RGB"),
                   ("8.7–63.0 mm", "calibrated gripper range from a five-point lookup table", "五点查表标定的夹爪开度范围")])
    body += h(3, "Aligning two clocks with one motion", "用一次运动对齐两个时钟")
    body += two_col(
        prose(("With the camera and the Quest rigidly mounted on the UMI, the device moves in front of a stationary ArUco marker. The camera estimates the marker’s position from video and calibrated intrinsics; the Quest records the controller trajectory, transformed into the camera frame by the measured hand–eye transform. Following the one-axis alignment of exUMI, we compare normalised velocity along a matching axis and search for the scalar time offset that minimises the mean-squared error between the two signals.",
               "相机与 Quest 刚性固定在 UMI 上，设备在一个静止的 ArUco 标记前运动。相机根据视频和标定内参估计标记位置；Quest 记录手柄轨迹，并通过测得的手眼变换转换到相机坐标系。参照 exUMI 的单轴对齐方法，我们比较同一轴上的归一化速度，搜索使两路信号均方误差最小的标量时间偏移。"),
              ("The accepted run estimated −56.738 ms: the main camera trails the Quest by about 56.7 ms, so Quest timestamps are shifted later to align the streams. This is a measured value for this set-up, not a universal hardware latency—and that distinction is exactly why the ledger exists.",
               "被接受的那次运行估计出 −56.738 ms：主相机比 Quest 晚约 56.7 ms，因此把 Quest 时间戳后移以对齐数据流。这是针对本套装置的实测值，而非通用的硬件时延——这个区别正是账本存在的意义。")),
        figure(IMG + "umi-quest-latency.jpg", "Camera ArUco axis against the Quest axis after shifting by 56.7 ms: the two motion curves line up.",
               "相机 ArUco 轴与平移 56.7 ms 后的 Quest 轴：两条运动曲线对齐。"))
    body += two_col(
        figure(IMG + "umi-tactile-latency.jpg", "Cross-stream timing alignment for the tactile cameras relative to RGB.", "触觉相机相对 RGB 的跨流时序对齐。"),
        figure(IMG + "umi-gripper-calibration.png", "Gripper-width lookup calibration from the ArUco marker on the finger.", "基于手指上 ArUco 标记的夹爪开度查表标定。"))
    body += video(VID + "umi-calibration.mp4", VID + "umi-calibration.jpg",
                  "Checking the calibration chain on the robot: the FR3 replays a trajectory written in the camera frame while an ArUco marker on the floor serves as the fixed reference. If the geometry and timing are right, the gripper follows the intended path.",
                  "在机器人上验证标定链路：FR3 回放一条在相机坐标系下写好的轨迹，地上的 ArUco 标记作为固定参考。只要几何与时序正确，夹爪就会沿预期路径运动。", wide=True)
    s += section("calib", "Calibration ledger", "标定账本", body)

    body = prose(("Raw streams keep their native timestamps in H5; alignment and camera-relative pose derivation are reproducible post-processing steps. A command-line audit checks stream completeness, timing faults and inverse-kinematics plausibility; a web audit lets us replay any episode with all streams side by side. Only accepted trajectories are promoted to the clean Zarr dataset that training consumes.",
                  "原始流在 H5 中保留各自的时间戳；对齐与相机相对位姿的推导是可重复的后处理步骤。命令行审计检查流完整性、时序故障与逆运动学可行性；网页审计则可以把任意一条示教的所有流并排回放。只有通过审计的轨迹才会被提升到训练所用的干净 Zarr 数据集。"),)
    body += stats([("222", "complete demonstrations in the full corpus", "条完整示教（完整语料）"),
                   ("135,952", "policy frames", "个策略帧"),
                   ("77", "demonstrations in the strict subset used for the controlled comparison", "条示教组成受控对比用的严格子集"),
                   ("7-D", "camera-relative actions: translation, rotation, gripper width", "相机相对动作：平移、旋转、夹爪开度")])
    body += video(VID + "umi-collection.mp4", VID + "umi-collection.jpg", "Portable collection: the hand-held gripper, wrist camera and tactile fingertips in the task workspace, with the FR3 standing by (16× speed).",
                  "便携采集：手持夹爪、手腕相机与触觉指尖在任务工作区中，FR3 在一旁待命（16 倍速）。", wide=True)
    body += video(VID + "umi-audit.mp4", VID + "umi-audit.jpg", "The audit viewer replaying an archived episode: trajectory in 3D, both tactile streams and the wrist view on one timeline.",
                  "审计查看器回放一条归档示教：3D 轨迹、两路触觉流与手腕视角在同一条时间线上。", wide=True)
    s += section("data", "Record first, align second, audit before training", "先记录，再对齐，训练前先审计", body, cls="alt")

    body = prose(("π0.5 is a vision-language-action model: a PaliGemma vision-language backbone with an action expert that generates action chunks by flow matching, pre-trained on large robot corpora and designed to be fine-tuned on a few hundred demonstrations. That makes it a natural match for a UMI corpus, which is exactly a few hundred demonstrations with a wrist view and a 7-D action.",
                  "π0.5 是一个视觉-语言-动作模型：PaliGemma 视觉语言骨干加上一个用流匹配生成动作块的动作专家，在大规模机器人数据上预训练，设计目标就是用几百条示教微调。这与 UMI 语料天然匹配——它正是几百条带手腕视角和 7 维动作的示教。"),
                 ("My branch: convert the clean Zarr corpus into LeRobot format (images, proprioceptive state, action chunks and a natural-language task prompt per episode), compute the normalisation statistics, fine-tune π0.5 with LoRA on a single GPU using the openpi stack, and serve the policy to the FR3 over a websocket inference server. At run time the policy receives the wrist image and robot state, predicts a 50-step chunk of camera-relative 7-D actions, and the controller converts them through inverse kinematics into joint commands. Rollouts were scored live with a success counter.",
                  "我的分支：把干净的 Zarr 语料转换成 LeRobot 格式（每条示教包含图像、本体状态、动作块和一条自然语言任务指令），计算归一化统计量，用 openpi 在单卡上以 LoRA 微调 π0.5，再通过 websocket 推理服务器把策略提供给 FR3。运行时策略接收手腕图像与机器人状态，预测 50 步相机相对的 7 维动作块，控制器经逆运动学转换为关节指令。实机回放用成功计数器实时记录。"),
                 ("Running a VLA and a Diffusion Policy on one calibrated corpus is what makes the two branches comparable. On the Diffusion Policy side, vision-only scored 10/34 and the tactile-conditioned version 14/34 on the contact task; the π0.5 rollouts show that the same data pipeline produces trajectories a modern VLA can learn from and execute on the real FR3.",
                  "在同一套标定过的语料上同时跑 VLA 和 Diffusion Policy，才让两条分支可以互相比较。Diffusion Policy 那边，纯视觉版本在接触任务上 10/34，触觉条件化版本 14/34；π0.5 的真机回放则表明同一条数据流水线产出的轨迹，现代 VLA 可以学会并在真实 FR3 上执行。"))
    body += contributions([
        ("Hand-held system", "手持系统", "Mounting the cameras and tactile sensors, Quest integration, gripper-width marker and lookup table.", "相机与触觉传感器安装、Quest 集成、夹爪开度标记与查表。"),
        ("Calibration", "标定", "Hand–eye calibration, ArUco trajectory checks on the FR3, latency measurement between streams.", "手眼标定、FR3 上的 ArUco 轨迹验证、各流之间的时延测量。"),
        ("Data", "数据", "Collection sessions, episode audit, promotion of accepted episodes to the clean dataset.", "采集会话、示教审计、合格示教提升到干净数据集。"),
        ("π0.5 policy", "π0.5 策略", "LeRobot conversion, openpi fine-tuning, inference server and FR3 deployment, live-scored rollouts.", "LeRobot 转换、openpi 微调、推理服务器与 FR3 部署、实时计分回放。"),
    ])
    body += links([("https://github.com/SuhangXia/tactile-umi", "Tactile UMI repository", "Tactile UMI 代码仓库"),
                   ("https://arxiv.org/abs/2602.01153", "UniForce on arXiv", "UniForce 论文（arXiv）"),
                   ("https://www.physicalintelligence.company/blog/pi05", "π0.5 by Physical Intelligence", "π0.5（Physical Intelligence）")])
    body += callout("The Tactile UMI system and corpus are joint work with Suhang Xia; the UniForce tactile representation was developed under the guidance of Zhuo Chen. The π0.5 fine-tuning and FR3 deployment described here are my branch.",
                    "Tactile UMI 系统与数据集是与夏苏杭的共同工作；UniForce 触觉表示在陈卓指导下完成。本页描述的 π0.5 微调与 FR3 部署是我负责的分支。")
    s += section("pi05", "Fine-tuning π0.5 on the corpus", "在语料上微调 π0.5", body)

    page("tactile-umi", pr['title'][0], pr['title'][1],
         "Tactile UMI: a hand-held visuotactile data-collection system with calibrated geometry and timing, and a π0.5 vision-language-action policy fine-tuned on it and deployed on a Franka FR3.",
         hero, hero_media, s)


# =====================================================================
# 3. TIAGo
# =====================================================================
def tiago():
    pr = PROJECTS[2]
    hero = project_hero(pr['kind'], *pr['title'], *pr['q'], [
        ("Role", "角色", "Simulation and navigation lead: Webots world, SLAM/AMCL/Nav2 pipeline; co-developed the speech + wave perception module", "仿真与导航负责人：Webots 场景、SLAM/AMCL/Nav2 流水线；共同开发语音 + 挥手感知模块"),
        ("Team", "团队", "Six MSc students, supervised by Dr. Oya Celiktutan; in partnership with Guy’s and St Thomas’ Hospital", "六名硕士生，导师 Dr. Oya Celiktutan；与 Guy’s and St Thomas’ 医院合作"),
        ("Period", "时间", "September 2025 – April 2026", "2025 年 9 月 – 2026 年 4 月"),
        ("Platform", "平台", "PAL Robotics TIAGo (physical unit and Webots model), ROS 2 Humble, Nav2, Docker / HuNavSim", "PAL Robotics TIAGo（实体机与 Webots 模型）、ROS 2 Humble、Nav2、Docker / HuNavSim"),
    ])
    hero_media = video(VID + "tiago-demo.mp4", VID + "tiago-demo.jpg",
                       "The simulated ward in Webots with the live map and planner view: TIAGo maps the ward, localises, receives a patient goal and navigates around furniture and people to a stand-off position.",
                       "Webots 中的仿真病房与实时地图/规划视图：TIAGo 建图、定位，接收患者目标后绕过家具与行人，导航到停靠位置。", wide=True)
    s = ''
    s += section("why", "The problem on the ward", "病房里的问题", prose(
        ("Chemotherapy patients sit for hours and often need small things—water, a blanket, a question answered. Each request is simple, but together they interrupt nurses all day. After a site visit to St Thomas’ Hospital and discussions with nursing staff, we scoped a socially assistive robot that handles these low-acuity requests, stays within clear safety boundaries, and defers anything clinical to staff.",
         "化疗患者要在座椅上待几个小时，经常需要一些小事——倒水、拿毯子、问个问题。每个请求都很简单，但加在一起会一整天打断护士的工作。我们实地走访了 St Thomas’ 医院并与护理人员交流后，确定了项目范围：一个处理这类低急迫度请求的社交辅助机器人，在明确的安全边界内工作，任何临床事务都交还给医护人员。"),
        ("The ward layout we built reflects what we saw: a central corridor, treatment bays on both sides with chairs and IV stands, a nurse station and a waiting area. That layout drove every design decision—the corridor is the default traversal zone, the bays need conservative short-range control, and a request can come from either side, so gestures must be detected across bilateral viewing angles.",
         "我们搭建的病房布局来自现场观察：中央走廊、两侧带座椅和输液架的治疗区、护士站和候诊区。这个布局决定了所有设计——走廊是默认通行区，治疗区需要保守的近距离控制，求助可能来自两侧，所以手势检测必须覆盖双侧视角。")))
    body = figure(IMG + "tiago-system-flow.jpg", "System architecture: the staged multimodal perception pipeline (audio trigger → visual confirmation → target localisation) feeding navigation goal generation and the bounded navigate-and-attend interaction.",
                  "系统架构：分阶段的多模态感知流水线（音频触发 → 视觉确认 → 目标定位）生成导航目标，进入“导航-到位陪伴”的受限交互模式。", cls="narrow")
    body += diagram_fig("tiago", "The runtime pipeline in one view. Perception is staged so background speech alone never triggers a move; navigation is the standard Nav2 layering with an inflation margin that is as much social as geometric.",
                        "一张图看运行流水线。感知分阶段进行，背景语音本身不会触发移动；导航是标准 Nav2 分层，其中膨胀边距既是几何安全距离也是社交距离。")
    body += two_col(
        figure(IMG + "tiago-nav-pipeline.jpg", "The SLAM + navigation pipeline I built: mapping (SLAM Toolbox) → save map → AMCL localisation → global planning → local control and obstacle avoidance → reach the goal with recovery behaviours.",
               "我搭建的 SLAM + 导航流水线：建图（SLAM Toolbox）→ 保存地图 → AMCL 定位 → 全局规划 → 局部控制与避障 → 带恢复行为地到达目标。"),
        figure(IMG + "tiago-nav-table.jpg", "Component map: Webots for physics, RViz for visualisation, SLAM Toolbox, AMCL, layered costmaps, NavFn, the local controller and the behaviour-tree navigator.",
               "组件对照表：Webots 负责物理仿真，RViz 可视化，SLAM Toolbox、AMCL、分层代价地图、NavFn、局部控制器与行为树导航器。"))
    s += section("system", "Architecture", "系统架构", body, cls="alt")

    body = prose(("Official TIAGo tutorials were ROS 1-centred; PAL’s ROS 2 simulation repository needed hardware and operating systems that not every team member could run, and Gazebo performed poorly on our laptops. A simulator is useless if only one person can run it. I evaluated Gazebo Classic, Gazebo Fortress, NVIDIA Isaac Sim and Webots on ROS 2 support, TIAGo availability, GPU demand and team-wide reproducibility, and chose Webots inside the containerised HuNavSim framework. It was not the most realistic option—it was the one the whole team could run and test on repeatably.",
                  "官方 TIAGo 教程以 ROS 1 为主；PAL 的 ROS 2 仿真仓库对硬件和操作系统有要求，不是每个组员都能运行，Gazebo 在我们的笔记本上也跑得很差。一个只有一个人能跑的仿真器没有意义。我从 ROS 2 支持、TIAGo 可用性、GPU 需求和全组可复现性四个维度评估了 Gazebo Classic、Gazebo Fortress、NVIDIA Isaac Sim 和 Webots，最终选择了容器化 HuNavSim 框架中的 Webots。它不是最逼真的选项，但它是全组都能运行、都能反复测试的选项。"),
                 ("The navigation stack is Nav2 in its standard layering: LiDAR and RGB-D sensing build an occupancy map by teleoperated exploration; AMCL estimates pose against the saved map; costmaps add an inflation layer around the robot footprint so routes stay clear of beds, chairs and IV stands; NavFn plans globally; the DWB controller samples velocities to follow the path and avoid moving people; behaviour trees handle replanning and recovery. Once perception confirms a request, the patient’s map-frame position becomes a stand-off goal one metre short, facing the patient.",
                  "导航栈采用标准分层的 Nav2：LiDAR 与 RGB-D 通过遥操作探索建立栅格地图；AMCL 基于保存的地图估计位姿；代价地图在机器人足迹周围加入膨胀层，使路径远离病床、座椅和输液架；NavFn 做全局规划；DWB 控制器采样速度跟踪路径并避开移动的人；行为树负责重规划与恢复。感知确认求助后，患者在地图系中的位置转换为距其一米、正对患者的停靠目标。"))
    body += h(3, "Perception: two modalities before the robot moves", "感知：机器人移动前的两重确认")
    body += prose(("Speech alone should not send a robot toward someone, and neither should a stray arm movement. The pipeline begins in a passive listening state: Faster-Whisper with voice-activity detection transcribes 3-second audio windows and matches keywords such as “help” and “tiago”. A match activates the visual stage, where MediaPipe pose estimation feeds a temporal wave detector—waving is sustained lateral wrist motion over several frames with the wrist above the shoulder. Only then is the person’s torso located from median-filtered RGB-D depth, projected through the camera intrinsics into the map frame, and published as a navigation goal.",
                   "单凭语音不该让机器人冲向某人，一次随意的抬手也不该。流水线从被动监听开始：Faster-Whisper 配合语音活动检测转写 3 秒的音频窗口并匹配“help”“tiago”等关键词；匹配后激活视觉阶段，MediaPipe 姿态估计送入时序挥手检测器——“挥手”定义为手腕高于肩膀、且在连续多帧中持续横向运动。只有这时才用中值滤波后的 RGB-D 深度定位人体躯干，经相机内参投影到地图坐标系，发布为导航目标。"),)
    body += two_col(
        figure(IMG + "tiago-robot.jpg", "The TIAGo platform: RGB-D head camera, stereo microphones, lifting torso, 7-DoF arm with a parallel gripper, laser range-finder and a differential-drive base.",
               "TIAGo 平台：RGB-D 头部相机、立体麦克风、升降躯干、带平行夹爪的 7 自由度手臂、激光测距仪与差速底盘。"),
        figure(IMG + "tiago-lab-team.jpg", "The team with the physical TIAGo in the KCL robotics lab. Late in the project the unit became unreliable—dropped SSH, missing topics after boot, a camera feed that would not come back—and we pivoted to a complete simulation delivery ten days before demo day.",
               "团队与实体 TIAGo 在 KCL 机器人实验室。项目后期实体机变得不稳定——SSH 掉线、开机后话题缺失、相机画面无法恢复——我们在演示日前十天果断转向完整的仿真交付。"))
    s += section("build", "Choosing the simulator, building the stack", "选择仿真器，搭建导航栈", body)

    body = prose(("Testing ran in Webots with static obstacles and dynamic agents representing patients and staff, ten trials per condition, metrics pulled from ROS 2 logs. Navigation was consistent; where the system fell short it was the perception stage, not navigation—which is the honest reading of the gap between 92% and 94%.",
                  "测试在 Webots 中进行，场景包含静态障碍和代表患者与医护的动态行人，每种条件 10 次试验，指标来自 ROS 2 日志。导航表现稳定；系统的短板在感知阶段而不是导航——这也是 92% 与 94% 之间差距的真实含义。"),)
    body += stats([("92%", "end-to-end success given a valid trigger", "有效触发下的端到端成功率"),
                   ("94%", "navigation success, 41.7 s mean time to goal", "导航成功率，平均到达时间 41.7 s"),
                   ("0.12 m", "final position error; 0.18 m stand-off error", "终点位置误差；停靠距离误差 0.18 m"),
                   ("97.6%", "gesture recognition accuracy, 185 ms latency", "手势识别准确率，时延 185 ms")])
    body += f'''<table><thead><tr><th>{t("Metric", "指标")}</th><th class="num">{t("Value", "数值")}</th><th>{t("Metric", "指标")}</th><th class="num">{t("Value", "数值")}</th></tr></thead><tbody>
<tr><td>{t("Full task completion time", "完整任务用时")}</td><td class="num">74.3 s</td><td>{t("Detection precision / recall / F1", "检测精确率 / 召回率 / F1")}</td><td class="num">92.6 / 89.8 / 91.2 %</td></tr>
<tr><td>{t("Path efficiency", "路径效率")}</td><td class="num">87.5 %</td><td>{t("Target localisation error", "目标定位误差")}</td><td class="num">0.21 m</td></tr>
<tr><td>{t("Collisions per trial", "每次试验碰撞次数")}</td><td class="num">0.1</td><td>{t("Recovery events per trial", "每次试验恢复行为次数")}</td><td class="num">0.3</td></tr>
<tr><td>{t("Final orientation error", "终点朝向误差")}</td><td class="num">7.4°</td><td>{t("Manual interventions per trial", "每次试验人工干预次数")}</td><td class="num">0.2</td></tr>
</tbody></table>'''
    body += callout("All results are from simulation; hardware integration on the physical TIAGo was not completed within the project window. Privacy, patient dignity and escalation to staff were built in as design constraints from the start.",
                    "所有结果来自仿真环境；实体 TIAGo 的硬件集成未能在项目周期内完成。隐私、患者尊严与向医护升级从一开始就作为设计约束纳入。")
    body += contributions([
        ("Simulation", "仿真", "Platform evaluation; Webots ward world with TIAGo, furniture and moving agents inside the HuNavSim container.", "仿真平台评估；在 HuNavSim 容器中搭建带 TIAGo、家具与移动行人的 Webots 病房场景。"),
        ("Navigation", "导航", "The full SLAM → AMCL → Nav2 pipeline, costmap inflation tuning, stand-off goal computation and the Docker goal bridge.", "完整的 SLAM → AMCL → Nav2 流水线、代价地图膨胀调参、停靠目标计算与 Docker 目标桥接。"),
        ("Perception", "感知", "Co-developed the speech trigger and wave-detection module and its hand-off to navigation.", "共同开发语音触发与挥手检测模块及其到导航的交接。"),
        ("Testing", "测试", "Trial protocol and metric extraction from ROS 2 logs.", "试验方案与从 ROS 2 日志中提取指标。"),
    ])
    body += links([(CV + "TIAGo_Group_Project_Report.pdf", "Group project portfolio (PDF)", "小组项目报告（PDF）"),
                   ("https://github.com/Lixiangqi2002/hunavsim_docker", "HuNavSim Docker (simulation base)", "HuNavSim Docker（仿真基础）"),
                   ("https://cyberbotics.com/doc/guide/tutorials", "Webots documentation", "Webots 文档")])
    body += figure(IMG + "tiago-poster-day.jpg", "Poster day with the team and our supervisor, King’s College London, 2026.", "海报日：与团队和导师合影，伦敦国王学院，2026。", cls="mid")
    body += f'<div class="gallery g2" style="max-width:30rem"><figure class="fig"><img src="{IMG}logo-gstt.jpg" alt="Guy’s and St Thomas’ NHS Foundation Trust" loading="lazy"></figure><figure class="fig"><img src="{IMG}logo-pal.jpg" alt="PAL Robotics" loading="lazy"></figure></div>'
    s += section("results", "Results", "结果", body, cls="alt")
    page("tiago", pr['title'][0], pr['title'][1],
         "A ROS 2 + Webots TIAGo assistive robot for chemotherapy wards: speech and wave-gesture engagement detection, SLAM/AMCL/Nav2 navigation and a social stand-off interaction model.",
         hero, hero_media, s)


# =====================================================================
# 4. Thread inspection
# =====================================================================
def thread():
    pr = PROJECTS[3]
    hero = project_hero(pr['kind'], *pr['title'], *pr['q'], [
        ("Role", "角色", "Research assistant; co-first author of the PLOS ONE system paper; corresponding author of two SPIE reviews; co-inventor on two patents", "科研助理；PLOS ONE 系统论文共同一作；两篇 SPIE 综述通讯作者；两项专利共同发明人"),
        ("Period", "时间", "March 2022 – July 2025", "2022 年 3 月 – 2025 年 7 月"),
        ("Where", "单位", "Yangtze University, with Prof. Gengpei Zhang’s group", "长江大学，张耕培教授课题组"),
        ("Stack", "技术栈", "Raspberry Pi, six fisheye cameras, LED strip lighting, stepper and robot-arm carriers; OpenCV, SIFT + RANSAC, Laplacian pyramids; StyleGAN2 / DFMGAN; YOLOv5 / v8, SSD", "树莓派、六目鱼眼相机、LED 条形光源、步进滑台与机械臂载体；OpenCV、SIFT + RANSAC、拉普拉斯金字塔；StyleGAN2 / DFMGAN；YOLOv5 / v8、SSD"),
    ])
    hero_media = figure(IMG + "p4_robot_arm_rig_photo.png", "The second-generation rig: a robot arm carries the six-fisheye probe with its LED ring into the threaded bore and records video while it moves—44% faster than the stepper slide it replaced.",
                        "第二代装置：机械臂携带带 LED 光环的六目鱼眼探头进入螺纹孔，边移动边录像——比它取代的步进滑台快 44%。", cls="mid")
    s = ''
    s += section("why", "The problem", "问题", prose(
        ("Threaded connections hold aerospace parts, engines and oil-and-gas tubulars together, and a defective internal thread means a failed seal. But internal threads live in narrow, dark, curved bores with a helical geometry: a camera cannot see the whole surface at once, a point light casts shadows from every thread crest, and manual gauge inspection is slow, subjective and wears the part. Contact methods are accurate but slow; laser and eddy-current methods fail on reflective or non-metal parts.",
         "螺纹连接把航空零件、发动机和油气管具连在一起，一个有缺陷的内螺纹意味着密封失效。但内螺纹藏在狭窄、黑暗、弯曲、呈螺旋几何的孔内：相机无法一次看到整个表面，点光源在每个牙顶都投下阴影，人工量规检测慢、主观且磨损零件。接触式方法准确但慢，激光和涡流方法在反光或非金属零件上失效。"),
        ("And once the imaging works, a second wall appears: real defect samples are rare, so a detector cannot be trained well. This project went through both walls in turn—first a multi-camera imaging and stitching system, then a generative pipeline that manufactures the training data the detector needs.",
         "而当成像问题解决之后，第二堵墙出现了：真实缺陷样本极少，检测器训练不好。这个项目先后穿过了这两堵墙——先是多相机成像与拼接系统，然后是为检测器制造训练数据的生成式流水线。")))
    body = diagram_fig("thread", "The full pipeline, from optics to detection.", "从光学到检测的完整流水线。")
    body += two_col(
        prose(("Six 1680×1080 fisheye cameras sit in two groups of three. Each group is arranged on a 120° ring and the two groups are offset by 60°, so their fields of view tile the whole bore; for small bores the groups shoot in a staggered mode so the second fills the gaps left by the first. A Raspberry Pi drives the cameras, the lighting and a stepper motor that advances the probe axially.",
               "六个 1680×1080 的鱼眼相机分成两组，每组三个。每组按 120° 环形布置，两组错开 60°，视场正好铺满整个孔壁；对于小孔径，两组交错拍摄，第二组补上第一组留下的空隙。树莓派控制相机、光源和沿轴向推进探头的步进电机。"),
              ("Lighting decided more than optics did. Point LEDs cast hard shadows from the thread crests, so each lens got a strip light beside it and the whole probe was wrapped in a diffuser to kill specular reflection from the metal. We first tested on a DN100 fully threaded tube, 110 mm inner diameter.",
               "光照的影响甚至超过了光学设计。点光源会在牙顶投下硬阴影，于是每个镜头旁边改用条形光源，整个探头再包一层柔光材料消除金属的镜面反射。首次测试对象是 DN100 全螺纹管，内径 110 mm。")),
        figure(IMG + "p4_sixcamera_rig_model.png", "Two three-camera groups on 120° rings, offset by 60°, so six fields of view cover the circumference.",
               "两组三相机按 120° 环布、错开 60°，六个视场覆盖整个圆周。"))
    body += gallery([
        (IMG + "p4_sixcamera_rig_photo.jpg", "The first probe: six fisheye modules on 3D-printed rings.", "第一代探头：3D 打印环上的六个鱼眼模块。"),
        (IMG + "p4_working_mode_staggered_cameras.jpg", "Staggered working mode: cameras 1–3 then 4–6 fill each other’s gaps in small bores.", "交错工作模式：相机 1–3 与 4–6 在小孔径内互相补空。"),
        (IMG + "p4_system_flowchart_hw_sw.png", "Hardware and software flow of the first system (PLOS ONE).", "第一代系统的硬件与软件流程（PLOS ONE）。"),
    ])
    s += section("hardware", "Seeing inside the bore", "看进孔内", body, cls="alt")

    body = prose(("Every frame first goes through Zhang’s checkerboard calibration with sub-pixel corner refinement and fisheye undistortion. We benchmarked denoisers on 10 dB noise—BM3D won on quality (PSNR 34.9 dB, SSIM 0.971), DnCNN was chosen later for real-time speed—and compared Retinex variants for the dark bore, where MSRCR kept colour fidelity and detail. A curvature-based crop then discards the strongly distorted fisheye margins.",
                  "每一帧先经过张正友棋盘格标定、亚像素角点优化与鱼眼畸变校正。我们在 10 dB 噪声下对比去噪方法——BM3D 质量最好（PSNR 34.9 dB，SSIM 0.971），后来为了实时性选用 DnCNN；又比较了 Retinex 系列在暗孔中的表现，MSRCR 在色彩保真与细节上最佳。随后用基于曲率的裁剪去掉鱼眼边缘畸变严重的区域。"),
                 ("Stitching was the real obstacle. Planar homography pipelines—Harris, FAST, SIFT, SURF, ORB with DLT or RANSAC—all fail on a thread: the texture is repetitive and the surface is a cylinder, not a plane. The method that worked projects every frame onto a cylindrical model first, then matches SIFT features with RANSAC and blends with Laplacian pyramids, producing a seamless 360° unrolled panorama of the thread.",
                  "拼接才是真正的障碍。平面单应性流水线——Harris、FAST、SIFT、SURF、ORB 配合 DLT 或 RANSAC——在螺纹上全部失效：纹理重复，表面是柱面而不是平面。可行的方法是先把每帧投影到柱面模型上，再用 SIFT + RANSAC 匹配，最后用拉普拉斯金字塔融合，得到无缝的 360° 螺纹展开图。"))
    body += figure(IMG + "p4_cylindrical_panorama_stitch.jpg", "The unrolled 360° panorama of the internal thread produced by cylindrical-model stitching.", "柱面模型拼接得到的内螺纹 360° 展开图。", wide=True)
    body += two_col(
        figure(IMG + "p4_stitching_method_comparison.jpg", "Planar stitching (A, B) tears and ghosts on the repetitive helical texture; the cylindrical model (C) joins frames cleanly.", "平面拼接（A、B）在重复的螺旋纹理上出现撕裂和重影；柱面模型（C）干净地拼合。"),
        figure(IMG + "p4_distortion_correction_before_after.jpg", "A fisheye frame before and after undistortion.", "鱼眼帧畸变校正前后。"))
    s += section("stitch", "Making a cylinder flat", "把圆柱展平", body)

    body = prose(("YOLOv8 trained on our annotated dataset reached mAP 91.6%, recall 84.7% and precision 88.4% on the corrosion class, against YOLOv5 (91.5 / 73.3 / 86.2) and SSD (71.1 / 46.7 / 87.5). On eight random bore images containing 19 defects it found 17. The resolution analysis sets the physical floor: a 100 mm bore with a 1080p camera resolves about 0.52 mm per pixel.",
                  "在我们标注的数据集上训练的 YOLOv8 在腐蚀类上达到 mAP 91.6%、召回率 84.7%、精确率 88.4%，对比 YOLOv5（91.5 / 73.3 / 86.2）和 SSD（71.1 / 46.7 / 87.5）。在随机抽取的 8 张含 19 处缺陷的孔内图像中检出 17 处。分辨率分析给出了物理下限：100 mm 孔径配 1080p 相机约为每像素 0.52 mm。"),
                 ("Then the data wall. Real internal-thread defects are too rare to train on, so the second paper built a Defect-aware Feature Manipulation GAN: a StyleGAN2 backbone pre-trained on hundreds of defect-free thread images, then defect-aware residual blocks and a defect-mapping network trained on a small set of defect images, with a second discriminator and a mode-seeking loss for diversity. It outputs a defect image and its mask together. Because real internal defects are so scarce, we validated the idea on external threads first—YOLOv8 trained on generated external images performed close to one trained on real ones—and only then trained the internal-thread detector on synthetic data: precision 94.3%, recall 79.5%, mAP 88.3%, finding 20 of 21 real defects in a sampled check (95.2%, up from 89.5% in the first system).",
                  "然后是数据这堵墙。真实内螺纹缺陷太少，无法直接训练，于是第二篇论文构建了缺陷感知特征操控 GAN（DFMGAN）：先用数百张无缺陷螺纹图像预训练 StyleGAN2 骨干，再用少量缺陷图像训练缺陷感知残差块和缺陷映射网络，配合第二个判别器和模式搜索损失保证多样性，同时输出缺陷图像及其掩膜。由于真实内螺纹缺陷过于稀少，我们先在外螺纹上验证思路——用生成的外螺纹图像训练的 YOLOv8 与用真实图像训练的表现接近——然后才用合成数据训练内螺纹检测器：精确率 94.3%、召回率 79.5%、mAP 88.3%，抽检 21 处真实缺陷检出 20 处（95.2%，高于第一代系统的 89.5%）。"))
    body += stats([("91.6%", "YOLOv8 mAP on the corrosion class (SSD: 71.1%)", "YOLOv8 在腐蚀类上的 mAP（SSD 仅 71.1%）"),
                   ("95.2%", "of real internal defects found by the detector trained on DFMGAN data", "用 DFMGAN 数据训练的检测器在真实内螺纹上的缺陷检出率"),
                   ("−44%", "acquisition time with the robot-arm carrier and video frame extraction", "机械臂载体 + 视频抽帧带来的采集时间下降"),
                   ("0.52 mm", "per pixel: the resolution floor for a 100 mm bore at 1080p", "每像素：100 mm 孔径在 1080p 下的分辨率下限")])
    body += two_col(
        figure(IMG + "p4_dfmgan_generator_structure.png", "The DFMGAN generator: StyleGAN2 synthesis blocks plus defect-aware residual blocks at three scales and a defect-mapping network.", "DFMGAN 生成器：StyleGAN2 合成块加上三个尺度的缺陷感知残差块与缺陷映射网络。"),
        figure(IMG + "p4_gan_system_framework.png", "Four steps of the second system: acquisition → DFMGAN training → YOLOv8 training → detection.", "第二代系统的四个步骤：采集 → DFMGAN 训练 → YOLOv8 训练 → 检测。"))
    body += gallery([
        (IMG + "p4_yolov8_detection_results_8imgs.jpg", "YOLOv8 detections on eight random bore images (first system).", "YOLOv8 在 8 张随机孔内图像上的检测结果（第一代系统）。"),
        (IMG + "p4_internal_detection_broken.jpg", "“Broken” thread detections by the detector trained on synthetic internal-thread data.", "用合成内螺纹数据训练的检测器对“断牙”缺陷的检测。"),
        (IMG + "p4_internal_real_vs_generated.png", "A real internal defect next to a DFMGAN-generated one.", "真实内螺纹缺陷与 DFMGAN 生成缺陷的对比。"),
    ])
    s += section("detect", "Detecting defects—and manufacturing the data to learn from", "检测缺陷，并“制造”学习所需的数据", body, cls="alt")

    body = prose(("Two reviews I corresponded grew directly out of the engineering: one on image stitching for internal threads, one on calibration and distortion correction. And two patent applications extend the hardware: an internal-thread system that detects defects with adaptive binarisation and a Radon transform rather than a learned model, and an external-thread device that places four stereo camera pairs at 90° around a vertical pipe on a lifting platform and stitches their point clouds.",
                  "我作为通讯作者的两篇综述直接来自工程实践：一篇关于内螺纹图像拼接，一篇关于标定与畸变校正。两项专利申请则扩展了硬件：一套用自适应二值化和 Radon 变换（而非学习模型）检测缺陷的内螺纹系统，以及一套在升降平台上围绕竖直管件 90° 布置四对双目相机并拼接点云的外螺纹检测装置。"),)
    body += two_col(
        figure(IMG + "p4_patent_external_thread_fig1_top_view.png", "External-thread inspection device (CN 202411050637.1): four stereo pairs and LED sources around the pipe, feeding a computer through a hub.", "外螺纹检测装置（CN 202411050637.1）：管件周围的四对双目相机与 LED 光源，经集线器连接计算机。"),
        figure(IMG + "p4_patent_radon_fig3to5_edge_radon_result.png", "Internal-thread system (CN 202411066290.X): original image, binarised edges and the Radon-transform map used to flag defects.", "内螺纹检测系统（CN 202411066290.X）：原图、二值化边缘与用于标记缺陷的 Radon 变换图。"))
    body += contributions([
        ("Imaging hardware", "成像硬件", "Camera ring geometry, strip lighting and diffuser, Raspberry Pi control of cameras, lighting and the stepper carrier.", "相机环几何、条形光源与柔光罩，树莓派对相机、光源与步进载体的控制。"),
        ("Classical vision", "传统视觉", "Fisheye calibration and undistortion, denoising and Retinex benchmarks, cylindrical-model stitching.", "鱼眼标定与畸变校正、去噪与 Retinex 对比、柱面模型拼接。"),
        ("Learning", "学习方法", "Dataset annotation; SSD / YOLOv5 / YOLOv8 comparison; DFMGAN training and the external-thread validation design.", "数据集标注；SSD / YOLOv5 / YOLOv8 对比；DFMGAN 训练与外螺纹验证方案。"),
        ("Writing and IP", "写作与知识产权", "Co-first author (PLOS ONE), co-author (Sensors), corresponding author on two SPIE reviews, two patent applications.", "共同一作（PLOS ONE）、合著（Sensors）、两篇 SPIE 综述通讯作者、两项专利申请。"),
    ])
    body += links([("https://doi.org/10.1371/journal.pone.0304224", "PLOS ONE: Internal thread defect detection system based on multi-vision", "PLOS ONE：基于多视觉的内螺纹缺陷检测系统"),
                   ("https://doi.org/10.3390/s24175636", "Sensors: Defect generation and detection with GANs and YOLO", "Sensors：基于 GAN 与 YOLO 的缺陷生成与检测"),
                   ("https://doi.org/10.1117/12.3065383", "SPIE: Review of image stitching for internal threads", "SPIE：内螺纹图像拼接综述"),
                   ("https://doi.org/10.1117/12.3045519", "SPIE: Review of calibration and distortion correction", "SPIE：标定与畸变校正综述")])
    s += section("outputs", "Papers, patents, and my part", "论文、专利与我的工作", body)
    page("thread-inspection", pr['title'][0], pr['title'][1],
         "A six-fisheye imaging probe, cylindrical panorama stitching, GAN-based defect synthesis and YOLOv8 detection for internal threads; two SCI Q1 papers, two SPIE reviews and two patents.",
         hero, hero_media, s)


# =====================================================================
# 5. GFRP ML
# =====================================================================
def gfrp():
    pr = PROJECTS[4]
    hero = project_hero(pr['kind'], *pr['title'], *pr['q'], [
        ("Role", "角色", "Research assistant; co-first author of both PLOS ONE papers", "科研助理；两篇 PLOS ONE 论文共同一作"),
        ("Period", "时间", "March 2021 – July 2025", "2021 年 3 月 – 2025 年 7 月"),
        ("Where", "单位", "Yangtze University", "长江大学"),
        ("Stack", "技术栈", "Python, scikit-learn, PyTorch; SVR / GPR / RBFNN baselines; genetic-algorithm augmentation; Reptile meta-learning; TPOT AutoML, SVM, MLP, Bagging, Random Forest", "Python、scikit-learn、PyTorch；SVR / GPR / RBFNN 基线；遗传算法数据增广；Reptile 元学习；TPOT AutoML、SVM、MLP、Bagging、随机森林"),
    ])
    hero_media = figure(IMG + "p5_meta_gfrp_columns_photo.jpg", "GFRP-tube-confined concrete column specimens. Each data point in this project is one of these, loaded to failure in an axial-compression test—which is why there are only 72 of them.",
                        "GFRP 管约束混凝土柱试件。项目中的每一个数据点都是这样一根柱子在轴压试验中被压到破坏得到的——这就是为什么只有 72 组。", wide=True)
    s = ''
    s += section("why", "The problem", "问题", prose(
        ("Glass-fibre-reinforced-polymer tubes filled with concrete make light, corrosion-resistant columns for bridges, marine and underground structures. Predicting their ultimate bearing capacity and ultimate displacement from design parameters would let engineers optimise a section before casting it. But every data point is a destructive test, so the datasets are tiny—72 specimens here—while deep networks typically want thousands of samples.",
         "玻璃纤维增强聚合物（GFRP）管内填混凝土，可以做成轻质、耐腐蚀的柱子，用于桥梁、海洋和地下结构。如果能从设计参数预测极限承载力和极限位移，工程师就能在浇筑前优化截面。但每个数据点都来自一次破坏性试验，数据集因此极小——这里只有 72 个试件——而深度网络通常需要成千上万个样本。"),
        ("I worked the problem from two directions. The first paper asks whether a deep model can be made to work with 72 samples at all, by generating physically plausible virtual samples and meta-learning an initialisation. The second asks which off-the-shelf learners—including an AutoML search—model two families of GFRP columns best, and then turns the best models into design recommendations.",
         "我从两个方向解决这个问题。第一篇论文问：能否通过生成物理上合理的虚拟样本并用元学习获得初始化，让深度模型在 72 个样本上也能工作？第二篇论文问：哪些现成的学习器——包括 AutoML 搜索——最适合建模两类 GFRP 柱？然后把最优模型变成设计建议。")))
    body = diagram_fig("gfrp", "The small-sample route: augment with a genetic algorithm, meta-learn an initialisation, fine-tune on the real specimens.",
                       "小样本路线：遗传算法增广 → 元学习初始化 → 在真实试件上微调。")
    body += prose(("Five inputs describe a column: the symmetry ratio of the embedded profile (I-section 100%, L-section 0%, C-section in between), its area ratio, concrete strength, height-to-diameter ratio and diameter-to-wall-thickness ratio. Two outputs: ultimate bearing capacity and ultimate displacement. 66 specimens train, 6 are held out—two of each section type—and every model is re-run 100 times with different random seeds so a lucky split cannot masquerade as a result.",
                  "五个输入描述一根柱子：内嵌型材的对称度（I 型 100%，L 型 0%，C 型介于两者之间）、面积比、混凝土强度、高径比、径厚比。两个输出：极限承载力与极限位移。66 个试件用于训练，6 个留出——每种截面各两个——每个模型用不同随机种子重复 100 次，避免一次幸运的划分冒充结果。"),
                 ("The augmentation treats each real sample as an individual and its parameters as chromosomes. Two training samples cross over, a mutation multiplies a parameter by a random factor in [0.5, 1.5], and the offspring survives only if three regressors trained on real data—SVR, GPR and RBFNN—agree it is plausible (fitness MAPE below 20%, tightened over generations). Seven generations produced about 15,000 virtual samples whose correlation structure matches the original data. Reptile, a first-order meta-learning algorithm, then pre-trains a five-layer fully connected network across tasks sampled from these meta-datasets, and the result is fine-tuned on the 66 real specimens.",
                  "增广把每个真实样本当作个体、参数当作染色体。两个训练样本交叉，变异则把某个参数乘以 [0.5, 1.5] 内的随机因子，只有当三个在真实数据上训练的回归器——SVR、GPR、RBFNN——都认为后代合理（适应度 MAPE 低于 20%，并逐代收紧）时才保留。七代演化产生了约 15,000 个虚拟样本，其相关性结构与原始数据一致。随后用一阶元学习算法 Reptile 在这些元数据集采样的任务上预训练一个五层全连接网络，再在 66 个真实试件上微调。"))
    body += two_col(
        figure(IMG + "p5_meta_genetic_data_augmentation_flow.jpg", "The genetic augmentation loop: crossover and mutation, fitness scored by SVR / GPR / RBFNN, repeated until each meta-dataset exceeds 5,000 samples.",
               "遗传增广循环：交叉与变异，由 SVR / GPR / RBFNN 评定适应度，重复至每个元数据集超过 5,000 个样本。"),
        figure(IMG + "p5_meta_correlation_heatmaps_before_after_aug.png", "Input–output correlation heatmaps before and after augmentation: the virtual samples preserve the physics encoded in the real ones.",
               "增广前后的输入–输出相关性热图：虚拟样本保留了真实样本中蕴含的物理关系。"))
    body += stats([("R² 0.982", "ultimate bearing capacity with Reptile (MAPE 9.5%); best baseline 0.866", "Reptile 预测极限承载力（MAPE 9.5%）；最佳基线 0.866"),
                   ("R² 0.955", "ultimate displacement (MAPE 6.1%); best baseline 0.875", "极限位移（MAPE 6.1%）；最佳基线 0.875"),
                   ("72 → 15,000", "real specimens to virtual samples", "真实试件 → 虚拟样本"),
                   ("100", "random-seed repeats behind every reported number", "每个报告数字背后的随机种子重复次数")])
    body += two_col(
        figure(IMG + "p5_meta_r2_bearing_capacity_100runs.jpg", "R² for ultimate bearing capacity over 100 runs: Reptile against SVR, GPR and RBFNN with and without augmented data.",
               "100 次运行中极限承载力的 R²：Reptile 对比有无增广数据的 SVR、GPR、RBFNN。"),
        figure(IMG + "p5_meta_bearing_capacity_param_curves.png", "What the model learned: bearing capacity rises with symmetry ratio up to about 80% then plateaus, rises with area ratio and concrete strength, and falls with H/D and D/T.",
               "模型学到的规律：承载力随对称度上升至约 80% 后趋于平缓，随面积比和混凝土强度上升，随高径比和径厚比下降。"))
    s += section("meta", "Making 72 samples enough", "让 72 个样本够用", body, cls="alt")

    body = prose(("The second study benchmarks TPOT—a genetic-programming AutoML that searches feature selectors, transformers, regressors and their hyper-parameters and exports a Python pipeline—against SVM, MLP, Bagging and Random Forest on two column families: concrete-wound GFRP columns and concrete-filled GFRP columns (60 unreinforced plus 3 × 27 reinforced specimens). A modelling loop cycles the random split, logs R² and MAE per cycle and keeps the best seed.",
                  "第二项研究把 TPOT——一种基于遗传编程的 AutoML，搜索特征选择器、变换器、回归器及其超参数并导出 Python 流水线——与 SVM、MLP、Bagging、随机森林在两类柱上对比：混凝土缠绕 GFRP 柱与混凝土填充 GFRP 柱（60 个无加筋 + 3 × 27 个加筋试件）。建模循环轮换随机划分，逐轮记录 R² 与 MAE，保留最优种子。"),
                 ("For wound columns SVM was best (bearing capacity MAE 0.36%, R² 0.9998) with TPOT second; Bagging and Random Forest failed outright on displacement. For filled columns TPOT was best on average (MAE 0.76%, R² 0.996). Probing the best models gave two design recommendations: for a wound column an I-section with 40 MPa concrete, H/D = 1.5 and D/T = 25; for a filled column a C-section with 45.3 MPa concrete, H/D = 10 and D/T = 20, with the diameter-to-thickness ratio flagged as the governing failure index.",
                  "对缠绕柱，SVM 最优（承载力 MAE 0.36%，R² 0.9998），TPOT 次之；Bagging 与随机森林在位移上完全失效。对填充柱，TPOT 平均最优（MAE 0.76%，R² 0.996）。对最优模型做探测得到两条设计建议：缠绕柱采用 I 型截面、40 MPa 混凝土、H/D = 1.5、D/T = 25；填充柱采用 C 型截面、45.3 MPa 混凝土、H/D = 10、D/T = 20，并指出径厚比是主导破坏的指标。"))
    body += two_col(
        figure(IMG + "p5_tpot_automl_pipeline_architecture.jpg", "The AutoML modelling architecture: spreadsheet in, TPOT pipeline generation, random-seed search, prediction and analysis out.",
               "AutoML 建模架构：表格数据输入，TPOT 生成流水线，随机种子搜索，输出预测与分析。"),
        figure(IMG + "p5_tpot_column_failure_photo.jpg", "Specimens after axial-compression failure—fibre rupture in the GFRP tube.", "轴压破坏后的试件——GFRP 管纤维断裂。"))
    body += contributions([
        ("Data", "数据", "Collected and normalised the test data from the literature; defined the five physical inputs.", "从文献收集并归一化试验数据；定义五个物理输入。"),
        ("Augmentation + meta-learning", "增广 + 元学习", "Genetic augmentation with three-model fitness; Reptile pre-training and fine-tuning; the 100-run evaluation protocol.", "三模型适应度的遗传增广；Reptile 预训练与微调；100 次重复的评测方案。"),
        ("AutoML benchmark", "AutoML 对比", "TPOT, SVM, MLP, Bagging and RF comparison on two column families; sensitivity sweeps that produced the design rules.", "两类柱上的 TPOT、SVM、MLP、Bagging、RF 对比；得出设计规律的灵敏度扫描。"),
        ("Writing", "写作", "Co-first author on both PLOS ONE papers.", "两篇 PLOS ONE 论文共同一作。"),
    ])
    body += links([("https://doi.org/10.1371/journal.pone.0305038", "PLOS ONE: Small-sample deep meta-learning for GFRP columns", "PLOS ONE：GFRP 柱的小样本深度元学习"),
                   ("https://doi.org/10.1371/journal.pone.0301865", "PLOS ONE: Design optimisation with machine learning", "PLOS ONE：基于机器学习的设计优化")])
    s += section("automl", "Which learner, and what to build", "选哪种学习器，以及该怎么设计", body)
    page("gfrp-ml", pr['title'][0], pr['title'][1],
         "Small-sample machine learning for GFRP-tube concrete columns: genetic data augmentation, Reptile meta-learning (R² 0.982) and an AutoML benchmark that yields design recommendations.",
         hero, hero_media, s)


# =====================================================================
# 6. Industrial monitoring
# =====================================================================
def monitoring():
    pr = PROJECTS[5]
    hero = project_hero(pr['kind'], *pr['title'], *pr['q'], [
        ("Role", "角色", "First inventor on both patents; mechanical concept, sensing chain and embedded vision design", "两项专利第一发明人；机械方案、传感链路与嵌入式视觉设计"),
        ("Period", "时间", "June 2023 – February 2024", "2023 年 6 月 – 2024 年 2 月"),
        ("Where", "单位", "Yangtze University, for oil and gas exploration sites in Hubei", "长江大学，面向湖北油气勘探井场"),
        ("Patents", "专利", "ZL 202323487863.X (granted 2024-09) and ZL 2023 2 3530543.8 (granted 2024-10)", "ZL 202323487863.X（2024 年 9 月授权）与 ZL 2023 2 3530543.8（2024 年 10 月授权）"),
    ])
    hero_media = None
    s = ''
    s += section("why", "The problem on site", "现场的问题", prose(
        ("Seismic-exploration and production wellheads release hydrogen sulphide, methane and sulphur dioxide. Regulations ban smoking and require hard hats, but supervision depends on people, cannot watch every face all day, and cannot stop a violation in real time. And when H₂S exceeds the safe limit on an open site, workers have no way to tell which way the wind is blowing—so they cannot pick the up-wind escape direction, and lose the seconds that matter most.",
         "地震勘探与生产井口会释放硫化氢、甲烷和二氧化硫。法规禁止吸烟并要求佩戴安全帽，但监管靠人，无法整天盯住每一张脸，也无法实时制止违规。而当空旷井场上硫化氢超过安全限值时，工人无从判断风向——也就无法选择逆风逃生方向，白白浪费最关键的几秒。"),
        ("Both devices came from the same field pain point: move perception onto hardware that is always on, and make the safety cue physical and instant.",
         "两个装置都来自同一个现场痛点：把感知放到始终在线的硬件上，让安全提示变成物理的、即时的东西。")))
    body = diagram_fig("wellsite", "The two devices as one system: an always-on vision sweep for compliance, and a self-powered beacon for escape.",
                       "两个装置组成一套系统：持续巡检的视觉合规监控，以及自供电的逃生指示装置。")
    body += two_col(
        prose(("A foldable tripod with an end cap sits over the wellhead. Inside the cap a rotation motor spins a boom that carries the control box. At the boom’s end a second motor drives a lead screw whose nut carries the camera mount, so the orbit radius of the vision probe is motorised and can be set to cover any working area; a third motor pitches the camera. The camera performs uniform circular sweeps of the whole work face, locks quickly onto a worker’s face region and uploads frames to the control box, which runs the analysis on board: is the mouth region showing smoking, and is the area above the brow covered by a hard hat? Violations are flagged automatically.",
               "一个带端盖的折叠三脚架架在井口上方。端盖内的旋转电机带动装有控制盒的摇臂转动；摇臂末端的第二个电机驱动丝杠，丝杠螺母带动相机支架，使视觉探头的巡检半径可以电动调节以覆盖任意作业区；第三个电机负责相机俯仰。相机对整个工作面做匀速环绕巡检，快速锁定工人的面部区域并把图像上传到控制盒，由控制盒在本地完成分析：口部区域是否在吸烟？眉毛以上是否有安全帽？违规行为自动标记。"),
              ("One leg carries a hand-crank winch with a ratchet drum and self-locking pawl, so the same tripod can hoist equipment—or a person—without back-driving. Safety hardware should do more than one job.",
               "其中一条腿装有带棘轮和自锁棘爪的手摇绞盘，同一个三脚架还能吊装设备——甚至救人——且不会反转。安全硬件应当一物多用。")),
        figure(IMG + "p6_patent_wellhead_fig1_overall_tripod_camera.png", "Patent drawing: the tripod over the wellhead with the boom-mounted camera head and the winch.", "专利附图：井口上方的三脚架、摇臂末端的相机头与绞盘。", cls="plain"))
    body += figure(IMG + "p6_patent_wellhead_fig2_monitoring_assembly_internal.png", "Inside the monitoring assembly: rotation motor, boom, control box, extension motor and lead screw, camera mount, pitch motor and camera.", "监控组件内部：旋转电机、摇臂、控制盒、伸缩电机与丝杠、相机支架、俯仰电机与相机。", cls="plain narrow")
    s += section("vision", "Device 1: a camera that patrols the wellhead", "装置一：巡检井口的相机", body, cls="alt")

    body = two_col(
        prose(("A ground base with four stakes holds a vertical post whose height is set by a double-threaded rod. On top, a bearing-mounted wind vane turns freely; its linkage rod rotates a platform that carries the H₂S detector, a siren, a solar power system and a microcontroller. A pointer board with LEDs arranged as an arrow is fixed to that rotating platform, so the arrow always points away from the wind—the safe escape direction—with no computation at all.",
               "带四根地钉的底座上立着一根立柱，高度由双头螺杆调节。顶部是轴承安装、可自由转动的风向标，其连杆带动一个平台旋转，平台上装有硫化氢检测仪、警报器、光伏供电系统和单片机。一块排成箭头形状的 LED 指示板固定在这个旋转平台上，于是箭头永远指向背风一侧——也就是安全的逃生方向——完全不需要计算。"),
              ("The signal chain is simple on purpose: detector → sensor → A/D converter → MCU → relay → LED arrow and alarm. When the sampled concentration exceeds the preset human-safety threshold, the MCU fires the siren and lights the arrow, so a worker hears the alarm and sees where to run in the same instant. Solar power suits open sites with no mains electricity.",
               "信号链刻意做得简单：检测仪 → 传感器 → A/D 转换 → 单片机 → 继电器 → LED 箭头与报警。采样浓度一旦超过预设的人体安全阈值，单片机立即触发警报并点亮箭头，工人在同一瞬间听到警报、看到逃生方向。光伏供电适合没有市电的空旷井场。")),
        gallery([(IMG + "p6_patent_wind_fig1_front_view.png", "Front view: stakes, height-adjustable post, wind vane, detector, siren, solar panel and the LED arrow board.", "正视图：地钉、可调高度立柱、风向标、检测仪、警报器、光伏板与 LED 箭头板。"),
                 (IMG + "p6_patent_wind_fig4_circuit_block_diagram.png", "The sensing and alarm chain.", "传感与报警链路。")], cols=2))
    body += contributions([
        ("Concept and mechanism", "方案与机构", "Three-axis gantry kinematics (rotation, lead-screw extension, pitch), tripod and winch; vane-coupled rotating platform.", "三轴巡检机构运动学（旋转、丝杠伸缩、俯仰）、三脚架与绞盘；风向标联动的旋转平台。"),
        ("Vision and embedded", "视觉与嵌入式", "Image acquisition, distortion correction and enhancement for the monitoring camera; face-region lock and PPE / smoking recognition on the control box.", "监控相机的图像采集、畸变校正与增强；控制盒上的面部区域锁定与安全帽 / 吸烟识别。"),
        ("Sensing chain", "传感链路", "H₂S threshold logic, MCU and relay, solar power sizing for unpowered sites.", "硫化氢阈值逻辑、单片机与继电器、无电井场的光伏供电选型。"),
        ("IP", "知识产权", "Drafted both utility-model patents as first inventor; both granted in 2024.", "作为第一发明人撰写两项实用新型专利；均于 2024 年授权。"),
    ])
    body += gallery([(IMG + "p6_patent_wellhead_page1.jpg", "CN 221768175 U — wellhead working-face monitoring device based on machine vision.", "CN 221768175 U —— 基于机器视觉的井口工作面监控装置。"),
                     (IMG + "p6_patent_wind_warning_page1.png", "CN 221927274 U — well-site wind-direction early-warning device.", "CN 221927274 U —— 井场风向预警装置。")], cols=2)
    s += section("beacon", "Device 2: an arrow that always points to safety", "装置二：永远指向安全的箭头", body)
    page("industrial-monitoring", pr['title'][0], pr['title'][1],
         "Two granted utility patents (first inventor): a three-axis machine-vision gantry that flags missing hard hats and smoking at wellheads, and a solar-powered H₂S beacon whose LED arrow follows the wind to show the escape route.",
         hero, hero_media, s)


# =====================================================================
# 7. HRI30 / Snap
# =====================================================================
def hri30():
    pr = PROJECTS[6]
    hero = project_hero(pr['kind'], *pr['title'], *pr['q'], [
        ("Role", "角色", "Built the two-stream system end to end: preprocessing, both models, training, batched inference and fusion", "端到端搭建双流系统：预处理、两个模型、训练、批量推理与融合"),
        ("Period", "时间", "May – August 2026, London", "2026 年 5 月 – 8 月，伦敦"),
        ("Dataset", "数据集", "HRI30: 30 industrial human–robot interaction actions, AVI clips with CSV labels", "HRI30：30 类工业人机交互动作，AVI 片段与 CSV 标签"),
        ("Stack", "技术栈", "PyTorch, torchvision r3d_18 (Kinetics-400), YOLOv8-Pose, custom ST-GCN, OpenCV, NumPy", "PyTorch、torchvision r3d_18（Kinetics-400）、YOLOv8-Pose、自实现 ST-GCN、OpenCV、NumPy"),
    ])
    hero_media = figure(IMG + "hri30-dataset.jpg", "Frames from an HRI30 clip with the model’s attention overlaid: the network looks at the worker’s arms and the tool, which is where the action lives.",
                        "HRI30 片段的帧与模型注意力叠加：网络关注工人的手臂和工具——动作就发生在那里。", wide=True)
    s = ''
    s += section("why", "Why two streams", "为什么是双流", prose(
        ("Human action recognition is what lets a collaborative robot understand what a worker is doing and stay out of their way. In a factory the video is messy: cluttered backgrounds, motion blur, subtle hand movements that look alike. A single modality is fragile. RGB clips carry appearance and tool context but are easily distracted by the background; skeletons carry the structure of the motion and ignore the background, but are sparse and lose the tool. Fusing the two gives a classifier that can lean on whichever cue is reliable for a given action.",
         "人体动作识别让协作机器人理解工人在做什么、并避开他们。工厂里的视频很“脏”：背景杂乱、运动模糊、细微的手部动作彼此相似。单一模态很脆弱：RGB 片段携带外观与工具信息，却容易被背景干扰；骨架携带动作的结构并忽略背景，却稀疏且丢失了工具。把两者融合，分类器就能在不同动作上依赖更可靠的那一路线索。"),
        ("HRI30 is an action-recognition dataset for industrial human–robot interaction with 30 action classes. I built the complete two-stream pipeline on it during my internship at Snap, from raw AVI files to a submission file.",
         "HRI30 是一个面向工业人机交互的动作识别数据集，包含 30 类动作。我在 Snap 实习期间在它上面搭建了完整的双流流水线，从原始 AVI 文件到最终提交文件。")))
    body = diagram_fig("hri30", "The architecture: a 3D CNN on sampled RGB clips and an ST-GCN on YOLOv8-Pose skeletons, fused late by weighted probabilities.",
                       "架构：3D CNN 处理采样后的 RGB 片段，ST-GCN 处理 YOLOv8-Pose 骨架，加权概率后期融合。")
    body += steps([
        ("Prepare RGB clips", "准备 RGB 片段", "Each AVI is decoded, converted BGR → RGB, resized to 112×112 and uniformly sampled to 16 frames with np.linspace, then stored as a (C, T, H, W) array so clips of different lengths become one tensor shape.",
         "每个 AVI 解码后转换 BGR → RGB，缩放到 112×112，用 np.linspace 均匀采样 16 帧，存成 (C, T, H, W) 数组，让不同长度的片段变成统一的张量形状。"),
        ("Extract skeletons", "提取骨架", "YOLOv8-Pose runs every second frame; the person with the largest box is taken as the main actor and their 17 COCO keypoints kept. Sequences of arbitrary length are linearly interpolated to 64 steps and stored as (2, 64, 17): x/y, time, joints.",
         "YOLOv8-Pose 每隔一帧运行一次；取框最大的人作为主要行为人，保留其 17 个 COCO 关键点。任意长度的序列线性插值到 64 步，存成 (2, 64, 17)：x/y、时间、关节。"),
        ("Datasets and label map", "数据集与标签映射", "Two Dataset classes align the label CSV with the processed .npy files, keep only clips that were successfully preprocessed, and build a label → index map that is saved with each checkpoint so inference can restore class order.",
         "两个 Dataset 类把标签 CSV 与处理好的 .npy 对齐，只保留成功预处理的片段，并构建“标签 → 索引”映射，随检查点一起保存，推理时据此还原类别顺序。"),
        ("RGB model", "RGB 模型", "torchvision’s r3d_18 with Kinetics-400 weights and a new fully connected head; cross-entropy, Adam at 1e-4, batch 8, 30 epochs, best validation checkpoint kept.",
         "torchvision 的 r3d_18 加载 Kinetics-400 权重并替换全连接头；交叉熵损失，Adam 1e-4，batch 8，30 轮，保留验证集最优检查点。"),
        ("Skeleton model", "骨架模型", "An ST-GCN implemented from scratch: a normalised COCO-17 adjacency (D^−1/2 A D^−1/2 with self-loops), six blocks of graph convolution + 9×1 temporal convolution + residual (64→64→128→128→256→256, two temporal stride-2 downsamplings), global pooling and a linear classifier. Adam 1e-3, batch 32, 40 epochs.",
         "从零实现的 ST-GCN：归一化的 COCO-17 邻接矩阵（带自环的 D^−1/2 A D^−1/2），六个“图卷积 + 9×1 时间卷积 + 残差”模块（64→64→128→128→256→256，两次时间步长 2 下采样），全局池化与线性分类器。Adam 1e-3，batch 32，40 轮。"),
        ("Inference and fusion", "推理与融合", "Both branches run batched inference on the test set and write per-video softmax probabilities to .npz; a fusion script aligns them by video id and label map, combines them as α·p_skeleton + (1−α)·p_rgb with α = 0.6, and writes test_set_labels.csv.",
         "两个分支在测试集上批量推理，把每个视频的 softmax 概率写入 .npz；融合脚本按视频 id 与标签映射对齐，按 α·p_skeleton + (1−α)·p_rgb（α = 0.6）合并后写出 test_set_labels.csv。"),
    ])
    s += section("system", "The pipeline", "流水线", body, cls="alt")

    body = prose(("The two branches behaved exactly as their inputs suggest. The RGB 3D CNN converged fast and reached near-100% training accuracy—strong appearance features, with the usual risk of over-fitting to backgrounds. The skeleton ST-GCN improved slowly and plateaued around 50–60%: motion alone is a harder signal, but it is complementary, and that is what fusion is for. The fused system scored 71.15% on the test set. Once the labelled test set was released and the skeleton weight was re-tuned, the credibility of the RGB branch increased and the final accuracy improved markedly; the likely reason is that the skeleton model was too simple to carry its share.",
                  "两个分支的表现与它们的输入特性完全一致。RGB 3D CNN 收敛很快，训练准确率接近 100%——外观特征强，但也带着对背景过拟合的常见风险。骨架 ST-GCN 提升缓慢，稳定在 50–60% 左右：单靠运动是更难的信号，但它与 RGB 互补，这正是融合的意义。融合系统在测试集上得到 71.15%。带标签的测试集公布后重新调整骨架权重，RGB 分支的可信度提高，最终准确率显著改善；可能的原因是骨架模型过于简单，难以承担它那一份。"),
                 ("What I would do next: a deeper skeleton model (more blocks, adaptive adjacency or a transformer over joints), a proper study of the train/validation ratio, and tests under harsher backgrounds and lighting—the conditions a real production line has and a benchmark does not.",
                  "下一步我会做：更深的骨架模型（更多模块、自适应邻接或关节上的 Transformer）、对训练/验证比例的系统研究，以及在更恶劣的背景和光照下测试——这是真实产线有、而基准数据集没有的条件。"))
    body += stats([("30", "action classes in HRI30", "类 HRI30 动作"),
                   ("16 × 112²", "frames per RGB clip", "每个 RGB 片段的帧数与分辨率"),
                   ("17 × 64", "joints × time steps per skeleton sequence", "每条骨架序列的关节数 × 时间步"),
                   ("71.15%", "test-set accuracy of the fused system", "融合系统的测试集准确率")])
    body += contributions([
        ("Preprocessing", "预处理", "AVI decoding, frame sampling, YOLOv8-Pose extraction, temporal interpolation, .npy caching.", "AVI 解码、帧采样、YOLOv8-Pose 提取、时间插值、.npy 缓存。"),
        ("Models", "模型", "3D ResNet-18 fine-tuning; ST-GCN implemented from the adjacency up.", "3D ResNet-18 微调；从邻接矩阵开始实现 ST-GCN。"),
        ("Training and inference", "训练与推理", "Symmetric training loops with checkpoint and label-map saving; batched inference; fusion and submission tooling; documented, reproducible project layout.", "对称的训练循环与检查点/标签映射保存；批量推理；融合与提交工具；有文档、可复现的项目结构。"),
    ])
    body += figure(IMG + "hri30-poster.jpg", "The project poster: motivation, the two branches, late fusion with α = 0.6, training curves and conclusions.", "项目海报：动机、两个分支、α = 0.6 的后期融合、训练曲线与结论。", wide=True)
    body += links([(CV + "HRI30_Poster.pdf", "Poster (PDF)", "海报（PDF）"),
                   ("https://doi.org/10.1109/ICRA46639.2022.9811871", "HRI30 dataset paper (ICRA 2022)", "HRI30 数据集论文（ICRA 2022）")])
    s += section("results", "What the two streams taught me", "双流带来的结论", body)
    page("hri30", pr['title'][0], pr['title'][1],
         "A dual-stream action-recognition system on HRI30: a Kinetics-pretrained 3D ResNet-18 on RGB clips and an ST-GCN on YOLOv8-Pose skeletons with weighted late fusion.",
         hero, hero_media, s)


if __name__ == '__main__':
    vtla(); umi(); tiago(); thread(); gfrp(); monitoring(); hri30()
