# -*- coding: utf-8 -*-
from common import *
from projects_meta import PROJECTS, GROUPS


def feature(pr, i):
    flip = ' flip' if i % 2 else ''
    src, poster = pr['media']
    if pr['media_type'] == 'video':
        media = f'<video autoplay muted loop playsinline preload="metadata" poster="{poster}"><source src="{src}" type="video/mp4"></video>'
    else:
        media = f'<img src="{src}" alt="" loading="lazy">'
    contain = ' contain' if pr.get('contain') else ''
    href = f'projects/{pr["slug"]}.html'
    return f'''<article class="feat{flip}">
<a class="feat-media{contain}" href="{href}" aria-hidden="true" tabindex="-1">{media}</a>
<div>
<div class="feat-kind">{t(*pr['kind'])}</div>
<h3><a href="{href}">{t(*pr['title'])}</a></h3>
<p class="feat-q en">{pr['q'][0]}</p><p class="feat-q zh">{pr['q'][1]}</p>
{p(*pr['desc'])}
<div class="feat-stack">{pr['stack']}</div>
<a class="more" href="{href}">{t("Read the project", "查看项目详情")}</a>
</div>
</article>'''


def research():
    out = []
    for key, ge, gz, se, sz in GROUPS:
        items = [pr for pr in PROJECTS if pr['group'] == key]
        out.append(f'<div class="group"><div class="group-h"><h3>{t(ge, gz)}</h3><span>{t(se, sz)}</span></div>')
        for i, pr in enumerate(items):
            out.append(feature(pr, PROJECTS.index(pr)))
        out.append('</div>')
    return ''.join(out)


PUBS = [
    ("PLOS ONE", "2024",
     "Data modeling analysis of GFRP tubular filled concrete column based on small sample deep meta learning method",
     "基于小样本深度元学习方法的 GFRP 管混凝土柱数据建模分析",
     "T. Deng, <b>C. Xue</b> (co-first author), G. Zhang", "https://doi.org/10.1371/journal.pone.0305038", "gfrp-ml"),
    ("PLOS ONE", "2024",
     "Internal thread defect detection system based on multi-vision",
     "基于多视觉的内螺纹缺陷检测系统",
     "X. Dou, <b>C. Xue</b> (co-first author), G. Zhang, Z. Jiang", "https://doi.org/10.1371/journal.pone.0304224", "thread-inspection"),
    ("PLOS ONE", "2024",
     "Study on design optimization of GFRP tubular column composite structure based on machine learning method",
     "基于机器学习方法的 GFRP 管柱复合结构设计优化研究",
     "P. Shu, <b>C. Xue</b> (co-first author), G. Zhang, T. Deng", "https://doi.org/10.1371/journal.pone.0301865", "gfrp-ml"),
    ("Sensors", "2024",
     "Internal thread defect generation algorithm and detection system based on generative adversarial networks and You Only Look Once",
     "基于生成对抗网络与 YOLO 的内螺纹缺陷生成算法与检测系统",
     "Z. Jiang, X. Dou, X. Liu, <b>C. Xue</b>, A. Wang, G. Zhang · Sensors 24(17), 5636", "https://doi.org/10.3390/s24175636", "thread-inspection"),
    ("Proc. SPIE (AASIP 2024)", "2024",
     "Review of image calibration and distortion correction based on internal threads",
     "面向内螺纹的图像标定与畸变校正综述",
     "H. Yuan, X. Dou, <b>C. Xue</b> (corresponding author), et al.", "https://doi.org/10.1117/12.3045519", "thread-inspection"),
    ("Proc. SPIE (RSTIP 2024)", "2024",
     "A review of image stitching algorithms based on internal thread",
     "面向内螺纹的图像拼接算法综述",
     "Z. Xu, <b>C. Xue</b> (corresponding author), X. Dou, et al.", "https://doi.org/10.1117/12.3065383", "thread-inspection"),
    ("PLOS ONE · under review", "2026",
     "Modeling analysis of toughened sandwich glass based on machine learning methods",
     "基于机器学习方法的钢化夹层玻璃建模分析",
     "<b>C. Xue</b>, X. Zhao, H. Yuan, Y. Zhang", None, None),
]

PATENTS = [
    ("First inventor", "第一发明人", "Wellhead working-face monitoring device based on machine vision", "基于机器视觉的井口工作面监控装置", "ZL 202323487863.X · granted 2024", "industrial-monitoring"),
    ("First inventor", "第一发明人", "Well-site wind-direction early-warning system", "风向预警系统", "ZL 2023 2 3530543.8 · granted 2024", "industrial-monitoring"),
    ("Third inventor", "第三发明人", "External-thread inspection device for tubular tools", "管具外螺纹检测装置", "CN 202411050637.1 · 2024", "thread-inspection"),
    ("Third inventor", "第三发明人", "Internal thread defect detection system", "内螺纹缺陷检测系统", "CN 202411066290.X · 2024", "thread-inspection"),
]


def publications():
    out = ['<ul class="pubs">']
    for venue, year, te, tz, auth, doi, slug in PUBS:
        link = f'<a href="{doi}" target="_blank" rel="noopener">{doi.replace("https://", "").replace("http://", "")}</a>' if doi else t("Under review", "审稿中")
        proj = f' · <a href="projects/{slug}.html">{t("Project page", "项目页面")}</a>' if slug else ''
        out.append(f'<li class="pub"><div class="pub-venue">{venue}<br>{year}</div><div><div class="pub-t">{t(te, tz)}</div><div class="pub-a">{auth}</div><div class="pub-l">{link}{proj}</div></div></li>')
    out.append('</ul>')
    out.append(h(3, "Patents", "专利"))
    out.append('<div class="patents">')
    for re_, rz, te, tz, no, slug in PATENTS:
        out.append(f'<div class="patent"><span class="role">{t(re_, rz)}</span><div>{t(te, tz)}</div><div class="no">{no}</div><div class="no"><a href="projects/{slug}.html">{t("Project page", "项目页面")}</a></div></div>')
    out.append('</div>')
    return ''.join(out)


def about():
    left = f'''
{p("I am Chengqi Xue, an MSc Robotics student at King’s College London (2025–2026). My undergraduate degree is in Automation from Yangtze University, where I graduated in the top 7% with a National Scholarship. My research is in embodied intelligence and multimodal robot learning: how vision, touch and language can be combined so that a robot acts well in contact-rich tasks.",
   "我叫薛程琪，伦敦国王学院机器人工程硕士（2025–2026），本科就读于长江大学自动化专业，专业排名前 7%，获国家奖学金。研究方向是具身智能与多模态机器人学习：如何把视觉、触觉和语言结合起来，让机器人在富接触任务中做出可靠的动作。")}
{p("I have the full path from algorithm to real hardware: on a Franka arm I built an end-to-end vision–tactile–language–action system with π0.5 as the VLA backbone, Qwen2.5-VL for reasoning and GelSight for touch, and finished with a real-robot demonstration. Before that, four years as a research assistant taught me to turn industrial problems—unlit thread bores, 72-sample datasets, hazardous well sites—into published, patented systems.",
   "我有从算法到真机落地的完整经验：在 Franka 机械臂上以 π0.5 作为 VLA 骨干，结合 Qwen2.5-VL 和 GelSight 触觉感知，搭建了端到端的视觉-触觉-语言-动作系统，并完成真机演示。此前四年科研助理经历，让我习惯把工业现场的问题——无光的螺纹孔、只有 72 组数据的试验、危险的井场——变成发表的论文、授权的专利和能运行的系统。")}
{p("How I work: break the problem apart first, then let data settle the argument. I can drive a project on my own and I like working across teams; English is a working language for me. What I want next is to put embodied-intelligence algorithms into real product settings.",
   "做事习惯先把问题拆清楚，再用数据验证结论；能独立推进项目，也愿意和不同团队协作；英语可以作为工作语言。接下来希望能在真实的产品场景里把具身智能算法落地。")}
<div class="links"><a class="btn" href="mailto:{EMAIL}">{t("Email me", "给我发邮件")}</a><a class="btn ghost" href="assets/cv/Chengqi_Xue_CV_EN.pdf" target="_blank" rel="noopener">{t("CV (English)", "英文简历")}</a><a class="btn ghost" href="assets/cv/Chengqi_Xue_CV_ZH.pdf" target="_blank" rel="noopener">{t("CV (Chinese)", "中文简历")}</a></div>
'''
    right = f'''
<figure class="portrait fig mt0"><img src="assets/img/portrait.jpg" alt="Chengqi Xue at the Franka workstation in the KCL robotics lab"><figcaption>{t("At the Franka workstation, KCL robotics lab, 2026.", "2026 年，KCL 机器人实验室 Franka 工位。")}</figcaption></figure>
{h(3, "Education", "教育背景")}
<ul class="timeline">
<li><span class="when">2025.09 – 2026.09</span><div class="what">{t("MSc Robotics, King’s College London", "伦敦国王学院 · 机器人工程硕士（MSc Robotics）")}</div><div class="small">{t("Robot dynamics and control, kinematics and motion planning, sensing and perception, machine learning, intelligence and autonomy. Supervised by Prof. Shan Luo.", "机器人动力学与控制、运动学与运动规划、感知与传感、机器学习、智能与自主系统。导师：罗山教授。")}</div></li>
<li><span class="when">2020.09 – 2024.06</span><div class="what">{t("BEng Automation, Yangtze University", "长江大学 · 自动化 · 工学学士")}</div><div class="small">{t("GPA 3.71, top 7%, National Scholarship (top 4%). Automatic control, motion control systems, machine vision, computer control, electronics, C programming.", "GPA 3.71，专业前 7%，国家奖学金（前 4%）。自动控制原理、运动控制系统、机器视觉、计算机控制技术、模拟/数字电子技术、C 语言程序设计。")}</div></li>
</ul>
{h(3, "Skills", "专业技能")}
<ul>
{li("Robotics: ROS 2, SLAM, Navigation2, motion planning; Webots, Gazebo, RViz; GelSight tactile sensing; Franka and TIAGo platforms", "机器人：ROS 2、SLAM、Navigation2、运动规划；Webots、Gazebo、RViz；GelSight 触觉感知；Franka、TIAGo 平台")}
{li("Learning and vision: PyTorch, OpenCV, YOLO, GANs, VLA and multimodal models (π0.5, Qwen2.5-VL), QLoRA fine-tuning, camera calibration and stitching", "学习与视觉：PyTorch、OpenCV、YOLO、GAN、VLA 与多模态模型（π0.5、Qwen2.5-VL）、QLoRA 微调、相机标定与图像拼接")}
{li("Tools: Python, MATLAB, C, Linux, Docker, Git", "工具：Python、MATLAB、C、Linux、Docker、Git")}
</ul>
'''
    awards = f'''
{h(3, "Honours and awards", "荣誉奖项")}
<ul class="awards">
<li><span class="when">2024.09</span>{t("Best Researcher Award, International Research Awards on Sensing Technology", "最佳研究员奖（Best Researcher Award），国际传感技术研究奖")}</li>
<li><span class="when">2023.12</span>{t("National Scholarship (top 4%), Yangtze University", "国家奖学金（前 4%），长江大学")}</li>
<li><span class="when">2023.10</span>{t("Third Prize (provincial), National Undergraduate Electronic Design Contest", "全国大学生电子设计竞赛省级三等奖")}</li>
<li><span class="when">2023.09</span>{t("First Prize (national), College Students AI Technology Competition", "全国大学生 AI 科技竞赛一等奖")}</li>
<li><span class="when">2022.07</span>{t("Second Prize, College Students “Internet+” Innovation and Entrepreneurship Competition", "大学生“互联网+”创新创业大赛二等奖")}</li>
</ul>
<div class="photos">
<figure><img src="assets/img/event-uk-ai-agent.jpg" alt="UK AI Agent Hackathon team photo" loading="lazy" data-zoom><figcaption>{t("UK AI Agent Hackathon, London, 2026.", "UK AI Agent Hackathon（英国 AI 智能体黑客松），伦敦，2026。")}</figcaption></figure>
<figure><img src="assets/img/event-ai-ningbo.jpg" alt="AI Ningbo Challenge Europe promotion event" loading="lazy" data-zoom><figcaption>{t("The 2nd “AI Ningbo” Challenge: Empowering Industries with AI, European-region launch, 2026.", "第二届“AI 宁波”人工智能赋能产业大赛（欧洲赛区）推介会，2026。")}</figcaption></figure>
<figure><img src="assets/img/tiago-poster-day.jpg" alt="Poster day with the TIAGo team" loading="lazy" data-zoom><figcaption>{t("Poster day with the TIAGo group project team, KCL, 2026.", "KCL TIAGo 小组项目海报日合影，2026。")}</figcaption></figure>
</div>
'''
    return f'<div class="about"><div>{left}</div><div>{right}</div></div><hr>{awards}'


def hero():
    return f'''<section class="hero" id="top">
<canvas id="gel" aria-hidden="true"></canvas>
<div class="wrap">
<h1 class="hero-name"><span class="zh">薛程琪</span><span class="en">Chengqi<br>Xue</span><small><span class="en">薛程琪 · MSc Robotics, King’s College London</span><span class="zh">Chengqi Xue · 伦敦国王学院 机器人工程硕士</span></small></h1>
<p class="hero-role en">I build robots that see, touch and reason—and I take them from algorithm to real hardware.</p>
<p class="hero-role zh">让机器人会看、会摸、会推理，并把算法真正落到真机上。</p>
<ul class="hero-tags">
<li>{t("Embodied intelligence", "具身智能")}</li><li>{t("Vision–language–action models", "视觉-语言-动作模型")}</li><li>{t("Tactile sensing", "触觉感知")}</li><li>{t("Robot manipulation", "机器人操作")}</li>
</ul>
<div class="hero-cta"><a class="btn" href="#research">{t("See the research", "查看研究项目")}</a><a class="btn ghost" href="#about">{t("About me", "关于我")}</a></div>
</div>
<div class="hero-hint">{t("The dots are a tactile marker field—move the pointer to press it.", "背景是触觉传感器的标记点阵，移动鼠标即可“按压”。")}</div>
</section>
'''


def thesis():
    return f'''<div class="thesis">
<div>
<h2>{t("From a tactile image to a confident grasp, every step should be measurable.", "从一张触觉图像到一次可靠的抓取，每一步都应当可测量。")}</h2>
{p("My work sits where perception meets action. I pair vision-based tactile sensors with large multimodal models so a robot can judge what it cannot see, and I care as much about the evaluation protocol, the calibration ledger and the deployment path as about the headline number.",
   "我的工作处在感知与动作的交界处：把视觉触觉传感器与多模态大模型结合，让机器人判断那些看不见的属性；同时我同样在意评测协议、标定记录和部署路径，而不只是一个好看的指标。")}
</div>
<div class="facts">
<div><div class="fact-v">4</div><div class="fact-l">{t("SCI Q1 journal papers (3 as co-first author)", "SCI Q1 期刊论文（3 篇共同一作）")}</div></div>
<div><div class="fact-v">4</div><div class="fact-l">{t("patents (2 as first inventor)", "项专利（2 项第一发明人）")}</div></div>
<div><div class="fact-v">2</div><div class="fact-l">{t("real-robot VLA deployments on Franka arms", "次 Franka 机械臂真机 VLA 部署")}</div></div>
<div><div class="fact-v">0.33 N</div><div class="fact-l">{t("force-estimation error from a tactile image alone, on unseen fabrics", "仅凭触觉图像估计接触力的误差（未见织物）")}</div></div>
</div>
</div>'''


def build():
    body = head("Chengqi Xue — Robotics and embodied AI", "薛程琪 — 机器人与具身智能",
                "Chengqi Xue, MSc Robotics at King’s College London. Embodied intelligence, vision–tactile–language–action learning, real-robot deployment.",
                root="", page_class="dark-top home")
    body += header(root="", active="")
    body += hero()
    body += section("thesis", "", "", thesis(), cls="").replace('<div class="sec-head"><h2><span class="en"></span><span class="zh"></span></h2></div>', '')
    body += section("research", "Research", "研究项目", research(),
                    "Seven projects, grouped by where they happened. Each page tells the whole story: the problem, the hardware, the method, the numbers, and what I built with my own hands.",
                    "七个项目，按发生的地点分组。每个项目页面都讲完整的故事：问题、硬件、方法、数据，以及我亲手做的部分。", cls="alt")
    body += section("publications", "Publications and patents", "论文与专利", publications(),
                    "Four SCI Q1 journal papers, two SPIE conference papers, and four patents from the undergraduate research years.",
                    "本科科研阶段发表 4 篇 SCI Q1 期刊论文、2 篇 SPIE 国际会议论文，获得 4 项专利。")
    body += section("about", "About", "关于我", about(), cls="alt")
    body += footer(root="")
    open('../index.html', 'w', encoding='utf-8').write(body)
    print("home ok")


if __name__ == '__main__':
    build()
