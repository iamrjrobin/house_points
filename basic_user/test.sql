SELECT "basic_user_employee"."id",
    "basic_user_employee"."name",
    "basic_user_employee"."designation",
    "basic_user_employee"."house_id",
    SUM("basic_user_point"."value") AS "points"
FROM "basic_user_employee"
    LEFT OUTER JOIN "basic_user_point" ON (
        "basic_user_employee"."id" = "basic_user_point"."employee_id"
    )
WHERE "basic_user_employee"."house_id" = 1
GROUP BY "basic_user_employee"."id",
    "basic_user_employee"."name",
    "basic_user_employee"."designation",
    "basic_user_employee"."house_id"
ORDER BY "points" DESC