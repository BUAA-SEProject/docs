# AUBB 产品全功能完整验证第二轮报告

## 1. 验证元信息

- 执行日期：2026-06-10
- 工作区：`/Users/moorefoss/Code/AUBB`
- 执行合同：`goal.md` 第二阶段、`goal-test.md`
- 本轮边界：第二阶段验收期间未修改应用代码、配置代码、测试代码和生产文档正文；第三阶段补漏已修改 `web/` 应用代码和单元测试，并在本报告中记录回归证据。
- 主证据规则：用户可见功能以 Playwright MCP 页面操作为主证据；命令、API、数据库、日志和对象存储仅作为辅助证据。
- 产物：
  - 功能清单：`docs/06-testing-and-ops/artifacts/product-full-verification-round2-feature-inventory.md`
  - 主报告：`docs/06-testing-and-ops/artifacts/product-full-verification-round2-report.md`
  - 三次演示彩排记录：`docs/06-testing-and-ops/artifacts/product-full-verification-round2-rehearsal-log.md`
  - 截图目录：`docs/06-testing-and-ops/artifacts/product-full-verification-round2-screenshots/`
  - 辅助证据目录：`docs/06-testing-and-ops/artifacts/product-full-verification-round2-evidence/`

## 2. 总体验证结论

当前结论：`不通过`

第二轮命令门禁全部通过，Playwright MCP 已形成 180 张截图证据，其中 3 张为第三阶段补漏回归截图，4 张为公共认证补充截图，5 张为公告发布和通知状态变更补充截图，6 张为讨论创建、回复和锁定补充截图，1 张为教师资源上传下载补充截图，1 张为教师题库新增简答题补充截图，1 张为教师判题环境新增配置补充截图，12 张为题库结构化题型、作业创建发布、学生结构化提交、教师批改、成绩发布与学生反馈补充截图，6 张为报告型实验创建发布、学生报告提交、教师评阅发布与学生反馈回查补充截图。三次演示彩排主线均已执行并记录。第一阶段修复后的 WebIDE 样例自测、编程题判题和实验 Web 终端主线在第二轮中均能演示。

第三阶段已修复并回归第二轮报告中的 3 个 P2 可理解性问题；补证过程中又发现并修复 `P1-R2-004`：实验报告评阅发布后学生端未显示教师评语，以及 `P2-R2-005`：报告型实验误请求运行时 current session 产生 400 网络噪音。已完成 `web` 定向单测、lint、typecheck、build、根目录 `just verify` 和 docs build。后续补充 MCP 验证已覆盖教师公告新建、教师资源上传下载、教师题库新增简答题、教师结构化题型新增、教师判题环境新增配置、教师作业创建发布、教师讨论创建/回复/锁定、教师通知全部已读、学生讨论回复、学生结构化作业提交、文件题附件上传下载、教师提交批改、成绩发布、学生成绩/反馈回查、实验创建发布、实验报告提交、教师评阅发布、学生实验反馈回查、报告型实验不再触发运行时会话查询、学生通知单条已读和通知网络摘要。本轮仍不能写为 `通过` 或 `有条件通过`，原因是仍存在强制项阻塞：管理员保存/创建、成员导入/状态变更、编辑/关闭/归档类动作以及完整逐页 console/network 归因未形成 MCP 主证据。根据 `goal-test.md`，强制项未证明时必须保持 `阻塞`。

## 3. 上次缺口复核

| 缺口 | 第二轮纠偏动作 | 当前状态 |
| --- | --- | --- |
| 旧报告中 WebIDE / 判题 P1 | 第二轮 MCP 复核 WebIDE 页面和运行自测 | 已通过回归 |
| 旧报告中实验终端 P1 | 第二轮 MCP 复核实验终端输出 `round2-terminal` | 已通过回归 |
| `just e2e-real` 第一轮失败 | 第二轮重新执行完整真实后端 E2E | 已通过，`50 passed (4.0m)` |
| 三次彩排缺失 | 第二轮执行三次全角色主线彩排并保存截图 | 主线通过，但仍有强制项阻塞 |
| 强制项允许停在 `未覆盖` | 第二轮清单只使用 `通过 / 失败 / 阻塞 / 不适用` | 已纠偏 |

## 4. 输入缺失与环境阻塞

| 项目 | 状态 | 证据 |
| --- | --- | --- |
| `goal-test.md`、`goal.md`、`goal-repair.md` | 通过 | 当前轮已读取 |
| `AGENTS.md`、`AGENTS-shared.md`、`web/AGENTS.md`、`server/AGENTS.md`、`docs/AGENTS.md` | 通过 | 当前轮已读取 |
| `docs/04-development/frontend-design.md` | 通过 | 当前轮已读取 |
| `web/src/shared/routing/nav-config.ts`、`web/src/shared/routing/route-access.ts` | 通过 | 当前轮已读取 |
| `web/src/tests/e2e/README.md` | 通过 | 当前轮已读取 |
| `server/docs/stable-api.md` | 通过 | 已读取稳定接口范围 |
| `server/docs/product-specs/` | 通过 | 已检查规格目录 |
| `server/docs/generated/db-schema.md` | 通过 | 文件存在，用作运行时数据检查依据 |
| `web/docs/backend-requests.md` | 通过 | 当前待处理表为空 |
| `env/e2e.example` | 通过 | 已读取环境变量模板，真实值仅来自本地 `env/e2e.env` |
| `web/src/app/`、`web/src/features/`、`web/src/shared/api/generated/openapi.ts` | 通过 | 已用于功能清单生成 |

## 5. 命令门禁结果

| 顺序 | 命令 | 状态 | 证据 |
| --- | --- | --- | --- |
| 1 | `just status` | 通过 | `product-full-verification-round2-evidence/commands/01-just-status.log` |
| 2 | `just --list` | 通过 | `product-full-verification-round2-evidence/commands/02-just-list.log` |
| 3 | `just dev-up` | 通过 | `product-full-verification-round2-evidence/commands/03-just-dev-up.log` |
| 4 | `just healthcheck-strict` | 通过 | `product-full-verification-round2-evidence/commands/04-just-healthcheck-strict.log` |
| 5 | 残留摘要检查 | 通过 | `product-full-verification-round2-evidence/commands/05-e2e-residual-cleanup-dry-run.log` |
| 6 | `just seed-fixtures` | 通过 | `caseCount=22`、`passedCount=22`、`failedCount=0`；见 `06-just-seed-fixtures.log` |
| 7 | `just e2e-real` | 通过 | `50 passed (4.0m)`；见 `07-just-e2e-real.log` |
| 8 | `just verify` | 通过 | 后端 `357` tests、web lint/typecheck、docs build 通过；见 `08-just-verify.log` |
| 9 | `just verify-full` | 通过 | 后端 verify、web lint/typecheck/unit/build、docs build 通过；见 `09-just-verify-full.log` |
| 10 | `cd docs && npm run docs:build` | 通过 | VitePress build complete，仍有既有 chunk size warning；见 `10-docs-build.log` |
| 11 | 第三阶段 `web` 定向单测 / lint / typecheck / build | 通过 | 登录/课程定向单测 2 files / 11 tests passed；学生实验页定向单测 1 file / 6 tests passed；`npm run lint`、`npm run typecheck`、`npm run build` 均通过。 |
| 12 | 第三阶段 `just verify` 与 docs build | 通过 | `just verify` 后端 357 tests / 0 failures，web lint/typecheck 与 docs build 通过；单独 `cd docs && npm run docs:build` 通过。 |

## 6. 全功能清单摘要

- 第二轮清单覆盖公共认证、管理员、教师、学生、助教、运行时、文档、NFR 和演示彩排。
- 截图证据数量：`180` 张 PNG。
- 命令辅助证据数量：`10` 个命令日志。
- 当前清单状态：
  - `通过`：登录、路由守卫、三角色首页、管理员治理/用户/权限/审计、教师课程、公告创建、资源上传下载、题库新增、判题环境新增、作业创建发布、提交批改、成绩发布、实验创建发布和报告评阅、讨论创建/回复/锁定、教师/学生通知已读状态变更、学生课程、讨论回复、结构化作业提交、文件附件、WebIDE、成绩/反馈、实验报告、助教授权与拒绝边界、命令门禁、三次彩排主线。
  - `失败`：第二轮 P2-R2-001、P2-R2-002、P2-R2-003 和补证发现的 P1-R2-004、P2-R2-005 已在第三阶段修复并回归，当前无未回归 P0/P1/P2 失败项。
  - `阻塞`：管理员保存/创建、成员导入/状态变更、编辑/关闭/归档类动作以及完整逐页 console/network 归因仍未形成 MCP 主证据。

## 7. 逐角色验证结果

| 角色 | 当前状态 | 说明 |
| --- | --- | --- |
| 无登录用户 | 通过 | `/login` 可加载，未登录访问 `/admin` 会回到登录；空表单提交已显示应用内错误说明，见 P2-R2-001 第三阶段回归。 |
| 学校管理员 | 阻塞 | 治理概览、平台配置查看、组织树、用户列表/详情、开课详情、权限解释、审计日志均有 MCP 截图；保存/创建/编辑类动作仍阻塞。 |
| 教师 | 阻塞 | 教学工作台、课程工作区、公告创建、资源上传下载、题库新增简答题和结构化题型、判题环境新增配置、讨论创建/回复/锁定、作业创建发布、提交批改、成绩册发布、实验创建发布、实验报告评阅发布、通知全部已读均有 MCP 证据；成员导入/状态变更、编辑/关闭/归档类动作仍阻塞。 |
| 学生 | 阻塞 | 学习中心、课程、讨论详情与回复、作业详情、结构化题提交、文件题附件上传下载、WebIDE、样例自测、提交详情、成绩、实验终端、实验报告提交、发布后教师评语回查、通知单条已读均有 MCP 证据；WebIDE 历史恢复、实验会话新启动/停止等非本轮补证动作仍未逐项执行。 |
| 开课助教 | 通过 | 授权课程与管理员禁止边界通过；未授权或不存在课程上下文已收敛为课程不可访问态，见 P2-R2-002/P2-R2-003 第三阶段回归。 |
| 班级助教 | 通过 | 登录、班级成员页、管理员禁止边界有 MCP 截图。 |
| 缺档案用户 | 通过 | 以第一轮和第二轮上下文准备的缺档案账号证明 `/profile-required` 可达，证据继承第二轮前置数据和截图 `053-profile-required-profileless-ta.png`。 |

## 8. 公共与认证验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| COMMON-001 | 通过 | `001-login-page.png` | 未登录入口可进入登录页。 |
| COMMON-002 | 通过 | `001-login-page.png` | 登录页显示平台说明、用户名/密码表单、显示密码按钮和公告。 |
| COMMON-003 | 通过 | `116-r2-repair-login-empty-submit.png` | 空表单提交后停留登录页，表单顶部显示“请输入用户名和密码”，用户名和密码输入框均进入 invalid 状态，见 P2-R2-001。 |
| COMMON-004 | 通过 | MCP 彩排 1 匿名 `/admin` 重定向记录 | 未登录访问受限页会跳转登录。 |
| COMMON-005 | 通过 | `119-r2-common-global-search-results.png`、`120-r2-common-global-search-gradebook.png` | 顶栏搜索输入“成绩”后显示“全部成绩 / 教师端”结果，并可跳转到 `/teacher/grading/gradebook`。 |
| COMMON-006 | 通过 | `043-student-notifications.png`、`044-me-notifications.png`、`123/124`、`126/127` | 学生、教师通知页可见，通知列表真实渲染；教师全部已读和学生单条已读均完成页面状态变更。 |
| COMMON-007 | 通过 | `121-r2-common-user-menu.png`、`122-r2-common-logout-login-page.png` | 用户菜单显示教师身份、用户名和退出登录入口；点击退出登录后回到 `/login`。 |
| AUTH-001 | 通过 | `002-admin-dashboard.png`、`056-r2-rehearsal1-admin-dashboard.png`、`092-r2-rehearsal3-admin-dashboard.png` | 管理员登录进入治理首页。 |
| AUTH-002 | 通过 | `013/014-teacher-dashboard.png`、`060-r2-rehearsal1-teacher-dashboard.png`、`096-r2-rehearsal3-teacher-dashboard.png` | 教师登录进入教学工作台。 |
| AUTH-003 | 通过 | `032/033-student-dashboard.png`、`064-r2-rehearsal1-student-dashboard.png`、`102-r2-rehearsal3-student-dashboard.png` | 学生登录进入学习中心。 |
| AUTH-004 | 通过 | `045-offering-ta-dashboard.png`、`047-class-ta-dashboard.png`、`071/074/109/113` 彩排截图 | 开课助教和班级助教均可登录教师端。 |
| AUTH-005 | 通过 | `053-profile-required-profileless-ta.png` | 缺档案用户可进入 profile-required。 |
| AUTH-006 | 通过 | `049-student-forbidden-admin.png`、`050-teacher-forbidden-admin.png`、`070/073/076/108/112/114` 彩排截图 | 非授权工作区进入 `/unauthorized`。 |
| AUTH-007 | 通过 | `044-me-notifications.png`、`069-r2-rehearsal1-me-notifications.png`、`107-r2-rehearsal3-me-notifications.png` | `/me/notifications` 可达。 |

## 9. 学生闭环验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| STUDENT-001~006 | 通过 | `032`-`038`、`064`-`065`、`086`-`087`、`102`-`103`、`131-r2-student-discussion-reply-posted.png`、`student-discussion-reply-network.txt` | 学生首页、课程、讨论、作业列表、作业详情和 WebIDE 页面可达；学生进入教师新建讨论 `36` 后可见教师回复并成功发布回复，接口 `POST /api/v1/me/discussions/36/replies` 返回 201。 |
| STUDENT-007~009 | 通过 | `140-r2-student-structured-assignment-filled.png`、`141-r2-student-structured-submission-detail.png`、`student-structured-submission-network.txt` | 学生提交作业 `259`，单选 A、多选 A/B、填空“下载”均在提交详情回显；接口 `POST /api/v1/me/assignments/259/submissions` 返回 201，生成提交 `55`。 |
| STUDENT-010 | 通过 | `037/038-student-assignment-detail.png`、`040-student-submission-detail.png`、`141-r2-student-structured-submission-detail.png` | 简答/结构化提交详情可达；本轮结构化提交详情和既有简答提交详情均可显示。 |
| STUDENT-011 | 通过 | `140-r2-student-structured-assignment-filled.png`、`141-r2-student-structured-submission-detail.png`、`student-structured-upload-sha256.txt` | 文件题附件上传后提交详情可见；下载文件与源文件 SHA256 一致。 |
| STUDENT-012~014 | 通过 | `039-student-webide.png`、`054-student-webide-sample-run.png`、`066-r2-rehearsal1-student-webide-run.png`、`104-r2-rehearsal3-student-webide-run.png` | WebIDE 可打开，运行自测显示 `ACCEPTED` / 通过。 |
| STUDENT-015~016 | 通过 | `040-student-submission-detail.png`、`141-r2-student-structured-submission-detail.png`、`147-r2-student-submission-55-feedback-visible.png`、`07-just-e2e-real.log` | 编程题正式提交闭环由真实 E2E 覆盖；结构化提交 `55` 的详情页可见分题答案和教师文件题反馈。 |
| STUDENT-017~018 | 通过 | `041-student-grades.png`、`043-student-notifications.png`、`106/107` 彩排截图、`126/127`、`146-r2-student-gradebook-259-published.png` | 成绩和通知入口可达；学生成绩页显示作业 `259` 为 `23 / 23`、`已发布`、提交 `55`；学生端对 `MCP-R2-20260610-143804` 公告通知执行单条标记已读后未读徽标 32 -> 31，目标行按钮消失。 |
| STUDENT-019~020 | 通过 | `042-student-labs.png`、`055-student-lab-terminal-echo.png`、`105-r2-rehearsal3-student-labs.png` | 实验列表和 Web 终端可演示，终端输出包含 `round2-terminal`。 |
| STUDENT-021 | 通过 | `149-r2-student-lab-report-filled-attachment.png`、`150-r2-student-lab-report-draft-saved.png`、`151-r2-student-lab-report-submitted.png`、`154-r2-student-lab-report-feedback-visible.png`、`student-lab-report-submit-network.txt`、`student-lab-report-attachment-sha256.txt`、`student-lab-report-feedback-network.txt` | 学生选择实验 `52`，填写 Markdown 报告、上传附件、保存草稿、确认正式提交；教师评阅发布后学生端显示 `已发布` 与教师评语，附件下载 SHA256 一致。 |

## 10. 教师闭环验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| TEACHER-001~003 | 通过 | `013`-`016`、`060`-`061`、`096`-`097` | 教师首页、课程列表、课程工作区和上下文导航可达。 |
| TEACHER-004 | 阻塞 | `016/017-teacher-members.png`、`075/113-r2-rehearsal*-class-ta-members.png` | 成员页可达；导入、添加和状态变更未执行，仍阻塞。 |
| TEACHER-005 | 通过 | `017/018`、`125-r2-teacher-announcement-created.png`、`teacher-announcement-create-network.txt` | 公告页可达；已新建 `MCP-R2-20260610-143804` 公告，列表可见，接口 `POST /api/v1/teacher/course-offerings/2/announcements` 返回 201。 |
| TEACHER-006 | 通过 | `018-teacher-resources.png`、`082-r2-rehearsal2-teacher-resources.png`、`134-r2-teacher-resource-uploaded.png`、`teacher-resource-upload-network.txt`、`teacher-resource-upload-sha256.txt` | 资源页面可达；教师上传 `MCP-R2-20260610-1553 教师资源补证` Markdown 文件后列表显示标题、文件名、说明、大小和下载入口，接口 `POST /api/v1/teacher/course-offerings/2/resources` 返回 201；下载文件与源文件 SHA256 一致。 |
| TEACHER-007~008 | 通过 | `019`-`021`、`128`-`133`、`teacher-discussion-create-network.txt`、`teacher-discussion-reply-network.txt`、`teacher-discussion-lock-network.txt` | 讨论列表和详情页面可达；教师新建讨论 `MCP-R2-20260610-145754 教师讨论补证` 后列表可见，教师回复写入后详情可见，学生回复也在教师详情页可见；锁定后列表显示“已锁定”，详情页发布按钮禁用。 |
| TEACHER-009 | 通过 | `021/022/023-teacher-question-bank-course.png`、`098-r2-rehearsal3-teacher-question-bank.png`、`135-r2-teacher-question-bank-created.png`、`137-r2-teacher-question-bank-structured-types-created.png`、`teacher-question-bank-create-network.txt`、`teacher-question-bank-structured-types-network.txt` | 题库页面可达；教师创建 `MCP-R2-20260610-1605 简答题补证` 后列表第一行显示新题；随后新增单选、多选、填空、文件题用于结构化作业，相关创建接口均返回 201。 |
| TEACHER-010 | 通过 | `022-teacher-judge-envs.png`、`136-r2-teacher-judge-environment-created.png`、`teacher-judge-environment-create-network.txt` | 判题环境页面可达；教师创建 `MCP-R2-20260610-1611 Python3 判题环境补证` 后列表显示新配置、语言、运行环境和可用状态，接口 `POST /api/v1/teacher/course-offerings/2/judge-environment-profiles` 返回 201。编辑/归档未单独执行，作为后续低优先级补证。 |
| TEACHER-011~013 | 阻塞 | `023`-`026`、`083/099` 彩排截图、`138-r2-teacher-assignment-create-filled.png`、`139-r2-teacher-assignment-published.png`、`teacher-assignment-create-network.txt`、`teacher-assignment-publish-network.txt` | 作业列表、创建表单、编辑页可达；教师创建结构化作业 `259` 并发布成功，接口 `POST /api/v1/teacher/course-offerings/2/assignments` 返回 201，`POST /api/v1/teacher/assignments/259/publish` 返回 200；编辑/关闭/重新发布未单独执行，仍阻塞。 |
| TEACHER-014~016 | 通过 | `026`-`029`、`062/063/084/085/100` 彩排截图、`142-r2-teacher-submission-55-before-grade.png`、`143-r2-teacher-submission-55-after-grade.png`、`144-r2-teacher-gradebook-259-before-publish.png`、`145-r2-teacher-gradebook-259-after-publish.png`、`teacher-submission-55-grade-network.txt`、`teacher-gradebook-259-publish-network.txt` | 提交列表、提交详情和成绩册页面可达；教师查看提交 `55`，为文件题保存人工分 `8` 和反馈，成绩册发布作业 `259` 后学生端可见总分与反馈。 |
| TEACHER-017~018 | 阻塞 | `029/030-teacher-question-bank-global.png`、`030/031-teacher-labs.png`、`086/101` 彩排截图、`148-r2-teacher-report-lab-created-published.png`、`152-r2-teacher-lab-report-detail-before-review.png`、`153-r2-teacher-lab-report-reviewed-published.png`、`teacher-report-lab-create-publish-network.txt`、`teacher-lab-report-review-publish-network.txt` | 全局题库和实验页可达；教师创建并发布报告型实验 `52`，查看学生报告 `21`、保存教师评语并发布评阅，相关接口返回 201/200；实验关闭未单独执行，仍阻塞。 |
| TEACHER-019 | 通过 | `031/032-teacher-notifications.png`、`123/124`、`teacher-notifications-after-network.txt` | 教师通知页可达；点击“全部已读”后顶部未读徽标从 9 清零，接口 `POST /api/v1/me/notifications/read-all` 返回 200。 |

## 11. 管理员闭环验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| ADMIN-001 | 通过 | `002-admin-dashboard.png`、`056`、`092` | 治理首页可达。 |
| ADMIN-002 | 阻塞 | `003-admin-platform-config.png`、`077` | 平台配置可查看；保存/恢复未执行，仍阻塞。 |
| ADMIN-003 | 阻塞 | `004-admin-org-units.png`、`093` | 组织树可查看；创建/编辑未执行，仍阻塞。 |
| ADMIN-004~005 | 通过 | `005/006/013-admin-user-detail*.png`、`078/094` | 用户列表、搜索和用户详情可达。 |
| ADMIN-006~008 | 阻塞 | `007`-`010`、`079` | 学期、课程模板、开课列表/详情可达；创建/编辑和共同管理学院选择未形成 MCP 主证据。 |
| ADMIN-009 | 通过 | `010-admin-course-offering-detail.png`、`079` | 开课详情可达。 |
| ADMIN-010~011 | 通过 | `011-admin-auth-explain.png`、`012-admin-audit-logs.png`、`058/059/080/095` | 权限解释和审计日志可达。 |

## 12. 助教与权限边界验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| TA-001~002 | 通过 | `045/046`、`071/072`、`090/109` | 开课助教可登录并进入授权开课。 |
| TA-003 | 通过 | `117-r2-repair-offering-ta-unauthorized-course.png` | 未授权开课 ID `5` 显示“无法访问该课程”，不再显示课程快捷操作入口，见 P2-R2-002。 |
| TA-004~005 | 通过 | `047/048`、`074/075`、`091/113` | 班级助教可登录并进入班级成员页。 |
| TA-006~009 | 通过 | `049/050`、`070/073/076/108/112/114` | 学生、教师、助教访问非授权工作区均显示 `/unauthorized`。 |
| TA-010 | 通过 | `118-r2-repair-offering-ta-invalid-course.png` | 不存在课程 ID `999999` 显示“无法访问该课程”，不再停留教学班加载态或展示快捷操作，见 P2-R2-003。 |

## 13. 运行时能力验证

| 编号 | 状态 | 证据 | 结论 |
| --- | --- | --- | --- |
| RUNTIME-001 | 通过 | `just verify`、`just verify-full`、`just e2e-real` 日志 | 后端测试和真实 E2E 证明提交、成绩、审计等核心数据链路可用；本轮未单独导出 SQL 摘要。 |
| RUNTIME-002 | 通过 | `just e2e-real` 日志、`134-r2-teacher-resource-uploaded.png`、`teacher-resource-upload-sha256.txt`、`student-structured-upload-sha256.txt`、`student-lab-report-attachment-sha256.txt`、`teacher-lab-report-attachment-sha256.txt` | 真实 E2E 覆盖资源上传下载；本轮 MCP 又补充教师资源、学生文件题附件、学生实验报告附件和教师端报告附件下载校验，下载文件与源文件 SHA256 一致。 |
| RUNTIME-003 | 通过 | `just healthcheck-strict`、`just e2e-real` 日志 | RabbitMQ 依赖健康，真实 E2E 判题链路通过。 |
| RUNTIME-004 | 通过 | `just healthcheck-strict`、`just e2e-real` 日志 | Redis 依赖健康，限流/登录真实 E2E 通过。 |
| RUNTIME-005 | 通过 | `123/124`、`126/127`、`teacher-notifications-after-network.txt`、`student-notifications-after-mark-read-network.txt` | 通知页、未读入口、SSE/轮询请求、教师全部已读和学生单条已读可用；网络摘要包含 `GET /api/v1/me/notifications/stream`、`GET /unread-count`、`POST /read-all`、`POST /{id}/read` 的成功记录。 |
| RUNTIME-006 | 通过 | `054`、`066`、`104` WebIDE 自测截图，`07-just-e2e-real.log` | go-judge / fake judge 主线返回 `ACCEPTED`。 |
| RUNTIME-007 | 通过 | `055-student-lab-terminal-echo.png` | 实验 Web 终端已连接并输出 `round2-terminal`。 |
| RUNTIME-008 | 通过 | `012`、`059`、`080` 审计日志截图 | 审计日志页面可查。 |

## 14. 文档一致性验证

`just verify`、`just verify-full` 和单独 `cd docs && npm run docs:build` 均通过。第二轮验收报告、功能清单和彩排记录写入 `docs/06-testing-and-ops/artifacts/` 下独立 `round2` 路径，未覆盖第一轮产物。

## 15. 前端质量与响应式验证

| 视口 | 状态 | 证据 | 说明 |
| --- | --- | --- | --- |
| `1280x800` | 通过 | `051-nfr-1280-student-assignments.png` | 学生作业列表在窄桌面宽度可用。 |
| `1440x900` | 通过 | `052-nfr-1440-admin-users.png` | 管理员用户表在标准桌面宽度可用。 |
| `390x844` | 通过 | `053-nfr-390-student-webide.png` | WebIDE 移动窄屏基础可见。 |
| 全站关键页 | 阻塞 | Playwright MCP 彩排截图 | 未单独保存完整 console/network 归因文件；负例 403 属权限验证预期。 |
| 权限/错误态 | 通过 | `116`、`117`、`118` | 登录空表单、未授权课程和不存在课程错误态均有可见说明，且未授权/不存在课程不再展示后续快捷入口。 |

## 16. 三次完整演示彩排记录摘要

| 彩排 | 状态 | 证据 | 说明 |
| --- | --- | --- | --- |
| 彩排 1 | 通过 | `056`-`076` | 管理员、教师、学生、WebIDE、学生权限、开课助教、班级助教主线均通过。 |
| 彩排 2 | 通过 | `077`-`091` | 管理员/教师段初次 MCP 调用超时，但已生成页面截图；随后补齐教师实验、学生和助教短段。 |
| 彩排 3 | 通过 | `092`-`114`、`116`-`118` | 管理员、教师、学生、助教主线通过；彩排中发现的 P2 已在第三阶段补漏回归。 |

三次彩排主线均已执行并记录，但因为强制功能仍有阻塞项，总体验收结论仍为 `不通过`。

## 17. 缺陷详情

### P2-R2-001 登录空表单缺少新增可见错误说明

- 严重级别：P2
- 功能清单编号：COMMON-003
- 模块：web/auth
- 角色：无登录用户
- 页面或对象：`/login`
- 操作步骤：打开登录页，不输入用户名和密码，点击“立即登录”。
- 实际表现：页面仍停留登录页，截图中只保留字段标签和占位提示，没有新增字段级或全局错误说明。
- 期望表现：字段旁或表单顶部显示“请输入用户名 / 请输入密码”等可理解反馈。
- 影响说明：不会阻断登录主线，但降低错误态可理解性。
- 证据：
  - MCP 截图：`product-full-verification-round2-screenshots/115-r2-login-empty-submit.png`
  - MCP 页面观察：点击后仍为 `/login`。
  - 第三阶段回归截图：`product-full-verification-round2-screenshots/116-r2-repair-login-empty-submit.png`
  - 第三阶段 MCP 页面观察：点击“立即登录”后显示 `role=alert` 的“请输入用户名和密码”，用户名和密码输入框均为 invalid。
  - 辅助证据：`web/src/tests/unit/auth/login-form.test.tsx` 覆盖空表单应用内校验。
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否。
- 修复说明：登录表单移除原生 required 阻断并启用 `noValidate`，由应用内校验显示统一错误区和 `aria-invalid`。
- 修复状态：已回归

### P2-R2-002 未授权开课上下文仍展示快捷入口

- 严重级别：P2
- 功能清单编号：TA-003、NFR-005
- 模块：web/teacher course workspace
- 角色：开课助教
- 页面或对象：`/teacher/courses/5`
- 操作步骤：以开课助教登录，直接打开未授权开课 ID `5`。
- 实际表现：页面显示“数据加载失败 / 当前用户无权查看教学班”，但仍显示“发布全课公告”“上传课程资源”“管理本课作业”等快捷入口。
- 期望表现：未授权上下文应进入统一拒绝态，隐藏或禁用后续动作入口。
- 影响说明：不构成越权访问，但会误导用户继续点击必然失败的动作。
- 证据：
  - MCP 截图：`product-full-verification-round2-screenshots/111-r2-rehearsal3-offering-ta-unauthorized-course.png`
  - MCP 页面观察：拒绝文案和快捷入口同时存在。
  - 第三阶段回归截图：`product-full-verification-round2-screenshots/117-r2-repair-offering-ta-unauthorized-course.png`
  - 第三阶段 MCP 页面观察：`/teacher/courses/5` 显示“无法访问该课程”和“课程不存在，或当前账号没有该课程的访问权限。”，不再显示“快捷操作”“发布全课公告”“上传课程资源”“管理本课作业”。
  - 辅助证据：`web/src/tests/unit/course/teacher-course-dashboard-page.test.tsx` 覆盖未授权课程隐藏后续动作。
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否。
- 修复说明：课程工作区先以 `useMyCoursesQuery()` 确认当前课程在教师/助教授权范围内，未命中时渲染页面级不可访问态并跳过后续动作区。
- 修复状态：已回归

### P2-R2-003 不存在课程 ID 页面停留加载态并展示快捷入口

- 严重级别：P2
- 功能清单编号：TA-003、NFR-005
- 模块：web/teacher course workspace
- 角色：开课助教
- 页面或对象：`/teacher/courses/999999`
- 操作步骤：以开课助教登录，直接打开不存在课程 ID `999999`。
- 实际表现：页面停留“教学班 加载中...”，同时显示“发布全课公告”“上传课程资源”“管理本课作业”等快捷入口。
- 期望表现：不存在或不可访问对象应显示清晰的不存在/无权状态，并隐藏动作入口。
- 影响说明：不影响正常授权课程主线，但影响错误态和演示故障预案可信度。
- 证据：
  - MCP 截图：`product-full-verification-round2-screenshots/110-r2-rehearsal3-offering-ta-invalid-course.png`
  - MCP 页面观察：加载态长时间未收敛，动作入口仍存在。
  - 第三阶段回归截图：`product-full-verification-round2-screenshots/118-r2-repair-offering-ta-invalid-course.png`
  - 第三阶段 MCP 页面观察：`/teacher/courses/999999` 显示“无法访问该课程”和“课程不存在，或当前账号没有该课程的访问权限。”，不再停留“加载中...”或显示快捷操作。
  - 辅助证据：`web/src/tests/unit/course/teacher-course-dashboard-page.test.tsx` 覆盖不存在课程 ID 不进入教学班加载态。
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否。
- 修复说明：课程工作区在课程清单已加载但找不到当前 `offeringId` 时直接渲染不可访问态，并仅在课程上下文确认后启用教学班查询。
- 修复状态：已回归

### P1-R2-004 实验报告评阅发布后学生端未显示教师评语

- 严重级别：P1
- 功能清单编号：STUDENT-021、TEACHER-018
- 模块：web/lab
- 角色：学生、教师
- 页面或对象：`/student/labs?classId=2&offeringId=2`
- 操作步骤：教师创建并发布报告型实验 `52`；学生提交报告 `21`；教师保存评语并发布评阅；学生重新打开同一实验报告。
- 实际表现：后端 `GET /api/v1/me/labs/52/report` 返回 `teacherCommentText`，但学生端页面只显示 `已发布`、报告正文和附件，没有显示教师评语。
- 期望表现：评阅结果发布后，学生端应显示教师评语或批注，形成“提交 -> 教师反馈 -> 学生回查”的完整闭环。
- 影响说明：会破坏实验报告演示主线中的反馈回查环节，属于可见反馈缺失。
- 证据：
  - 后端响应体：`product-full-verification-round2-evidence/runtime/student-lab-report-feedback-response-body.json`，包含 `teacherCommentText`。
  - 修复前页面观察：学生端页面文本不包含“教师评语”和 `MCP-R2 教师评阅补证`。
  - 修复后回归截图：`product-full-verification-round2-screenshots/154-r2-student-lab-report-feedback-visible.png`
  - 修复后网络摘要：`product-full-verification-round2-evidence/runtime/student-lab-report-feedback-network.txt`
  - 辅助单测：`web/src/tests/unit/lab/student-labs-page.test.tsx` 覆盖发布后显示教师反馈。
- 是否阻塞演示彩排：是，未修复时会阻断实验报告反馈演示。
- 是否阻塞后续功能验证：否，已回归。
- 修复说明：学生实验报告页面在报告状态为 `PUBLISHED` 且后端返回教师评语或批注时，显示“教师评语”反馈区。
- 修复状态：已回归

### P2-R2-005 报告型实验误请求运行时 current session 产生 400 网络噪音

- 严重级别：P2
- 功能清单编号：STUDENT-021、NFR-004
- 模块：web/lab
- 角色：学生
- 页面或对象：`/student/labs?classId=2&offeringId=2`
- 操作步骤：学生打开实验页并选择报告型实验 `52`。
- 实际表现：页面显示教师反馈的同时仍请求 `GET /api/v1/me/labs/52/sessions/current`，该接口对报告型实验返回 400。
- 期望表现：报告型实验只加载报告正文、附件和教师反馈，不应查询终端实验的当前运行时会话。
- 影响说明：不阻断实验报告反馈显示，但会污染 console/network 归因文件，降低演示回归证据可信度。
- 证据：
  - 修复前 MCP 网络观察：选择报告型实验后出现 `GET /api/v1/me/labs/52/sessions/current` 400。
  - 辅助单测：`web/src/tests/unit/lab/student-labs-page.test.tsx` 覆盖报告型实验不查询 runtime session。
  - 修复后 MCP 网络观察：选择同一报告型实验后实验相关请求只有 `GET /api/v1/me/labs/52/report` 200，不再出现 `/api/v1/me/labs/52/sessions/current` 请求。
- 是否阻塞演示彩排：否。
- 是否阻塞后续功能验证：否，已回归。
- 修复说明：学生实验页先从实验清单判断选中实验类型，只有 `TERMINAL` 实验才启用 `useMyCurrentLabSessionQuery`；报告型实验传入 `0` 触发 hook 的 `enabled: !!labId` 禁用查询。
- 修复状态：已回归

## 18. 阻塞项与不适用项

当前阻塞项主要是第二轮未形成 MCP 主证据的真实写入动作。已补证项包括教师公告新建、教师资源上传下载、教师题库新增简答题与结构化题型新增、教师判题环境新增配置、教师作业创建发布、教师提交批改与成绩发布、教师实验创建发布与报告评阅发布、教师讨论创建/回复/锁定、教师通知全部已读、学生讨论回复、学生结构化作业提交、文件题附件、学生成绩/反馈回查、学生实验报告提交与教师评语回查、学生通知单条已读和通知网络摘要，不再列为阻塞：

- 管理员：平台配置保存/恢复、组织节点创建/编辑、学期创建/编辑、课程模板创建/编辑、开课创建/编辑、共同管理学院选择、教学班创建/编辑。
- 教师：成员添加/导入/状态变更，题库编辑/归档，判题环境编辑/归档，作业编辑/关闭/撤回/重新发布，实验编辑/关闭。
- 学生：WebIDE 历史恢复、实验会话新启动/停止等本轮未重复执行的非报告型动作。
- 非功能：完整逐页 console/network 归因文件未单独保存。

这些阻塞项不是当前已知代码缺陷的充分证据，但会阻止本轮验收写为 `通过`。

## 19. 第三阶段修复结果

第三阶段已处理第二轮明确可复现的 P2：

1. P2-R2-001：登录空表单错误态已显示应用内错误说明。
2. P2-R2-002：未授权课程上下文已收敛为课程不可访问态，不再展示快捷入口。
3. P2-R2-003：不存在课程 ID 已收敛为课程不可访问态，不再停留加载态或展示快捷入口。
4. P1-R2-004：实验报告评阅发布后学生端已显示教师评语，完成 TDD 单测和 MCP 回归。
5. P2-R2-005：报告型实验已停止查询运行时 current session，完成 TDD 单测和 MCP 网络回归。

其余阻塞项应优先补 MCP 写入动作验证；如果验证中发现真实缺陷，再追加编号进入下一轮修复清单。当前第三阶段补证已覆盖教师公告新建、教师资源上传下载、教师题库新增简答题与结构化题型新增、教师判题环境新增配置、教师作业创建发布、教师提交批改、成绩发布、教师实验创建发布、实验报告评阅发布、教师讨论创建/回复/锁定、教师通知全部已读、学生讨论回复、学生结构化提交、文件题附件上传下载、学生成绩/反馈回查、学生实验报告提交与教师评语回查、报告型实验不再查询运行时 current session、学生通知单条已读和通知网络摘要；其中 P1-R2-004 和 P2-R2-005 涉及应用代码修改，其余补证不涉及应用代码修改。

## 20. 最终 just status 与提交信息

- 第二轮文本产物更新前 `just status`：`server/`、`web/`、`docs/` dirty entries 均为 0；第二轮 artifacts 位于 docs ignore 目录，需要 `git add -f`。
- 第三阶段修复前 `just status`：`server/` dirty entries 0；`web/` dirty entries 5；`docs/` dirty entries 3，另有 ignored round2 repair checklist 和 116-118 截图需要 `git add -f`。
- 第三阶段代码提交：`web` `5ea8296 fix(frontend): 修复登录与课程错误态`；`web` `1618469 fix(lab): 显示实验报告教师反馈`。
- 第三阶段 docs 产物提交：以本报告所在 `docs/` 提交为准。
- 当前剩余状态：第二轮仍有部分强制写入动作缺少 MCP 主证据，总体验收保持 `不通过`；公告、资源、题库新增、判题环境新增、作业创建发布、学生结构化提交、文件题、提交批改、成绩发布、实验创建发布、实验报告提交/评阅/反馈、报告型实验网络噪音、讨论与通知状态变更已补齐，下一步应优先补齐管理员保存/创建、成员导入/状态变更、编辑/关闭/归档类动作以及完整逐页 console/network 归因，发现真实缺陷后再追加编号进入下一轮修复清单。
