# -*- coding: utf-8 -*-
"""Inline bilingual SVG diagrams. Each text node is emitted twice (class en / class zh),
so the page-level language toggle also switches the diagram labels."""
import html

FONT = "'IBM Plex Sans','Noto Sans SC','PingFang SC','Microsoft YaHei',system-ui,sans-serif"
C = dict(ink="#16222E", muted="#6C7886", line="#8A96A3", teal="#1C9E8A", teal_bg="#E3F3EF", mag="#DE6A92", mag_bg="#FBE9EF",
         navy="#0D1B2A", navy_bg="#E6EAEF", amber="#C98A1E", amber_bg="#FBF1DC", paper="#FFFFFF", grey_bg="#F0F2F1")


class D:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.parts = []

    def text(self, x, y, en, zh, size=13, weight=400, fill=C['ink'], anchor='middle', lh=1.3, italic=False):
        """en/zh may be lists of lines."""
        for cls, lines in (('en', en), ('zh', zh)):
            if isinstance(lines, str):
                lines = [lines]
            n = len(lines)
            y0 = y - (n - 1) * size * lh / 2
            style = f"font-family:{FONT};font-size:{size}px;font-weight:{weight};fill:{fill}" + (";font-style:italic" if italic else "")
            t = [f'<text class="{cls}" x="{x}" y="{y0:.1f}" text-anchor="{anchor}" dominant-baseline="middle" style="{style}">']
            for i, ln in enumerate(lines):
                dy = 0 if i == 0 else size * lh
                t.append(f'<tspan x="{x}" dy="{dy:.1f}">{html.escape(ln)}</tspan>')
            t.append('</text>')
            self.parts.append(''.join(t))

    def box(self, x, y, w, h, en, zh, sub_en=None, sub_zh=None, fill=C['paper'], stroke=C['line'], size=13, r=6, bold=600, sub_size=11, dash=False):
        d = ' stroke-dasharray="5 4"' if dash else ''
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"{d}/>')
        cx, cy = x + w / 2, y + h / 2
        if sub_en:
            n1 = len(en) if isinstance(en, list) else 1
            n2 = len(sub_en) if isinstance(sub_en, list) else 1
            total = n1 * size * 1.3 + n2 * sub_size * 1.3 + 3
            ty = cy - total / 2 + n1 * size * 1.3 / 2
            self.text(cx, ty, en, zh, size=size, weight=bold)
            self.text(cx, ty + n1 * size * 1.3 / 2 + 3 + n2 * sub_size * 1.3 / 2, sub_en, sub_zh, size=sub_size, fill=C['muted'])
        else:
            self.text(cx, cy, en, zh, size=size, weight=bold)

    def group(self, x, y, w, h, en, zh, fill=C['grey_bg'], stroke='none', size=12, color=C['muted']):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}"/>')
        self.text(x + 12, y + 16, en, zh, size=size, weight=600, fill=color, anchor='start')

    def arrow(self, x1, y1, x2, y2, color=C['line'], dash=False, width=1.4):
        d = ' stroke-dasharray="5 4"' if dash else ''
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" marker-end="url(#ah)"{d}/>')

    def path(self, dpath, color=C['line'], dash=False, width=1.4, arrow=True):
        d = ' stroke-dasharray="5 4"' if dash else ''
        m = ' marker-end="url(#ah)"' if arrow else ''
        self.parts.append(f'<path d="{dpath}" fill="none" stroke="{color}" stroke-width="{width}"{m}{d}/>')

    def label(self, x, y, en, zh, size=11, fill=C['muted'], anchor='middle', italic=False):
        self.text(x, y, en, zh, size=size, fill=fill, anchor=anchor, italic=italic)

    def svg(self, title_en, title_zh):
        return (f'<svg class="diagram" viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{html.escape(title_en)}" xmlns="http://www.w3.org/2000/svg">'
                f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{C["line"]}"/></marker></defs>'
                f'<rect width="{self.w}" height="{self.h}" fill="#fff" rx="8"/>' + ''.join(self.parts) + '</svg>')


def vtla_architecture():
    d = D(1100, 520)
    # Pipeline A (force) top-left
    d.group(20, 20, 520, 150, "Pipeline A · self-collected force data (trains the load estimator only)", "流水线 A · 自采力数据（只训练力估计器）", fill=C['teal_bg'], color=C['teal'])
    d.box(36, 52, 150, 100, ["200 fabrics", "12,178 presses"], ["200 种织物", "12,178 次按压"], ["GelSight Mini on Franka,", "ATI Nano17 under the fabric"], ["Franka 上的 GelSight Mini，", "织物下方放置 ATI Nano17"])
    d.arrow(186, 102, 214, 102)
    d.box(216, 52, 150, 100, ["99,797 frames", "+ force labels"], ["99,797 帧", "+ 力标签"], ["40 ms sync correction,", "22 N trust cut-off"], ["40 ms 同步校正，", "22 N 可信上限"])
    d.arrow(366, 102, 394, 102)
    d.box(396, 52, 130, 100, ["ResNet-18", "load estimator"], ["ResNet-18", "力估计器"], ["MAE 0.33 N on", "unseen fabrics"], ["未见织物", "MAE 0.33 N"], fill='#fff', stroke=C['teal'])
    # Pipeline B (VLM) bottom-left
    d.group(20, 190, 520, 150, "Pipeline B · released MLLM-Fabric data (trains and evaluates the VLM only)", "流水线 B · 公开 MLLM-Fabric 数据（只训练/评测 VLM）", fill=C['mag_bg'], color=C['mag'])
    d.box(36, 222, 150, 100, ["3,937 train", "400 test prompts"], ["3,937 训练", "400 测试样本"], ["byte-verified prompt", "generator (8,734 / 8,734)"], ["逐字节校验的提示生成器", "（8,734 / 8,734）"])
    d.arrow(186, 272, 214, 272)
    d.box(216, 222, 150, 100, ["+ 4,000 adjacent-level", "pairs, 0 new labels"], ["+ 4,000 组相邻等级对", "零新增标注"], ["fabric-disjoint split,", "per-cell look-up ceiling"], ["织物不相交划分，", "逐单元查表上限"])
    d.arrow(366, 272, 394, 272)
    d.box(396, 222, 130, 100, ["Qwen2.5-VL-7B", "+ QLoRA r=32"], ["Qwen2.5-VL-7B", "+ QLoRA r=32"], ["0.985 official /", "0.865 unseen fabrics"], ["官方协议 0.985 /", "未见织物 0.865"], fill='#fff', stroke=C['mag'])
    d.label(280, 180, "no data cross this line before deployment", "部署之前两条流水线的数据互不交叉", italic=True)
    # Deployment chain right
    d.group(560, 20, 520, 480, "Deployment on the Franka arm · the two pipelines meet here", "Franka 真机部署 · 两条流水线在这里汇合", fill=C['navy_bg'], color=C['navy'])
    steps = [
        (["Press each hanging garment", "with the GelSight finger"], ["GelSight 指尖依次按压", "悬挂的每件衣物"], ["taught once by hand, replayed with a 20 ms hard stop", "示教一次后回放，20 ms 硬停保护"]),
        (["Estimate force per frame,", "select 4 frames at 0 / 13.5 / 16.8 / 19.9 N"], ["逐帧估计接触力，", "在 0 / 13.5 / 16.8 / 19.9 N 处选帧"], ["six selection gates; no force sensor in the loop", "六道筛选门；回路中没有力传感器"]),
        (["Compose the prompt:", "RGB + 4 tactile frames per fabric"], ["组合提示：每件织物", "RGB + 4 帧触觉图像"], ["same byte-verified generator as Pipeline B", "与流水线 B 相同的逐字节校验生成器"]),
        (["VLM answers 24 pairwise questions", "(6 pairs × 4 properties)"], ["VLM 回答 24 组成对比较", "（6 对 × 4 种属性）"], ["softness · thickness · elasticity · texture, both orders", "柔软度·厚度·弹性·纹理，正反两序"]),
        (["Rank 4 garments, recommend one", "with reliability warnings"], ["对 4 件衣物排序并给出推荐", "附带可靠性提示"], ["“suitable for summer” → F4", "“适合夏天穿” → F4"]),
        (["Grasp a single fabric layer", "and place it in the basket"], ["夹住单层织物", "放入篮筐"], ["same end-effector, no tool change", "同一末端执行器，无需换工具"]),
    ]
    y = 50
    for i, (e, z, (se, sz)) in enumerate(steps):
        d.box(580, y, 480, 60, e, z, [se], [sz], size=13, sub_size=11, fill='#fff', stroke=C['navy'] if i in (1, 3) else C['line'])
        if i < len(steps) - 1:
            d.arrow(820, y + 60, 820, y + 72)
        y += 72
    # cross links
    d.path("M526,102 C600,102 540,160 580,160", color=C['teal'], dash=True)
    d.path("M526,272 C600,272 540,304 580,304", color=C['mag'], dash=True)
    d.label(545, 150, "F̂", "F̂", size=12, fill=C['teal'])
    d.label(556, 318, "adapter", "适配器", size=11, fill=C['mag'])
    return d.svg("VTLA system architecture", "VTLA 系统架构")


def umi_pi05():
    d = D(1100, 430)
    d.group(20, 20, 330, 390, "Hand-held Tactile UMI · data collection", "手持 Tactile UMI · 数据采集", fill=C['teal_bg'], color=C['teal'])
    sensors = [("Wrist RGB camera", "手腕 RGB 相机", "fisheye, 30 fps", "鱼眼，30 fps"),
               ("2 × GelSight fingertips", "2 × GelSight 指尖", "custom GelSight + GelSight Mini", "自制 GelSight + GelSight Mini"),
               ("Meta Quest tracking", "Meta Quest 位姿追踪", "6-DoF controller pose", "6 自由度手柄位姿"),
               ("Gripper width", "夹爪开度", "ArUco + 5-point lookup", "ArUco + 五点查表")]
    y = 48
    for e, z, se, sz in sensors:
        d.box(36, y, 150, 60, e, z, [se], [sz], size=12, sub_size=9.5)
        d.arrow(186, y + 30, 206, y + 30)
        y += 70
    d.box(208, 60, 128, 230, ["Calibrate", "and align"], ["标定与对齐"], ["hand–eye (40 pairs)", "Quest↔camera −56.7 ms", "tactile↔RGB +25 ms", "audit every episode"], ["手眼标定（40 组）", "Quest↔相机 −56.7 ms", "触觉↔RGB +25 ms", "逐条示教审计"], fill='#fff', stroke=C['teal'], sub_size=9.5)
    d.box(36, 328, 300, 64, ["Clean dataset: 222 demonstrations, 135,952 frames"], ["干净数据集：222 条示教，135,952 帧"], ["camera-relative 7D actions: xyz · rotation · gripper"], ["相机坐标系 7 维动作：位置 · 姿态 · 夹爪"], size=12, sub_size=10)
    d.arrow(271, 290, 271, 326)
    # middle: pi0.5
    d.arrow(350, 360, 388, 360)
    d.group(390, 20, 360, 390, "π0.5 vision-language-action policy · my branch", "π0.5 视觉-语言-动作策略 · 我负责的分支", fill=C['mag_bg'], color=C['mag'])
    d.box(406, 50, 328, 70, ["Convert to LeRobot format"], ["转换为 LeRobot 数据格式"], ["images, state, action chunks, language prompt"], ["图像、状态、动作块、语言指令"], size=12, sub_size=10)
    d.arrow(570, 120, 570, 136)
    d.box(406, 138, 328, 120, ["Fine-tune π0.5 (openpi)"], ["微调 π0.5（openpi）"], ["PaliGemma VLM backbone + action expert", "flow-matching action chunks, 50 steps", "LoRA on a single GPU, task prompt in natural language"], ["PaliGemma VLM 骨干 + 动作专家", "流匹配生成动作块（50 步）", "单卡 LoRA，自然语言任务指令"], fill='#fff', stroke=C['mag'])
    d.arrow(570, 258, 570, 274)
    d.box(406, 276, 328, 70, ["Inference server → Franka FR3"], ["推理服务器 → Franka FR3"], ["wrist RGB + state → 7D action chunk → IK → arm"], ["手腕 RGB + 状态 → 7 维动作块 → 逆运动学 → 机械臂"], size=12, sub_size=10)
    d.box(406, 360, 328, 40, ["Rollouts scored live: success counter on screen"], ["实机回放实时计数成功率"], size=11, bold=400, fill=C['grey_bg'], stroke='none')
    # right: comparison branch
    d.arrow(750, 200, 788, 200)
    d.group(790, 20, 290, 390, "Reference branch (lab mate)", "对照分支（实验室同学）", fill=C['grey_bg'])
    d.box(806, 60, 258, 90, ["UniForce tactile encoder", "+ Diffusion Policy"], ["UniForce 触觉编码器", "+ Diffusion Policy"], ["frozen contact tokens from 6-frame", "tactile histories"], ["6 帧触觉历史 → 冻结的接触 token"], size=12, sub_size=10)
    d.box(806, 170, 258, 110, ["Same demonstrations,", "same robot, same task"], ["同一批示教、同一台机器人、", "同一任务"], ["vision-only DP 10/34 vs tactile DP 14/34", "(Fisher p = 0.447, not significant)"], ["纯视觉 DP 10/34 vs 触觉 DP 14/34", "（Fisher p = 0.447，未达显著）"], size=12, sub_size=10)
    d.box(806, 300, 258, 90, ["What the comparison taught us"], ["这次对比的收获"], ["a VLA backbone and a diffusion policy can be", "evaluated on one calibrated corpus"], ["VLA 骨干与扩散策略可以在同一套", "标定过的数据上公平比较"], size=12, sub_size=10, bold=600)
    return d.svg("Tactile UMI to π0.5 pipeline", "Tactile UMI 到 π0.5 的流程")


def hri30_arch():
    d = D(1100, 400)
    d.box(20, 150, 150, 100, ["HRI30 video", ".avi clips"], ["HRI30 视频", ".avi 片段"], ["30 industrial actions,", "train / test split"], ["30 类工业动作，", "训练 / 测试划分"])
    # RGB branch
    d.group(200, 20, 650, 160, "RGB appearance stream", "RGB 外观分支", fill=C['teal_bg'], color=C['teal'])
    d.box(216, 60, 180, 100, ["Uniform sampling", "16 frames · 112×112"], ["均匀采样", "16 帧 · 112×112"], ["(C, T, H, W) clips as .npy"], ["保存为 (C,T,H,W) .npy"], size=12, sub_size=10)
    d.arrow(396, 110, 422, 110)
    d.box(424, 60, 220, 100, ["3D ResNet-18 (r3d_18)"], ["3D ResNet-18（r3d_18）"], ["Kinetics-400 pre-trained, new FC head,", "Adam 1e-4, 30 epochs"], ["Kinetics-400 预训练，新分类头，", "Adam 1e-4，30 轮"], size=12, sub_size=10, stroke=C['teal'])
    d.arrow(644, 110, 670, 110)
    d.box(672, 60, 160, 100, ["Softmax p_rgb"], ["Softmax 概率 p_rgb"], ["near 100% train acc,", "strong visual features"], ["训练集接近 100%，", "视觉特征强"], size=12, sub_size=10)
    # skeleton branch
    d.group(200, 220, 650, 160, "Skeleton motion stream", "骨架运动分支", fill=C['mag_bg'], color=C['mag'])
    d.box(216, 260, 180, 100, ["YOLOv8-Pose", "17 keypoints"], ["YOLOv8-Pose", "17 个关键点"], ["largest person per frame,", "interpolated to 64 steps"], ["每帧取最大框的人，", "插值到 64 步 (2,64,17)"], size=12, sub_size=10)
    d.arrow(396, 310, 422, 310)
    d.box(424, 260, 220, 100, ["ST-GCN · 6 blocks"], ["ST-GCN · 6 个模块"], ["64→64→128→128→256→256", "graph conv + 9×1 temporal conv + residual"], ["64→64→128→128→256→256", "图卷积 + 9×1 时间卷积 + 残差"], size=12, sub_size=10, stroke=C['mag'])
    d.arrow(644, 310, 670, 310)
    d.box(672, 260, 160, 100, ["Softmax p_skel"], ["Softmax 概率 p_skel"], ["50–60% acc, sparser", "but complementary cue"], ["50–60% 准确率，更稀疏", "但与 RGB 互补"], size=12, sub_size=10)
    d.arrow(170, 200, 216, 110)
    d.arrow(170, 200, 216, 310)
    # fusion
    d.arrow(832, 110, 878, 190)
    d.arrow(832, 310, 878, 230)
    d.box(880, 150, 200, 110, ["Weighted late fusion"], ["加权后期融合"], ["p = w·p_rgb + (1−w)·p_skel", "aligned by video id + label map", "→ test_set_labels.csv"], ["p = w·p_rgb + (1−w)·p_skel", "按视频 id 与类别映射对齐", "→ test_set_labels.csv"], size=13, sub_size=10, stroke=C['navy'])
    d.label(980, 290, "71.15% on the test set", "测试集准确率 71.15%", size=13, fill=C['navy'])
    return d.svg("Dual-stream action recognition architecture", "双流动作识别架构")


def wellsite_system():
    d = D(1100, 400)
    d.group(20, 20, 520, 360, "Device 1 · machine-vision wellhead monitor (patent ZL 202323487863.X)", "装置一 · 基于机器视觉的井口工作面监控装置（ZL 202323487863.X）", fill=C['teal_bg'], color=C['teal'])
    d.box(36, 56, 150, 90, ["Rotation motor"], ["旋转电机"], ["spins the boom:", "360° sweep"], ["带动摇臂旋转，", "360° 扫描工作面"], size=12)
    d.box(196, 56, 150, 90, ["Extension + lead screw"], ["伸缩电机 + 丝杠"], ["changes the orbit radius", "to cover the area"], ["改变巡检半径，", "覆盖整个作业区"], size=12)
    d.box(356, 56, 150, 90, ["Pitch motor"], ["俯仰电机"], ["tilts the camera toward", "the worker’s face"], ["俯仰相机，", "对准工人面部"], size=12)
    d.arrow(111, 146, 111, 170); d.arrow(271, 146, 271, 170); d.arrow(431, 146, 431, 170)
    d.box(36, 172, 470, 70, ["Camera on a 3-DoF gantry over a foldable tripod"], ["折叠三脚架上的三自由度相机巡检机构"], ["uniform sweep · locks onto the face region · uploads to the control box"], ["匀速环绕巡检 · 快速锁定面部区域 · 图像上传控制盒"], size=13, sub_size=10.5)
    d.arrow(271, 242, 271, 266)
    d.box(36, 268, 230, 90, ["Embedded control box"], ["嵌入式控制盒"], ["image analysis: hard hat above", "the brow? smoking at the mouth?"], ["图像分析：眉上是否有安全帽？", "口部是否在吸烟？"], size=12, stroke=C['teal'])
    d.arrow(266, 313, 290, 313)
    d.box(292, 268, 214, 90, ["Violation alert"], ["违规告警"], ["flagged automatically; the tripod", "winch doubles as a rescue hoist"], ["自动标记违规；三脚架绞盘", "可兼作救援提升"], size=12)
    d.group(560, 20, 520, 360, "Device 2 · wind-direction early-warning beacon (patent ZL 2023 2 3530543.8)", "装置二 · 井场风向预警装置（ZL 2023 2 3530543.8）", fill=C['amber_bg'], color=C['amber'])
    d.box(576, 56, 150, 90, ["H₂S detector"], ["硫化氢检测仪"], ["sensor → A/D → MCU", "human-safety threshold"], ["传感器 → A/D → 单片机", "阈值 = 人体安全限值"], size=12)
    d.box(736, 56, 150, 90, ["Wind vane"], ["风向标"], ["bearing-mounted; its rod", "turns the platform"], ["轴承安装；连杆带动", "整个平台同步转动"], size=12)
    d.box(896, 56, 168, 90, ["Solar power"], ["光伏供电"], ["panel + battery for", "open, unpowered sites"], ["面板 + 电池，", "适配无电空旷井场"], size=12)
    d.arrow(651, 146, 651, 170); d.arrow(811, 146, 811, 170); d.arrow(980, 146, 980, 170)
    d.box(576, 172, 488, 70, ["MCU + relay on the rotating platform"], ["旋转平台上的单片机 + 继电器"], ["height-adjustable post · four ground stakes"], ["可调高度立柱 · 四根地钉固定"], size=13)
    d.arrow(820, 242, 820, 266)
    d.box(576, 268, 230, 90, ["Siren"], ["声光报警"], ["fires when the concentration", "exceeds the limit"], ["浓度超限时", "立即报警"], size=12)
    d.box(834, 268, 230, 90, ["LED arrow always points down-wind"], ["LED 箭头始终指向逆风逃生方向"], ["workers see the escape", "direction at a glance"], ["工人一眼看到", "逃生方向"], size=12, stroke=C['amber'])
    return d.svg("Well-site monitoring and early-warning system", "井场监测预警系统")


def gfrp_funnel():
    d = D(1100, 300)
    xs = [20, 236, 452, 668, 884]
    boxes = [
        (["72 real specimens"], ["72 组真实试件"], ["axial-compression tests;", "5 inputs, 2 outputs"], ["文献中的轴压试验；", "5 个输入，2 个输出"], C['paper'], C['line']),
        (["Genetic augmentation"], ["遗传式数据增广"], ["samples = individuals,", "parameters = chromosomes;", "crossover + mutation"], ["样本为个体、参数为染色体；", "交叉 + 变异 [0.5, 1.5]"], C['teal_bg'], C['teal']),
        (["15,000 virtual samples"], ["15,000 组虚拟样本"], ["kept if SVR/GPR/RBFNN", "fitness MAPE < 20%;", "7 generations"], ["仅保留 SVR/GPR/RBFNN 适应度", "MAPE < 20% 的样本，7 代演化"], C['paper'], C['line']),
        (["Reptile meta-learning"], ["Reptile 元学习"], ["5-layer MLP pre-trained", "across tasks, then", "fine-tuned on real data"], ["5 层 MLP（8-16-32）跨任务预训练，", "再用真实数据微调"], C['mag_bg'], C['mag']),
        (["R² 0.982 / 0.955"], ["R² 0.982 / 0.955"], ["bearing capacity / displacement;", "baselines reach ≤ 0.875"], ["极限承载力 / 极限位移，", "增广基线最高仅 0.875"], C['navy_bg'], C['navy']),
    ]
    for x, (e, z, se, sz, f, s) in zip(xs, boxes):
        d.box(x, 80, 196, 120, e, z, se, sz, size=13, sub_size=10, fill=f, stroke=s)
    for x in xs[:-1]:
        d.arrow(x + 196, 140, x + 214, 140)
    d.label(550, 40, "Small-sample modelling of GFRP-tube concrete columns", "GFRP 管混凝土柱的小样本建模", size=14, fill=C['ink'])
    d.label(550, 250, "The same inputs (section symmetry, area ratio, concrete strength, H/D, D/T) then drive a sensitivity sweep that yields design rules.",
            "随后用同样的输入（截面对称度、面积比、混凝土强度、长径比、径厚比）做灵敏度扫描，得到设计规律。", size=12)
    return d.svg("Small-sample learning pipeline", "小样本学习流程")


def thread_pipeline():
    d = D(1100, 300)
    xs = [20, 200, 380, 560, 740, 920]
    boxes = [
        (["Six-fisheye probe"], ["六目鱼眼探头"], ["2 groups × 3 cameras,", "120° apart, offset 60°;", "LED strip light"], ["两组 × 3 相机，120° 环布，", "错开 60°；LED 条形光源"], C['teal_bg'], C['teal']),
        (["Calibrate + undistort"], ["标定 + 畸变校正"], ["Zhang’s checkerboard,", "sub-pixel corners"], ["张正友棋盘标定，", "亚像素角点"], C['paper'], C['line']),
        (["Denoise + enhance"], ["去噪 + 增强"], ["BM3D / DnCNN,", "MSRCR Retinex"], ["BM3D / DnCNN，", "MSRCR Retinex"], C['paper'], C['line']),
        (["Cylindrical stitching"], ["柱面投影拼接"], ["SIFT + RANSAC on a", "cylinder; Laplacian-", "pyramid blending"], ["柱面模型上的 SIFT + RANSAC，", "拉普拉斯金字塔融合"], C['mag_bg'], C['mag']),
        (["DFMGAN synthesis"], ["DFMGAN 缺陷生成"], ["StyleGAN2 backbone +", "defect-aware blocks;", "few-shot"], ["StyleGAN2 骨干 +", "缺陷感知模块，少样本"], C['paper'], C['line']),
        (["YOLOv8 detection"], ["YOLOv8 检测"], ["mAP 91.6%, recall 84.7%;", "95% of real defects", "found"], ["mAP 91.6%，召回 84.7%；", "真实孔内缺陷检出 95%"], C['navy_bg'], C['navy']),
    ]
    for x, (e, z, se, sz, f, s) in zip(xs, boxes):
        d.box(x, 90, 160, 110, e, z, se, sz, size=12.5, sub_size=9.5, fill=f, stroke=s)
    for x in xs[:-1]:
        d.arrow(x + 160, 145, x + 198, 145)
    d.label(550, 45, "From a dark 100 mm bore to a labelled 360° panorama", "从黑暗的 100 mm 孔内到带标注的 360° 展开图", size=14, fill=C['ink'])
    d.label(550, 245, "Acquisition moved from a stepper slide to a robot-arm carrier with video frame extraction: 27 s → 15 s per 10 cm of thread (−44%).",
            "采集方式从步进滑台改为机械臂携带探头 + 视频抽帧：每 10 cm 螺纹 27 s → 15 s（−44%）。", size=12)
    return d.svg("Internal-thread inspection pipeline", "内螺纹检测流程")


def tiago_pipeline():
    d = D(1100, 300)
    d.group(20, 20, 500, 260, "Perception · staged so the robot never approaches on a false trigger", "感知 · 分阶段触发，避免误判后贸然接近", fill=C['teal_bg'], color=C['teal'])
    d.box(36, 60, 140, 90, ["Speech trigger"], ["语音触发"], ["Faster-Whisper + VAD,", "3 s windows, keywords", "“help”, “tiago”"], ["Faster-Whisper + VAD，", "3 s 窗口，关键词", "“help”“tiago”"], size=12, sub_size=9.5)
    d.arrow(176, 105, 204, 105)
    d.box(206, 60, 150, 90, ["Wave confirmation"], ["挥手确认"], ["MediaPipe pose; wrist above", "shoulder; sustained lateral", "motion over frames"], ["MediaPipe 姿态，手腕高于肩", "多帧持续横向运动"], size=12, sub_size=9.5)
    d.arrow(356, 105, 378, 105)
    d.box(380, 60, 126, 90, ["Locate the patient"], ["定位患者"], ["median RGB-D depth →", "camera → map frame"], ["RGB-D 深度中值 →", "相机系 → 地图系"], size=12, sub_size=9.5)
    d.box(36, 170, 470, 90, ["Stand-off goal: stop 1 m short, facing the patient"], ["停靠目标：距患者 1 m 处停下，正对患者"], ["97.6% gesture accuracy · 185 ms latency · 0.21 m localisation error"], ["手势识别 97.6% · 时延 185 ms · 定位误差 0.21 m"], size=12.5, sub_size=10.5, stroke=C['teal'])
    d.arrow(441, 150, 441, 168)
    d.arrow(520, 215, 558, 215)
    d.group(560, 20, 520, 260, "Navigation · ROS 2 Nav2 in Webots", "导航 · Webots 中的 ROS 2 Nav2", fill=C['navy_bg'], color=C['navy'])
    chain = [("SLAM map", "SLAM 建图"), ("AMCL", "AMCL 定位"), ("Costmap", "代价地图"), ("NavFn", "NavFn 全局"), ("DWB", "DWB 局部"), ("BT recovery", "行为树恢复")]
    x = 576
    for i, (e, z) in enumerate(chain):
        d.box(x, 60, 76, 50, [e], [z], size=11, bold=600)
        if i < len(chain) - 1:
            d.arrow(x + 76, 85, x + 84, 85)
        x += 84
    d.box(576, 130, 488, 60, ["LiDAR + RGB-D → occupancy map → inflated costmap", "→ global plan → local velocity commands"], ["LiDAR + RGB-D → 栅格地图 → 膨胀代价地图", "→ 全局路径 → 局部速度指令"], size=12, bold=400)
    d.box(576, 200, 488, 60, ["92% end-to-end · 94% navigation · 0.12 m final error", "87.5% path efficiency (n = 10 trials)"], ["端到端 92% · 导航 94% · 终点误差 0.12 m", "路径效率 87.5%（10 次试验）"], size=12, bold=600, stroke=C['navy'])
    return d.svg("TIAGo perception and navigation pipeline", "TIAGo 感知与导航流程")


DIAGRAMS = dict(vtla=vtla_architecture, umi=umi_pi05, hri30=hri30_arch, wellsite=wellsite_system, gfrp=gfrp_funnel, thread=thread_pipeline, tiago=tiago_pipeline)

if __name__ == '__main__':
    # quick preview page
    body = ''.join(f'<h2>{k}</h2>{f()}' for k, f in DIAGRAMS.items())
    open('../_diag_preview.html', 'w').write(f'<!doctype html><html data-lang="en"><head><meta charset="utf-8"><link rel="stylesheet" href="assets/css/style.css"><style>svg{{width:100%;max-width:1100px;display:block;margin:1rem auto}}</style></head><body>{body}</body></html>')
    print('ok')
