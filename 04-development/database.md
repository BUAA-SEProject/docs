# 数据库设计

## 1. 当前设计原则

1. 关系型事实来源统一落在 PostgreSQL。
2. 结构变更统一通过 Flyway 管理，不手工改表。
3. 当前仓库使用 `BIGINT IDENTITY` 作为主键策略。
4. 状态字段显式建模，避免用隐含布尔值拼接业务状态。
5. 平台治理身份与课程成员关系分开建模。

## 2. 当前已实现的治理表

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

说明：

- 画像字段用于承接学校主数据与教务身份，不替代账号基础字段。
- 当前实现允许用户基础手机号与画像手机号并存，前者偏账号联系信息，后者偏教务画像口径。

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

说明：

- 成员关系用于表达“学生在班级中”“教师在课程中”等业务归属。
- 成员关系不等于治理权限，治理权限仍由 `user_scope_roles` 承担。

### 2.5 `user_scope_roles`

| 字段 | 说明 |
| --- | --- |
| `id` | 记录主键 |
| `user_id` | 用户主键 |
| `scope_org_unit_id` | 作用域组织 |
| `role_code` | `SCHOOL_ADMIN / COLLEGE_ADMIN / COURSE_ADMIN / CLASS_ADMIN` |
| `created_at` | 创建时间 |

说明：

- 一个用户可拥有多个平台治理身份。
- 每个治理身份必须绑定一个组织节点。
- 教师在当前治理阶段临时通过 `CLASS_ADMIN` 表达，不作为课程域最终角色模型。

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

说明：

- 当前只保留一份生效配置。
- 配置修改后立即生效，不再引入草稿、发布、回退和历史表。

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

### 2.8 `academic_terms`

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

### 2.9 `course_catalogs`

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

### 2.10 `course_offerings`

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

说明：

- `course_offerings` 是课程域第一切片的主业务边界。
- 后续任务、实验、评测和成绩都应围绕 `offering_id` 挂接。

### 2.11 `course_offering_college_maps`

| 字段 | 说明 |
| --- | --- |
| `id` | 主键 |
| `offering_id` | 开课实例 |
| `college_unit_id` | 共同管理学院 |
| `relation_type` | `PRIMARY / SECONDARY / CROSS_LISTED` |

说明：

- 用于表达课程可被多个学院共同管理。

### 2.12 `teaching_classes`

| 字段 | 说明 |
| --- | --- |
| `id` | 教学班主键 |
| `offering_id` | 所属开课实例 |
| `class_code` | 班级编码，课程内大小写不敏感唯一 |
| `class_name` | 班级名称 |
| `entry_year` | 入学年份，如 2024、2025 |
| `org_class_unit_id` | 对应组织树中的 CLASS 节点 |
| `capacity` | 班级容量 |
| `status` | `ACTIVE / FROZEN / ARCHIVED` |
| `announcement_enabled` | 公告功能开关 |
| `discussion_enabled` | 讨论区功能开关 |
| `resource_enabled` | 资源功能开关 |
| `lab_enabled` | 实验功能开关 |
| `assignment_enabled` | 作业功能开关 |

说明：

- 一个开课实例可拥有多个不同年份教学班。

### 2.13 `course_members`

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

说明：

- 课程成员角色与平台治理身份分离建模。
- 当前学生不能自主选课，成员仅允许教师批量添加或导入既有系统用户。

## 3. 当前索引约定

- `org_units`：
  - `lower(code)` 唯一索引
  - `parent_id + sort_order + id`
- `users`：
  - `lower(username)` 唯一索引
  - `lower(email)` 唯一索引
  - `primary_org_unit_id`
  - `account_status`
- `academic_profiles`：
  - `user_id` 唯一索引
  - `lower(academic_id)` 唯一索引
  - `identity_type + profile_status`
- `user_org_memberships`：
  - `user_id + org_unit_id + membership_type` 唯一索引
  - `user_id`
  - `org_unit_id`
- `user_scope_roles`：
  - `user_id + scope_org_unit_id + role_code` 唯一索引
  - `user_id`
  - `scope_org_unit_id`
- `academic_terms`：
  - `lower(term_code)` 唯一索引
- `course_catalogs`：
  - `lower(course_code)` 唯一索引
  - `department_unit_id`
- `course_offerings`：
  - `lower(offering_code)` 唯一索引
  - `catalog_id`
  - `term_id`
  - `primary_college_unit_id`
  - `status`
- `course_offering_college_maps`：
  - `offering_id + college_unit_id` 唯一索引
  - `college_unit_id`
- `teaching_classes`：
  - `offering_id + lower(class_code)` 唯一索引
  - `offering_id`
  - `org_class_unit_id`
- `course_members`：
  - `offering_id`
  - `teaching_class_id`
  - `user_id`
  - `member_role + member_status`
  - `INSTRUCTOR` 按 `offering_id + user_id` 唯一
  - `STUDENT` 按 `offering_id + user_id` 唯一
  - `TA` 按 `offering_id + user_id + teaching_class_id` 唯一
- `audit_logs`：
  - `actor_user_id + created_at`
  - `action + created_at`
  - `target_type + created_at`

## 4. 设计边界

- 平台治理身份只解决平台配置、组织、用户、审计等后台治理问题。
- 教师、助教、学员等课程业务角色不落在 `users` 或 `user_scope_roles` 的全局字段上。
- 学号/工号和成员关系已落到独立表，不再把这类业务信息塞进 `users` 主表。
- 课程系统当前通过 `course_catalogs`、`course_offerings`、`teaching_classes` 和 `course_members` 表达课程主数据、班级和成员关系。
- 如未来引入统一认证，可新增外部身份映射表，但不应破坏当前基础资料与治理身份边界。

## 5. 后续课程域扩展位

后续课程域建议新增但当前未实现的表包括：

- `course_resources`
- `tasks`
- `submissions`
- `judge_runs`
- `grades`

这些表应围绕课程主链路独立建模，不回写为平台级全局角色。
