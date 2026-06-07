# AUBB 业务闭环 Playwright MCP 测试报告（2026-06-07）

> 状态：已完成本轮 Playwright MCP 业务闭环审计。本文档记录真实本地前后端、清空本地数据后的业务闭环审计证据。测试期间未修改业务代码。

## 1. 测试环境与数据初始化

| 项目 | 记录 |
| --- | --- |
| 工作区 | `/Users/moorefoss/Code/AUBB` |
| 前端 | `http://127.0.0.1:3000` |
| 后端 | `http://127.0.0.1:18080` |
| 启动入口 | `just dev-up` |
| 健康检查 | `just healthcheck` |
| 截图目录 | `docs/06-testing-and-ops/artifacts/business-loop-2026-06-07/` |

### 1.1 初始状态

- `just status`：`server/`、`web/`、`docs/` 初始 dirty entries 均为 0；根目录不是 git 仓库。
- 启动前健康检查：`just healthcheck` 通过，后端 readiness、OpenAPI 和前端登录页均可访问。
- 本地环境：`env/e2e.env` 存在；`AUBB_BOOTSTRAP_ENABLED=true`；bootstrap 管理员用户名为 `U-SA1`。

### 1.2 清空本地数据

- 停止服务：`just dev-down`。
- 清空范围：仅作用于本地 `server/compose.yaml` Docker 项目。
- 清空命令：`cd server && docker compose down -v --remove-orphans`。
- 清空结果：删除本地 volumes `server_postgres-data`、`server_rabbitmq-data`、`server_minio-data`、`server_redis-data`。
- 残留风险：go-judge 服务无持久 volume；前端构建缓存和日志不属于业务数据，本轮未删除。

### 1.3 重新启动与 bootstrap

- 重新启动：`just dev-up`。
- 启动结果：后端 `18080`、前端 `3000` 均监听。
- bootstrap 日志：`Platform bootstrap completed schoolOrgUnitId=1 adminUserId=1 schoolCreated=true adminCreated=true schoolAdminRoleCreated=true academicProfileCreated=true platformConfigCreated=true`。
- 重启后健康检查：`just healthcheck` 通过。

## 2. 测试账号与角色

| 角色 | 用户名 | 所属组织 | 权限范围 | 状态 |
| --- | --- | --- | --- | --- |
| 平台管理员 | `U-SA1` | `AUBB-Realrun-School` | 平台治理、组织、用户、课程模板、开课、审计 | bootstrap 已创建，UI 登录通过 |
| 主讲教师 | `BL-TEACHER` | `闭环测试学院` | 课程运营、成员管理、题库、判题环境、作业、成绩 | 已创建并完成教师档案 |
| 整课助教 | `BL-TA-COURSE` | `闭环测试学院` | 整门课程协助 | 已创建并加入开课为 `OFFERING_TA` |
| 班级助教 | `BL-TA-CLASS` | `闭环测试学院` | 指定教学班协助 | 已创建并绑定教学班 `BL-CLASS-A` |
| 学生 A | `BL-STU-A` | `闭环测试 1 班` | 作业提交、成绩反馈 | 已创建并提交闭环作业 |
| 学生 B | `BL-STU-B` | `闭环测试 1 班` | 隔离与越权验证 | 已创建并验证未提交/越权隔离 |

本轮已通过 UI 创建以下测试账号，初始密码均为 `Password123`：

| 角色 | 用户名 | UI 创建状态 | 当前补充状态 |
| --- | --- | --- | --- |
| 主讲教师 | `BL-TEACHER` | 已创建，用户 ID 2 | 已通过 UI 保存教师教籍资料；本轮为解除 BUG-20260607-001 的后端 NPE，使用本地 DB 绕过补充 `primary_org_unit_id=2` |
| 整课助教 | `BL-TA-COURSE` | 已创建，用户 ID 3 | 已通过 UI 保存教师档案，学工号 `TA-BL-COURSE`；已加入课程成员，角色 `OFFERING_TA` |
| 班级助教 | `BL-TA-CLASS` | 已创建，用户 ID 4 | 已通过 UI 保存教师档案，学工号 `TA-BL-CLASS`；已加入课程成员，角色 `TA`，绑定教学班 1 |
| 学生 A | `BL-STU-A` | 已创建，用户 ID 5 | 已通过 UI 保存学生档案，学号 `STU-BL-A`；已加入课程成员，角色 `STUDENT`，绑定教学班 1 |
| 学生 B | `BL-STU-B` | 已创建，用户 ID 6 | 已通过 UI 保存学生档案，学号 `STU-BL-B`；已加入课程成员，角色 `STUDENT`，绑定教学班 1 |

## 3. 完整步骤执行记录

### 阶段 1：平台治理初始化

| 步骤 | 页面 / 动作 | 页面状态 | 截图 | 控制台 / 网络 | 结果 |
| --- | --- | --- | --- | --- | --- |
| 1.1 | 管理员登录 | 登录页和治理工作台可访问 | `01-01`、`01-02` | `POST /api/v1/auth/login` 200；登录后进入 `/admin` | 通过 |
| 1.2 | 平台配置 | 可查看并保存平台配置 | `01-03`、`01-04`、`01-04b` | 平台配置读取/保存接口 200 | 通过 |
| 1.3 | 组织管理 | 可创建学院、课程、班级节点；重复根节点有错误提示 | `01-05` ~ `01-10` | 组织创建/详情接口返回成功；重复根节点被拒绝 | 通过 |
| 1.4 | 用户管理 | 可创建教师、助教、学生测试账号 | `01-11` ~ `01-13` | 用户创建接口返回成功 | 通过 |
| 1.5 | 权限说明 / 授权 | 权限说明页和权限下拉可打开 | `01-14`、`01-15` | 页面加载正常 | 通过 |
| 1.6 | 学期管理 | 可创建 `BL-2026-SPRING` 学期 | `01-16`、`01-17` | 学期创建接口返回成功 | 通过 |
| 1.7 | 课程模板 | 可创建闭环测试课程模板 | `01-18`、`01-19` | 课程模板创建接口返回成功 | 通过 |
| 1.8 | 开课管理：新增开课 | 阻塞：主讲教师候选为空 | `01-21`、`01-23`、`01-24` | `GET /api/v1/admin/users?identityType=TEACHER&pageSize=100` 返回 500；响应 `INTERNAL_ERROR`；后端日志为 `UserAdministrationApplicationService.listUsers` NPE | 阻塞 |
| 1.9 | 开课详情 | 记录阻塞并最小绕过后，开课创建成功并可进入详情 | `01-25`、`01-26`、`01-27` | 开课创建接口返回成功，开课 ID 1 | 绕过后通过 |

### 阶段 2：教师课程运营

| 步骤 | 页面 / 动作 | 页面状态 | 截图 | 控制台 / 网络 | 结果 |
| --- | --- | --- | --- | --- | --- |
| 2.1 | 主讲教师登录与工作台 | 登录成功，进入教师工作台 | `02-01` | `POST /api/v1/auth/login` 200；SSE route change 偶发 `ERR_ABORTED` | 通过 |
| 2.2 | 我的课程 | 可见 `2026春-闭环测试课程-A` | `02-02` | `GET /api/v1/me/courses` 200 | 部分通过：课程模板/学期显示为未配置 |
| 2.3 | 课程工作台 | 可进入课程主页；直接入口含成员、班级、公告/资源等 | `02-03`、`02-04` | 课程相关接口 200 | 部分通过：元信息显示 `学期未配置 · 课程模板未配置` |
| 2.4 | 公告发布 | 创建 `闭环课程开课通知` | `02-05` | `POST /api/v1/teacher/course-offerings/1/announcements` 201 | 通过 |
| 2.5 | 资源上传 | 上传 `resource-bl-readme.txt` | `02-06` | `POST /api/v1/teacher/course-offerings/1/resources` 201 | 部分通过：上传者列为空 |
| 2.6 | 讨论创建与详情 | 创建 `闭环课程讨论主题` 并进入详情 | `02-07`、`02-08` | `POST /api/v1/teacher/course-offerings/1/discussions` 201 | 部分通过：详情页主帖/回复层级不清 |
| 2.7 | 实验创建与发布 | 创建并发布 `闭环实验一：环境准备` | `02-09`、`02-10` | `POST /api/v1/teacher/course-offerings/1/labs` 201；`POST /api/v1/teacher/labs/1/publish` 200 | 部分通过：未选择具体班级时空态文案与按钮禁用状态不清 |

### 阶段 3：成员与助教权限

| 步骤 | 页面 / 动作 | 页面状态 | 截图 | 控制台 / 网络 | 结果 |
| --- | --- | --- | --- | --- | --- |
| 3.1 | 主讲教师进入成员管理 | 成员表可加载；新增成员弹窗要求输入数字用户 ID | `03-01` | `GET /api/v1/teacher/course-offerings/1/members` 200 | 部分通过：用户选择体验差 |
| 3.2 | 学生/班级助教班级绑定校验 | 未选择班级时可触发表单校验 | `03-02` | 未发起成功添加请求 | 部分通过：错误提示存在，但弹窗状态容易混淆 |
| 3.3 | 添加整课助教 | `userId=3`，`memberRole=OFFERING_TA`，不绑定教学班 | `03-03`、`03-04` | `POST /members/batch` 200，`{"successCount":1,"failCount":0}` | 通过；关闭弹窗后列表不自动刷新 |
| 3.4 | 添加班级助教 | `userId=4`，`memberRole=TA`，`teachingClassId=1` | `03-02`、`03-04` | `POST /members/batch` 200 | 部分通过：最终列表班级列仍不显示班级 |
| 3.5 | 添加学生 B | `userId=6`，`memberRole=STUDENT`，`teachingClassId=1` | `03-03`、`03-04` | `POST /members/batch` 200，响应成功 1 人 | 部分通过：关闭弹窗后需要重新导航才看到新成员 |
| 3.6 | 补齐 TA/学生档案 | 通过用户详情页保存教师/学生档案 | `03-07` | `PUT /api/v1/admin/users/{3,4,5,6}/profile` 均 200 | 通过；列表“身份”列仍显示 `-` |
| 3.7 | 整课助教登录 | 补档前根路径卡在“正在跳转到工作区”；补档后进入教师工作台 | `03-05`、`03-08` | 登录 200；补档前无后续角色跳转请求 | 部分通过：未补档账号缺少明确引导 |
| 3.8 | 整课助教成员页 | 可查看整门课成员，成员写操作全部可见 | `03-09` | `GET /members` 200 | 部分通过：写操作显隐需按产品权限收敛 |
| 3.9 | 整课助教访问管理端 | `/admin` 被拒绝 | `03-10` | 路由进入 `/unauthorized` | 通过 |
| 3.10 | 班级助教登录 | 可进入教师工作台，但课程聚合返回 `roles:["OFFERING_TA"]`、`classes:[]` | `03-11` | `GET /api/v1/me/courses` 200，响应角色/班级范围错误 | 权限缺陷 |
| 3.11 | 班级助教课程工作台 | 可看到“新增教学班”和成员管理入口 | `03-12` | 页面加载成功 | 权限风险：班级助教入口过宽 |
| 3.12 | 班级助教成员页 | 仅显示本班学生和自己，但成员写操作仍可见；班级列为空 | `03-13` | `GET /members` 200 | 部分通过：读范围部分正确，写操作和展示仍有问题 |
| 3.13 | 班级助教访问管理端 | `/admin` 被拒绝 | `03-14` | 路由进入 `/unauthorized` | 通过 |

### 阶段 4：题库与判题环境

| 步骤 | 页面 / 动作 | 页面状态 | 截图 | 控制台 / 网络 | 结果 |
| --- | --- | --- | --- | --- | --- |
| 4.1 | 课程题库页 | 题库总览可进入课程题库；空状态可见 | `04-01` | `GET /question-bank/questions` 200 | 部分通过：空状态文案泛化 |
| 4.2 | 新增题目弹窗与题型列表 | 题型包含单选、多选、简答、文件上传、编程 | `04-01` | 无异常 | 阻塞：表单没有题型专属配置字段 |
| 4.3 | 创建单选题 | 只能填写题干文本，无法配置选项/正确答案 | `04-02` | `POST /question-bank/questions` 400，`QUESTION_BANK_OPTIONS_INVALID` | 阻塞 |
| 4.4 | 创建多选题 | 同单选题，无选项/多选答案配置 | `04-02` | `POST /question-bank/questions` 400，`QUESTION_BANK_OPTIONS_INVALID` | 阻塞 |
| 4.5 | 创建简答题 | `闭环简答题：实验反馈` 创建成功并出现在列表 | `04-03` | `POST /question-bank/questions` 201 | 通过 |
| 4.6 | 创建文件上传题 | 无文件类型、数量、大小限制字段 | `04-04` | `POST /question-bank/questions` 400，`QUESTION_BANK_FILE_COUNT_INVALID` | 阻塞 |
| 4.7 | 创建编程题 | 无支持语言、模板代码、入口文件、测试点或判题配置字段 | `04-05` | `POST /question-bank/questions` 400，`QUESTION_BANK_LANGUAGES_REQUIRED` | 阻塞 |
| 4.8 | 创建 Python 3 判题环境 | `闭环 Python 3 环境` 创建成功 | `04-06` | `POST /judge-environment-profiles` 201 | 通过；资源限制不可配置 |
| 4.9 | 创建 C++17 判题环境 | 新增弹窗带出上一次 Python 值，覆盖后创建成功 | `04-07`、`04-08` | `POST /judge-environment-profiles` 201 | 部分通过：创建表单未复位 |
| 4.10 | 编辑判题环境 | C++17 环境编辑保存成功 | `04-08` | `PUT /api/v1/teacher/judge-environment-profiles/2` 200 | 通过 |
| 4.11 | 归档与包含归档筛选 | 归档有确认；默认列表隐藏归档，勾选后显示 `已归档` | `04-09` | 归档请求成功；列表查询 200 | 通过 |

### 阶段 5：作业创建与发布

| 步骤 | 页面 / 动作 | 页面状态 | 截图 | 控制台 / 网络 | 结果 |
| --- | --- | --- | --- | --- | --- |
| 5.1 | 教师进入作业管理并创建作业 | 可进入 `/teacher/assignments/create`，已选择课程与教学班 | `05-01` | `GET /classes`、`GET /judge-environment-profiles`、`GET /question-bank/questions` 均 200 | 通过 |
| 5.2 | 配置五种题型 | 单选、多选、简答、文件上传、编程题均可在作业试卷内配置；创建页总分显示 60 | `05-01` | 表单本地状态正常 | 部分通过：配置区层级很深、信息密度高 |
| 5.3 | 首次提交作业 | 页面停留在创建页，未显示错误提示 | `05-02` | `POST /api/v1/teacher/course-offerings/1/assignments` 返回 400，响应 `Invalid request content`；console 记录 400 | 阻塞 |
| 5.4 | 诊断并最小绕过 | 后端控制器 `ProgrammingJudgeCaseRequest.stdinText` 要求 `@NotBlank`，前端允许测试用例 stdin 为空；通过页面填入 `ignored` 后继续 | `05-03` | 第二次 `POST /assignments` 返回 201，创建作业 ID 1 | 绕过后通过 |
| 5.5 | 发布前列表 | 作业状态为“草稿”，可见编辑、发布、关闭操作 | `05-04` | `GET /assignments` 200 | 部分通过：列表总分显示“暂无” |
| 5.6 | 发布确认弹窗 | 点击发布后出现确认弹窗，文案说明学生可见与开始提交 | `05-05` | 未发起发布请求前弹窗展示正常 | 通过 |
| 5.7 | 确认发布 | 作业状态更新为“已发布”，发布按钮禁用，关闭按钮可用 | `05-06` | `POST /api/v1/teacher/assignments/1/publish` 200；刷新列表 200 | 通过；总分仍显示“暂无” |

### 阶段 6：学生学习与结构化提交

| 步骤 | 页面 / 动作 | 页面状态 | 截图 | 控制台 / 网络 | 结果 |
| --- | --- | --- | --- | --- | --- |
| 6.1 | 学生 A 登录与工作台 | 登录成功，工作台显示课程数、教学班数和待办入口 | `06-01` | `POST /api/v1/auth/login` 200；学生工作台接口 200 | 通过 |
| 6.2 | 学生课程详情 | 可见课程公告、资源、讨论；没有直接聚合的作业/实验入口 | `06-02` | 课程详情、公告、资源、讨论接口 200 | 部分通过：入口结构不完整 |
| 6.3 | 学生作业列表 | `闭环综合作业一` 对学生可见，按钮为“开始做题” | `06-03` | `GET /api/v1/me/assignments` 200 | 部分通过：课程卡片仍显示 `草稿`，作业总分显示“暂无” |
| 6.4 | 作业详情空状态 | 作业详情显示总分 60 和五类答题控件 | `06-04` | `GET /api/v1/me/assignments/1` 200 | 通过 |
| 6.5 | 结构化答题与附件上传 | 完成单选、多选、简答，上传 `resource-bl-readme.txt` | `06-05` | `POST /api/v1/me/assignments/1/submission-artifacts` 201，返回 artifact ID 1 | 部分通过：页面只显示“附件 #1”，不显示文件名 |
| 6.6 | 刷新恢复本地草稿 | 刷新后出现“已恢复本地草稿”，客观题、简答和附件状态恢复 | `06-06` | 页面重新加载成功 | 通过 |

### 阶段 7：编程题工作区

| 步骤 | 页面 / 动作 | 页面状态 | 截图 | 控制台 / 网络 | 结果 |
| --- | --- | --- | --- | --- | --- |
| 7.1 | 进入编程工作区 | 编辑器打开 `main.py`，但文件树初始为空 | `07-01` | workspace 接口 200，响应 `files=[]`、`entryFilePath=main.py` | 部分通过 |
| 7.2 | 普通键盘编辑并保存 | 通过 Playwright 键盘输入后，UI 有编辑态但 Monaco model 仍为空，保存可能持久化空代码 | `07-02` | `PUT /api/v1/me/assignments/1/programming-workspace` 返回空 `codeText` | 阻塞 |
| 7.3 | 最小绕过继续审计 | 记录阻塞后，通过页面内 Monaco model 注入代码以继续验证保存、运行和提交链路 | `07-03`、`07-04` | 保存返回 revision，`files[0].content` 含 Python 代码 | 绕过后通过 |
| 7.4 | 样例运行 | `print('Hello AUBB')` 执行成功但判错；改为 `sys.stdout.write('Hello AUBB')` 后样例通过 | `07-05`、`07-06` | `POST /sample-runs` 201；首次 `WRONG_ANSWER`，第二次 `ACCEPTED` | 部分通过：输出差异解释不足 |
| 7.5 | 文件树新建文件 | 文件菜单可打开，但 `+` 按钮无可访问名称；新建 `helper.py` 后后端拒绝多文件 | `07-07`、`07-08` | `POST /workspace/operations` 400，`PROGRAMMING_MULTIPLE_FILES_DISABLED`；后续自动保存也 400 | 缺陷 |
| 7.6 | 刷新恢复后端状态 | 刷新后本地 `helper.py` 消失，恢复后端 `main.py` 状态 | `07-09` | workspace 重新加载 200 | 通过 |
| 7.7 | 历史版本侧栏 | 侧栏打开，但右侧宽度约 98px，内容被裁切 | `07-10` | 历史接口 200 | 缺陷 |
| 7.8 | 重置模板确认 | 点击重置会出现确认弹窗，说明当前修改将丢失；本轮取消 | `07-11` | 未执行重置请求 | 通过 |
| 7.9 | IDE 内正式提交 | 弹窗提示提交后查看详情，但实际只提交编程题答案，结构化作业校验失败；页面无错误提示且不跳转 | `07-12`、`07-13` | `POST /api/v1/me/assignments/1/submissions` 400，`SUBMISSION_ANSWER_SET_INVALID` | 阻塞 |

### 阶段 8：自动评判与提交详情

| 步骤 | 页面 / 动作 | 页面状态 | 截图 | 控制台 / 网络 | 结果 |
| --- | --- | --- | --- | --- | --- |
| 8.1 | 整份作业提交前核对 | 返回作业详情，五题答案均在页面中保留 | `08-01` | 本地草稿恢复正常 | 通过 |
| 8.2 | 学生 A 提交整份作业 | 点击整份作业“提交答案”成功，进入 `/student/submissions/2` | `08-02` | `POST /api/v1/me/assignments/1/submissions` 201，提交编号 `SUB-75bcd4377be54ac08867ea9901986d38` | 通过 |
| 8.3 | 自动判分与判题 | 单选、多选各 10 分；编程判题任务返回 `ACCEPTED`、20/20 | `08-02` | `GET /api/v1/me/submissions/2/judge-jobs` 200，`score=20`、`maxScore=20` | 后端判题通过 |
| 8.4 | 刷新提交详情 | 刷新后提交总分仍为 20/60，编程题卡片显示 0 分，未同步判题 20 分 | `08-03` | 提交详情 200；q5 `gradingStatus=PROGRAMMING_JUDGED` 但答案无 finalScore | 缺陷 |
| 8.5 | 提交详情内容展示 | 顶部“答案内容”显示“无文本答案”；客观题、附件、代码展示不完整 | `08-02`、`08-03` | 页面接口 200 | 缺陷 |
| 8.6 | 学生 B 越权访问学生 A 提交 | 直接访问 `/student/submissions/2` 被拒绝，页面提示“当前用户无权查看该提交” | `08-04` | `GET /api/v1/me/submissions/2` 403；`GET /judge-jobs` 403 | 通过 |
| 8.7 | 学生 B 自己的作业列表 | 可见同一作业为未提交状态，不显示学生 A 提交 | `08-05` | `GET /api/v1/me/assignments` 200 | 通过；总分仍显示“暂无” |

### 阶段 9：助教/教师批改与成绩处理

| 步骤 | 页面 / 动作 | 页面状态 | 截图 | 控制台 / 网络 | 结果 |
| --- | --- | --- | --- | --- | --- |
| 9.1 | 整课助教工作台 | 可进入教师工作台，侧边栏含提交管理、成绩册；课程卡显示 `OFFERING_TA`、教学班 0、草稿 | `09-01` | `GET /api/v1/me/courses` 200 | 部分通过：状态/角色展示仍混乱 |
| 9.2 | 整课助教提交管理筛选 | 选择课程和作业后自动加载学生 A 提交；列表得分 40 | `09-02`、`09-03` | `GET /api/v1/teacher/assignments/1/submissions` 200 | 通过；列表分数与学生详情阶段 8 的 20/60 不一致 |
| 9.3 | 整课助教提交详情 | 能查看答案、附件、判题任务；编程分 20，附件显示文件名 | `09-04` | `GET /api/v1/teacher/submissions/2` 200；`judge-jobs` 200 | 部分通过：客观题仍显示“无文本答案”，代码换行丢失 |
| 9.4 | 整课助教人工批阅 | 简答题保存 8 分，文件上传题保存 7 分；最终分数 55/60 | `09-05` | `POST /answers/3/grade` 200；`POST /answers/4/grade` 200 | 通过 |
| 9.5 | 整课助教提交级重判 | 确认弹窗清楚，但确认后后端 403；页面无错误提示 | `09-06`、`09-07` | `POST /teacher/submissions/2/judge-jobs/requeue` 403 `当前用户无权重判该提交` | 权限入口缺陷 |
| 9.6 | 整课助教成绩册 | 可查看学生 A 55、学生 B 0、平均分 27.5；发布/导出/调分入口可见 | `09-08`、`09-09`、`09-10` | `GET /gradebook` 200；`GET /gradebook/report` 200 | 部分通过 |
| 9.7 | 整课助教导出与导入模板 | 导出 Excel 返回 403 无 UI 错误；下载导入模板成功 | `09-11` | `GET /gradebook/export` 403；`GET /grades/import-template` 200 | 部分通过 |
| 9.8 | 整课助教批量调分 | 表单和确认弹窗可用，但确认后后端 403；页面无错误提示 | `09-12`、`09-13` | `POST /grades/batch-adjust` 403 `当前用户无权覆盖成绩` | 权限入口缺陷 |
| 9.9 | 整课助教发布成绩 | 确认弹窗清楚，但确认后后端 403；页面无错误提示 | `09-14`、`09-15` | `POST /grades/publish` 403 `当前用户无权发布成绩` | 权限入口缺陷 |
| 9.10 | 主讲教师成绩册与导出 | 主讲教师可查看相同成绩册，导出 Excel 成功下载 `gradebook-offering-1.csv` | `09-16` | `GET /gradebook/export` 200 | 通过 |
| 9.11 | 主讲教师发布成绩 | 确认弹窗说明学生可见；发布接口 200，后端 `gradePublished=true` | `09-17`、`09-18` | `POST /grades/publish` 200；刷新成绩册 200 | 通过；页面无明显“已发布”状态，按钮仍显示“发布成绩” |
| 9.12 | 班级助教本班提交列表 | 班级助教工作台显示 `TA`、教学班 1；可查看本班学生 A 提交，得分 55 | `09-19`、`09-20` | `GET /api/v1/me/courses` 200 返回 `roles:["TA"]`、`classes:[BL-CLASS-A]`；提交列表 200 | 本班可见通过；无第二教学班，未覆盖他班负例 |

### 阶段 10：学生反馈闭环

| 步骤 | 页面 / 动作 | 页面状态 | 截图 | 控制台 / 网络 | 结果 |
| --- | --- | --- | --- | --- | --- |
| 10.1 | 学生 A 工作台 | 登录成功；课程卡仍显示 `草稿` | `10-01` | 学生工作台接口 200 | 部分通过：课程状态延续错误 |
| 10.2 | 学生 A 成绩页 | 选择课程后显示 `闭环综合作业一` 55/60、状态“已发布” | `10-02`、`10-03` | `GET /api/v1/me/course-offerings/1/gradebook` 200，`totalFinalScore=55`、`gradePublished=true` | 通过 |
| 10.3 | 学生 A 提交详情反馈 | 各题分数和反馈可见；附件和判题结果可见 | `10-04` | `GET /api/v1/me/submissions/2` 200；`judge-jobs` 200 | 部分通过：客观题/文件题/代码展示问题仍在 |
| 10.4 | 学生 A 通知中心 | 出现成绩发布、评测完成、作业发布三条通知 | `10-05` | `GET /api/v1/me/notifications` 200，`total=3` | 通过 |
| 10.5 | 学生 B 成绩隔离 | 选择课程后只显示学生 B 自己状态：0/60、已发布、未提交 | `10-06` | `GET /api/v1/me/course-offerings/1/gradebook` 200 | 通过 |
| 10.6 | 学生 B 越权访问学生 A 提交 | 直接访问提交 2 仍被拒绝；页面显示“当前用户无权查看该提交” | `10-07` | `/api/v1/me/submissions/2` 403；`/judge-jobs` 403 | 通过 |

### 阶段 11：管理员审计与收尾

| 步骤 | 页面 / 动作 | 页面状态 | 截图 | 控制台 / 网络 | 结果 |
| --- | --- | --- | --- | --- | --- |
| 11.1 | 管理员工作台 | 治理概览可进入；有平台配置和治理模块入口 | `11-01` | `GET /api/v1/admin/platform-config/current` 200 | 通过；首页不展示业务运营统计 |
| 11.2 | 审计日志列表 | 可见成绩发布允许、助教发布拒绝、学生越权授权拒绝、登录/退出等记录 | `11-02` | `GET /api/v1/admin/audit-logs?page=1&pageSize=20` 200 | 通过 |
| 11.3 | 审计日志详情 | `GRADE_PUBLISH` 详情显示 `permissionCode=grade.publish`、`reason=ALLOW`、`initialPublication=true` | `11-03` | 审计列表响应含完整 metadata | 通过 |
| 11.4 | 工作区状态 | `server/`、`web/` 干净；`docs/` 仅有本报告和截图目录未跟踪 | 不适用 | `just status`：`server` dirty 0、`web` dirty 0、`docs` dirty 2；根目录非 git 仓库 | 通过 |

## 4. 截图索引

| 编号 | 文件 | 说明 |
| --- | --- | --- |
| 01-01 | `01-01-admin-login-page.png` | 管理员登录页 |
| 01-02 | `01-02-admin-dashboard.png` | 管理员治理工作台 |
| 01-03 | `01-03-admin-platform-config-initial.png` | 平台配置初始状态 |
| 01-04 | `01-04-admin-platform-config-saved.png` | 平台配置保存后状态 |
| 01-04b | `01-04b-admin-platform-config-saved-viewport.png` | 平台配置保存后视口复核 |
| 01-05 | `01-05-admin-org-root.png` | 组织管理根节点 |
| 01-06 | `01-06-admin-org-create-college-dialog.png` | 创建学院组织弹窗 |
| 01-07 | `01-07-admin-org-college-detail.png` | 学院组织详情 |
| 01-08 | `01-08-admin-org-course-detail.png` | 课程组织详情 |
| 01-09 | `01-09-admin-org-class-detail.png` | 班级组织详情 |
| 01-10 | `01-10-admin-org-duplicate-root-error.png` | 重复根节点错误提示 |
| 01-11 | `01-11-admin-users-initial.png` | 用户管理初始列表 |
| 01-12 | `01-12-admin-user-create-dialog.png` | 创建用户弹窗 |
| 01-13 | `01-13-admin-users-created.png` | 测试用户创建后列表 |
| 01-14 | `01-14-admin-auth-explain-initial.png` | 权限说明初始页 |
| 01-15 | `01-15-admin-auth-permission-dropdown.png` | 权限下拉选项 |
| 01-16 | `01-16-admin-terms-empty.png` | 学期管理空状态 |
| 01-17 | `01-17-admin-term-created.png` | 闭环学期创建后状态 |
| 01-18 | `01-18-admin-course-catalogs-empty.png` | 课程模板空状态 |
| 01-19 | `01-19-admin-course-catalog-created.png` | 课程模板创建后状态 |
| 01-20 | `01-20-admin-course-offerings-empty.png` | 开课管理空状态 |
| 01-21 | `01-21-admin-course-offering-no-teacher-options.png` | 新增开课教师候选为空 |
| 01-22 | `01-22-admin-user-teacher-profile-saved.png` | 教师档案保存后状态 |
| 01-23 | `01-23-admin-course-offering-teacher-still-empty-after-profile.png` | 补齐教师档案后候选仍为空 |
| 01-24 | `01-24-admin-course-offering-teacher-options-500-empty.png` | 教师候选接口 500 后仍显示暂无选项 |
| 01-25 | `01-25-admin-course-offering-form-filled.png` | 最小绕过后开课表单填写完成 |
| 01-26 | `01-26-admin-course-offering-created-list.png` | 开课创建成功后列表 |
| 01-27 | `01-27-admin-course-offering-detail.png` | 开课详情 |
| 02-01 | `02-01-teacher-dashboard.png` | 主讲教师工作台 |
| 02-02 | `02-02-teacher-my-courses.png` | 主讲教师我的课程 |
| 02-03 | `02-03-teacher-course-workbench-empty-class.png` | 课程工作台初始状态 |
| 02-04 | `02-04-teacher-course-class-created.png` | 教学班创建后课程工作台 |
| 02-05 | `02-05-teacher-announcement-created.png` | 公告发布后状态 |
| 02-06 | `02-06-teacher-resource-uploaded.png` | 资源上传后列表 |
| 02-07 | `02-07-teacher-discussion-created.png` | 讨论创建后列表 |
| 02-08 | `02-08-teacher-discussion-detail.png` | 讨论详情 |
| 02-09 | `02-09-teacher-lab-created-draft.png` | 实验草稿创建后状态 |
| 02-10 | `02-10-teacher-lab-published.png` | 实验发布后状态 |
| 03-01 | `03-01-teacher-members-student-added-class-column-empty.png` | 主讲教师成员管理：学生 A 添加后班级列为空 |
| 03-02 | `03-02-class-ta-missing-class-validation.png` | 班级助教未选教学班的表单校验 |
| 03-03 | `03-03-members-no-auto-refresh-after-dialog-close.png` | 新增多个成员后关闭弹窗，背景列表未自动刷新 |
| 03-04 | `03-04-members-final-class-column-empty.png` | 重新导航后 5 名成员出现，但有班级成员的班级列仍为空 |
| 03-05 | `03-05-offering-ta-root-redirect-stuck.png` | 整课助教补档前登录后卡在根路径跳转页 |
| 03-06 | `03-06-offering-ta-teacher-courses-unauthorized.png` | 整课助教补档前直接访问教师课程页被拒绝 |
| 03-07 | `03-07-admin-users-profiles-completed.png` | 管理员补齐 TA/学生档案后的用户列表 |
| 03-08 | `03-08-offering-ta-dashboard.png` | 整课助教补档后进入教师工作台 |
| 03-09 | `03-09-offering-ta-members-write-actions-visible.png` | 整课助教成员管理写操作可见 |
| 03-10 | `03-10-offering-ta-admin-unauthorized.png` | 整课助教访问管理端被拒绝 |
| 03-11 | `03-11-class-ta-dashboard-role-mismatch.png` | 班级助教课程聚合角色显示为 `OFFERING_TA` |
| 03-12 | `03-12-class-ta-course-workbench-overbroad-actions.png` | 班级助教课程工作台显示新增教学班入口 |
| 03-13 | `03-13-class-ta-members-class-scope-write-actions.png` | 班级助教成员页范围部分正确但写操作可见 |
| 03-14 | `03-14-class-ta-admin-unauthorized.png` | 班级助教访问管理端被拒绝 |
| 04-01 | `04-01-question-form-type-list-missing-specific-fields.png` | 题库新增题目弹窗题型列表与缺失专属字段 |
| 04-02 | `04-02-single-choice-create-400-no-ui-error.png` | 单选题创建 400 但 UI 无错误提示 |
| 04-03 | `04-03-essay-question-created.png` | 简答题创建成功并展示在题库列表 |
| 04-04 | `04-04-file-question-create-400-no-config-fields.png` | 文件上传题缺文件数量配置导致 400 |
| 04-05 | `04-05-programming-question-create-400-no-language-fields.png` | 编程题缺支持语言配置导致 400 |
| 04-06 | `04-06-python-judge-environment-created.png` | Python 3 判题环境创建成功 |
| 04-07 | `04-07-judge-environment-create-form-stale-values.png` | 第二次新增判题环境表单残留上一次值 |
| 04-08 | `04-08-two-judge-environments-created.png` | Python 与 C++17 判题环境列表 |
| 04-09 | `04-09-judge-environment-include-archived.png` | 包含归档后显示已归档环境 |
| 05-01 | `05-01-assignment-create-filled-five-types.png` | 创建作业页配置五种题型、总分 60、可用 Python 环境模板 |
| 05-02 | `05-02-assignment-create-400-no-ui-error.png` | 首次创建作业返回 400 但页面无错误提示 |
| 05-03 | `05-03-assignment-create-stdin-workaround-filled.png` | 通过页面为编程题测试用例 stdin 填入最小绕过值 |
| 05-04 | `05-04-assignment-list-draft-total-empty.png` | 作业列表草稿状态，列表总分显示“暂无” |
| 05-05 | `05-05-assignment-publish-confirm-dialog.png` | 发布作业确认弹窗 |
| 05-06 | `05-06-assignment-list-published-total-empty.png` | 发布后作业状态为“已发布”，但总分仍显示“暂无” |
| 06-01 | `06-01-student-a-dashboard.png` | 学生 A 工作台课程和待办入口 |
| 06-02 | `06-02-student-a-course-detail.png` | 学生 A 课程详情：公告、资源、讨论可见 |
| 06-03 | `06-03-student-a-assignments-list.png` | 学生 A 作业列表：已发布作业可见但总分“暂无” |
| 06-04 | `06-04-student-a-assignment-detail-empty.png` | 学生 A 作业详情五类答题控件空状态 |
| 06-05 | `06-05-student-a-structured-answers-file-uploaded.png` | 学生 A 填写结构化答案并上传附件 |
| 06-06 | `06-06-student-a-draft-restored-after-refresh.png` | 刷新后恢复本地草稿 |
| 07-01 | `07-01-student-a-programming-workspace-initial.png` | 编程工作区初始状态，文件树为空但编辑器打开 `main.py` |
| 07-02 | `07-02-student-a-programming-code-saved.png` | 普通键盘编辑后保存为空代码的风险证据 |
| 07-03 | `07-03-student-a-programming-code-injected-workaround.png` | 记录阻塞后通过 Monaco model 注入代码继续审计 |
| 07-04 | `07-04-student-a-programming-code-saved-after-workaround.png` | 绕过后保存成功，代码持久化 |
| 07-05 | `07-05-student-a-programming-sample-run-result.png` | 样例运行 `WRONG_ANSWER`，输出差异解释不足 |
| 07-06 | `07-06-student-a-programming-sample-run-accepted.png` | 样例运行 `ACCEPTED` |
| 07-07 | `07-07-student-a-programming-file-menu.png` | 文件菜单打开，新建文件入口可见 |
| 07-08 | `07-08-student-a-programming-new-file-created.png` | 多文件禁用场景下 UI 仍创建本地 `helper.py` |
| 07-09 | `07-09-student-a-programming-after-refresh-helper-removed.png` | 刷新后后端状态恢复，`helper.py` 消失 |
| 07-10 | `07-10-student-a-programming-history-panel.png` | 历史版本侧栏被右侧裁切 |
| 07-11 | `07-11-student-a-programming-reset-confirm-dialog.png` | 重置模板确认弹窗 |
| 07-12 | `07-12-student-a-programming-submit-click-result.png` | IDE 内提交确认弹窗 |
| 07-13 | `07-13-student-a-programming-submit-400-no-navigation.png` | IDE 内提交 400 后页面无错误、不跳转 |
| 08-01 | `08-01-student-a-assignment-before-whole-submit.png` | 整份作业提交前答案保留 |
| 08-02 | `08-02-student-a-submission-detail-initial.png` | 学生 A 提交详情初始状态 |
| 08-03 | `08-03-student-a-submission-detail-after-refresh-score-still-missing.png` | 判题成功后刷新，提交详情仍未同步编程题分数 |
| 08-04 | `08-04-student-b-cannot-view-student-a-submission.png` | 学生 B 访问学生 A 提交被 403 拒绝 |
| 08-05 | `08-05-student-b-assignments-own-state.png` | 学生 B 自己的作业列表状态 |
| 09-01 | `09-01-offering-ta-dashboard.png` | 整课助教工作台，课程卡角色与状态展示 |
| 09-02 | `09-02-offering-ta-submissions-list.png` | 整课助教提交管理初始列表 |
| 09-03 | `09-03-offering-ta-submissions-after-filters.png` | 整课助教筛选课程/作业后的提交列表 |
| 09-04 | `09-04-offering-ta-submission-detail.png` | 整课助教提交详情与题型展示 |
| 09-05 | `09-05-offering-ta-manual-grading-saved.png` | 整课助教人工批阅保存后总分 55/60 |
| 09-06 | `09-06-offering-ta-rejudge-confirm-dialog.png` | 整课助教提交级重判确认弹窗 |
| 09-07 | `09-07-offering-ta-rejudge-403-no-ui-error.png` | 整课助教重判 403 后页面无错误反馈 |
| 09-08 | `09-08-offering-ta-gradebook-initial.png` | 整课助教成绩册初始状态 |
| 09-09 | `09-09-offering-ta-gradebook-course-selected.png` | 整课助教成绩册选择课程后状态 |
| 09-10 | `09-10-offering-ta-gradebook-assignment-selected.png` | 整课助教成绩册选择作业后成绩数据 |
| 09-11 | `09-11-offering-ta-gradebook-export-403-no-ui-error.png` | 整课助教导出成绩册 403 后无 UI 错误 |
| 09-12 | `09-12-offering-ta-bulk-adjust-attempt.png` | 整课助教批量调分表单 |
| 09-13 | `09-13-offering-ta-bulk-adjust-403-no-ui-error.png` | 整课助教批量调分 403 后无 UI 错误 |
| 09-14 | `09-14-offering-ta-publish-grades-confirm-dialog.png` | 整课助教发布成绩确认弹窗 |
| 09-15 | `09-15-offering-ta-publish-grades-403-no-ui-error.png` | 整课助教发布成绩 403 后无 UI 错误 |
| 09-16 | `09-16-teacher-gradebook-assignment-selected.png` | 主讲教师成绩册选择作业后状态 |
| 09-17 | `09-17-teacher-publish-grades-confirm-dialog.png` | 主讲教师发布成绩确认弹窗 |
| 09-18 | `09-18-teacher-grades-published.png` | 主讲教师发布成绩成功后成绩册页面 |
| 09-19 | `09-19-class-ta-dashboard-before-submissions.png` | 班级助教复测工作台，角色与教学班范围 |
| 09-20 | `09-20-class-ta-submissions-after-filters.png` | 班级助教本班提交列表 |
| 10-01 | `10-01-student-a-dashboard-after-grade-publish.png` | 学生 A 成绩发布后工作台 |
| 10-02 | `10-02-student-a-grades-published.png` | 学生 A 成绩页初始状态 |
| 10-03 | `10-03-student-a-grades-course-selected.png` | 学生 A 选择课程后查看已发布成绩 |
| 10-04 | `10-04-student-a-submission-detail-after-grade-publish.png` | 学生 A 成绩发布后提交详情与反馈 |
| 10-05 | `10-05-student-a-notifications-after-grade-publish.png` | 学生 A 通知中心成绩发布通知 |
| 10-06 | `10-06-student-b-grades-own-state.png` | 学生 B 只能看到自己的未提交成绩状态 |
| 10-07 | `10-07-student-b-cannot-view-student-a-submission-after-publish.png` | 成绩发布后学生 B 仍不能查看学生 A 提交 |
| 11-01 | `11-01-admin-dashboard-after-business-loop.png` | 管理员工作台业务闭环后状态 |
| 11-02 | `11-02-admin-audit-logs-initial.png` | 管理员审计日志列表 |
| 11-03 | `11-03-admin-audit-grade-publish-detail.png` | 成绩发布审计日志详情 |

## 5. 功能通过项列表

- 平台 bootstrap 管理员登录、平台基础配置、组织节点创建、用户创建、学期创建、课程模板创建均可通过真实 UI 完成。
- 解除 BUG-20260607-001 后，管理员可通过真实 UI 创建开课实例并进入开课详情。
- 主讲教师可登录、看到课程、创建教学班、发布公告、上传资源、创建讨论、创建并发布实验。
- 主讲教师可通过成员管理添加整课助教、班级助教、学生 A、学生 B；后端成员添加接口均返回 `successCount=1`。
- TA/学生档案可通过管理员用户详情页保存，`PUT /api/v1/admin/users/{id}/profile` 返回 200。
- 整课助教补齐教师档案后可进入教师工作台、课程工作台和成员管理页；访问管理端被拒绝。
- 班级助教补齐教师档案后可进入教师工作台；成员页读范围只显示本班学生和自己；访问管理端被拒绝。
- 题库简答题基础入库可用，`POST /question-bank/questions` 返回 201。
- 判题环境 Python 3、C++17 基础配置可创建；编辑、归档、包含归档筛选可用。
- 教师可在作业创建页直接配置单选、多选、简答、文件上传、编程题并创建结构化作业；发布确认弹窗和发布接口可用。
- 学生 A 可看到已发布作业，作业详情展示单选、多选、简答、文件上传、编程题五类控件。
- 学生 A 可上传作业附件，刷新后本地草稿能恢复客观题、简答答案和附件状态。
- 编程工作区保存、样例运行、历史记录、重置确认等基础入口存在；通过记录后的最小绕过可验证样例运行 `ACCEPTED`。
- 学生 A 通过整份作业提交入口可提交 5 题答案，提交响应返回提交 ID 2 和提交编号。
- 学生 B 直接访问学生 A 提交详情被 403 拒绝，页面提示“当前用户无权查看该提交”；学生 B 作业列表不泄露学生 A 的提交状态。
- 整课助教可查看提交列表、提交详情和成绩册，并可保存简答题、文件上传题的人工评分；学生 A 最终分数更新为 55/60。
- 主讲教师可导出成绩册并发布成绩；发布接口返回 `gradePublished=true`，学生端成绩页随后可见 55/60 已发布成绩。
- 学生 A 可在成绩页、提交详情和通知中心看到成绩发布、人工反馈和评测完成信息。
- 学生 B 成绩页只显示自己的 0/60 未提交状态，成绩发布后仍不能越权访问学生 A 提交。
- 管理员审计日志可记录教师成绩发布允许、助教发布/调分拒绝、学生越权访问拒绝等关键安全事件，并可查看 `GRADE_PUBLISH` 详情 metadata。

## 6. 缺陷列表

### BUG-20260607-001：新增开课主讲教师候选加载 500，管理员无法通过 UI 创建开课

- 严重级别：Blocker
- 影响阶段：阶段 1.8 开课管理，阻塞后续教师课程、成员、作业、提交和成绩闭环。
- 复现步骤：
  1. 清库后通过 UI 创建 `BL-TEACHER`。
  2. 在用户详情页将身份类型保存为“教师”，并将组织成员关系替换为闭环测试学院。
  3. 打开 `/admin/course-offerings`，点击“新增开课”。
- 实际结果：弹窗“主讲教师”区域只显示“暂无可选项”，没有错误说明；开课表单无法选择教师。
- 网络证据：`GET /api/v1/admin/users?identityType=TEACHER&pageSize=100` 返回 500，响应体为 `{"code":"INTERNAL_ERROR","message":"服务内部发生未预期错误"}`。
- 后端日志：`.aubb/run/logs/server.log` 中 `UserAdministrationApplicationService.lambda$listUsers$0(UserAdministrationApplicationService.java:254)` 触发 `NullPointerException`，对应 `primaryOrgById.get(user.getPrimaryOrgUnitId())`。
- 截图证据：`01-23-admin-course-offering-teacher-still-empty-after-profile.png`、`01-24-admin-course-offering-teacher-options-500-empty.png`。
- UI 问题：前端将候选加载失败呈现为“暂无可选项”，用户无法区分“没有教师数据”和“接口失败”。

### BUG-20260607-002：成员表后端返回班级名称，前端班级列为空

- 严重级别：Major
- 影响阶段：阶段 3 成员管理、后续班级助教范围判断。
- 复现步骤：
  1. 主讲教师在 `/teacher/courses/1/members` 添加学生或班级助教，选择 `闭环测试 1 班 (BL-CLASS-A)`。
  2. 重新导航到成员管理页。
- 实际结果：学生 A、学生 B、班级助教的“教学班”列为空或直接显示为“未绑定”，用户无法确认成员是否已绑定教学班。
- 期望结果：表格应展示 `闭环测试 1 班` 或 `BL-CLASS-A`。
- 网络证据：`GET /api/v1/teacher/course-offerings/1/members?page=1&pageSize=20` 返回的学生/班级助教记录含 `teachingClassId=1`、`classCode="BL-CLASS-A"`、`className="闭环测试 1 班"`。
- 截图证据：`03-04-members-final-class-column-empty.png`、`03-13-class-ta-members-class-scope-write-actions.png`。

### BUG-20260607-003：班级助教课程聚合接口将班级助教升格为整课助教

- 严重级别：Critical
- 影响阶段：阶段 3.10、3.11，影响班级助教权限边界。
- 复现步骤：
  1. 将 `BL-TA-CLASS` 作为 `TA` 添加到课程，绑定 `teachingClassId=1`。
  2. 给该用户保存教师档案后登录。
  3. 打开教师工作台。
- 实际结果：课程卡片显示 `OFFERING_TA`，教学班数显示 `0`；`GET /api/v1/me/courses` 返回 `roles:["OFFERING_TA"]`、`classes:[]`。
- 期望结果：应返回班级助教角色及授权教学班，前端应据此展示班级范围。
- 截图证据：`03-11-class-ta-dashboard-role-mismatch.png`。
- 风险：如果后续提交、成绩、作业接口复用该聚合角色，班级助教可能获得整课范围能力。
- 复测补充：阶段 9.12 重新登录 `BL-TA-CLASS` 后，当前 `GET /api/v1/me/courses` 返回 `roles:["TA"]` 与 `classes:[BL-CLASS-A]`，提交列表本班可见通过。该问题需要开发侧确认阶段 3 的错误响应是否由档案补齐前后状态、缓存或会话刷新触发。

### BUG-20260607-004：新增成员成功后弹窗和列表状态未及时复位

- 严重级别：Major
- 影响阶段：阶段 3.3、3.5。
- 复现步骤：
  1. 在“添加成员”弹窗中成功添加整课助教。
  2. 不关闭弹窗，切换角色、用户 ID 和教学班准备添加下一名成员。
  3. 添加多名成员后关闭弹窗。
- 实际结果：弹窗仍显示上一轮“添加成功 1 人，失败 0 人”；关闭弹窗后背景成员列表不自动刷新，仍显示旧成员集合。
- 期望结果：修改输入时应清理旧结果；添加成功后应刷新成员列表或提供明确刷新提示。
- 截图证据：`03-03-members-no-auto-refresh-after-dialog-close.png`、`03-04-members-final-class-column-empty.png`。

### BUG-20260607-005：未补齐档案的课程助教账号登录后缺少明确引导

- 严重级别：Major
- 影响阶段：阶段 3.7，影响新账号首次使用。
- 复现步骤：
  1. 创建 `BL-TA-COURSE` 并加入课程成员，但暂不保存教师档案。
  2. 使用该账号登录。
- 实际结果：根路径停留在“正在跳转到工作区...”；直接访问 `/teacher/courses` 进入 Unauthorized。
- 期望结果：应提示账号缺少教师/学生档案、角色未配置或联系管理员，而不是无限跳转。
- 截图证据：`03-05-offering-ta-root-redirect-stuck.png`、`03-06-offering-ta-teacher-courses-unauthorized.png`。

### BUG-20260607-006：题库新增题目表单无法配置后端必需的题型专属字段

- 严重级别：Blocker
- 影响阶段：阶段 4.3、4.4、4.6、4.7，并阻塞后续包含客观题、文件题、编程题的完整作业闭环。
- 复现步骤：
  1. 打开 `/teacher/courses/1/question-bank`。
  2. 点击“新增题目”。
  3. 选择单选题、多选题、文件上传题或编程题，填写基础字段并点击“创建”。
- 实际结果：
  - 单选/多选：后端返回 `QUESTION_BANK_OPTIONS_INVALID`，提示“客观题至少需要两个选项”。
  - 文件上传题：后端返回 `QUESTION_BANK_FILE_COUNT_INVALID`，提示“文件题必须配置正整数文件数量上限”。
  - 编程题：后端返回 `QUESTION_BANK_LANGUAGES_REQUIRED`，提示“编程题必须至少配置一种支持语言”。
  - 前端弹窗没有对应配置字段，也没有展示后端错误消息。
- 期望结果：不同题型应出现对应配置区，至少包括选项/答案、文件数量/类型/大小、编程语言/模板/入口文件/测试点/判题配置。
- 截图证据：`04-01-question-form-type-list-missing-specific-fields.png`、`04-02-single-choice-create-400-no-ui-error.png`、`04-04-file-question-create-400-no-config-fields.png`、`04-05-programming-question-create-400-no-language-fields.png`。

### BUG-20260607-007：判题环境新增弹窗未在二次打开时清空上一条数据

- 严重级别：Major
- 影响阶段：阶段 4.9。
- 复现步骤：
  1. 新增 `闭环 Python 3 环境` 并提交成功。
  2. 再次点击“新增配置”。
- 实际结果：弹窗仍带出上一次 Python 环境的编码、名称、语言版本、说明和运行命令。
- 期望结果：新增弹窗应展示空表单或明确的默认值，不能残留上一条已提交数据。
- 截图证据：`04-07-judge-environment-create-form-stale-values.png`。

### BUG-20260607-008：作业编程题测试用例 stdin 允许留空，但后端要求非空且前端不显示错误

- 严重级别：Major
- 影响阶段：阶段 5.3，阻塞教师创建无输入编程题作业。
- 复现步骤：
  1. 打开 `/teacher/assignments/create?offeringId=1`。
  2. 添加编程题，启用样例试运行，配置期望输出与测试用例期望输出。
  3. 将“标准输入 (stdin)”留空并点击“创建作业”。
- 实际结果：页面停留在创建页，没有字段级错误、弹窗错误或 toast；console 只有 400 资源加载失败。
- 网络证据：`POST /api/v1/teacher/course-offerings/1/assignments` 返回 400，响应体为 `{"detail":"Invalid request content.","instance":"/api/v1/teacher/course-offerings/1/assignments","status":400,"title":"Bad Request"}`。
- 根因证据：后端 `AssignmentTeacherController.ProgrammingJudgeCaseRequest.stdinText` 标注 `@NotBlank`；前端请求体提交 `judgeCases[0].stdinText=""`。
- 期望结果：若无输入编程题是合法场景，应允许空 stdin；若不合法，前端应在测试用例 stdin 字段旁提示必填，并展示后端字段错误。
- 绕过策略：通过页面将样例输入和测试用例 stdin 填为 `ignored` 后，第二次创建返回 201。
- 截图证据：`05-02-assignment-create-400-no-ui-error.png`、`05-03-assignment-create-stdin-workaround-filled.png`。

### BUG-20260607-009：作业列表总分列显示“暂无”，但创建/发布响应已有总分 60

- 严重级别：Major
- 影响阶段：阶段 5.5、5.7、6.3、8.7，影响教师核对作业卷面和学生核对作业要求。
- 复现步骤：
  1. 创建包含 5 题、总分 60 的作业。
  2. 返回 `/teacher/assignments?offeringId=1`。
  3. 发布作业后再次查看列表。
- 实际结果：列表“总分”列持续显示“暂无”。
- 网络证据：创建响应与发布响应均包含 `paper.totalScore=60`；列表接口 `GET /api/v1/teacher/course-offerings/1/assignments?page=1&pageSize=20` 返回的作业项中 `paper=null`，导致列表没有可展示总分。
- 期望结果：列表应展示作业总分，或后端列表摘要直接返回 `totalScore`。
- 截图证据：`05-04-assignment-list-draft-total-empty.png`、`05-06-assignment-list-published-total-empty.png`、`06-03-student-a-assignments-list.png`、`08-05-student-b-assignments-own-state.png`。

### BUG-20260607-010：学生课程卡片显示课程为“草稿”，但学生已可访问已发布作业

- 严重级别：Major
- 影响阶段：阶段 6.1、6.3，影响学生对课程/作业开放状态的理解。
- 复现步骤：
  1. 教师发布作业 `闭环综合作业一`。
  2. 学生 A 登录并查看工作台、课程列表或作业列表。
- 实际结果：学生端课程卡片仍显示 `草稿`，但作业列表中已发布作业可见且可开始做题。
- 期望结果：学生端应展示与学生可操作状态一致的课程/开课状态，或隐藏教师侧草稿状态。
- 截图证据：`06-01-student-a-dashboard.png`、`06-03-student-a-assignments-list.png`。

### BUG-20260607-011：学生课程详情缺少作业和实验聚合入口

- 严重级别：Major
- 影响阶段：阶段 6.2，影响学生从课程详情进入核心学习任务。
- 复现步骤：学生 A 打开课程详情页。
- 实际结果：页面展示公告、资源、讨论，但没有直接聚合的作业、实验入口或任务概览。
- 期望结果：课程详情应提供作业、实验、资源、讨论等核心学习活动的稳定入口。
- 截图证据：`06-02-student-a-course-detail.png`。

### BUG-20260607-012：作业附件上传成功后只显示附件编号，不显示文件名

- 严重级别：Major
- 影响阶段：阶段 6.5、8.5，影响学生提交前后核对附件。
- 复现步骤：
  1. 学生 A 在作业文件上传题上传 `resource-bl-readme.txt`。
  2. 查看作业详情和提交详情。
- 实际结果：上传接口返回 `originalFilename="resource-bl-readme.txt"`，页面仅显示“附件 #1”或在提交详情中将附件放到独立区域，题目卡片仍显示“无文本答案”。
- 期望结果：文件上传题应在题目区域展示原始文件名、大小、上传状态和下载/删除入口。
- 截图证据：`06-05-student-a-structured-answers-file-uploaded.png`、`08-02-student-a-submission-detail-initial.png`。

### BUG-20260607-013：编程工作区初始文件树为空，但编辑器打开 `main.py`

- 严重级别：Major
- 影响阶段：阶段 7.1，影响 IDE 初始可理解性。
- 复现步骤：学生 A 从作业详情进入编程题工作区。
- 实际结果：工作区响应 `files=[]`、`entryFilePath=main.py`；UI 编辑器 tab 打开 `main.py`，但左侧文件树为空。
- 期望结果：即使后端尚无保存文件，也应在文件树中展示入口文件或模板文件，避免用户误以为无文件。
- 截图证据：`07-01-student-a-programming-workspace-initial.png`。

### BUG-20260607-014：编程编辑器普通键盘输入与保存存在空代码持久化风险

- 严重级别：Critical
- 影响阶段：阶段 7.2，可能导致学生误以为代码已保存但后端保存为空。
- 复现步骤：
  1. 使用 Playwright MCP 在 Monaco 编辑器中通过键盘输入 Python 代码。
  2. 点击保存。
  3. 检查页面 model 和保存响应。
- 实际结果：UI 呈现编辑态，但 `window.monaco.editor.getModels()[0].getValue()` 仍为空；保存请求返回空 `codeText` / 空文件内容。
- 期望结果：可见编辑内容必须与 Monaco model 和保存请求一致；保存空内容应有明确保护和反馈。
- 证据说明：本轮主证据来自真实浏览器键盘交互；是否影响人工手动输入仍需后续手工复核，但已经构成自动化可复现的编辑器交互风险。
- 截图证据：`07-02-student-a-programming-code-saved.png`。

### BUG-20260607-015：样例运行对尾随换行过于严格且缺少可理解的输出差异说明

- 严重级别：Major
- 影响阶段：阶段 7.4。
- 复现步骤：
  1. 代码写入 `print('Hello AUBB')`。
  2. 运行样例，期望输出为 `Hello AUBB`。
- 实际结果：执行状态 `SUCCEEDED`，判定 `WRONG_ANSWER`，原因是 stdout 为 `Hello AUBB\n`；页面没有清楚展示期望/实际差异。
- 期望结果：产品规则应明确是否忽略尾随空白；不忽略时应展示可读 diff、实际输出、期望输出和空白字符提示。
- 截图证据：`07-05-student-a-programming-sample-run-result.png`、`07-06-student-a-programming-sample-run-accepted.png`。

### BUG-20260607-016：多文件禁用时 IDE 仍允许新建文件，后端 400 后本地状态发散

- 严重级别：Critical
- 影响阶段：阶段 7.5，影响编程题文件管理和保存。
- 复现步骤：
  1. 在不允许多文件的编程题工作区点击文件 `+`。
  2. 选择“新建文件”，输入 `helper.py`。
- 实际结果：后端 `POST /workspace/operations` 返回 400 `PROGRAMMING_MULTIPLE_FILES_DISABLED`，但 UI 仍出现本地 `helper.py`，后续自动保存继续 400；刷新后本地文件消失。
- 期望结果：禁用多文件时应隐藏/禁用新建文件入口；若后端拒绝，应回滚本地状态并显示错误。
- 截图证据：`07-07-student-a-programming-file-menu.png`、`07-08-student-a-programming-new-file-created.png`、`07-09-student-a-programming-after-refresh-helper-removed.png`。

### BUG-20260607-017：编程历史版本侧栏宽度过窄，内容被裁切

- 严重级别：Major
- 影响阶段：阶段 7.7。
- 复现步骤：学生 A 在编程工作区打开历史版本侧栏。
- 实际结果：侧栏靠右显示，宽度约 98px，版本信息和操作区域被裁切，难以使用。
- 期望结果：历史版本应有稳定宽度、可滚动内容区和清楚的恢复操作。
- 截图证据：`07-10-student-a-programming-history-panel.png`。

### BUG-20260607-018：IDE 内提交只发送编程题答案，结构化作业返回 400 且 UI 无反馈

- 严重级别：Critical
- 影响阶段：阶段 7.9，阻塞学生从编程工作区完成整份作业提交。
- 复现步骤：
  1. 学生 A 已在作业详情填写 5 题答案。
  2. 从编程工作区点击“提交”并确认。
- 实际结果：请求只包含编程题答案；后端返回 `SUBMISSION_ANSWER_SET_INVALID`，提示“当前提交必须覆盖结构化作业中的全部题目”；页面无错误提示、不跳转，确认文案仍暗示提交后进入详情。
- 期望结果：IDE 内提交应回收整份作业草稿并提交全部答案，或文案明确“仅保存/提交编程题”并在结构化作业中禁用该路径；400 必须展示给用户。
- 截图证据：`07-12-student-a-programming-submit-click-result.png`、`07-13-student-a-programming-submit-400-no-navigation.png`。

### BUG-20260607-019：判题任务已 `ACCEPTED` 20/20，但提交详情分数仍停留在 20/60，编程题显示 0 分

- 严重级别：Critical
- 影响阶段：阶段 8.3、8.4，影响成绩正确性和学生反馈闭环。
- 复现步骤：
  1. 学生 A 提交整份作业。
  2. 等待编程题 judge job 返回 `ACCEPTED`、`score=20`、`maxScore=20`。
  3. 刷新提交详情。
- 实际结果：提交详情 `scoreSummary.finalScore` 仍为 20/60；编程题卡片显示 0 分；但 judge job 接口显示编程题已得 20/20。
- 期望结果：编程题判题完成后，提交详情总分和题目分数应同步更新为 40/60（客观题 20 + 编程题 20，简答/文件待人工）。
- 截图证据：`08-02-student-a-submission-detail-initial.png`、`08-03-student-a-submission-detail-after-refresh-score-still-missing.png`。

### BUG-20260607-020：提交详情无法按题型正确展示客观题、附件和代码答案

- 严重级别：Major
- 影响阶段：阶段 8.5、9.3、10.3，影响学生、助教和教师核对提交内容。
- 复现步骤：学生 A 提交后打开 `/student/submissions/2`。
- 实际结果：顶部“答案内容”显示“无文本答案”；客观题卡片显示“无文本答案”而不是 A / A+B；文件题卡片显示“无文本答案”；编程代码换行被压成一行。成绩发布后学生详情仍有同样问题，教师/助教提交详情也存在客观题“无文本答案”和代码换行丢失。
- 期望结果：提交详情应按题型展示选项、附件、代码块、判题结果和人工反馈，代码保留换行格式。
- 截图证据：`08-02-student-a-submission-detail-initial.png`、`08-03-student-a-submission-detail-after-refresh-score-still-missing.png`、`09-04-offering-ta-submission-detail.png`、`10-04-student-a-submission-detail-after-grade-publish.png`。

### BUG-20260607-021：整课助教可见后端拒绝的成绩操作，403 后页面无反馈

- 严重级别：Major
- 影响阶段：阶段 9.5、9.7、9.8、9.9，影响助教批改和成绩处理流程。
- 复现步骤：
  1. 使用 `BL-TA-COURSE` 登录。
  2. 在提交详情点击“重判”，在成绩册点击导出、批量调分、发布成绩。
  3. 在确认弹窗中确认操作。
- 实际结果：重判、成绩册导出、批量调分、发布成绩入口均对整课助教可见；确认后后端返回 403，但页面不展示明确错误、权限不足原因或后续处理建议。
- 网络证据：
  - `POST /api/v1/teacher/submissions/2/judge-jobs/requeue` 403，消息 `当前用户无权重判该提交`。
  - `GET /api/v1/teacher/course-offerings/1/gradebook/export` 403，消息 `当前用户无权导出成绩册`。
  - `POST /api/v1/teacher/assignments/1/grades/batch-adjust` 403，消息 `当前用户无权覆盖成绩`。
  - `POST /api/v1/teacher/assignments/1/grades/publish` 403，消息 `当前用户无权发布成绩`。
- 期望结果：前端应按角色隐藏或禁用无权限操作；如果入口可见，403 必须转为 toast/弹窗/字段错误，说明当前角色无权执行。
- 截图证据：`09-06-offering-ta-rejudge-confirm-dialog.png`、`09-07-offering-ta-rejudge-403-no-ui-error.png`、`09-11-offering-ta-gradebook-export-403-no-ui-error.png`、`09-13-offering-ta-bulk-adjust-403-no-ui-error.png`、`09-15-offering-ta-publish-grades-403-no-ui-error.png`。

### BUG-20260607-022：成绩发布成功后成绩册缺少已发布状态，按钮仍显示“发布成绩”

- 严重级别：Major
- 影响阶段：阶段 9.11、10.2，影响教师对成绩发布状态的确认。
- 复现步骤：
  1. 使用 `BL-TEACHER` 打开成绩册并选择课程、作业。
  2. 点击“发布成绩”并确认。
  3. 发布成功后查看成绩册页面。
- 实际结果：`POST /api/v1/teacher/assignments/1/grades/publish` 返回 200，刷新成绩册响应显示 `gradePublished=true`、`publishedCount=1`，学生端成绩页也能看到已发布成绩；但教师成绩册页面仍显示“发布成绩”按钮，缺少“已发布”、发布时间、已发布人数或禁用态。
- 期望结果：发布成功后教师端应明确展示已发布状态、发布时间/发布人、学生可见范围，并防止重复点击造成误解。
- 截图证据：`09-17-teacher-publish-grades-confirm-dialog.png`、`09-18-teacher-grades-published.png`、`10-03-student-a-grades-course-selected.png`。

## 7. UI/UX 问题列表

- 管理员用户详情页的“成员关系组织编号”“身份作用域组织编号”只支持数字输入，没有组织搜索/选择器；非技术管理员很难知道应填 `2`、`4` 或课程派生组织 ID。
- 管理员用户列表中，TA/学生补齐档案后“学号/工号”列更新，但“身份”列仍显示 `-`；该列实际像是系统身份而不是档案身份，与筛选器“档案身份/身份角色”文案容易混淆。
- 开课创建弹窗在 1280x800 视口下高度偏大，底部确认按钮需要滚动才能稳定操作。
- 教师课程卡片、课程详情页显示 `学期未配置 · 课程模板未配置`，但管理员开课详情已有有效学期和课程模板，信息不一致。
- 课程工作台缺少讨论和实验的直接聚合入口；本轮讨论详情通过直接 URL 进入。
- 讨论详情页将主帖正文放在“回复”视觉区域下方，主帖/回复层级不清。
- 资源列表“上传者”列为空，上传成功后无法确认责任人。
- 实验中心选择课程后，“全部教学班”视觉上像有效选择，但创建按钮仍禁用，并提示“选择课程和教学班后创建实验”，需要更明确地区分“全部”和“未选择”。
- 成员添加弹窗要求输入数字用户 ID，没有用户搜索、按姓名/学号选择或校验预览。
- 成员添加弹窗切换用户、角色、教学班时不清理旧成功消息，容易误导正在添加的新成员。
- 成员表格教学班列为空，角色列直接跟在学号/工号后，导致用户误以为已显示班级或成员未绑定。
- 教师/TA 顶部身份统一显示“教师”，课程成员角色只在课程卡片中以枚举值出现，缺少“整课助教/班级助教”面向用户的角色说明。
- 题库空状态文案“您可以尝试刷新或执行其他操作”过于泛化，应提示“暂无题目，可点击新增题目”。
- 题库题目列表把分类、类型、标签、分值等内容压在一行中，列间视觉分隔弱；标签顺序也不易读。
- 题库新增题目弹窗对题型切换没有动态字段，也没有显示后端 400 错误消息。
- 判题环境页标题说明写到“资源限制”，列表也有“资源限制”列，但新增/编辑弹窗没有 CPU、内存、时间、镜像、工作目录等资源限制字段。
- 判题环境第二次新增时表单残留上一条配置，容易误创建重复环境。
- 判题环境列表“运行环境”列实际显示配置名称，未展示镜像/容器/运行时路径；“CPU 未限 默认目录”信息不完整。
- 作业创建页长表单把题目基础信息、选项、文件限制、编程限制、样例、语言、测试用例和模板文件全部展开在一个页面，信息层级过深，教师很难在发布前快速核对关键风险项。
- 作业创建页“高级判题配置”文案说明它仅用于兼容旧作业，但按钮尺寸和层级偏弱；普通用户不容易判断是否需要配置。
- 编程题测试用例 stdin 留空时没有即时必填提示，提交失败后也没有错误反馈。
- 作业列表操作列只有图标按钮，虽然有可访问名称，但视觉上缺少 tooltip 或文字说明；新用户需要悬停或试点才能理解编辑、发布、关闭的区别。
- 作业列表总分列显示“暂无”，与创建页总分 60 和发布响应不一致。
- 学生工作台/作业列表同时出现“课程草稿”和“已发布作业可做题”，状态体系冲突。
- 学生课程详情缺少作业、实验的直接聚合入口，学生需要从侧边导航或其他页面进入核心任务。
- 文件上传题上传成功后只显示“附件 #1”，没有原文件名、大小、类型、下载/删除入口，提交前核对成本高。
- 编程工作区文件树和编辑器状态不一致：文件树为空但编辑器已有 `main.py` tab。
- 编程工作区文件 `+` 按钮缺少可访问名称；多文件禁用时仍显示新建文件/目录入口。
- 样例运行错误结果缺少期望输出、实际输出、尾随空白差异的可读解释。
- 编程历史版本侧栏过窄，内容被裁切，无法承担版本恢复功能。
- IDE 内提交确认文案承诺“提交后跳转详情”，但 400 后无错误提示、不跳转，用户无法知道提交失败。
- 提交详情把不同题型统一退化为“无文本答案”，客观题、文件题、编程题的展示格式不符合核对和批改需要。
- 编程代码在提交详情中失去换行格式，无法正常阅读。
- 成绩册和学生成绩页在只有一个课程时仍要求手动选择课程；若没有选择，页面缺少明确的“请选择课程以查看成绩”引导和默认选择策略。
- 整课助教成绩处理入口在无权限时仍可见，确认后没有可见错误，用户只能从网络面板知道后端拒绝。
- 教师成绩发布成功后没有“已发布”状态或发布时间展示，按钮仍显示“发布成绩”，容易误判发布是否成功。
- 管理员工作台业务闭环后仍只展示治理/配置入口，缺少近期作业、提交、判题、成绩发布、权限拒绝等运营统计或异常摘要；关键业务态势只能从审计日志逐条查找。

## 8. 权限问题列表

- 班级助教在 `/api/v1/me/courses` 中被返回为 `OFFERING_TA` 且 `classes=[]`，存在班级权限范围丢失或升格风险。
- 复测补充：阶段 9.12 同一班级助教当前课程聚合响应为 `roles:["TA"]`、`classes:[BL-CLASS-A]`，本班提交列表可见通过；阶段 3 的错误响应仍需查明触发条件。
- 班级助教课程工作台可见“新增教学班”表单，成员页可见“批量导入、添加成员、停用成员、转班成员”等写操作。虽然成员读取范围只显示本班学生和自己，但写操作入口未按班级助教范围收敛。
- 整课助教成员页可见全部成员写操作，是否符合“整课助教”权限需要产品确认；如果整课助教只应协助批改/查看，则当前入口过宽。
- 整课助教可查看提交、保存人工批阅和查看成绩册，但重判、成绩册导出、批量调分、发布成绩均被后端 403 拒绝；前端仍展示入口且 403 后无可见错误，属于权限入口与反馈缺陷。
- 整课助教和班级助教访问 `/admin` 均被 Unauthorized 拒绝，平台治理边界通过。
- 未补齐教师档案但已加入课程成员的助教账号无法进入教师端，缺少明确的角色/档案缺失提示。
- 学生 B 直接访问学生 A 提交详情和判题任务均返回 403，页面给出“当前用户无权查看该提交”，学生间提交隔离通过。
- 学生 B 的作业列表只显示自己的未提交状态，不显示学生 A 的提交编号或成绩，学生间列表隔离通过。
- 管理员审计日志能记录成绩发布允许、助教成绩操作拒绝、学生越权访问拒绝等事件，且 `GRADE_PUBLISH` 详情包含 `permissionCode`、`reason`、`initialPublication`。

## 9. 阻塞与绕过记录

### BLOCK-20260607-001：开课创建因教师候选 500 阻塞

- 阻塞点：无法通过新增开课弹窗选择主讲教师。
- 已完成记录：截图、网络响应、后端异常栈已记录在 BUG-20260607-001。
- 最小绕过策略：仅在本地测试数据库中为本轮 UI 创建的测试用户补充 `primary_org_unit_id`，解除用户列表 NPE 后继续通过真实浏览器验证开课页面。该动作只用于继续审计链路，不视为产品通过项。
- 风险标注：绕过会改变本地测试数据的组织归属，因此后续报告中需要把“用户详情页无法通过 UI 设置主属组织 / 只能输入数字组织编号”作为独立体验问题记录。

### BLOCK-20260607-002：助教账号未补齐教师档案时无法进入教师端

- 阻塞点：`BL-TA-COURSE` 首次登录后停留在根路径跳转页；直接访问教师课程页为 Unauthorized。
- 已完成记录：`03-05`、`03-06` 已截图；登录接口返回 200，但前端没有给出缺少档案或角色配置的明确说明。
- 最小绕过策略：返回管理员用户详情页，通过 UI 为 `BL-TA-COURSE`、`BL-TA-CLASS` 保存教师档案，为 `BL-STU-A`、`BL-STU-B` 保存学生档案。
- 绕过证据：`PUT /api/v1/admin/users/{3,4,5,6}/profile` 均返回 200；补档后整课助教和班级助教均可进入教师端。

### BLOCK-20260607-003：作业创建因编程题测试用例空 stdin 返回 400

- 阻塞点：无输入编程题在 UI 中看起来可提交，但后端请求体校验要求 `judgeCases[].stdinText` 非空。
- 已完成记录：`05-02` 已截图；请求体和响应体已通过 Playwright MCP 网络面板记录；后端 DTO 只读核对完成。
- 最小绕过策略：不改代码、不直接写库，通过作业创建页面把样例输入和测试用例 stdin 填入 `ignored` 后再次提交。
- 绕过证据：第二次 `POST /api/v1/teacher/course-offerings/1/assignments` 返回 201，作业 ID 1；随后 `POST /api/v1/teacher/assignments/1/publish` 返回 200。

### BLOCK-20260607-004：编程编辑器普通键盘输入保存为空，阻塞 IDE 保存/运行审计

- 阻塞点：通过真实浏览器键盘输入代码后，Monaco model 仍为空，保存请求会持久化空代码。
- 已完成记录：`07-02` 已截图；页面 model 和保存响应已核对。
- 最小绕过策略：在记录阻塞后，仅通过当前页面的 Monaco API 设置同一段代码，继续用 UI 的保存、运行、提交按钮验证后续链路。
- 绕过证据：`07-03`、`07-04` 显示代码进入编辑器并保存成功；保存响应包含 `main.py` 内容。

### BLOCK-20260607-005：IDE 内提交只提交编程题答案，无法完成结构化作业提交

- 阻塞点：编程工作区“提交”请求只包含编程题答案，后端要求结构化作业提交覆盖全部题目。
- 已完成记录：`07-12`、`07-13` 已截图；网络响应为 `SUBMISSION_ANSWER_SET_INVALID`。
- 最小绕过策略：返回完整作业详情页，使用整份作业“提交答案”入口提交五题答案。
- 绕过证据：`POST /api/v1/me/assignments/1/submissions` 返回 201，提交 ID 2。

### BLOCK-20260607-006：整课助教无权发布成绩，需切换主讲教师完成发布闭环

- 阻塞点：整课助教可打开发布成绩确认弹窗，但确认后 `POST /api/v1/teacher/assignments/1/grades/publish` 返回 403。
- 已完成记录：`09-14`、`09-15` 已截图；网络响应为 `当前用户无权发布成绩`。
- 最小绕过策略：记录权限入口缺陷后，切换 `BL-TEACHER` 使用同一成绩册页面执行发布成绩。
- 绕过证据：主讲教师 `POST /api/v1/teacher/assignments/1/grades/publish` 返回 200，学生 A 成绩页显示 55/60 已发布。

## 10. 控制台错误和网络失败摘要

- 登录、路由切换和账号切换期间多次出现 `/api/v1/me/notifications/stream` 的 `net::ERR_ABORTED`，表现为 SSE 连接在导航时中断；截至阶段 3 未发现该中断阻塞页面功能。
- 阶段 1 开课教师候选：`GET /api/v1/admin/users?identityType=TEACHER&pageSize=100` 返回 500，是本轮第一个硬阻塞。
- 成员添加：`POST /api/v1/teacher/course-offerings/1/members/batch` 三次返回 200，请求体分别为 `TA + teachingClassId=1`、`OFFERING_TA`、`STUDENT + teachingClassId=1`。
- 成员列表：`GET /api/v1/teacher/course-offerings/1/members?page=1&pageSize=20` 返回 200，响应包含班级字段，但 UI 未展示。
- 班级助教课程聚合：`GET /api/v1/me/courses` 返回 200，但响应将班级助教返回为 `roles:["OFFERING_TA"]`、`classes:[]`。
- 用户档案补齐：`PUT /api/v1/admin/users/{3,4,5,6}/profile` 均返回 200。
- 题库：简答题 `POST /api/v1/teacher/course-offerings/1/question-bank/questions` 返回 201；单选/多选/文件上传/编程题分别因缺选项、缺文件数量、缺支持语言返回 400。
- 判题环境：`POST /api/v1/teacher/course-offerings/1/judge-environment-profiles` 创建 Python 3 和 C++17 均返回 201；编辑 C++17 返回 200；归档后默认列表隐藏，`includeArchived=true` 列表显示归档项。
- 作业创建：首次 `POST /api/v1/teacher/course-offerings/1/assignments` 返回 400，原因是编程题测试用例 `stdinText=""` 与后端 `@NotBlank` 冲突；页面未显示错误。
- 作业创建绕过后：第二次 `POST /api/v1/teacher/course-offerings/1/assignments` 返回 201，响应含 `paper.totalScore=60`、5 题和作业 ID 1。
- 作业发布：`POST /api/v1/teacher/assignments/1/publish` 返回 200，状态变为 `PUBLISHED`；随后列表查询返回 200，但列表项 `paper=null`，前端总分显示“暂无”。
- 学生附件上传：`POST /api/v1/me/assignments/1/submission-artifacts` 返回 201，响应含 `id=1`、`originalFilename="resource-bl-readme.txt"`、`sizeBytes=123`；UI 未展示文件名。
- 编程工作区保存：普通键盘输入后保存响应为空代码；记录后通过 Monaco model 绕过，后续保存响应包含 `import sys\nsys.stdout.write('Hello AUBB')\n`。
- 样例运行：首次 `POST /api/v1/me/assignments/1/programming-workspace/sample-runs` 返回 `WRONG_ANSWER`，stdout 比期望多尾随换行；第二次返回 `ACCEPTED`。
- 文件操作：`POST /api/v1/me/assignments/1/programming-workspace/operations` 新建 `helper.py` 返回 400 `PROGRAMMING_MULTIPLE_FILES_DISABLED`；UI 仍保留本地文件并触发后续自动保存 400。
- IDE 内提交：`POST /api/v1/me/assignments/1/submissions` 返回 400 `SUBMISSION_ANSWER_SET_INVALID`，响应消息为“当前提交必须覆盖结构化作业中的全部题目”；页面无错误反馈。
- 整份作业提交：`POST /api/v1/me/assignments/1/submissions` 返回 201，请求覆盖五题答案；提交 ID 2，提交编号 `SUB-75bcd4377be54ac08867ea9901986d38`。
- 判题任务：`GET /api/v1/me/submissions/2/judge-jobs` 返回 200，编程题 `ACCEPTED`、`score=20`、`maxScore=20`；刷新提交详情后总分仍为 20/60。
- 学生隔离：学生 B 访问 `/api/v1/me/submissions/2` 和 `/judge-jobs` 均返回 403；学生 B 作业列表查询 200，不包含学生 A 提交状态。
- 整课助教人工批阅：`POST /api/v1/teacher/submissions/2/answers/3/grade` 返回 200，保存 8 分简答反馈；`POST /api/v1/teacher/submissions/2/answers/4/grade` 返回 200，保存 7 分文件题反馈；提交详情最终分数 55/60。
- 整课助教成绩权限：重判 `POST /api/v1/teacher/submissions/2/judge-jobs/requeue` 返回 403；成绩册导出 `GET /api/v1/teacher/course-offerings/1/gradebook/export` 返回 403；批量调分 `POST /api/v1/teacher/assignments/1/grades/batch-adjust` 返回 403；发布成绩 `POST /api/v1/teacher/assignments/1/grades/publish` 返回 403，页面均无可见错误反馈。
- 整课助教成绩册：`GET /api/v1/teacher/course-offerings/1/gradebook` 返回 200，学生 A 55、学生 B 0、平均分 27.5；导入模板下载成功。
- 主讲教师成绩册：`GET /api/v1/teacher/course-offerings/1/gradebook/export` 返回 200 并下载 `gradebook-offering-1.csv`；`POST /api/v1/teacher/assignments/1/grades/publish` 返回 200，响应含 `initialPublication=true`。
- 学生成绩反馈：学生 A `GET /api/v1/me/course-offerings/1/gradebook` 返回 200，`totalFinalScore=55`、`gradePublished=true`；学生 A 通知中心 `GET /api/v1/me/notifications` 返回 200，`total=3`，包含成绩发布、评测完成、作业发布通知。
- 成绩发布后隔离：学生 B 成绩页只显示 0/60、已发布、未提交；直接访问学生 A 提交详情和判题任务继续返回 403。
- 管理员审计：`GET /api/v1/admin/audit-logs?page=1&pageSize=20` 返回 200，包含教师 `GRADE_PUBLISH` 成功、整课助教成绩操作拒绝、学生越权授权拒绝等记录；`GRADE_PUBLISH` 详情 metadata 包含 `permissionCode=grade.publish`、`reason=ALLOW`、`initialPublication=true`。
- 收尾状态：`just status` 显示 `server/`、`web/` dirty entries 均为 0；`docs/` 有 2 个未跟踪条目，分别为本报告和截图目录。

## 11. 后续修复优先级建议

1. P0：修复 `UserAdministrationApplicationService.listUsers` 对 `primaryOrgUnitId=null` 的 NPE，并让前端区分“接口失败”和“无候选数据”。
2. P0：复核班级助教在 `/api/v1/me/courses` 中角色升格和班级范围丢失的触发条件，逐一复查提交、成绩、作业等接口是否复用错误范围。
3. P0：修复编程判题分数与提交详情/总分的同步，确保 `ACCEPTED` 20/20 后提交详情和成绩册能获得正确分数。
4. P0：修复 IDE 内提交结构化作业只发送编程题答案的问题，或移除/改写该入口避免误导学生。
5. P1：按角色隐藏或禁用整课助教无权执行的重判、成绩册导出、批量调分、发布成绩入口；同时把 403 转为可见错误反馈。
6. P1：成绩发布成功后在教师成绩册展示“已发布”、发布时间/发布人、已发布人数和禁用/二次确认状态。
7. P1：修复成员表格班级列字段映射，确保 `className/classCode` 正确展示。
8. P1：成员管理写操作按角色显隐和后端授权双重收敛；班级助教不应看到或执行超出授权班级范围的整课写操作。
9. P1：新增成员弹窗成功/失败状态随输入变化复位，添加成功后刷新列表或提供明确刷新动作。
10. P1：补齐题库新增题目表单的题型专属配置，并将后端校验错误显示在对应字段或弹窗错误区。
11. P1：判题环境表单复位，并补齐资源限制、镜像/运行时等字段或修正文案与列表列名。
12. P1：统一编程题测试用例 stdin 的产品规则；若允许无输入题，后端放宽校验；若不允许，前端必须字段级阻止并显示错误。
13. P1：作业列表摘要返回或展示总分，避免发布前后总分显示为“暂无”。
14. P1：修复编程工作区文件树初始状态、多文件禁用入口、历史版本侧栏和样例输出 diff。
15. P1：提交详情按题型展示客观题选项、附件文件名、代码块和判题结果，避免统一显示“无文本答案”。
16. P2：成绩册和学生成绩页在单课程场景下自动选择默认课程，或提供更明确的空态引导。
17. P2：管理员工作台补充近期提交、判题、成绩发布和权限拒绝等业务运营摘要。
18. P2：用户详情页提供组织选择器、用户选择器和档案/系统身份文案区分，减少数字 ID 操作。
19. P2：修复课程模板/学期、资源上传者、讨论详情层级、实验教学班选择、学生课程入口等数据展示与文案问题。
