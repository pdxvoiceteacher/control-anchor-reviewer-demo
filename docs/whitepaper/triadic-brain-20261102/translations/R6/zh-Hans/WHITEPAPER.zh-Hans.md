# Triadic Brain

## 人类与 AI 协同认知的公开设计

概念与系统设计：Thomas Prislac  
Ultra Verba Lux Mentis  
简体中文书面普通话全篇主文译稿（`zh-Hans`）  
英文源文档版本：2026-11-03.R6  
2026 年 11 月 3 日

**译本说明：**本文件为简体中文书面普通话全篇主文译稿，由机器辅助翻译；范围包括摘要、全部正文、全部 86 条混合类型注册表记录、附录 A 与 B、两处数学代码块及参考文献。它不构成熟练中文人工译审或专业翻译认证；独立语言与技术审查的实际范围和结果由随附的翻译索引记录。详细功能族指南、术语与翻译义项表、概念图，以及研究与工程术语对照仍为英文补充资料，未在本译稿中翻译。英文编辑对照源为[白皮书 R6 英文主文](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/WHITEPAPER.en.md)，文档版本 `2026-11-03.R6`，源文件 SHA-256 为 `f7e5ef46c6ac203e61d6b353f4295af0f3270b01db197c55e941b9a7c9fffe3d`。术语依据为同一提交中的 [R6 英文术语与翻译义项表](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/TERMS.en.md)。译文仅绑定这一确切源版本；后续版本不会自动同步。本文保留原文的未决含义、证据限制和授权边界；不宣称已经获得人工语言、无障碍或运行时认证。

AI 辅助文档。文档审查关注含义、证据与呈现；不构成运行时资格验证或外部背书。

## 阅读路径

建议先阅读[摘要](#S00)、[花园任务](#S02)和[架构](#S03)，再进一步了解[记忆](#S05)、[共享词汇](#S06)、[效率](#S07)、[治理](#S08)、[观测](#S09)、[协作](#S10)、[人类类比](#S11)、[可选扩展](#S12)或[证据与交付](#S13)。

[线性功能族指南（英文补充资料）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md)解释 86 条混合类型的注册表记录，仅在适用时说明功能输入、输出及所有者。[简明索引](#APP-A)便于比较。[英文概念图下载（补充资料）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/PUBLIC_CONCEPTS.json)包含结构化文档，并非可执行模式定义。[英文术语与翻译义项表（补充资料）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/TERMS.en.md)保留重要区别。本译本所依据的是英文设计文档版；该英文源资料包本身不包含译本。

[常用研究与工程术语对照（英文补充资料）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/STANDARDS_RESEARCH_CROSSWALK.en.md)将项目名称与常见检索术语联系起来，包括来源归属、类比推理、理由维护（reason maintenance）、本地优先软件，以及结果使用组件一侧的授权（consumer-side authorization）。它说明哪些重合只是部分重合、等价关系在哪里止步，以及哪些额外职责仍属于项目提案。这些互补机制有助于调查缺口，但不会替代互联设计，也不会重命名其接口。[结构化术语对照（英文补充资料）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/STANDARDS_RESEARCH_CROSSWALK.json)涵盖全部 86 条注册表记录。

[知识水系附录](#APP-B)解释项目的廊道、河流与阶地研究，包括源材料定义的方程，以及其实现和证据的局限。它使用现有注册表，并未增加新组件。

详细证据见 [《Triadic Brain 从字节身份到可修订知识》，技术手稿第 1.2 版（英文）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/papers/triadic-brain-micro-spectrum/2026-11-03-edition-1.2/TRIADIC_BRAIN_MICRO_SPECTRUM.md)。本白皮书保留更广阔的最终目标和全部经协调的职责；该手稿分析一个留存源代码快照中选定的变换与研究衔接。两者都不描述全部当前代码，也不证明已经部署了网络。[第 13 节](#S13)说明两者的证据术语如何对应。

如需图示阅读路径，可查看 [Brain 图谱（英文）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/88d5f44d3d52d93df2b56101bc8328386b2dbc5b/docs/brain-map/README.md)，其中区分了公开演示代码、注明日期的开发报告和提案。它既不是全部 86 条注册表记录的图谱，也不是完整 Brain 已获资格验证的证据。[较早的 R5.1 图集（英文）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/tree/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/whitepaper/triadic-brain-20261102/visuals)仍是一份历史职责快照。其中的所提供既有资料比较叶节点描述的是经过检查的输入输出契约，不是在技术手稿选定的源代码闭包中已经确认的生产调用方。

阅读这些文档不会使任何人自动加入网络，也不授予访问、执行、持久化、资源支出、凭据或联系他人的权限。参与仍须获得相关主机或运营者的授权，并尊重受影响各方的权利。

<a id="S00"></a>

## 摘要

Triadic Brain 正在被设计为帮助人们共同思考、学习和工作，同时对自己的计算机、信息和 AI 辅助保有实质控制。其预期运行载体是用户拥有的节点；该节点能够在本地工作，也能在所有者同意时，与其他独立治理的节点协作。Control Anchor 是该节点的人机界面。产品是相互连接的 Brain 整体：包括任务接入、分析工作、评估、记忆、控制、证据与协作。

实际目标是为劳动者和资源不足的机构提供有用、可检查的帮助。社区应能够选择模型、理解数据去向、设定自身资源限制、保存有权保留的知识，并在不抛弃已有工作的情况下离开某个服务提供方或网络。设备条件较好的参与者可以贡献有边界的算力。其他人可以贡献专业知识、纠正意见、可复用方法、易于理解的解释或有价值的负面结果。参与不应要求交出私密记录，也不应要求接受贡献方的结论。

效率很重要，因为时间、电力、硬件和注意力都有限。所有权与实际自由的价值，并不以胜过每一种集中式服务为前提。即使本地或协作路径开销较大，只要符合条件且成本与取舍透明，人们也完全可以合理地优先选择它。

本文介绍预期的互联系统，以及在其开发过程中持续保留的职责。选定组件在各自声明的快照范围内已有源代码实现和留存的限定范围证据。本版未进行新的产品执行或当前代码审计。本文档并未证明真实安装环境中的认知能力、完整的原生隔离、真实的双节点交换，以及其后的三节点 Wi-Fi 工作流。跨数百万台计算机的全球参与是一种愿景，而非已测得的容量。涌现出集体意识的可能性仍是开放的研究假说；产品价值并不依赖于解决这一问题。

<a id="S01"></a>

## 1 目的与范围

Triadic Brain 以人的目的为起点，而不是以用尽所有可用模型或计算机为要求。图书管理员可能需要整理地方历史馆藏，小型学校可能需要改编教学材料，家庭可能需要比较维修方案。系统应帮助他们利用已有证据、识别不确定性、获得有意义的质疑，并在易于理解的控制下保留有用成果。

这一志向很广：让协同智能支持自主能动性、创造力、学习，以及关怀生态。但实现必须具体。这份输入归谁所有？哪项任务获得了授权？哪台计算机可以处理它？什么内容可以保留？当答案出错、连接中断或权限变化时会发生什么？一个网络如果无法回答这些问题，就不会仅因采用分布式形式而实现所有权目标。

因此，设计保留了几项承诺。每个节点保留本地授权权力。模型与协调器应能通过经过支持和测试的接口更换。资源共享出于自愿。异议和不利证据保持可见。人们需要便于使用的方式来检查、纠正、停止、导出和退出。机构可以采用可追责的本地规则，但不能暗中改写其他参与者的证据或权利。这些是设计与验收义务，而不是声称软件会自动带来社会公平。

本文协调的是功能，而不是将每个历史名称都视为独立产品。功能是一项具有输入、输出、限制及使用组件的职责。名称可以改变，职责仍可延续。附录保留了 86 条混合类型记录，包括系统与部署范围、能力职责、契约、原则、可选配置方案、研究、历史沿革，以及一份历史测试文档。记录类型与成熟度是分开的；这既不是运行时功能的数量，也不是已完成模块的清单。配套概念图使用相同标识符，让译者、开发者和读者不必依赖某个特定英文标签，也能讨论同一职责。

<a id="S02"></a>

## 2 一项任务的完整过程

设想一个社区团体正在制定花园计划。它拥有公共气候数据集、场地草图、有限预算和志愿者笔记。部分笔记包含个人信息，应留在组织者自己的计算机上。团体希望得到易于理解的方案比较和可复用的规划方法。以下描述的是目标体验，不是已部署试点的报告。

**设定目的与边界。**组织者通过 Control Anchor 选择问题、相关证据、受支持的本地模型，以及有限的资源预算。个人笔记保留在本地。公共气候数据可以与获准接入的对等节点共享。是否保留结果，与是否发送任务，是彼此独立的选择。这两种选择都不暗含允许使用笔记进行训练。界面会说明哪些检查得到支持，哪些仍需由人完成。

**接收并保存任务。**Sonya 是接入与适配器边界。它保留任务的身份、来源和声明的上下文，将传入文本视为不可信内容，只路由受支持的工作。AEGIS 应用技术准入与保护规则。UCC 按已接受的控制版本应用受支持的有限程序。权威保管记录保存任务尝试及其实际结果，包括拒绝或不确定状态，而不只是记录成功的答案。

**在委托权限内规划。**用户指定的执行协调者提出有边界的序列：整理证据、计算选定的量、比较替代方案，并获得质疑。有些步骤是确定性的，无需模型。一个模型可以依次承担多个角色，也可以由多个符合条件的独立工作者贡献。事先授权的自主执行可以完成被允许的序列，无需每个小步骤都重新询问。执行协调者不能扩大自身权限，不能自行取得另一个节点的资源，也不能暗中换用更宽松的策略。

**分析与质疑。**Analyst（分析者）提出方案。CoherenceLattice 连接主张、来源、假设及未决问题。Challenge（质疑）角色寻找薄弱之处。Sophia 按其声明的检查与证据，评估固定的候选方案。Synthesis（综合）角色回应发现，但不删除异议。不同角色名称或重复的模型回答，本身并不能证明判断具有独立性。

**仅在有用且获准时使用对等节点。**第二个节点可能接收公共气候数据子集和一项范围严格限定的比较任务。双方所有者都必须允许相关披露和执行。对等节点的资源所有者必须预留真实容量并落实限制。不能仅因另一台计算机可以运行更大的模型，就把组织者的私密笔记传出去。

**呈现可供决策的内容，而非神秘分数。**Atlas 展示方案、支持证据、相反发现及剩余不确定性。如果检索权与当前使用权允许，它可以比较一种符合条件的既有方法。有用的输出可以说明：某个方案更便宜，但依赖于尚未核实的用水假设。组织者可以纠正假设，或要求范围更窄的下一步。数值置信标签不能取代这样的解释。

**在情况改变时重新审视问题。**假设团体发现可用水量更少，或主动将目标从产量最大化改为维护工作最小化。预期的[规划循环 F47](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F47)会创建后继上下文和有边界的计划，而不是改写最初的观测。依据证据形成的判断仍可追溯归属。CoherenceLattice 提出调整后的替代方案；Sophia 审查调整后的候选方案；Atlas 将已知事项和未完成工作延续下去。执行协调者在可归责的恢复或暂缓之前，重新检查相关角色、范围、同意和资源限制。问题连续性意味着保留变化及其来源，而不是禁止获得授权的新目的。

与花园答案无关但有用的模式会进入独立的[新颖性路径 F70](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F70)。可以提名它供日后审查，而不必强塞进答案或自动存储。如果会话重启或模型被替换，[恢复 F62](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F62)应在当前所有者的控制下恢复已提交的上下文和待定效果，同时拒收过时工作者迟到的输出。恢复不能重复可能已经发生但仍不确定的外部效果。这种互联反馈与恢复行为属于设计意图；完整的实际安装循环尚未得到演示验证。

**保留有用的部分。**在取得适当权限后，PMR 可以保留经过检查的规划模式、其假设、关键沿革以及已知失效条件。系统不必永远保存每一份临时草稿。经单独审查的公开衍生版本可以分享方法，同时排除姓名、私密笔记和可识别身份的元数据。其他团体可以对其改编，并在自己的目标情境中进行检查。

**如实处理中断。**如果任务可能已经开始，但回复丢失，系统应核对原始尝试并厘清结果，而不是盲目重发。如果权限被撤销，未来依赖该权限的操作必须重新检查当前授权。此前已披露的信息无法保证被收回。历史记录应区分已经发生的事实与当前允许的行为。

决定性成果是在可接受的总负担下完成有用工作，其中包括审查与纠正。一项未能成立、却避免了高昂错误成本的类比，可能与一条成功建议同样有价值。

<a id="S03"></a>

## 3 架构及其边界

核心分析关系由 CoherenceLattice、Sophia 和 Atlas 构成。CoherenceLattice 构建有证据依据的分析候选；Sophia 评估固定候选；Atlas 让结果、分歧及符合条件的既有资料上下文易于理解。这组三元关系处于更大的系统之内，后者包括接入、程序、保管、控制和本地资源所有权。不应将它理解为三个生物脑区，也不应理解为始终需要三个模型。

| 职责 | 预期贡献 | 边界 |
| --- | --- | --- |
| Sonya | 接收任务、绑定上下文、路由受支持的适配器并采集返回材料 | 传入内容不能给自己授权 |
| Sonya 节点 | 持有参与者的资源、已接受的集成和本地策略 | 参与不会把所有权转交给网络执行协调者 |
| Control Anchor | 让人们配置、检查、选择、停止及恢复受支持的工作 | 可见的设置必须真正传达到作出决定的服务 |
| CoherenceLattice | 为主张提供依据，并保留替代方案、映射及残余问题 | 结构有效不等于语义真实 |
| Sophia | 评估固定候选，保留发现和异议 | 建议性发现不授予执行权或记忆权限 |
| Atlas | 帮助读者理解情境、解释结果并比较符合条件的既有资料 | 展示和检索不授权保留或复用 |
| 执行协调者 | 维持目标并协调有限的委托工作 | 不得自行授予权力或无限复制 |
| UCC 与权威责任所有者 | 提供受支持的建议性评估，同时单独落实技术性运行保护 | 业务发现不是对提示的否决权，也不是外部行动授权 |
| 保管与 TEL | 保存实际生命周期证据及其声明的关系 | 两者都不是访问模型隐藏思维的特权通道 |
| PMR | 治理可选保留及跨任务复用 | 保留、检索、注入和训练是独立选择 |

Sonya 指的是逻辑边界，并不要求一个进程持有所有凭据。实现可以将网关传输、权威保管和下游隔离分开。这些进程边界必须被记录并测试。声称某个下游步骤没有调用提供方，并不能抹去工作流其他位置此前发生的调用。

Control Anchor 应回答五个日常问题：什么正在运行？我的数据去了哪里？使用什么资源？为什么获准？我怎样停止或更改它？文本、图形及结构化视图应描述同一已接受状态。改变选择后，过时预览必须失效。如果仪表盘显示了权限，但绕过它的调用方仍能规避限制，就还不够；执行约束必须位于真正的行动边界。

同一产品有两个连接方向。受支持的 AI 宿主或插件可以向经过身份验证的原生 Brain 提交明确任务；原生 Brain 也可以通过 Sonya 向选定模型或提供方发送获准请求。两个方向都使用同一套本地策略与保管授权体系。宿主集成不会拦截每一条无关的聊天消息。宿主草稿或转述、实际观测到的精确输入，以及原生回复，必须保持可区分。向云端宿主返回数据属于披露，不能描述为完全本地处理。参见 [Sonya F04](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F04)和[互补证据 F61](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F61)。

共享上下文意味着相关任务、证据、假设、版本、权利及未决状态一起经过获准的各阶段，并不意味着每个参与者都收到所有记录。质疑工作者可能需要看到提出的主张和选定证据，但仍无权读取私密背景笔记。必须同时考虑上下文是否充分，以及披露是否限于最低必要范围。

角色不同于担任该角色的模型、服务该模型的运行时、它收到的任务，以及它必须满足的输出契约。模型可替换性要求实际检查受支持的模态、上下文限制、错误、披露行为、许可和访问权。检测到已安装的桌面应用，并不能证明获得了 API 授权。本地模型、远程服务和自主代理都可能成为有用的参与者，但每一个都需要获准接入的接口和限定范围的授权。

欢迎自主参与者提出工作或协作建议。它们的消息首先作为不可信数据进入系统。仅有通信并不授予执行、持久化、复制或访问个人存储空间的权限。在所有者委托的目的、时限及资源限制内，获准接入的代理可以执行有限序列并报告结果。这既保留有意义的自主性，也不会让任何可达机器都开放执行。

<a id="S04"></a>

## 4 从主张走向理解

CoherenceLattice 旨在组织问题、证据与候选答案之间的关系。它应保留替代方案，并揭示所提供材料在哪些地方支持、反驳或未能回应某项主张。这比将流畅语言当作证据更有用。来源可以真实却不相关；准确抄录的数字仍可能在错误的单位或假设下使用。

相干性逆向综合（coherence retrosynthesis）从结果、差异或残余问题出发，向后寻找可能解释它们的候选分支、反向假说和区别。在花园示例中，出乎意料的不佳结果可能促使人们重新审视遮阴、土壤或日程安排的假设。留存的源代码说明包括对已声明或预先编排的替代方案所做的限定工作。依赖导向的回溯重建要问：为了论证或复现某个结果，需要哪些变换和充分支持？多对一变换可能留下数种不同的历史，哈希值也无法恢复缺失的原始内容。通用的自主替代方案发现、完整的逆向推理引擎，以及语义上的实用性，仍是彼此独立的研究与集成问题。参见[技术手稿第 14.2 节（英文）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/papers/triadic-brain-micro-spectrum/2026-11-03-edition-1.2/TRIADIC_BRAIN_MICRO_SPECTRUM.md#142-retrosynthesis-as-dependency-directed-reconstruction)。

在留存实现中普通的已采集模型输出 JOINED 路径上，确定性的依据核验会检查精确摘录和声明的支持关系。精确引用和词汇覆盖率并不能证明语义蕴含。桥接层将未经测量的不确定性赋为保守值 1。如果有效构建到达未经修改的原生 UCM 筛查环节，即使唯一候选项的归一化质量为 1，这一不确定性也会迫使该环节给出拒绝（REFUSE）。CAPTURE_ONLY 绕过此分支，而较底层的 captured API 则采用不同的不确定性契约。这是基于源代码与调用路径、带有条件的推论，不是实测失败率，也不是适用于每个模型回复的规则。答案仍可供检查。参见[技术手稿第 7.1–7.2 节（英文）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/papers/triadic-brain-micro-spectrum/2026-11-03-edition-1.2/TRIADIC_BRAIN_MICRO_SPECTRUM.md#7-native-transformations-from-answer-text-to-a-reviewed-candidate)。

Sophia 的评估绑定实际受审的候选。后续编辑若未经过适当的后继版本检查，不得继承先前评估。

在所检查的路径中，Sophia 根据不含原始载荷的回执（raw-free receipts）重新计算选定的成果关系；它不会独立重读缺失的提供方字节，也不会重新运行业务策略谓词。正确记录的原生拒绝可以得到审计 HOLD（暂缓），而不是导致审计本身被拒绝。Atlas 保留由此产生的隔离与人工决策立场。澄清请求只是要求采取的下一步，并不能证明修复已经执行。

Sophia 的发现应说明检查了什么、哪些证据可用，以及哪些内容仍缺乏支持。设计保留问题完整性、有限的既有资料使用、使用后的影响审查，以及有边界的探索。这些职责有助于防止系统回答一个更方便的替代问题、将既有资料引入超出获准范围的用途，或仅因有能力继续就不断循环。

质疑应有实质内容。如果两个工作者依赖同一个错误来源，它们的一致意见并不是两份独立确认。同一观测的重复副本不能凭空凑足所需的独立支持数量。即使汇总分数看起来有利，相反证据、缺失测量、过时数据及超出领域的情形仍然相关。

Atlas 让这些工作以易于理解的形式呈现。它可以展示原始问题、方案、支持、反对意见、假设及获准的后续行动。其运行职责包括帮助理解既有资料和进行比较。可选的 Atlas432 词典是另一项功能：它是有边界的情境化人文学科参考工具，其含义必须绑定特定来源和版本。它可以提供相互竞争的解释，或拒绝不充分的匹配。它不是对人的分类系统、穷尽性的本体，也不是道德排名。

这一区别在实际使用中很重要。运行层面的 Atlas 可以比较两种先前检查过的花园程序；Atlas432 则可能支持一次可选的解释性讨论，探讨某社区意象的含义。两种使用都不应暗中写入长期记忆，词典关系分数也不应被呈现为经过校准的概率。

<a id="S05"></a>

## 5 保留重要内容的记忆

选择性保留与巩固是设计的基础。有用的系统应把经验转化为可复用方法，而不要求未来每项任务都重放过去的每一次发现。早期概念工作描述了经验如何成为精炼的方法；PMR 研究计划明确提出了受约束的保留、考虑图关系的剪枝、压缩、隔离、撤销及精简表示。当前说明进一步澄清这些职责如何相互配合。

Thomas 的行走示例体现了预期直觉：人不会每迈一步，都有意识地回想学走路时的每一课。对于 Triadic Brain，工程提案是保留有边界的程序或紧凑模式，并附带其范围、假设、关键证据及重新审视的条件。这是在说明程序化，而不是声称复制生物学习。

记忆有多项职责。工作记忆支持当前任务；情景记忆保存选定事件；语义记忆持有符合条件的知识表示；程序性记忆持有可复用方法；前瞻记忆持有未来意图。每一种都需要所有者、目的、适当保留期限及当前使用控制。列出这些角色，并不能证明它们都已在可持久运行的产品中实现。

PMR，即 Provenance Memory Reservoir（溯源记忆库），涉及符合条件的既有资料的可选保留与复用。它不同于强制性的任务保管；后者记录在声明的运行边界内实际发生了什么。为问责而需要的记录，未必符合用于新答案的条件。保留项目可能已经过时、被反驳、受到限制或等待审查。历史执行状态与当前用途价值是独立维度：改变当前权限不会改写原始事件。

巩固应为仍在提出的主张保留足够沿革。如果紧凑程序依赖一个在其他方面评分较低的祖先记录，考虑图关系的剪枝可能需要保留那个祖先。仅保存哈希的记录可以支持日后检查身份，却无法重建缺失内容。精确重放、功能性重放，以及对先前活动提供较弱佐证，需要不同的保留材料，不应混用同一个不加区分的“重放”标签。

预期生命周期包括：必要时保留原件、保留依赖、生成获准的紧凑衍生物、归档、隔离、降级为有限参考，或删除符合删除条件的材料。用户的保留选择、受影响方权利及适用义务约束这些选择。被反驳的记录仍可能作为反面证据有用，而不应悄悄重新变成建议。当上下文变化，或结果与预期冲突时，系统应重新审视相关假设，并要求新的证据依据。

剪枝可以释放存储、RAM 或已排定容量，供其他工作使用。信息不会字面意义上变成算力。巩固也不会自动训练模型权重。检索、程序复用、配置方案修改和模型训练是不同过程，需要不同权限和评估。

### 一份既有资料要经过多个独立决定

在预期复用途径中，[沿革查询 F68](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F68)提供索引和针对特定目的的建议。[检索 F84](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F84)返回符合条件的候选材料，并附溯源信息与允许使用的理由。[记忆处置立场 F85](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F85)可以将提案标为待定、隔离或可供保留的候选；这个标签不会执行写入。[问题连续性 F80](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F80)检查任务现在正在回答哪个问题。[既有资料路由 F81](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F81)限制所选既有资料如何进入任务，而[影响审查 F82](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F82)在使用之后检查其声明的用途。任何存储、披露或当前使用事务，都由实际获得授权的所有者执行，而不是由这些建议执行。[生命周期 F69](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F69)治理之后考虑依赖的保留或撤销操作。[逆向综合候选 F14](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F14)可以进入所提供既有资料的比较过程，但不暗示整条链已经运行。

即使某个实现把多项职责合并到同一进程中，这些职责仍可以保持独立。目前并未全部确定它们与实际使用组件之间的精确衔接。因此，检索结果、审查建议和已完成的记忆事务需要不同记录。

留存的沿革中，一个具体的编解码器和一个纯保留规划器提供了范围较窄的机制。技术手稿还指出一个有限的所提供既有资料比较叶节点，但在其选定的源代码闭包中，没有已经确认的生产调用方。这些发现既不能证明完整的语义巩固生命周期已经成立，也不描述后来的实现工作。经过资格验证、具备持久性且经过身份验证的使用组件，必须将精确保留的字节、当前授权、实际存储效果、后续符合条件的使用，以及可见的影响证据连接起来。考虑依赖的重新审视还需要明确、充分的替代支持集合：若其他充分、可用且获准的支持仍然存在，失去一个来源并不一定推翻某项主张。仅有可用性和许可，并不能使这些支持在科学上充分。基础设计正是在这里成为可测试的端到端能力。

<a id="S06"></a>

## 6 保留差异的共享词汇

本文按当前维护的工程含义使用 GUFT：一种带类型、可扩展的跨领域表示与研究语法。通用数据包可以承载任务的原生证据、单位、不确定性、残差、溯源信息、同意和拒绝。共享格式应让关系可检查，同时保留来源领域的含义。历史缩写展开仍以具体来源为准；本文不把这个名称提升为已经证实的物理统一理论。

Universal Coherence Mapping（通用相干映射，UCM）是该研究计划中的一种投影。投影是附加视图，而不是原生状态的替代。例如，物理测量和文化解释都可以包含不确定性与溯源信息，但它们并不会因此成为同一种证据。不同源版本中的符号或坐标也可能有不同含义。量必须附带单位、估计器版本、变换及限制。技术手稿区分了原生结构性 UCM 代理量、历史基准与审计变换、时间序列量、基于相位的参照来源提案，以及合成波形编解码器。共用符号并不会将这些命名空间连接成一体。归一化质量不是经过校准的正确性概率，默认值零不是观测，而另行命名的 Formula-of-Record 的完整定义方程，在该手稿限定的源材料窗口内仍未恢复出来。

词汇体系之所以有用，部分在于它能明确表示映射不成立。保留的设计包括多个映射、没有充分映射、超出领域的输入，以及所提出的新模式。它还区分缺失的观测、受限的观测，以及在当前语法下不适用的谓词。这些情形需要不同回应。隐私限制不是某现象不存在的证据。不适用的类别不应强迫把某个人或成果归入误导性的分类。

分层参考视图，包括历史上从 432 到 36 到 3 再到 1 的提案，必须在重要之处保留分布、分歧和残差。不能仅因界面容得下一个数字，就把不可通约的轴取平均，合成一个最高总分。提出扩充词汇，应是为了回应反复出现的残差，或已证明缺少的区别；随后还要与更简单的替代方案、留出案例和有意义的原生解释比较。类别更多本身不代表进步。

AHA 是假说与类比工作流。它从有依据的来源结构和一个目标问题开始，说明哪些关系可能迁移、哪些不变量应成立、有哪些差异、尺度或情境如何改变主张，以及什么目标观测会削弱或否定它。例如，队列管理模式可能启发一种志愿者任务安排。这种模式是否帮助人们公平协调，必须在目标情境中检查；结构相似只是一项候选。

受治理的桥接保留参照来源段落、目标假说、拟议插入内容、相反解读和解释。有用的评估会将拟议迁移与常规的原生解决方案、无参照来源的替代方案及相关阴性对照进行比较。看似合理但实际错误的类比尤其有信息价值。在手稿所检查的引擎中，对于已提供的 AHA 案例，会检查声明的关系是否存在、关系类型、方向以及映射后的端点。已声明的单位与尺度变换会被记录；关系映射并不执行语义变换或单位变换。REVIEWABLE 表示可检查，不表示已在目标情境中验证。未提供 AHA 案例时，该路径返回 UNAVAILABLE。在这条路径中，自动发现参照来源、反馈到模型调度、已执行的目标证伪，以及效率收益，都尚未得到确立。在这个已实现的子集之外，更广泛的受治理桥接职责仍被保留。参见[技术手稿第 10 节（英文）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/papers/triadic-brain-micro-spectrum/2026-11-03-edition-1.2/TRIADIC_BRAIN_MICRO_SPECTRUM.md#10-aha-and-explicit-cross-domain-transformations)。

共享语法还支持一条拟议的通信路径：解析一个精确、带版本的引用，检查其依赖和当前使用权，比较原生领域与单位，然后展开例外和残差，或拒绝该映射。共享库的创建、同步、查找和纠正成本都应计入核算。历史词典和复制／残差编解码器提供了较窄的机制；它们不能证明自动语法学习、无损语义迁移或经过协商的跨节点展开已经成立。参见[技术手稿第 14.1 节（英文）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/papers/triadic-brain-micro-spectrum/2026-11-03-edition-1.2/TRIADIC_BRAIN_MICRO_SPECTRUM.md#141-reference-communication-with-residuals)。

Rosetta 保留另一条边界。其观测桥通过本地适配器，把声明的轴映射为带类型的观测、状态、溯源信息，以及可选的几何或波形视图。声明值不自动等于测量值。基底之外的残差与转换残差回答的是不同问题。合成波形或参考频率是一种表达性表示，不是某个人的物理频率，也不是物理能量的证据。这些可选视图必须保留几何、原生含义及来源的权威性之间的区别。

<a id="S07"></a>

## 7 效率与如实核算负担

Triadic Brain 力图在适合复用的地方避免重复劳动，也力图避免把隐藏成本转嫁给审查者、贡献方或更难拒绝的人。正确的问题是：受支持的工作流是否以可接受的总负担产生有用结果，而不是某个孤立计数是否变小。

Total Action Functional（总作用量泛函，TAF）是一项研究目标，涵盖物理、信息，以及治理或相干性负担。其规范表述将归一化项与声明权重分开。物理作用量项需要适当归一化；在没有有意义的物理作用量测度的领域，需要明确说明领域替代量，而不是借用不合适的单位。分数不能凌驾于同意、隐私、拒绝或资源所有者的限制之上。

留存源代码中的限定范围诊断和保留字节说明，范围更窄。保留字节代理量可以解释：在声明的核算规则下，选定表示保留了多少，或有多少被计入成本。它并不测量全部物理工作、人工审查、不确定性或外部化伤害。临时采用的加权运行时分数，不是经过完整测量的规范 TAF。明确区分两者的名称及范围，可以保留有用的测量工具，同时避免夸大它们所能证明的内容。

DeltaSyn 提供具体的压缩与重建机制。在所检查的独立实现谱系中，有边界的来源匹配和复制／残差操作可以重建指定表示，并核算声明成本。字节精确重建意味着所选字节完全原样恢复；规范表示精确重建则针对指定的规范表示。任一标签本身都不能证明语义等价或认知改善。

DSCC 是独立的规范与保证工作线。它的六项帧核算涵盖代码、模型、既有资料同步、溯源、残差和成帧。独立 DeltaSyn 实现有五项核算成分：模型、既有资料同步、载荷、残差和溯源；软件包与证据归档大小另行报告。共有压缩主题，并不会使这些账目可互换，也不会把规定的操作变成已实现的操作。

纯 PMR 规划器考虑声明的隐私、同意、重放要求、关键程度、撤销及启用状态。它可以建议保留原件、保留依赖、将某种表示视为冗余，或寻求审查。建议不会执行存储事务。声明同意，不等于已经验证必须给予许可之人的身份。原生使用组件必须在真正的提交边界检查当前授权。

压缩主张必须将重建所需信息计入成本。带外提供的参照来源不能从核算中消失。预先共享的参照来源需要确切身份和适用的共享假设；随包提供的参照来源，其字节数必须计入。负收益仍是有效观测。更短的描述不等于测得了节能。

性能评估应包括准备、检索、传输、排队、推理、编码、解码、验证、协调、失败和人工纠正。冷态与热态条件不同。资源计数需要定义统计总体。物理能量需要适当仪器和相匹配的边界。质量、有用的弃答、错误自信与无障碍，应和延迟、内存使用一起纳入考量。

### 分别检验复用与实际自主性

拟议的生命周期复用比较固定一组重复任务工作负载、源代码快照、所需输出、硬件与运行时条件、停止规则和观测时域。重新计算组从头推导结果；复用组验证既有资料的身份、支持依据、适用性、时效性和权限，再对其改编，或回退到重新计算。评估之前应声明验收标准和质量可比性的容许差异范围，并在可行时采用盲法裁定。只有在已验收质量和覆盖范围可比的前提下，才能声称实现了等效服务的节省；失败、拒绝、过时、取消和未决任务都必须保留在统计总体中。

对于每一种实测资源单位，拟议的节省量为整个工作负载的重新计算成本，减去整个工作负载的复用成本。在观测时域内，应计入可归因的初始生成、检索、验证、改编、存储、复制、传输、协调、失败、回退工作及后续纠正；每个资源事件只计一次，并纳入转移给对等节点的工作。应说明共享准备工作和持久存储的分摊方式，区分冷启动总量与热缓存结果。实测计算量、能量、流量、存储占用、延迟和人工审查时间必须分别保留。并行计算量不等于经过的延迟时间；token 数、调用次数和保留字节数，都不能证明能耗或正确性。缺失的测量仍标为不可用。这是一个可测量的假说和拟议比较，不是已经完成的研究，也不是已经测得的收益。

实际自主性是一项单独评估的设计目标：参与者是否真的能够退出、选择模型或提供方、保留本地控制，并实行可问责的协作治理？既要记录成功的选择，也要记录障碍和失败。节省不能抵消对最低权利的侵犯，而人们可以合理地选择以更高成本换取更大自主性。去中心化本身既不保证自由，也不保证数值上的改善。参见[技术手稿第 14.3 节（英文）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/papers/triadic-brain-micro-spectrum/2026-11-03-edition-1.2/TRIADIC_BRAIN_MICRO_SPECTRUM.md#143-provenance-reuse-and-autonomy-in-shared-work)。

预期的试点比较器评估为本地及分布式任务图提供的证据。替代工作必须从自己的证据开始，而不能继承无法获得的结果。真正的比较需要实际观测、声明的基线和完整的成本覆盖。即使某种协作安排比集中式替代方案更慢，更广泛的自由目标仍有价值。

<a id="S08"></a>

## 8 落实到行动的治理

由人治理的系统包括事先授权的自主执行。核心要求是，受委托行动必须处于真实且可检查的授权之内。它既不应强迫人们逐条手动批准每条无害指令，也不应让宽泛目标变成无限行动的许可。

UCC 指确定性控制和受支持的有限程序。用户或机构的要求以带版本的配置方案表达，并连接到系统实际能够执行的程序，或明确指出的人工工作。尚不受支持的文字要求必须继续标为不受支持，而不是转化为近似检查后就标记完成。缺失值、假值、检查失败及从未运行的检查，是不同结果。

业务控制评估为获得授权的审查提供指导，而不是最终专业结论。它们不阻止普通提示、不扣留实际回复、不要求普通继续操作必须先审查，也不授权外部业务行动。应分别保留原始自动化发现、实际回应，以及任何获得授权的人工结论。技术身份验证、受保护的保管、隐私、资源限制、安全执行及明确的采集中断规则仍可独立执行。分析缺失或未执行，既不是通过，也不能据此合理声称“不适用”。为受支持流程选择的审查要求仍须可见，但不能变成日常工作的普遍人工关卡。

忠于来源的控制编写保留原始要求、拟议解释、排除项、冲突以及明确采用的版本。模型可以帮助解释或起草控制，但不能通过生成文本激活它。草稿变化应使受影响的预览失效。新策略可以改变未来行动，但不应更改过去任务已记录的结果。

moralWARE（亦写作 MORALware）是规范与权利治理功能族。它将选定的规范配置方案，与彼此分开的提案、Guardian 审查、证据审计及确定性守卫职责结合起来。LANTERN 和 ANCHOR 等历史名称描述了这一分阶段设计的某些部分；此处的 ANCHOR 不是 Control Anchor 界面。其目标是理由可见、具有申诉途径的可问责审查，而不是通用道德分数。留存的设计检查点将完整 moralWARE 链安排在有用的本地循环之后；历史守卫源代码不能证明已经存在活跃的受保护行动使用组件。这不是对其当前实现进行的新审计。

Sophia 可以承担 Guardian（守护审查）角色，但同一个评估者不能仅靠换个标签批准自己的工作，就制造出独立性。证据审查应检查论据是否真正支持拟议决定，以及问题框定是否排除了受影响的人或重要替代方案。情境性策略可以变化，但防止伪造证据、冒充审查者或暗中扩权的核心保护必须明确。

CECP 保留其 Critical Epistemic Continuity Protocol（关键认知连续性协议）的沿革，以及具体的、以权利底线为先的评估。它询问必要性、比例适当性、最小伤害、可逆性、基本服务连续性、负担承担者、正当程序、申诉和救济。这些问题有助于防止一种技术上整齐的优化，把不可接受的成本强加给别人。已接受的非运行时语义或结构有效的评估，不授予运行权限。

TIAIP 是可选的创伤知情审查配置方案。该配置方案、一个历史独立应用及一个兼容模块是不同成果，不继承彼此的资格验证。在 Brain 中，其目标是提供一种可选、受用户控制的方式，塑造相关审查与披露。限定范围内的合成证据，不是临床验证、诊断，也不是实际情境中充分照护的证明。

与提供方无关的审查核心独立于该可选配置方案而存在。它保留发现、人工决定、修复请求、后继沿革、重新验证、恢复，以及与确切决定绑定的导出。修复后的后继版本应绑定授权该修复的候选和决定。人工批准不能抹去确定性失败，也不能让未执行的程序变成已经执行。如果应用可以重启，进程内的一次性消费检查仍需持久、跨进程的支持。

AEGIS 涵盖准入和防御性遏制。其预期响应有边界且可问责：暂停、隔离、切断一条数据路径、保留相关证据、暂时停用限定范围内的能力，并在明确事先授权时通知适当所有者。可疑事件不是动机或过错的证明。设计包括反证、审查者分配与回避、期限、安全过渡状态、救济和恢复。保护系统不应制造出无法复核的永久排除机制。

EIR 提供情境解释与对照观点视角，包括司法管辖、翻译损失和纠正。交互自主性审查会问：系统行为是否对人施压、使人孤立或操纵人，或削弱其实际脱离能力？成果审查考虑来源、呈现、无障碍和含义损失。这些功能应帮助用户运用判断，而不是以隐蔽的中心教条取代判断。

<a id="S09"></a>

## 9 观测到了什么以及没有观测到什么

保管在声明的采集边界内保存实际任务生命周期。它应保留准入前的尝试、相关请求与响应绑定、生效版本、错误、纠正及不确定性。预留不等于已完成推理。已采集到的响应可以同时伴随处理失败或审查待定。报告必须保留这些区别，而不是把不兼容的计数混成一个成功率。

保管设计要求在声明的保留与删除规则下，建立最小化、受访问控制的记录，而不是允许永久保存每一份被拒绝的载荷。凭据、根密钥或任务密钥必须排除在普通事件日志和公开溯源信息之外。在适当且充分的情况下，问责记录可以保留不含内容的引用，而非原始载荷，同时说明相应的重放限制。例外保留必须明确且有理由；它既不暗含对 PMR 的同意，也不是永久性的审计豁免。

技术手稿指出所检查实现中的一个具体限制：选定的载荷和衍生文件可以到期失效，而仅追加的事件记录仍可能保留原始请求字节、生效上下文和规范化响应文本。这种到期处理并不等于完整擦除内容。提供方、导出文件、备份和对等节点各有独立的副本生命周期。关闭 PMR 不等于保管过程没有存储内容，不含原始载荷的审查回执也不一定匿名。要弥补这一缺口，需要考虑副本的保留机制和如实面向用户作出说明，而不是给现有的到期操作贴上更强的标签。参见[技术手稿第 15 节（英文）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/papers/triadic-brain-micro-spectrum/2026-11-03-edition-1.2/TRIADIC_BRAIN_MICRO_SPECTRUM.md#15-security-privacy-and-failure-analysis)。

TEL，即 Thought Exchange Layer（思维交换层），记录声明的阶段和证据关系。如果结果契约要求图快照、摘要和事件流，它们就是不同的成果；有利的摘要不能替代缺失的必需事件。TEL 不是私密认知过程的转录，也不采集隐藏的思维链。其声明的阶段轨迹不同于实际保管事件；逻辑排序标签既不是经过的时间，也不是跨主机的因果时钟。提供方响应正文的原始字节、规范化响应文本和下游衍生的语义采集内容，也属于不同的观测域。重新检查衍生成果，并不是对原始响应进行第二次独立观测。

可用证据通道必须保持类型明确。实际观测到的输入、输出和行动，不同于公开的模型解释、提供方生成的推理摘要、仪器采集的数值信号及后续分析解释。受支持的解释通道在获得授权后可以保留，但其文本不保证完整，也不保证忠实反映内部因果。不能用生成文字填补无法获得的观测，再把它改标为实测证据。

TAC，即 Telemetry Aperture Controller（遥测孔径控制器），是关于受治理观测与采样的独立设计。它会问：在维持适当审计底线的同时，那些足以改变决定的不确定性，能够合理支持怎样的分辨率、时间窗口和保留级别？更多采样不会自动授权更多保留、导出或跨节点联邦共享。必要性、同意或由相关获授权所有者／适用治理流程确立的紧急依据，以及自动降级、尾段保留、申诉和窗口结束后的审查，仍是各自独立的职责。任何紧急采集都必须局限于明确范围和时长；模型自己声称“紧急”，不能扩大访问。事先授权的防御步骤不必每一步都等待新的提示。当前准入孔径不等于已经部署的通用 TAC 采集器。

一项可选的特征描述功能，历史上称为 **Coherence Event Signatures（相干事件特征，CES）**，提供带类型的事件上下文特征，用于比较和追踪。它属于 [F30](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F30)，但又是独立子功能：TAC 选择获准的观测；CES 根据提供的信息描述事件特征。事件标识符、内容哈希、分析测度和密码学签名是不同对象。当前 CES 集成仍未解决，它也不是本地试点的先决条件。[准入孔径 F29](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F29)又有所不同：它的必要关卡不可补偿，也就是说，其他方面的高分不能抵消同意或隐私要求未通过这一事实。

Brain 的溯源记录应保存主张的起源、改变它的活动、可追溯归属的纠正，以及任何已知缺口。每次导出都应仅携带接收方获准查看的关系；来源引用不是检索授权。这些是项目要求，不是选择一种格式就能确立的属性。相关术语见 [W3C PROV](https://www.w3.org/TR/prov-overview/)。

回执应至少对人和机器都有实际用途。一个人不应非得成为协议专家，才能展开查看来源、检查发现、请求纠正、理解保留安排、导出符合条件的记录，或恢复待处理任务。键盘、屏幕阅读器、低视力及初次使用者的可用性，需要与真实用户一起观察。仅有文档不能证明救济途径无障碍可用。

<a id="S10"></a>

## 10 用户拥有的计算机之间的协作

Sonya 网络旨在连接独立治理的节点，历史上有时也被称为 Sophia 网络。每个参与者拥有自己的资源及已接受的集成。协调机制可以提出任务放置建议，但只有相关所有者才能授权并落实。网络执行协调者不是万能管理员。

共享 CPU、GPU 和 RAM，意味着在符合条件的机器上调度工作。RAM 仍附属于实际执行所有者，并具有相应限制、预留和生命周期。Wi-Fi 不会把分离的 PC 变成透明、无延迟、全局一致的单一内存空间。需要频繁同步的任务，在普通链路上可能表现不佳；可拆分为有边界且相互独立工作的任务，可能更适合。

初始目标是真实的双节点交换，随后是三节点 Wi-Fi 试点。技术手稿发现了范围有限的、经身份验证的成果传输源代码，以及独立的、默认关闭的对等节点模型契约和所有权挂接点。在其选定的源代码闭包中，所维护的配对传输路径路由的是成果，而非模型作业；对等节点模型路径在生产环境中的构建或调用尚未确立。这些是仍缺少互联衔接的实现接合点，不是已经安装认知群体的证据，也不是声称已经评估了所有后续代码。有用的证据包括加入流程、经验证的身份、实际贡献、资源限制、取消、重启、回复丢失和恢复。模拟的对等节点或第二个进程可以测试组件边界，但不能演示一台独立治理的物理机器。

存储和证据分发可以使用内容寻址对象、选择性复制、流言传播协议或类似 torrent 的交换。这不必依赖区块链、代币经济或私密活动的公开记录。内容标识符绑定特定表示；它们的构建方式、分块及编码都很重要。它们支持完整性与检索，而非保密、真实或授权。[IPFS 内容寻址文档](https://docs.ipfs.tech/concepts/content-addressing/)

三个共享层级让预期区别具有实际可操作性。**本地**材料留在节点声明的本地保管与处理规则之内。**可信群组**材料按约定目的及保留策略，与选定接收方共享。**公开**材料是单独审查过的衍生版本，按其实际权利可供不受限的受众访问。这些层级与执行信任相互独立：公开输出可以在本地计算，而私密任务可能使用经过专门资格验证的机密计算路径。

元数据也需要保护。即使正文被删除，姓名、时间戳、参与模式、依赖关系及可猜测内容仍可能泄露敏感信息。看似无害的摘要不会自动净化其资料包中的日志或附件。发布决定必须检查完整衍生物及其元数据，而不只是可见的第一页。

### 加密与计算有不同边界

传输加密在协议假设下保护通道。TLS 旨在为端点之间提供经过身份验证、保密且受完整性保护的通信，同时仍有某些流量属性可被观察。其保护不会向获得授权的接收端点隐藏明文。[TLS 1.3 规范](https://www.rfc-editor.org/rfc/rfc9846)

磁盘加密在规定状态与威胁场景下保护存储数据。例如，BitLocker 针对设备遗失、被盗或不当退役造成的暴露。授权工作负载处理明文时，普通磁盘加密并不能保证对特权主机保密。[Microsoft BitLocker 概述](https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/)

普通虚拟机不足以证明主机无法查看工作负载。机密计算增加了一条独立的受保护执行与证明路径，其硬件、软件及部署假设必须经过资格验证。专门的密码学方法可能在各自协议和成本条件下支持特定计算。设计并不承诺每一种加密 AI 工作负载都能在任意志愿提供的 PC 上私密运行。[Microsoft 机密计算概述](https://learn.microsoft.com/en-us/azure/confidential-computing/overview)

钱包类比涉及受保护的密钥保管及限定范围的释放。密钥应绑定确切任务、接收方、工作负载和当前策略，并具备恢复及撤销控制。角色凭据不自动等于任务加密密钥。仅有来源哈希和原生角色标签，不构成授权。看起来有效的回执，不能替代实际密钥所有者经过身份验证的决定。

### 撤销与不确定效果

撤销必须落实到实际提交点。工作者可能先检查权限，随后在披露或派发前，与一项撤销发生竞态。可靠实现需要绑定当前版本，在必要时原子地消费授权，并有权威方式核对、厘清结果。“最近检查过”并不总是足够。

派发前取消，与工作可能开始后取消，是两回事。确认消息丢失可能使结果处于未知状态。系统应检查原始尝试，而不是凭空新建一次尝试，冒产生重复效果的风险。撤销可以阻止未来获得授权的使用或释放，但不能保证抹除已向另一方披露的数据。衍生成果和保留的依赖需要各自的传播与保留规则。

实际退出不只是一个“离开”按钮。参与者需要获准的导出、清晰的剩余义务、停止新工作的方式，以及对失去自身控制的副本的如实说明。即使参与者贡献的算力很少，协作也应保留这些选择。

<a id="S11"></a>

## 11 人类学习与涌现问题

人类类比帮助提出设计问题，但并不声称软件就是生物脑。内部运行条件、外部证据、拟议行动和观测结果应保持区分。资源不足可以成为缩小任务或暂停的理由，却不能让事实主张因此为真。执行协调者可以修订假说、寻找证据或提出获准行动，但计划不能证明行动已经发生。

Mark Solms 与 Karl Friston 提供了一项相关理论参考。在 2018 年论文中，他们将生物自我维持、预测推断、注意与情感联系起来。他们把精度描述为证据或预测可靠性的估计，并讨论其如何改变预测误差的影响。他们还讨论了向更自动化形式的巩固，以及预测失败时某些记忆被重新开启。这些是作者对生物系统的主张，不是对 Triadic Brain 的评估或背书。本文页码指的是 26 页的已接收手稿，而非期刊印刷页码。[Solms 与 Friston，已接收手稿，第 6–12 及 17 页](https://discovery.ucl.ac.uk/id/eprint/10057681/1/Friston_Paper.pdf)

工程推论是克制但有用的：可复用程序应附带适用情境与重新审视的理由；证据加权应考虑可靠性，而不是简单重复次数；更新内部表示应与改变外部世界保持区分。项目关于删除、同意、权限及保留的规则，是额外的治理选择，并非生物理论所规定。

软件表达的置信程度不自动等于统计精度。信息论目标不是以焦耳计的读数。马尔可夫毯是在特定模型内的统计构造，而不是防火墙或密码学保护。这些区别防止类比演变为缺乏支持的工程保证。[已接收手稿，第 4 页脚注 6–7，第 6–7 及 13–14 页](https://discovery.ucl.ac.uk/id/eprint/10057681/1/Friston_Paper.pdf)

更广泛的愿景，是建立一种环境，让人类与专业化代理发展出并非逐项预编排的有用协作模式。Thomas 将其描述为一种“人工促成的自然构造”（artificially natural construct）：通过设计条件，让迭代活动能够产生未预先计划的组织形式。系统无需包含整个宇宙的手工编码模型，也可以尝试学习和复用有边界的关系。

这一愿景仍留下重要的开放问题。生物体的细胞、独立微生物，以及宿主的微生物组，是不同生物情形；没有哪一种能直接映射为软件代理。更好的协调、大规模网络、自我描述或程序性巩固，本身都不能解决系统是否具有主观体验的问题。Solms 和 Friston 明确不把感受归于每一个具有马尔可夫毯的动力系统。可能的集体意识，以及单独命名的奇点愿景，仍是开放问题，而非必然里程碑或有用产品的先决条件。本版没有定义已测得的奇点阈值。[已接收手稿，第 11 页](https://discovery.ucl.ac.uk/id/eprint/10057681/1/Friston_Paper.pdf)

富有成效的研究计划仍可在预算匹配的条件下，将协调代理与单代理、汇集输出及移除通信的基线比较。它可以检验：复用能否在不损失质量的情况下节省工作量；假设变化能否促使重新审视常规程序；剪枝能否保留仍然需要的证据。这些将确立具体工程发现，而不是意识测试。

<a id="S12"></a>

## 12 可选扩展与保留的研究

Brain 应当无需激活每个研究功能族也有用。可选组件必须声明依赖、权利、输入输出契约及效果边界。历史发布或源代码审查，不会自动使新集成取得资格验证。

Open Web Steward 说明了这一区别。它是本地静态工作台，用于已提供事实、教学胶囊、用户粘贴的不可信候选、发现、人工处置立场、有边界的修复后继版本，以及导出。它不是网络爬虫或提供方适配器。即使通用包装层呈现了结果，其原生检查仍然重要。新旧契约版本需要明确比较语义，不能假设同名或近似名称字段就等价。

CivicProof 保留了一条可选的公共事务问责与离线选举研究沿革。它的存在不赋予对公共决策的权力，也不意味着已经建立通用 Brain 运行时。IntegrityLock 保留完整性及版本绑定证据的职责。本地审查运行时提供限定范围的审查成果。受治理的序列内核保留中性的验证、编译、规划、渲染、终态闭合与回执职责，并将它们同可选组合分开，后者包括历史上名为 Call Engine 或 Clavis 的内容。完成、拒绝、暂缓和未完成的序列都需要明确终态；记录闭合不同于执行其要求的程序。序列描述及其闭合回执都不授予执行权或内容使用权。当前内核与实际使用组件是否精确等价，仍未解决。可选内容必须保留自身的访问权与使用权。

数学量注册表、形式证明框架及公式到实际使用组件的对应账目，同样可以具有正当位置，但不能因此变成实证验证。定理在声明假设下可以有效，而其应用仍可能未经校准，其软件使用组件也可能尚未获得资格验证。

这些区别是在保存已有工作，而不是否定它。功能图让可选、历史和未解决的职责保持可见，从而可以继续研究或有意延期处理。它也降低两类风险：重新构建源代码已经存在的机制，以及引入旧机制却未带入当前的授权与披露保障。

<a id="S13"></a>

## 13 证据与交付路径

项目区分**设计意图**、**已有源代码实现**、**限定范围资格验证**和**实际安装或网络证据**。设计意图保留应当能够做什么。源代码指出在已标识快照中存在的机制。限定范围资格验证记录针对确切候选、总体和环境实际发生了什么。实际安装或网络证据涉及真实机器上的互联行为。一个类别中的进展，不会暗中完成另一个类别。

技术手稿作了更细的区分，本次 R6 对齐同样遵循这些区分：

| 证据类别 | 该陈述能够支持什么 | 它不能提供什么 |
| --- | --- | --- |
| 已检查的源代码 | 已标识的定义、分支或契约确实存在 | 执行或实用性 |
| 已检查的调用路径 | 在选定的源代码闭包中，特定生成组件连接到使用组件 | 已被调用或已部署的工作流 |
| 已编写的测试 | 检查及测试夹具总体确实存在 | 测试通过的结果 |
| 留存的执行报告 | 曾报告一次限定范围的历史执行 | 新的重新运行或与当前源代码的一致性 |
| 分析推论 | 结论在声明的方程与假设下成立 | 观测到的生产结果 |
| 拟议机制 | 预期的接口或实验已作出规定 | 采用或完成 |
| 研究假说 | 已陈述猜想或形式模型 | 实证有效性，或必然已准备好接受测试的可观测量 |
| 不可用或未观测 | 在范围内尚未确立相关证据 | 零值、假值或虚构数值 |

这些类别可以同时存在于一项职责中。由源材料定义的公式是实质性研究，但并不会因此成为名称相近的使用组件所实现的方程。未改变的注册表成熟度标签是简洁的导航辅助，不能替代这些区别。参见[技术手稿第 2 节（英文）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/papers/triadic-brain-micro-spectrum/2026-11-03-edition-1.2/TRIADIC_BRAIN_MICRO_SPECTRUM.md#2-method-and-evidence-classes)。

留存的 R5.1 设计检查点报告了选定认知贡献与复用组件、Observer 和 Home 路径、TAF 服务路径及软件包闭合的限定范围证据，各自限于记录的范围。R6 保留这些陈述，但不声称进行了新的执行，也不重新评估所有当前分支。技术手稿在较窄范围内进行的源代码重建，识别了具体的接入、保管、采集、原生评估、审查和呈现路径，以及本文解释的条件性筛查、对等节点路径和生命周期限制。两份文档都未确立完整的实际安装认知循环、原生隔离，以及真实的双节点和三节点 Wi-Fi 工作流。后续代码变更需要自己的源代码绑定和证据；无论技术论文还是本白皮书，都不将项目当前的实现状态固定不变。注册表附录刻意避免给出完成百分比。

实际顺序是先实现本地有用性。受支持的宿主入口与原生入口应检查同一份生效任务与策略历史；宿主自身不完整的记录不能替代原生证据。没有宿主订阅、PMR 或对等节点时，本地仍应可以有用；实时宿主集成则有自己的资格验证范围。受维护的已安装本地入口，应能接受获准任务、调用选定且受支持的运行时、保存实际结果，并向用户展示相应证据。独立的后续任务应保留上下文与父任务关系，而不暗含跨任务记忆。面向未来的策略变化应影响之后的工作，同时保存过去结果。不受支持的路径和缺失证据应保持可见。

接下来是由独立治理的所有者参与的真实双节点交换。它必须展示披露了什么、运行了什么、资源消耗在哪里，以及如何处理中断。其后的三节点 Wi-Fi 试点则询问：包含质疑与综合的互联认知工作流是否有用、易懂且可恢复？这些阶段不仅需要成功演示，也需要不利情形。

记忆复用需要自己的连贯证明：精确且符合条件的既有资料字节、经过身份验证的当前使用授权、实际保管效果、通过预期使用组件进行的比较或注入，以及可见的既有资料影响后续工作的记录。能够保留或比较一项参考，不等于证明了完整生命周期。

研究可以与这些交付阶段并行推进。迁移效用、语义巩固、自适应角色选择、机密计算及大规模联邦协作，都需要自己的证据。它们既不应被宣传为已经完成，也不应成为阻碍交付有用且有边界的本地工作流的笼统前提。

有用进展包括负面结果。被拒绝的映射、压缩损失、不可靠指标或困难的退出路径，都可能暴露下一项必要改进。项目应警惕叙述成熟度快于用户能力、重复架构取代缺失集成，以及优化分数掩盖人的负担。可靠性、公平性和停止的能力，优先于最大化参与度。

<a id="S14"></a>

## 14 可编辑的多语言设计

随着定义、实现和证据的发展，这份设计文档预计会频繁更新，但没有固定的发布日程。每一版都应指出变化并保留早期版本。英文主版本与机器可读概念图旨在共同演进。修改定义时，应指出受影响的功能族，必要时保留早期义项，并说明改变的是设计义务、研究主张，还是实现描述。JSON 是公开文档的配套表示，不是运行时模式定义，也不是授权文件。

计划中的语言版本应基于稳定的源文档。各版应保留功能族标识符，区分持续维护的术语与解释性译法，并标出歧义，而不是暗中合并概念。审查必须特别关注权限、同意、不确定性、拒绝、关怀，以及可能能力与已演示能力之间的区别。流畅的译文仍可能改变关键边界。本译本所依据的 R6 源资料包只包含列明的英文文件。早期译本和独立的可视化资料包不会自动继承 R6 对齐；翻译白皮书主文也不意味着补充资料已被翻译。翻译和渲染后的视觉审查属于独立工作，不会因这次文本对齐而自动完成。

Triadic Brain 的概念与系统设计作者是 Thomas Prislac。AI 辅助支持了组织、起草、协调和审查。AI 生成的文字或引用的研究论文，都不构成外部背书。本文旨在形成持久、可检查的说明，让他人能够理解、质疑和改进，而不必要求作者反复重述多年来的设计背景。

这里的邀请是务实的：协助建立有用的本地能力、识别缺失关系、贡献易于理解的解释、质疑缺乏支持的主张，并保护相关人员的权利。协作 Brain 通过易懂的工作和可纠正的证据赢得信任，而不是靠词汇量之大或抱负之宏伟。

<a id="APP-A"></a>

## 附录 A 保留的注册表记录

这份图谱保留了 86 条异质的注册表记录。其中的记录类型列，防止历史文档、原则或模式定义被误认为预期的运行时能力。它并不声称已经读过所有历史材料、每个术语都有唯一映射，或每项描述的能力都已实现。配套 JSON 和线性功能族指南提供带类型的术语义项、已知功能输入输出、权限限制、叙述指引，以及各条记录特有的证据或维护需求。相关记录链接是不排序、不穷尽的编辑关联，而非执行依赖，也不是接口已经集成的证明。以下名称是面向读者的标签，而不是 API 变更。链接指向英文补充指南中的详情。

**成熟度说明。** **Bounded（限定证据）**表示选定组件在声明范围内的证据。**Source（源代码）**表示选定机制存在于留存的源代码沿革中；它不是对当前代码的新审计。**Design（设计）**表示一项被保留的职责，但其完整行为尚未得到演示。**Research（研究）**表示研究、可选内容或尚未解决的映射。任何标签都不意味着整个产品或实际安装网络已经验收。历史沿革（Historical lineage）、历史材料（Historical material）及人员／流程规范（Human/process discipline）标签描述的是非运行时记录，不是额外的成熟度阶段。标签不是完成程度排名；在功能族指南中，源代码是否存在、定义是否协调，以及资格验证，是相互独立的维度。

| ID | 注册表记录（英文补充指南详情） | 记录类型 | 报告范围 |
| --- | --- | --- | --- |
| F01 | [Triadic Brain](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F01) | 系统范围 | Source |
| F02 | [历史集成沿革](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F02) | 历史沿革 | Historical lineage |
| F03 | [Control Anchor](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F03) | 能力职责 | Bounded |
| F04 | [Sonya 接入与适配器](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F04) | 能力职责 | Source |
| F05 | [Sonya 节点](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F05) | 部署实体 | Source |
| F06 | [协作节点网络](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F06) | 部署实体 | Design |
| F07 | [CoherenceLattice](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F07) | 能力职责 | Bounded |
| F08 | [相干性逆向综合](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F08) | 能力职责 | Source |
| F09 | [Sophia](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F09) | 能力职责 | Bounded |
| F10 | [Atlas 情境导览](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F10) | 能力职责 | Source |
| F11 | [发布者视图](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F11) | 能力职责 | Source |
| F12 | [Atlas432 情境词典](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F12) | 可选配置方案或扩展 | Research |
| F13 | [PMR 保留与复用](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F13) | 能力职责 | Source |
| F14 | [逆向综合既有资料候选](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F14) | 模式定义或词汇契约 | Source |
| F15 | [GUFT 带类型语法](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F15) | 研究提案 | Source |
| F16 | [Universal Coherence Mapping（通用相干映射）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F16) | 能力职责 | Source |
| F17 | [AHA 类比与迁移](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F17) | 能力职责 | Source |
| F18 | [受治理的桥接工作流](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F18) | 研究提案 | Research |
| F19 | [用户指定的执行协调者](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F19) | 能力职责 | Source |
| F20 | [Analyst 分析、Challenge 质疑与 Synthesis 综合](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F20) | 能力职责 | Bounded |
| F21 | [受绑定的对等节点贡献](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F21) | 能力职责 | Source |
| F22 | [UCC 有限程序](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F22) | 能力职责 | Source |
| F23 | [AEGIS 准入与遏制](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F23) | 能力职责 | Source |
| F24 | [moralWARE 权利与规范审查](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F24) | 贯穿多环节的职责 | Design |
| F25 | [规范守卫内核](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F25) | 能力职责 | Source |
| F26 | [分阶段规范工作流](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F26) | 贯穿多环节的职责 | Design |
| F27 | [Guardian 守护审查与证据审计者](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F27) | 贯穿多环节的职责 | Design |
| F28 | [Thought Exchange Layer（思维交换层）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F28) | 能力职责 | Source |
| F29 | [准入孔径](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F29) | 能力职责 | Source |
| F30 | [Telemetry Aperture Controller（遥测孔径控制器）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F30) | 能力职责 | Design |
| F31 | [CECP 连续性与权利评估](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F31) | 可选配置方案或扩展 | Source |
| F32 | [TIAIP 可选配置方案](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F32) | 可选配置方案或扩展 | Bounded |
| F33 | [与提供方无关的审查与恢复](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F33) | 能力职责 | Source |
| F34 | [情境解释视角](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F34) | 研究提案 | Research |
| F35 | [权威保管](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F35) | 能力职责 | Bounded |
| F36 | [经所有者准入的协作执行](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F36) | 能力职责 | Bounded |
| F37 | [受权利治理的成果交换](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F37) | 能力职责 | Source |
| F38 | [由所有者控制的保密释放](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F38) | 能力职责 | Design |
| F39 | [角色与投入程度选择](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F39) | 研究提案 | Design |
| F40 | [试点证据比较器](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F40) | 贯穿多环节的职责 | Design |
| F41 | [CivicProof 扩展](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F41) | 可选配置方案或扩展 | Research |
| F42 | [完整性保护](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F42) | 贯穿多环节的职责 | Source |
| F43 | [DeltaSyn 压缩研究](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F43) | 研究提案 | Source |
| F44 | [迭代修复与发现](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F44) | 贯穿多环节的职责 | Source |
| F45 | [用户治理的情境控制](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F45) | 贯穿多环节的职责 | Source |
| F46 | [TAF 目标与诊断](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F46) | 研究提案 | Source |
| F47 | [有边界的认知规划](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F47) | 能力职责 | Source |
| F48 | [按目的分开的记忆角色](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F48) | 贯穿多环节的职责 | Research |
| F49 | [谓词适用性审查](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F49) | 研究提案 | Research |
| F50 | [明确的映射结果](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F50) | 模式定义或词汇契约 | Research |
| F51 | [保留分布的聚合](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F51) | 可选配置方案或扩展 | Research |
| F52 | [Rosetta 观测桥](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F52) | 可选配置方案或扩展 | Research |
| F53 | [带类型的量命名空间](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F53) | 模式定义或词汇契约 | Research |
| F54 | [公式与实现对照](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F54) | 贯穿多环节的职责 | Research |
| F55 | [跨领域迁移评估](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F55) | 研究提案 | Design |
| F56 | [运行层面的自我模型](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F56) | 研究提案 | Research |
| F57 | [公众解释层级](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F57) | 贯穿多环节的职责 | Research |
| F58 | [以成果为中心的情境审查](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F58) | 贯穿多环节的职责 | Research |
| F59 | [忠于来源的控制编写](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F59) | 能力职责 | Research |
| F60 | [尝试与总体核算](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F60) | 贯穿多环节的职责 | Research |
| F61 | [互补观测界面](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F61) | 贯穿多环节的职责 | Research |
| F62 | [会话恢复与过时所有者隔离](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F62) | 能力职责 | Source |
| F63 | [带类型的证据通道](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F63) | 模式定义或词汇契约 | Research |
| F64 | [角色与能力契约](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F64) | 模式定义或词汇契约 | Source |
| F65 | [带类型的连续性关系](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F65) | 模式定义或词汇契约 | Research |
| F66 | [带类型的溯源图](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F66) | 模式定义或词汇契约 | Research |
| F67 | [无障碍工作流回执](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F67) | 贯穿多环节的职责 | Research |
| F68 | [PMR 沿革查询与建议](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F68) | 能力职责 | Source |
| F69 | [考虑依赖的记忆生命周期](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F69) | 研究提案 | Research |
| F70 | [相关性与新颖性路由](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F70) | 能力职责 | Source |
| F71 | [受治理的序列内核](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F71) | 研究提案 | Research |
| F72 | [本地优先的所有权](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F72) | 贯穿多环节的职责 | Research |
| F73 | [经过资格验证的模型替换](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F73) | 贯穿多环节的职责 | Source |
| F74 | [本地审查运行时](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F74) | 能力职责 | Source |
| F75 | [版本绑定的重放](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F75) | 能力职责 | Source |
| F76 | [与证据关联的进展纪律](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F76) | 贯穿多环节的职责 | Human/process discipline |
| F77 | [交互自主性审查](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F77) | 研究提案 | Design |
| F78 | [防止指标投机的控制](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F78) | 贯穿多环节的职责 | Research |
| F79 | [TCHES 历史测试文档](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F79) | 历史测试材料 | Historical material |
| F80 | [固定问题的连续性](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F80) | 能力职责 | Source |
| F81 | [范围受限的既有资料使用](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F81) | 能力职责 | Source |
| F82 | [使用后的既有资料影响审查](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F82) | 能力职责 | Source |
| F83 | [有边界的探索与停止](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F83) | 能力职责 | Source |
| F84 | [符合条件的既有资料检索](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F84) | 能力职责 | Source |
| F85 | [记忆意图审查立场](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F85) | 能力职责 | Source |
| F86 | [形式假设与使用组件的一致性](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F86) | 贯穿多环节的职责 | Source |

<a id="HIST-F79"></a>

### 历史测试材料

F79 保留了早期 TCHES 文档的引用。TCHES 曾被用作测试文档；它不是预期的 Brain 能力、可选产品或实现目标。保留这段历史，不是在断言某个特定测试程序、使用组件或结果。不会为了维持一个功能数量，而虚构替代功能。

<a id="APP-B"></a>

## 附录 B 知识水系与可修订的探究

项目的**知识水系（Knowledge Waters）**用语，将实用的探究方法与数学研究计划联系起来。**廊道（corridor）**是一条可能的探究路线。**交织（braiding）**比较相关路线，同时保留各自不同的证据与未解决的分歧。**知识河流（knowledge river）**代表持续的研究方向。其支流包括修复、解释、校准和维护照管，而不仅是引人注目的发现。**阶地（terrace）**表示暂时的稳定：一种可在声明范围内复现的评估，在其证据或假设发生变化时可以重新审视。

发现目标包括从未决证据中形成有用的新问题和 AHA 候选。廊道可以保留尚未探索的替代方案，支流可以加入有区分力的观测，交织可以保留互补关系与异议，阶地则可以标记仍可能断裂或重新开启的支持。拟议的发现螺旋让用户选择问题、获准来源、分支和有边界的投入，然后返回一个候选，以及下一项能够区分替代方案的观测。发现候选、经验证的发现和行动许可仍然彼此分开。处于暂缓状态的答案不会派发更多调用，新颖性本身也不是验证。参见[技术手稿第 10.1 节（英文）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/papers/triadic-brain-micro-spectrum/2026-11-03-edition-1.2/TRIADIC_BRAIN_MICRO_SPECTRUM.md#101-a-discovery-spiral-from-unresolved-evidence)。

这个循环不是通向最终真理的阶梯。表面稳定可能来自重复的假设、被排除的反证或被压制的新颖性。变化的观测可以重新开启问题并产生相互关联的修订，同时让早期证据保持可见。收敛不等于正确；反复使用不等于独立支持。探究图谱不会授权行动。在使用记忆库类比的地方，它涉及受治理的存储和可能的复用；它并不会自动成为与河流或阶地模型相同的对象。

### 由源材料定义的数学模型

一种图场表述将廊道通量与局部对齐定义为：

```text
F_ij = w_ij ((C_i + C_j) / 2) (Θ_j − Θ_i)
A_i  = |Σ_j F_ij| / (Σ_j |F_ij| + ε)
```

这里 C 是声明的廊道密度变量，Θ 是声明的势，w 是图权重，A 是对齐比率。该表述在拟议的河流演化中使用对齐的廊道传输与记忆支持。这些符号不是实测水量、真理概率，也不自动赋予权限。必须说明它们的定义域、估计器、单位或归一化方式、参数选择，以及实证解释。同一符号在另一种表述中可能有不同含义；阶地密度、透明度和可追溯性不得合并为同一个量。

另一种独立的递归描述为：

```text
X_(n+1) = M ∘ S ∘ R (X_n)
```

它表示接收性接入、结构化以及记忆／连续性作用于一个不断演变的状态。这些功能处理过程可以横跨现有组件。它们不是对 Sonya、Sophia 和 Atlas 的一一重命名，也不要求使用三个固定模型。螺旋可以说明如何带着保留的历史重新审视问题；它并不能证明每条认知轨迹都会不可避免地呈螺旋状演变或收敛。

### 区分模型、实现与证据

| 在设计沿革中找到的材料 | 它支持什么 | 它不能确立什么 |
| --- | --- | --- |
| 图场与递归规范 | 实质性的拟议数学定义，包括河流／阶地动力学和重新开启 | 经过校准的可观测量、普遍物理定律或有益认知 |
| 数值与启发式生成组件 | 源代码包含特定更新规则和诊断构造 | 不同生成组件之间的等价性，或与图场方程的精确一致性 |
| 受限的代数证明项 | 针对已声明形式对象中明确有界量的实质性论证 | 一般河流动力学、经过校准的含义，或一次新的编译与公理闭包审计 |
| 定理式陈述与形式框架 | 预期命题，以及使假设明确化的位置 | 对所声称动力学的完整证明；占位命题并不证明任何场方程 |
| 合成指标测试夹具 | 用于说明的形态或受控示例 | 对实际探究的测量或独立验证 |
| 建议性审计与呈现使用组件 | 有源代码支持的审查和展示职责 | 已完成的可互操作链；生成组件与使用组件的数据形态仍需明确协调 |

技术手稿还将较完整的图场提案，与简化的河流内核及其顺序执行的阶地调用方区分开来。所检查的调用方提供的步长为 1，而不是沿用内核较小的默认步长；阶地更新使用的是刚刚更新后的河流场。因此，稳定性取决于图、系数、实际步长和截断限幅行为。截断限幅可以使数值保持有界，同时一个解析构造示例仍会出现循环；该示例不是已执行的测试，也不是对已部署图的诊断。手稿给出了方程及有条件的谱分析，但并未声称得到了实证认知结果，也未声称对所有图都稳定。参见[技术手稿第 9.1–9.3 节（英文）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/papers/triadic-brain-micro-spectrum/2026-11-03-edition-1.2/TRIADIC_BRAIN_MICRO_SPECTRUM.md#9-corridors-rivers-terraces-and-numerical-consequences)。

两个历史河流生成组件使用不同的数据形态：较简单的一个从新颖性推导流动标签，较丰富的一个则输出河流类别及独立的风险维度。所检查的审计组件要求强度与风险指标 capture-risk 的输入，而这些输出并不直接提供它们；缺失的风险记录可能被当作零风险。呈现使用组件要求的又是另一种以溯源与审查为键的数据形态。留存说明中没有确立一条协调这些形态的适配器链。这并不评估该快照之外的适配器或后继实现。这些是具体的源代码层面兼容性缺口，而不只是尚未执行的部署测试；这些启发式数值也没有哪一个能够证明与上述方程等价。

面向实际使用，拟议的对应解释是**与证据关联、可修订的探究**：保留替代方案、比较它们的约束、让未决差异保持可见，并说明什么会改变结论。这运用的是已有的构建、审查、呈现、记忆和沿革职责。它没有增添新的 Waters 器官，也不是有用本地工作的先决条件。

相关现有记录包括：用于来源特定量的 [F53](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F53)，用于假设与实现对应关系的 [F86](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F86)，用于相关构建与审查的 [F07](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F07) 和 [F09](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F09)，用于解释的 [F10](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F10) 和 [F11](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F11)，用于证据类型与修订沿革的 [F63](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F63) 和 [F66](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F66)，以及用于评估任何所声称迁移收益的 [F55](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/7c40bb33c64017f7b11a5b83a272cf87424c73e1/docs/whitepaper/triadic-brain-20261102/R6/FAMILY_GUIDE.en.md#F55)。这些是职责关联，并不是断言每个历史生成组件都已被当前 Brain 采用为实现。

<a id="REFERENCES"></a>

## 参考文献

本文的项目组件定义属于原创设计定义与编辑性协调。一般技术机制及生物类比采用相关主张附近所链接的一手来源：

- Prislac, T. (2026)。[*Triadic Brain from Byte Identity to Revisable Knowledge*（Triadic Brain 从字节身份到可修订知识），技术手稿第 1.2 版（英文）](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/papers/triadic-brain-micro-spectrum/2026-11-03-edition-1.2/TRIADIC_BRAIN_MICRO_SPECTRUM.md)。已发表的技术源代码说明；详细的来源与证据限制仍以该版为准。公开可获取不等于期刊接收或产品验证。
- W3C。[PROV Overview（PROV 概述）](https://www.w3.org/TR/prov-overview/)。
- IETF。*The Transport Layer Security Protocol Version 1.3*（传输层安全协议 1.3 版），RFC 9846。通道保护及其端点假设。
- Microsoft。*BitLocker overview*（BitLocker 概述）及 *Azure confidential computing overview*（Azure 机密计算概述）。存储与受保护执行各有不同威胁模型；引用不暗示选定该平台。
- IPFS。*Content addressing*（内容寻址）。绑定表示的标识符及其构建；引用不要求采用 IPFS。
- Solms, M., and Friston, K. (2018)。*How and why consciousness arises: Some considerations from physics and physiology*（意识如何产生以及为何产生：物理学与生理学的若干考量）。**Journal of Consciousness Studies, 25**(5–6), 202–238。[一手书目记录](https://discovery.ucl.ac.uk/id/eprint/10057681/)。本文的手稿页码引用指向单独编页的已接收手稿。
