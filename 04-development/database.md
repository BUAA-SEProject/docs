# 数据库设计

## 1. 设计原则

- 统一使用 `uuid` 或雪花 ID 作为主键。
- 关键业务表必须包含 `created_at`、`updated_at`、`created_by`、`updated_by`。
- 状态字段显式建模，禁止使用隐含状态。
- 提交、评测、成绩和审计采用留痕式设计，不做无历史覆盖。

## 2. 核心表

### 2.1 平台治理

| 表名 | 关键字段 |
| --- | --- |
| `platform_configs` | `id`, `version`, `name`, `theme`, `module_flags`, `status` |
| `org_units` | `id`, `parent_id`, `name`, `type`, `level`, `status` |
| `users` | `id`, `username`, `display_name`, `email`, `phone`, `platform_role`, `status`, `password_hash` |

### 2.2 课程与任务

| 表名 | 关键字段 |
| --- | --- |
| `courses` | `id`, `name`, `owner_user_id`, `term`, `org_unit_id`, `status`, `invite_code` |
| `course_members` | `id`, `course_id`, `user_id`, `course_role`, `joined_at`, `status` |
| `course_resources` | `id`, `course_id`, `name`, `type`, `file_key`, `visibility` |
| `tasks` | `id`, `course_id`, `type`, `title`, `content_md`, `open_at`, `due_at`, `submission_limit`, `grading_mode`, `status` |
| `task_testcases` | `id`, `task_id`, `name`, `input_text`, `expected_output`, `is_public`, `weight` |
| `task_rubrics` | `id`, `task_id`, `item_name`, `score`, `description`, `sort_order` |

### 2.3 提交、评测、成绩

| 表名 | 关键字段 |
| --- | --- |
| `submissions` | `id`, `task_id`, `user_id`, `submit_no`, `status`, `source_type`, `source_text`, `accepted_at` |
| `submission_files` | `id`, `submission_id`, `file_name`, `file_key`, `size_bytes`, `mime_type` |
| `judge_runs` | `id`, `submission_id`, `attempt_no`, `status`, `score`, `raw_payload`, `normalized_payload`, `finished_at` |
| `review_records` | `id`, `submission_id`, `reviewer_user_id`, `rubric_snapshot`, `manual_score`, `comment_text` |
| `grades` | `id`, `task_id`, `user_id`, `submission_id`, `auto_score`, `manual_score`, `final_score`, `status`, `published_at` |
| `grade_rechecks` | `id`, `grade_id`, `applicant_user_id`, `reason`, `status`, `result_comment` |

### 2.4 消息与审计

| 表名 | 关键字段 |
| --- | --- |
| `notifications` | `id`, `receiver_user_id`, `type`, `title`, `content`, `is_read`, `related_type`, `related_id` |
| `announcements` | `id`, `title`, `content`, `scope_type`, `scope_value`, `status`, `published_at` |
| `audit_logs` | `id`, `actor_user_id`, `action`, `target_type`, `target_id`, `result`, `request_id`, `ip`, `extra_json` |

## 3. 索引设计

| 表名 | 索引 |
| --- | --- |
| `users` | `username` 唯一索引，`platform_role + status` 组合索引 |
| `courses` | `owner_user_id`、`org_unit_id + status` |
| `course_members` | `course_id + user_id` 唯一索引 |
| `tasks` | `course_id + status`、`open_at`、`due_at` |
| `submissions` | `task_id + user_id`、`user_id + accepted_at` |
| `judge_runs` | `submission_id + attempt_no` 唯一索引、`status` |
| `grades` | `task_id + user_id` 唯一索引、`status + published_at` |
| `audit_logs` | `actor_user_id + created_at`、`action + created_at` |

## 4. 关系规则

- 一个课程只有一个 `owner_user_id`，但可有多个助教和学员成员关系。
- 一个任务必须属于一门课程。
- 一次提交可以对应多次评测记录，但成绩默认绑定当前有效评测与批改结果。
- 通知与审计通过 `related_type + related_id` 关联业务对象。

## 5. 初始化数据建议

- 平台管理员账号 1 个
- 默认组织 1 个
- 演示教师 2 个
- 演示学员 4 个
- 演示课程 1 门
- 演示任务 2 个
