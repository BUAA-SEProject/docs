# 数据库设计

## 1. 设计原则

- 统一使用 `uuid` 作为主键。
- 关键业务表必须包含 `created_at`、`updated_at`、`created_by`、`updated_by`。
- 状态字段显式建模，禁止使用隐含状态。
- 在线 IDE 草稿、正式提交、正式评测和成绩采用分层留痕设计。
- IDE 工作区仅保存当前可变草稿；正式提交和正式评测依赖不可变快照。

## 2. 核心表

### 2.1 平台治理

| 表名 | 关键字段 |
| --- | --- |
| `platform_configs` | `id`, `version`, `name`, `theme`, `module_flags`, `resource_policy_json`, `status` |
| `org_units` | `id`, `parent_id`, `name`, `type`, `level`, `status` |
| `users` | `id`, `username`, `display_name`, `email`, `phone`, `platform_role`, `status`, `password_hash` |
| `user_identities` | `id`, `user_id`, `provider`, `provider_subject`, `provider_meta_json`, `status` |

### 2.2 课程与任务

| 表名 | 关键字段 |
| --- | --- |
| `courses` | `id`, `name`, `owner_user_id`, `term`, `org_unit_id`, `status`, `invite_code` |
| `course_members` | `id`, `course_id`, `user_id`, `course_role`, `joined_at`, `status` |
| `course_resources` | `id`, `course_id`, `name`, `type`, `file_key`, `visibility` |
| `tasks` | `id`, `course_id`, `type`, `title`, `content_md`, `open_at`, `due_at`, `submission_limit`, `grading_mode`, `status` |
| `task_language_profiles` | `id`, `task_id`, `language`, `label`, `build_command`, `run_command`, `entry_file`, `time_limit_ms`, `memory_limit_mb`, `output_limit_kb`, `is_default`, `status` |
| `task_testcases` | `id`, `task_id`, `name`, `input_key`, `expected_output_key`, `is_public`, `weight`, `order_no` |
| `task_starter_files` | `id`, `task_id`, `language_profile_id`, `path`, `content_text`, `is_readonly`, `sort_order` |
| `task_rubrics` | `id`, `task_id`, `item_name`, `score`, `description`, `sort_order` |

### 2.3 IDE 工作区与运行

| 表名 | 关键字段 |
| --- | --- |
| `ide_workspaces` | `id`, `task_id`, `user_id`, `active_language_profile_id`, `version_no`, `save_status`, `last_opened_file`, `last_saved_at` |
| `ide_workspace_files` | `id`, `workspace_id`, `path`, `node_type`, `content_text`, `content_hash`, `size_bytes`, `is_deleted`, `version_no` |
| `workspace_snapshots` | `id`, `workspace_id`, `task_id`, `user_id`, `source_type`, `language_profile_id`, `version_no`, `storage_prefix`, `file_count` |
| `workspace_snapshot_files` | `id`, `snapshot_id`, `path`, `storage_key`, `size_bytes`, `sha256` |
| `sandbox_runs` | `id`, `workspace_id`, `snapshot_id`, `task_id`, `user_id`, `status`, `stdin_text`, `stdout_text`, `stderr_text`, `compile_output`, `exit_code`, `time_ms`, `memory_kb`, `finished_at` |

### 2.4 提交、评测、成绩

| 表名 | 关键字段 |
| --- | --- |
| `submissions` | `id`, `task_id`, `user_id`, `snapshot_id`, `submit_no`, `status`, `source_type`, `accepted_at`, `current_judge_run_id` |
| `submission_files` | `id`, `submission_id`, `path`, `storage_key`, `size_bytes`, `sha256` |
| `judge_runs` | `id`, `submission_id`, `attempt_no`, `status`, `compile_status`, `score`, `raw_payload`, `normalized_payload`, `finished_at` |
| `review_records` | `id`, `submission_id`, `reviewer_user_id`, `rubric_snapshot`, `manual_score`, `comment_text` |
| `grades` | `id`, `task_id`, `user_id`, `submission_id`, `auto_score`, `manual_score`, `final_score`, `status`, `published_at` |
| `grade_rechecks` | `id`, `grade_id`, `applicant_user_id`, `reason`, `status`, `result_comment` |

### 2.5 消息与审计

| 表名 | 关键字段 |
| --- | --- |
| `notifications` | `id`, `receiver_user_id`, `type`, `title`, `content`, `is_read`, `related_type`, `related_id` |
| `announcements` | `id`, `title`, `content`, `scope_type`, `scope_value`, `status`, `published_at` |
| `audit_logs` | `id`, `actor_user_id`, `action`, `target_type`, `target_id`, `result`, `request_id`, `ip`, `extra_json` |

## 3. 关键表结构说明

### 3.1 `task_language_profiles`

| 字段 | 类型建议 | 说明 |
| --- | --- | --- |
| `language` | `varchar(32)` | 语言代码，如 `cpp17`、`python3` |
| `build_command` | `text` | 编译命令模板 |
| `run_command` | `text` | 运行命令模板 |
| `entry_file` | `varchar(255)` | 默认入口文件 |
| `time_limit_ms` | `integer` | 单用例 CPU / 时钟时间限制 |
| `memory_limit_mb` | `integer` | 单用例内存限制 |
| `output_limit_kb` | `integer` | 输出大小限制 |

### 3.2 `ide_workspaces`

| 字段 | 类型建议 | 说明 |
| --- | --- | --- |
| `task_id` | `uuid` | 每个编程任务对应一个学员工作区 |
| `user_id` | `uuid` | 工作区归属学员 |
| `active_language_profile_id` | `uuid` | 当前选中的语言模板 |
| `version_no` | `integer` | 工作区已保存版本号 |
| `save_status` | `varchar(32)` | `ready / dirty / saving / save_failed` |
| `last_opened_file` | `varchar(255)` | 上次打开的文件路径 |
| `last_saved_at` | `timestamptz` | 最近一次成功保存时间 |

### 3.3 `sandbox_runs`

| 字段 | 类型建议 | 说明 |
| --- | --- | --- |
| `snapshot_id` | `uuid` | 本次运行关联的工作区快照 |
| `status` | `varchar(32)` | `queued / running / success / failed / timeout` |
| `stdin_text` | `text` | 自定义输入 |
| `stdout_text` | `text` | 标准输出 |
| `stderr_text` | `text` | 标准错误 |
| `compile_output` | `text` | 编译输出摘要 |
| `time_ms` | `integer` | 运行耗时 |
| `memory_kb` | `integer` | 峰值内存 |

### 3.4 `judge_runs`

| 字段 | 类型建议 | 说明 |
| --- | --- | --- |
| `attempt_no` | `integer` | 第几次评测 / 重评 |
| `status` | `varchar(32)` | `queued / running / success / failed / timeout / system_error` |
| `compile_status` | `varchar(32)` | `success / compile_error / skipped` |
| `score` | `numeric(5,2)` | 总分 |
| `raw_payload` | `jsonb` | 原始 `go-judge` 响应 |
| `normalized_payload` | `jsonb` | 归一化后的测试点结果和摘要 |

## 4. 索引设计

| 表名 | 索引 |
| --- | --- |
| `users` | `username` 唯一索引，`platform_role + status` 组合索引 |
| `user_identities` | `provider + provider_subject` 唯一索引 |
| `courses` | `owner_user_id`、`org_unit_id + status` |
| `course_members` | `course_id + user_id` 唯一索引 |
| `tasks` | `course_id + status`、`open_at`、`due_at` |
| `task_language_profiles` | `task_id + language` 唯一索引、`task_id + is_default` |
| `ide_workspaces` | `task_id + user_id` 唯一索引、`user_id + updated_at` |
| `ide_workspace_files` | `workspace_id + path` 唯一索引、`workspace_id + is_deleted` |
| `workspace_snapshots` | `workspace_id + version_no`、`task_id + user_id + created_at` |
| `sandbox_runs` | `workspace_id + created_at`、`user_id + status + created_at` |
| `submissions` | `task_id + user_id + submit_no` 唯一索引、`user_id + accepted_at` |
| `submission_files` | `submission_id + path` 唯一索引 |
| `judge_runs` | `submission_id + attempt_no` 唯一索引、`status + created_at` |
| `grades` | `task_id + user_id` 唯一索引、`status + published_at` |
| `audit_logs` | `actor_user_id + created_at`、`action + created_at` |

## 5. 关系规则

- 一个课程只有一个 `owner_user_id`，但可有多个助教和学员成员关系。
- 一个任务必须属于一门课程，并可关联多个语言配置、用例和模板文件。
- 一个编程任务对每位学员最多只维护一个当前工作区。
- 一个工作区可产生多个快照和多次试运行记录。
- 一次正式提交必须绑定一个不可变 `snapshot_id`。
- 一次提交可以对应多次评测记录，但成绩默认绑定当前有效评测与批改结果。
- 通知与审计通过 `related_type + related_id` 关联业务对象。

## 6. 初始化数据建议

- 平台管理员账号 1 个
- 默认组织 1 个
- 演示教师 2 个
- 演示学员 4 个
- 演示课程 1 门
- 演示任务 2 个：1 个编程任务（含模板工程与样例）、1 个文档任务
