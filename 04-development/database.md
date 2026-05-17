---
title: "数据库设计"
section: "04-development"
status: current
---
# 数据库设计

## 1. 当前设计原则

1. 关系型事实来源统一落在 PostgreSQL。
2. 结构变更统一通过 Flyway 管理，不手工改表。
3. 当前仓库使用 `BIGINT IDENTITY` 作为主键策略。
4. 状态字段显式建模，避免用隐含布尔值拼接业务状态。
5. 平台治理身份与课程成员关系分开建模。

## 2. 平台治理表

### 2.1 `org_units`

| 字段 | 说明 |
| --- | --- |
| `id` | 组织主键 |
| `parent_id` | 上级组织 |
| `code` | 组织编码，大小写不敏感唯一 |
| `name` | 组织名称 |
| `type` | `SCHOOL / COLLEGE / COURSE / CLASS` |
| `level` | 固定层级 `1 ~ 4` |
| `sort_order` | 排序号 |
| `status` | `ACTIVE / DISABLED` |

### 2.2 `users`

| 字段 | 说明 |
| --- | --- |
| `id` | 用户主键 |
| `primary_org_unit_id` | 默认归属组织 |
| `username` | 登录名，大小写不敏感唯一 |
| `display_name` | 显示名称 |
| `email` | 邮箱，大小写不敏感唯一 |
| `phone` | 手机号，可为空 |
| `password_hash` | 密码哈希 |
| `account_status` | `ACTIVE / DISABLED / LOCKED / EXPIRED` |
| `failed_login_attempts` | 连续失败次数 |
| `locked_until` | 锁定截止时间 |
| `expires_at` | 账号失效时间 |
| `last_login_at` | 最近登录时间 |

### 2.3 `academic_profiles`

| 字段 | 说明 |
| --- | --- |
| `id` | 画像主键 |
| `user_id` | 用户主键，1:1 关联 |
| `academic_id` | 学号/工号，大小写不敏感唯一 |
| `real_name` | 真实姓名 |
| `identity_type` | `TEACHER / STUDENT / ADMIN` |
| `profile_status` | `ACTIVE / SUSPENDED / GRADUATED / LEFT` |
| `phone` | 画像手机号，可为空 |

### 2.4 `user_org_memberships`

| 字段 | 说明 |
| --- | --- |
| `id` | 成员关系主键 |
| `user_id` | 用户主键 |
| `org_unit_id` | 组织节点 |
| `membership_type` | `ENROLLED / TEACHES / ASSISTS / MANAGES / BELONGS_TO_GROUP` |
| `membership_status` | `ACTIVE / INACTIVE / COMPLETED / REMOVED` |
| `source_type` | `MANUAL / IMPORT / SYNC / SSO_BIND` |
| `start_at` | 起始时间 |
| `end_at` | 结束时间 |

### 2.5 `user_scope_roles`

| 字段 | 说明 |
| --- | --- |
| `id` | 记录主键 |
| `user_id` | 用户主键 |
| `scope_org_unit_id` | 作用域组织 |
| `role_code` | `SCHOOL_ADMIN / COLLEGE_ADMIN / COURSE_ADMIN / CLASS_ADMIN` |
| `created_at` | 创建时间 |

### 2.6 `platform_configs`

| 字段 | 说明 |
| --- | --- |
| `id` | 主键 |
| `platform_name` | 平台名称 |
| `platform_short_name` | 平台简称 |
| `logo_url` | Logo 地址 |
| `footer_text` | 页脚文案 |
| `default_home_path` | 默认首页路径 |
| `theme_key` | 主题标识 |
| `login_notice` | 登录页提示 |
| `module_flags` | 模块开关 JSON |
| `updated_by_user_id` | 最近更新人 |

### 2.7 `audit_logs`

| 字段 | 说明 |
| --- | --- |
| `id` | 审计主键 |
| `actor_user_id` | 操作人 |
| `action` | 动作编码 |
| `target_type` | 目标类型 |
| `target_id` | 目标标识 |
| `result` | `SUCCESS / FAILURE` |
| `request_id` | 请求链路标识 |
| `ip` | 来源地址 |
| `metadata` | 扩展上下文 JSON |
| `created_at` | 创建时间 |

### 2.8 `auth_sessions`

| 字段 | 说明 |
| --- | --- |
| `id` | 会话主键 |
| `user_id` | 用户主键 |
| `sid` | 会话标识，JWT 中携带 |
| `refresh_token_hash` | refresh token 哈希 |
| `status` | 会话状态 |
| `created_at` | 创建时间 |
| `expires_at` | 过期时间 |

## 3. 课程主数据表

### 3.1 `academic_terms`

| 字段 | 说明 |
| --- | --- |
| `id` | 学期主键 |
| `term_code` | 学期编码，大小写不敏感唯一 |
| `term_name` | 学期名称 |
| `school_year` | 学年 |
| `semester` | `SPRING / SUMMER / AUTUMN / WINTER` |
| `start_date` | 开始日期 |
| `end_date` | 结束日期 |
| `status` | `PLANNING / ONGOING / ENDED / ARCHIVED` |

### 3.2 `course_catalogs`

| 字段 | 说明 |
| --- | --- |
| `id` | 课程模板主键 |
| `course_code` | 课程编码，大小写不敏感唯一 |
| `course_name` | 课程名称 |
| `course_type` | `REQUIRED / ELECTIVE / GENERAL / PRACTICE` |
| `credit` | 学分 |
| `total_hours` | 总学时 |
| `department_unit_id` | 所属学院 |
| `description` | 课程描述 |
| `status` | `ACTIVE / DISABLED` |

### 3.3 `course_offerings`

| 字段 | 说明 |
| --- | --- |
| `id` | 开课实例主键 |
| `catalog_id` | 关联课程模板 |
| `term_id` | 关联学期 |
| `offering_code` | 开课编码，大小写不敏感唯一 |
| `offering_name` | 开课名称 |
| `primary_college_unit_id` | 主学院 |
| `org_course_unit_id` | 对应组织树中的 COURSE 节点 |
| `delivery_mode` | `ONLINE / OFFLINE / HYBRID` |
| `language` | `ZH / EN / BILINGUAL` |
| `capacity` | 课程容量 |
| `selected_count` | 已选人数 |
| `status` | `DRAFT / PUBLISHED / ONGOING / FROZEN / ENDED / ARCHIVED` |
| `start_at` / `end_at` | 开课起止时间 |

### 3.4 `course_offering_college_maps`

| 字段 | 说明 |
| --- | --- |
| `id` | 主键 |
| `offering_id` | 开课实例 |
| `college_unit_id` | 共同管理学院 |
| `relation_type` | `PRIMARY / SECONDARY / CROSS_LISTED` |

### 3.5 `teaching_classes`

| 字段 | 说明 |
| --- | --- |
| `id` | 教学班主键 |
| `offering_id` | 所属开课实例 |
| `class_code` | 班级编码，课程内大小写不敏感唯一 |
| `class_name` | 班级名称 |
| `entry_year` | 入学年份 |
| `org_class_unit_id` | 对应组织树中的 CLASS 节点 |
| `capacity` | 班级容量 |
| `status` | `ACTIVE / FROZEN / ARCHIVED` |
| `announcement_enabled` | 公告功能开关 |
| `discussion_enabled` | 讨论区功能开关 |
| `resource_enabled` | 资源功能开关 |
| `lab_enabled` | 实验功能开关 |
| `assignment_enabled` | 作业功能开关 |

### 3.6 `course_members`

| 字段 | 说明 |
| --- | --- |
| `id` | 课程成员主键 |
| `offering_id` | 所属开课实例 |
| `teaching_class_id` | 所属教学班，可空 |
| `user_id` | 平台用户 |
| `member_role` | `INSTRUCTOR / TA / STUDENT / OBSERVER` |
| `member_status` | `PENDING / ACTIVE / DROPPED / COMPLETED / REMOVED` |
| `source_type` | `MANUAL / IMPORT / SYNC` |
| `remark` | 备注 |
| `joined_at` / `left_at` | 加入和离开时间 |

## 4. 作业与题库表

### 4.1 `assignments`

| 字段 | 说明 |
| --- | --- |
| `id` | 作业主键 |
| `offering_id` | 所属开课实例 |
| `title` | 作业标题 |
| `status` | `DRAFT / PUBLISHED / CLOSED` |
| 其他字段 | 截止时间、提交限制、评分模式等 |

### 4.2 `question_bank_questions`

| 字段 | 说明 |
| --- | --- |
| `id` | 题目主键 |
| `offering_id` | 所属开课实例 |
| `question_type` | 题型 |
| `content` | 题目内容 |
| `config_json` | 题目配置（含编程题隐藏测试点） |
| `category` | 分类/标签 |

### 4.3 `question_bank_question_options`

| 字段 | 说明 |
| --- | --- |
| `id` | 选项主键 |
| `question_id` | 所属题目 |
| `option_content` | 选项内容 |
| `is_correct` | 是否正确答案 |

### 4.4 `assignment_sections`

| 字段 | 说明 |
| --- | --- |
| `id` | 大题主键 |
| `assignment_id` | 所属作业 |
| `section_name` | 大题名称 |
| `sort_order` | 排序号 |

### 4.5 `assignment_questions`

| 字段 | 说明 |
| --- | --- |
| `id` | 试卷题目主键 |
| `section_id` | 所属大题 |
| `question_bank_question_id` | 关联题库题目 |
| `score` | 分值 |
| `sort_order` | 排序号 |
| `config_json` | 题目配置快照 |

### 4.6 `assignment_question_options`

| 字段 | 说明 |
| --- | --- |
| `id` | 选项主键 |
| `assignment_question_id` | 所属试卷题目 |
| `option_content` | 选项内容 |
| `is_correct` | 是否正确答案 |

### 4.7 `assignment_judge_profiles`

| 字段 | 说明 |
| --- | --- |
| `id` | 评测配置主键 |
| `assignment_id` | 所属作业 |
| 评测脚本、语言、环境等配置 | |

### 4.8 `assignment_judge_cases`

| 字段 | 说明 |
| --- | --- |
| `id` | 测试用例主键 |
| `judge_profile_id` | 所属评测配置 |
| `input` | 输入 |
| `expected_output` | 期望输出 |
| `score` | 分值 |

## 5. 提交与工作区表

### 5.1 `submissions`

| 字段 | 说明 |
| --- | --- |
| `id` | 提交主键 |
| `assignment_id` | 所属作业 |
| `user_id` | 提交用户 |
| `submit_no` | 提交序号 |
| `status` | 提交状态 |
| `accepted_at` | 受理时间 |

### 5.2 `submission_answers`

| 字段 | 说明 |
| --- | --- |
| `id` | 答案主键 |
| `submission_id` | 所属提交 |
| `assignment_question_id` | 对应试卷题目 |
| `answer_content` | 答案内容 |
| `auto_score` | 客观题自动评分 |
| `manual_score` | 人工评分 |
| `final_score` | 最终评分 |

### 5.3 `submission_artifacts`

| 字段 | 说明 |
| --- | --- |
| `id` | 附件主键 |
| `submission_id` | 所属提交 |
| `file_name` | 文件名 |
| `storage_key` | 对象存储键 |
| `file_size` | 文件大小 |

### 5.4 `programming_workspaces`

| 字段 | 说明 |
| --- | --- |
| `id` | 工作区主键 |
| `user_id` | 用户 |
| `assignment_id` | 所属作业 |
| `assignment_question_id` | 所属编程题 |
| `language` | 编程语言 |
| `files_snapshot` | 目录树源码快照 |
| `latest_input` | 最近一次标准输入 |

### 5.5 `programming_workspace_revisions`

| 字段 | 说明 |
| --- | --- |
| `id` | 修订主键 |
| `workspace_id` | 所属工作区 |
| `revision_no` | 修订序号 |
| `revision_kind` | 修订类型 |
| `files_snapshot` | 源码快照 |

## 6. 评测与成绩表

### 6.1 `judge_jobs`

| 字段 | 说明 |
| --- | --- |
| `id` | 评测作业主键 |
| `submission_answer_id` | 关联分题答案（结构化题） |
| `assignment_id` | 关联作业（legacy） |
| `submission_id` | 关联提交 |
| `status` | 评测状态 |
| `result_json` | 评测结果 |
| `report_storage_key` | 详细报告对象存储键 |

### 6.2 `programming_sample_runs`

| 字段 | 说明 |
| --- | --- |
| `id` | 样例试运行主键 |
| `user_id` | 用户 |
| `assignment_id` | 所属作业 |
| `assignment_question_id` | 所属编程题 |
| `workspace_id` | 关联工作区 |
| `revision_id` | 关联修订 |
| `input` | 输入 |
| `output` | 输出 |
| `status` | 运行状态 |

### 6.3 成绩册读模型

当前 V48 后不再保留独立 `grade_appeals`、`grade_publish_snapshot_batches`、`grade_publish_snapshots` 或 assignment 级 `grade_weight`。成绩册和统计报告直接聚合 `assignments / submissions / submission_answers / course_members`，成绩发布状态仍由 `assignments.grade_published_at` 与 `assignments.grade_published_by_user_id` 表达。

## 7. 实验表

### 7.1 `labs`

| 字段 | 说明 |
| --- | --- |
| `id` | 实验主键 |
| `teaching_class_id` | 所属教学班 |
| `title` | 实验标题 |
| `description` | 实验说明 |
| `status` | `DRAFT / PUBLISHED / CLOSED` |
| `open_at` / `due_at` | 开放和截止时间 |

### 7.2 `lab_reports`

| 字段 | 说明 |
| --- | --- |
| `id` | 实验报告主键 |
| `lab_id` | 所属实验 |
| `user_id` | 学生 |
| `content` | 报告内容 |
| `status` | `DRAFT / SUBMITTED / REVIEWED / PUBLISHED` |
| `review_comment` | 教师评语 |
| `review_score` | 教师评分 |

### 7.3 `lab_report_attachments`

| 字段 | 说明 |
| --- | --- |
| `id` | 附件主键 |
| `report_id` | 所属报告 |
| `file_name` | 文件名 |
| `storage_key` | 对象存储键 |
| `file_size` | 文件大小 |

## 8. 通知表

### 8.1 `notifications`

| 字段 | 说明 |
| --- | --- |
| `id` | 通知主键 |
| `type` | 通知类型 |
| `title` | 通知标题 |
| `content` | 通知内容 |
| `created_at` | 创建时间 |

### 8.2 `notification_receipts`

| 字段 | 说明 |
| --- | --- |
| `id` | 收件记录主键 |
| `notification_id` | 关联通知 |
| `user_id` | 收件用户 |
| `is_read` | 是否已读 |
| `read_at` | 阅读时间 |

## 9. 索引约定

- `org_units`：`lower(code)` 唯一索引、`parent_id + sort_order + id`
- `users`：`lower(username)` 唯一索引、`lower(email)` 唯一索引
- `academic_profiles`：`user_id` 唯一索引、`lower(academic_id)` 唯一索引
- `user_org_memberships`：`user_id + org_unit_id + membership_type` 唯一索引
- `user_scope_roles`：`user_id + scope_org_unit_id + role_code` 唯一索引
- `academic_terms`：`lower(term_code)` 唯一索引
- `course_catalogs`：`lower(course_code)` 唯一索引
- `course_offerings`：`lower(offering_code)` 唯一索引
- `course_offering_college_maps`：`offering_id + college_unit_id` 唯一索引
- `teaching_classes`：`offering_id + lower(class_code)` 唯一索引
- `course_members`：`INSTRUCTOR` 按 `offering_id + user_id` 唯一、`STUDENT` 按 `offering_id + user_id` 唯一
- `audit_logs`：`actor_user_id + created_at`、`action + created_at`

## 10. 设计边界

- 平台治理身份只解决平台配置、组织、用户、审计等后台治理问题。
- 教师、助教、学员等课程业务角色不落在 `users` 或 `user_scope_roles` 的全局字段上。
- 学号/工号和成员关系已落到独立表，不再把这类业务信息塞进 `users` 主表。
- 成绩册聚合继续挂接在 `assignments / submissions / submission_answers / course_members`，当前不引入独立成绩表。
- 当前实现明确禁止学生自主选课；课程成员仅由教师批量添加或导入既有系统用户。
