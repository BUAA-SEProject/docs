2. [GET] http://127.0.0.1:3000/api/v1/me/notifications/stream => [200] OK
3. [GET] http://127.0.0.1:3000/api/v1/me/notifications/unread-count
35. [GET] http://127.0.0.1:3000/api/v1/me/notifications/stream => [FAILED] net::ERR_ABORTED
36. [GET] http://127.0.0.1:3000/api/v1/me/notifications/stream => [200] OK
37. [GET] http://127.0.0.1:3000/api/v1/me/notifications/unread-count => [200] OK
38. [GET] http://127.0.0.1:3000/api/v1/me/courses => [200] OK
39. [GET] http://127.0.0.1:3000/api/v1/teacher/course-offerings/5/classes => [403] Forbidden
40. [GET] http://127.0.0.1:3000/api/v1/me/notifications/stream => [FAILED] net::ERR_ABORTED
41. [GET] http://127.0.0.1:3000/api/v1/teacher/course-offerings/5/classes => [403] Forbidden
42. [GET] http://127.0.0.1:3000/api/v1/me/notifications/unread-count => [200] OK
43. [GET] http://127.0.0.1:3000/teacher/courses/5/announcements?_rsc=1tv5l => [200] OK
54. [GET] http://127.0.0.1:3000/api/v1/teacher/course-offerings/5/classes => [403] Forbidden
55. [GET] http://127.0.0.1:3000/api/v1/teacher/course-offerings/5/announcements => [403] Forbidden
56. [GET] http://127.0.0.1:3000/api/v1/teacher/course-offerings/5/classes => [403] Forbidden
57. [GET] http://127.0.0.1:3000/api/v1/teacher/course-offerings/5/announcements => [403] Forbidden
58. [GET] http://127.0.0.1:3000/api/v1/me/notifications/unread-count => [200] OK

Note: 41 static requests not shown, run with "static" option to see them.