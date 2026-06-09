2. [GET] http://127.0.0.1:3000/api/v1/me/notifications/stream => [200] OK
3. [GET] http://127.0.0.1:3000/api/v1/me/notifications/unread-count
36. [GET] http://127.0.0.1:3000/api/v1/me/notifications/stream => [FAILED] net::ERR_ABORTED
37. [GET] http://127.0.0.1:3000/api/v1/me/notifications/stream => [200] OK
38. [GET] http://127.0.0.1:3000/api/v1/me/notifications/unread-count => [200] OK
39. [GET] http://127.0.0.1:3000/api/v1/me/discussions/29 => [200] OK
40. [GET] http://127.0.0.1:3000/api/v1/me/notifications/stream => [FAILED] net::ERR_ABORTED
41. [POST] http://127.0.0.1:3000/api/v1/me/discussions/29/replies => [201] Created
42. [GET] http://127.0.0.1:3000/api/v1/me/discussions/29 => [200] OK
43. [GET] http://127.0.0.1:3000/api/v1/me/notifications/unread-count => [200] OK

Note: 32 static requests not shown, run with "static" option to see them.